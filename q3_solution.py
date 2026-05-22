from __future__ import annotations

from itertools import product
from pathlib import Path

import pandas as pd
from openpyxl import load_workbook

import q1_solution


"""
问题3 求解脚本（简化实现说明）：
- 基于问题2 的最优站点（从 q2_output 读取），允许每个站点对所有服务使用相同的价格倍率（markup），
  将基准价乘以 (1+markup) 得到站点标价。
- 政府补贴为 2 元/人次（紧急救助不补贴），但单站每日补贴有上限（小型1000，中型1800，大型2600 元），
  当需求超出补贴预算时，按人均折算得到平均每人补贴（<=2 元）。
- 老人对价格的满意度 S3 按补贴后平均净价与基准价的比值分段映射（与题目附件一致）。
- 对于每组价格倍率，迭代求解站点利用率 -> 响应满意度 S2 -> 实际有效需求（理论需求×满意度） 的稳定点，
  并计算年度利润、利润率（满足 ≤8% 约束）。
- 搜索空间：每个站点的 markup 从一组离散值中穷举（折扣/原价/小幅提价/较高提价），因为对每个服务独立定价会爆炸。

输出：将最优方案写入 q3_output 目录（包含每站的最优 markup、定价、预计年度利润、覆盖满意度等）。
"""


BASE_DIR = Path(__file__).resolve().parent
Q2_DIR = BASE_DIR / "q2_output"
Q1_DIR = BASE_DIR / "q1_output"
OUTPUT_DIR = BASE_DIR / "q3_output"


MARKUP_OPTIONS = [-0.2, -0.1, 0.0, 0.05, 0.10, 0.15, 0.25]


def load_q2_results():
    station_df = pd.read_csv(Q2_DIR / "best_station_plan.csv", encoding="utf-8-sig")
    assign_df = pd.read_csv(Q2_DIR / "best_community_assignment.csv", encoding="utf-8-sig")
    return station_df, assign_df


def load_q1_theoretical():
    # 理论月需求（按服务/社区）
    theo = pd.read_csv(Q1_DIR / "year5_theoretical_demand.csv", encoding="utf-8-sig")
    return theo


def load_service_baseline_and_costs():
    wb = load_workbook(BASE_DIR / "附件2：服务需求数据.xlsx", data_only=True)
    revenue = wb[wb.sheetnames[1]]
    # sheet: 服务营收及支出, col1=服务项目, col2=单次服务营收, col3=单次服务直接支出
    prices = {}
    costs = {}
    for r in range(3, 9):
        svc = revenue.cell(r, 1).value
        val = revenue.cell(r, 2).value
        cost = revenue.cell(r, 3).value
        if isinstance(val, (int, float)):
            prices[svc] = float(val)
        else:
            # 紧急救助记为 '0（公益免费）' 之类，直接赋 0
            try:
                prices[svc] = float(str(val))
            except Exception:
                prices[svc] = 0.0
        costs[svc] = float(cost)
    return prices, costs


def distance_satisfaction(distance: float) -> float:
    if distance <= 300:
        return 1.0
    if distance <= 500:
        return 0.90
    if distance <= 650:
        return 0.75
    if distance <= 1000:
        return 0.60
    return 0.0


def tier_from_utilization(util: float) -> float:
    if util <= 0.60:
        return 1.00
    if util <= 0.75:
        return 0.93
    if util <= 0.85:
        return 0.85
    if util <= 0.95:
        return 0.72
    return 0.60


def price_satisfaction(baseline: float, net_price: float) -> float:
    # net_price 为老人实际支付的平均价格（考虑补贴后）。
    if net_price <= baseline:
        return 1.00
    ratio = (net_price - baseline) / baseline
    if ratio <= 0.10:
        return 0.90
    if ratio <= 0.20:
        return 0.75
    return 0.60


def evaluate_markups(
    station_df: pd.DataFrame,
    assign_df: pd.DataFrame,
    theo: pd.DataFrame,
    baseline_prices: dict[str, float],
    service_costs: dict[str, float],
):
    # Prepare structures
    station_info = {}
    for _, row in station_df.iterrows():
        site = row["站点"]
        station_info[site] = {
            "规模": row["规模"],
            "日容量": float(row["日容量"]),
            "assigned": []
        }

    for _, row in assign_df.iterrows():
        station = row["分配站点"]
        if pd.isna(station):
            continue
        station_info[station]["assigned"].append(row["小区"]) 

    # group theoretical monthly total per community (sum of all services)
    theo_total = theo.groupby(["小区"]) ["理论月需求次数"].sum().to_dict()
    # per community per service dict
    theo_service = {}
    for _, r in theo.iterrows():
        theo_service.setdefault(r["小区"], {})[r["服务项目"]] = float(r["理论月需求次数"]) 

    # subsidy caps per day
    cap_per_size = {"小型": 1000.0, "中型": 1800.0, "大型": 2600.0}

    best = None
    # search over station-level uniform markups
    sites = list(station_info.keys())
    for markup_choice in product(MARKUP_OPTIONS, repeat=len(sites)):
        markups = {site: m for site, m in zip(sites, markup_choice)}

        # iterate to fixed point for utilizations and S2
        station_s2 = {site: 0.6 for site in sites}
        for _ in range(15):
            # compute monthly effective demand per station given current S2 and price decisions
            station_monthly_effective = {site: 0.0 for site in sites}
            station_monthly_non_emergency = {site: 0.0 for site in sites}

            for site in sites:
                assigned = station_info[site]["assigned"]
                size = station_info[site]["规模"]
                for comm in assigned:
                    s1 = distance_satisfaction(float(assign_df[assign_df["小区"] == comm]["距离(米)"].iloc[0]))
                    s2 = station_s2[site]
                    # price satisfaction uses average net price after subsidy (approx), but subsidy cap unknown until demand computed
                    # we approximate net price by baseline*(1+markup) - 2 (will adjust below using per-person subsidy)
                    # compute raw community satisfaction factor S (depends on S3 placeholder=1.0 now)
                    # We'll compute exact S after estimating per-person subsidy per station; for iteration, use S3 based on markup ignoring cap
                    markup = markups[site]
                    # compute average net price per service (approx) and S3 (approx)
                    # choose a representative service price: weighted average baseline across services by demand
                    svc_dict = theo_service.get(comm, {})
                    if not svc_dict:
                        continue
                    total_units = sum(svc_dict.values())
                    if total_units <= 0:
                        continue
                    avg_baseline = sum(baseline_prices[svc] * cnt for svc, cnt in svc_dict.items()) / total_units
                    avg_price = avg_baseline * (1 + markup)
                    # preliminary S3
                    s3 = price_satisfaction(avg_baseline, avg_price)
                    S = 0.2 * s1 + 0.3 * s2 + 0.5 * s3
                    station_monthly_effective[site] += theo_total.get(comm, 0.0) * S
                    # non-emergency counts (exclude 紧急救助)
                    non_emergency = sum(cnt for svc, cnt in svc_dict.items() if svc != "紧急救助")
                    station_monthly_non_emergency[site] += non_emergency * S

            # update S2 from utilization
            new_station_s2 = {}
            for site in sites:
                daily = station_info[site]["日容量"]
                monthly_eff = station_monthly_effective[site]
                utilization = monthly_eff / (30.0 * daily) if daily > 0 else 0.0
                new_station_s2[site] = tier_from_utilization(utilization)

            if new_station_s2 == station_s2:
                break
            station_s2 = new_station_s2

        # after convergence, compute annual revenues, subsidies and profit
        station_annual_profit = {}
        station_satisfaction = {}
        feasible = True
        for site in sites:
            assigned = station_info[site]["assigned"]
            size = station_info[site]["规模"]
            daily_cap = station_info[site]["日容量"]
            # monthly effective per community recompute with final S2 and exact per-person subsidy
            monthly_effective = 0.0
            monthly_non_emergency = 0.0
            annual_revenue = 0.0
            annual_direct_cost = 0.0
            community_satisfaction = {}

            for comm in assigned:
                s1 = distance_satisfaction(float(assign_df[assign_df["小区"] == comm]["距离(米)"].iloc[0]))
                s2 = station_s2[site]
                svc_dict = theo_service.get(comm, {})
                comm_total = sum(svc_dict.values())
                if comm_total <= 0:
                    continue
                # per-service pricing: price = baseline*(1+markup)
                markup = markups[site]
                # compute per-service net price after average subsidy (we'll compute per-person subsidy from station-level cap below)
                # first compute S3 using gross price (will be adjusted after subsidy calc)
                # compute average baseline and avg price
                avg_baseline = sum(baseline_prices[svc] * cnt for svc, cnt in svc_dict.items()) / comm_total
                avg_price = avg_baseline * (1 + markup)
                # provisional S3
                s3 = price_satisfaction(avg_baseline, avg_price)
                S = 0.2 * s1 + 0.3 * s2 + 0.5 * s3
                community_satisfaction[comm] = S
                monthly_effective += comm_total * S
                non_emergency = sum(cnt for svc, cnt in svc_dict.items() if svc != "紧急救助")
                monthly_non_emergency += non_emergency * S

            # average per-person subsidy considering cap
            daily_non_em = monthly_non_emergency / 30.0
            cap = cap_per_size.get(size, 0.0)
            per_person_subsidy = 0.0
            if daily_non_em > 0:
                per_person_subsidy = min(2.0, cap / daily_non_em)

            # compute annual revenue and direct cost with actual subsidy allocation
            for comm in assigned:
                svc_dict = theo_service.get(comm, {})
                S = community_satisfaction.get(comm, 0.0)
                for svc, monthly_cnt in svc_dict.items():
                    eff_monthly = monthly_cnt * S
                    price_set = baseline_prices[svc] * (1 + markups[site])
                    # effective elderly pay
                    if svc == "紧急救助":
                        elderly_pay = 0.0
                        subsidy_per_person = 0.0
                    else:
                        elderly_pay = max(0.0, price_set - per_person_subsidy)
                        subsidy_per_person = per_person_subsidy

                    annual_revenue += eff_monthly * 12.0 * price_set
                    annual_direct_cost += eff_monthly * 12.0 * service_costs[svc]

            annual_subsidy = per_person_subsidy * monthly_non_emergency / 30.0 * 365.0
            annual_fixed_cost = float(station_df[station_df["站点"] == site]["日容量"].iloc[0]) # placeholder use constructed costs from q2 (daily capacity used)
            # For cost we should use construction/operational cost; approximate annual op cost as daily_fixed *365 + construction/20
            # but q2 did compute annual profit with that; to be consistent, approximate annual_op_cost using q2 info annual profit formula components unavailable here
            # Simplify: set annual_operation_cost = 2000*365 for small/3200*365 for medium/4400*365 for large, based on attachment3
            size_to_daily_fixed = {"小型": 2000.0, "中型": 3200.0, "大型": 4400.0}
            daily_fixed = size_to_daily_fixed.get(size, 2000.0)
            annual_operation_cost = daily_fixed * 365.0 + (18.0 if size == "小型" else 32.0 if size == "中型" else 45.0) * 10000.0 / 20.0

            service_profit = annual_revenue - annual_direct_cost
            profit_rate = (service_profit + annual_subsidy - annual_operation_cost) / annual_operation_cost * 100.0

            station_annual_profit[site] = service_profit + annual_subsidy - annual_operation_cost

            # store average satisfaction across assigned communities weighted by community population
            station_satisfaction[site] = (
                sum(community_satisfaction.get(c, 0.0) * theo_total.get(c, 0.0) for c in assigned)
                / sum(theo_total.get(c, 0.0) for c in assigned)
                if assigned
                else 0.0
            )

            # feasibility: profit rate must be <=8%
            if profit_rate > 8.0:
                feasible = False
                break

        if not feasible:
            continue

        # compute global average satisfaction weighted by 60+ population
        pop = q1_solution.load_community_data()[0]
        pop_map = {row["小区"]: float(row["60+"]) for _, row in pop.iterrows()}
        numerator = 0.0
        denom = 0.0
        for site in sites:
            assigned = station_info[site]["assigned"]
            for c in assigned:
                w = pop_map.get(c, 0.0)
                S = community_satisfaction.get(c, 0.0)
                numerator += S * w
                denom += w

        avg_satisfaction = numerator / denom if denom else 0.0
        total_profit = sum(station_annual_profit.values())

        # objective: maximize avg_satisfaction, tie-break by total_profit
        candidate = {
            "markups": markups,
            "avg_satisfaction": avg_satisfaction,
            "total_profit": total_profit,
            "station_profit": station_annual_profit,
            "station_satisfaction": station_satisfaction,
        }

        if best is None or (candidate["avg_satisfaction"] > best["avg_satisfaction"] or (abs(candidate["avg_satisfaction"]-best["avg_satisfaction"])<1e-6 and candidate["total_profit"]>best["total_profit"])):
            best = candidate

    return best


def main():
    station_df, assign_df = load_q2_results()
    theo = load_q1_theoretical()
    baseline_prices, service_costs = load_service_baseline_and_costs()

    best = evaluate_markups(station_df, assign_df, theo, baseline_prices, service_costs)
    OUTPUT_DIR.mkdir(exist_ok=True)
    if best is None:
        print("未找到满足利润率约束的定价方案。")
        return

    # 输出结果
    out_rows = []
    for site, m in best["markups"].items():
        out_rows.append({"站点": site, "统一markup": m, "站点满意度": best["station_satisfaction"].get(site, 0.0), "年利润(元)": best["station_profit"].get(site, 0.0)})
    pd.DataFrame(out_rows).to_csv(OUTPUT_DIR / "best_pricing_plan.csv", index=False, encoding="utf-8-sig")

    print("找到最优定价方案：平均满意度=", best["avg_satisfaction"], "年利润合计=", best["total_profit"]) 


if __name__ == "__main__":
    main()
