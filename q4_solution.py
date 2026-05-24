from __future__ import annotations

from contextlib import contextmanager
from itertools import combinations, product
from pathlib import Path
import json

import pandas as pd

import q1_solution
import q2_solution
import q3_solution

BASE_DIR = Path(__file__).resolve().parent
OUT_DIR = BASE_DIR / "q4_output"
OUT_DIR.mkdir(exist_ok=True)

SCENARIOS = {
    "baseline": {
        "growth_rate": 0.07,
        "self_to_semi": 0.045,
        "semi_to_disabled": 0.10,
        "daily_cost_multiplier": 1.0,
        "budget_wan": 120.0,
    },
    "scenario_growth": {
        "growth_rate": 0.08,
        "self_to_semi": 0.055,
        "semi_to_disabled": 0.095,
        "daily_cost_multiplier": 1.0,
        "budget_wan": 120.0,
    },
    "scenario_cost": {
        "growth_rate": 0.07,
        "self_to_semi": 0.045,
        "semi_to_disabled": 0.10,
        "daily_cost_multiplier": 1.2,
        "budget_wan": 120.0,
    },
    "scenario_budget": {
        "growth_rate": 0.07,
        "self_to_semi": 0.045,
        "semi_to_disabled": 0.10,
        "daily_cost_multiplier": 1.0,
        "budget_wan": 140.0,
    },
}


@contextmanager
def patched_attributes(*pairs: tuple[object, str, object]):
    originals = []
    try:
        for obj, name, value in pairs:
            originals.append((obj, name, getattr(obj, name)))
            setattr(obj, name, value)
        yield
    finally:
        for obj, name, original in reversed(originals):
            setattr(obj, name, original)


def forecast_years(communities: pd.DataFrame, growth_rate: float, self_to_semi: float, semi_to_disabled: float, years: int = 5, death_rate: float = 0.05) -> list[pd.DataFrame]:
    result = communities.copy()
    yearly_results: list[pd.DataFrame] = []
    for _ in range(years):
        new_60_plus = growth_rate * result["60+"]
        next_self = (1 - death_rate) * result["自理"] * (1 - self_to_semi) + new_60_plus
        next_semi = (1 - death_rate) * (result["自理"] * self_to_semi + result["半失能"] * (1 - semi_to_disabled))
        next_disabled = (1 - death_rate) * (result["半失能"] * semi_to_disabled + result["失能"])
        result = result.copy()
        result[["自理", "半失能", "失能"]] = pd.DataFrame({"自理": next_self, "半失能": next_semi, "失能": next_disabled})
        result["60+"] = result[["自理", "半失能", "失能"]].sum(axis=1)
        yearly_results.append(result.copy())
    return yearly_results


def build_forecast_inputs(growth_rate: float, self_to_semi: float, semi_to_disabled: float) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    communities, _, _ = q1_solution.load_community_data()
    demand_rates, service_prices, cap_ratios = q1_solution.load_service_data()
    forecast5 = forecast_years(communities, growth_rate, self_to_semi, semi_to_disabled)[-1]
    theoretical, actual = q1_solution.build_service_tables(
        forecast=forecast5,
        communities=communities,
        demand_rates=demand_rates,
        service_prices=service_prices,
        cap_ratios=cap_ratios,
    )
    demand_total = actual.groupby(["小区", "服务项目"], as_index=False)["实际月均需求次数"].sum()
    return forecast5, theoretical, actual, demand_total


def build_population_table(forecast5: pd.DataFrame) -> pd.DataFrame:
    community_population = forecast5[["小区", "60+"]].copy()
    community_population.rename(columns={"60+": "60岁以上人口"}, inplace=True)
    return community_population


def search_station_plan(
    distance_matrix: pd.DataFrame,
    community_population: pd.DataFrame,
    demand_total: pd.DataFrame,
    baseline_prices: dict[str, float],
    service_costs: dict[str, float],
    budget_wan: float,
) -> list[dict[str, object]]:
    population_map = {
        row["小区"]: float(row["60岁以上人口"])
        for _, row in community_population.iterrows()
    }
    sites = list(distance_matrix.index)
    ranked_sites = sorted(
        sites,
        key=lambda site: sum(
            population_map.get(community, 0.0)
            for community in population_map
            if distance_matrix.loc[community, site] <= 1000
        ),
        reverse=True,
    )
    candidate_sites = ranked_sites[: q2_solution.TOP_CANDIDATE_SITES]

    candidates: list[dict[str, object]] = []

    for station_count in range(1, min(q2_solution.MAX_SELECTED_SITES, len(candidate_sites)) + 1):
        for selected_sites in combinations(candidate_sites, station_count):
            if min(option[1] for option in q2_solution.SIZE_OPTIONS) * station_count > budget_wan:
                continue

            for size_choice in product([option[0] for option in q2_solution.SIZE_OPTIONS], repeat=station_count):
                size_names = {site: size_name for site, size_name in zip(selected_sites, size_choice)}
                construction_cost = sum(
                    next(option[1] for option in q2_solution.SIZE_OPTIONS if option[0] == size_name)
                    for size_name in size_choice
                )
                if construction_cost > budget_wan:
                    continue

                base_result = q2_solution.evaluate_plan(
                    selected_sites=list(selected_sites),
                    size_names=size_names,
                    distance_matrix=distance_matrix,
                    community_population=community_population,
                    demand_total=demand_total,
                    service_prices=baseline_prices,
                    service_costs=service_costs,
                )
                if base_result is None:
                    continue
                candidates.append(
                    {
                        "coverage": float(base_result["coverage"]),
                        "avg_satisfaction": float(base_result["avg_satisfaction"]),
                        "total_profit": float(base_result["total_profit"]),
                        "base_result": base_result,
                    }
                )

    if not candidates:
        raise RuntimeError("没有找到满足预算约束的可行方案。")

    candidates.sort(
        key=lambda item: (item["coverage"], item["avg_satisfaction"], item["total_profit"]),
        reverse=True,
    )
    return candidates[:10]


def save_scenario_outputs(name: str, result: dict[str, object]) -> None:
    scen_dir = OUT_DIR / name
    scen_dir.mkdir(exist_ok=True)
    result["base_result"]["station_rows"].to_csv(scen_dir / "best_station_layout.csv", index=False, encoding="utf-8-sig")
    result["base_result"]["community_rows"].to_csv(scen_dir / "best_community_assignment.csv", index=False, encoding="utf-8-sig")
    result["station_df"].to_csv(scen_dir / "best_pricing_plan.csv", index=False, encoding="utf-8-sig")
    result["service_df"].to_csv(scen_dir / "best_pricing_per_service.csv", index=False, encoding="utf-8-sig")
    result["community_df"].to_csv(scen_dir / "best_community_satisfaction.csv", index=False, encoding="utf-8-sig")


def run_scenario(name: str, params: dict[str, float]) -> dict[str, object]:
    forecast5, theoretical, actual, demand_total = build_forecast_inputs(
        params["growth_rate"],
        params["self_to_semi"],
        params["semi_to_disabled"],
    )
    community_population = build_population_table(forecast5)
    distance_matrix = q2_solution.load_distance_matrix()
    baseline_prices, service_costs = q3_solution.load_service_baseline_and_costs()
    size_options = [
        (size_name, construction_cost, daily_fixed * params["daily_cost_multiplier"], capacity)
        for size_name, construction_cost, daily_fixed, capacity in q2_solution.SIZE_OPTIONS
    ]
    daily_fixed_map = {
        size_name: daily_fixed * params["daily_cost_multiplier"]
        for size_name, daily_fixed in q3_solution.SIZE_TO_DAILY_FIXED.items()
    }

    with patched_attributes(
        (q2_solution, "SIZE_OPTIONS", size_options),
        (q3_solution, "SIZE_TO_DAILY_FIXED", daily_fixed_map),
    ):
        candidates = search_station_plan(
            distance_matrix=distance_matrix,
            community_population=community_population,
            demand_total=demand_total,
            baseline_prices=baseline_prices,
            service_costs=service_costs,
            budget_wan=params["budget_wan"],
        )

        result = None
        for candidate in candidates:
            base_result = candidate["base_result"]
            station_info, _ = q3_solution.build_station_inputs(
                base_result["station_rows"],
                base_result["community_rows"],
                forecast5[["小区", "60+"]].copy(),
                actual,
            )
            q3_solution.attach_station_distances(station_info, base_result["community_rows"])

            station_rows: list[dict[str, object]] = []
            service_rows: list[dict[str, object]] = []
            community_rows: list[dict[str, object]] = []
            total_profit = 0.0
            total_subsidy = 0.0
            weighted_satisfaction_sum = 0.0
            weighted_population_sum = 0.0
            min_profit_rate = None
            max_profit_rate = None
            feasible = True

            for site, info in station_info.items():
                pricing = q3_solution.evaluate_station_prices(site, info, baseline_prices, service_costs)
                if pricing is None:
                    feasible = False
                    break

                station_rows.append(
                    {
                        "站点": site,
                        "规模": pricing["规模"],
                        "助餐": pricing["service_prices"].get("助餐", 0.0),
                        "日间照料": pricing["service_prices"].get("日间照料", 0.0),
                        "上门护理": pricing["service_prices"].get("上门护理", 0.0),
                        "康复理疗": pricing["service_prices"].get("康复理疗", 0.0),
                        "助浴": pricing["service_prices"].get("助浴", 0.0),
                        "紧急救助": pricing["service_prices"].get("紧急救助", 0.0),
                        "响应满意度S2": round(float(pricing["response_s2"]), 4),
                        "平均满意度": round(float(pricing["avg_satisfaction"]), 4),
                        "政府补贴(元)": round(float(pricing["annual_subsidy"]), 2),
                        "年运营成本(元)": round(float(pricing["annual_operation_cost"]), 2),
                        "年度利润(元)": round(float(pricing["station_profit"]), 2),
                        "利润率(%)": round(float(pricing["profit_rate"]), 4),
                    }
                )
                service_rows.extend(pricing["service_rows"])
                community_rows.extend(pricing["community_rows"])
                total_profit += float(pricing["station_profit"])
                total_subsidy += float(pricing["annual_subsidy"])
                station_population = sum(float(v) for v in info["population_weight"].values())
                weighted_satisfaction_sum += float(pricing["avg_satisfaction"]) * station_population
                weighted_population_sum += station_population
                min_profit_rate = float(pricing["profit_rate"]) if min_profit_rate is None else min(min_profit_rate, float(pricing["profit_rate"]))
                max_profit_rate = float(pricing["profit_rate"]) if max_profit_rate is None else max(max_profit_rate, float(pricing["profit_rate"]))

            if feasible:
                pricing_station_df = pd.DataFrame(station_rows)
                pricing_service_df = pd.DataFrame(service_rows)
                pricing_community_df = pd.DataFrame(community_rows)
                pricing_avg_satisfaction = weighted_satisfaction_sum / weighted_population_sum if weighted_population_sum > 0 else 0.0
                result = {
                    "coverage": float(base_result["coverage"]),
                    "avg_satisfaction": pricing_avg_satisfaction,
                    "total_profit": total_profit,
                    "total_subsidy": total_subsidy,
                    "min_profit_rate": min_profit_rate if min_profit_rate is not None else 0.0,
                    "max_profit_rate": max_profit_rate if max_profit_rate is not None else 0.0,
                    "base_result": base_result,
                    "station_df": pricing_station_df,
                    "service_df": pricing_service_df,
                    "community_df": pricing_community_df,
                }
                break

        if result is None:
            raise RuntimeError(f"场景 {name} 没有找到满足利润率约束的可行定价方案。")

    save_scenario_outputs(name, result)
    result.update(
        {
            "forecast5": forecast5,
            "theoretical": theoretical,
            "actual": actual,
            "community_population": community_population,
        }
    )
    return result


def build_summary(results: dict[str, dict[str, object]]) -> dict[str, object]:
    summary: dict[str, object] = {}
    for name, result in results.items():
        base_result = result["base_result"]
        summary[name] = {
            "station_count": int(len(base_result["station_rows"])),
            "stations": base_result["station_rows"]["站点"].tolist(),
            "coverage": round(float(result["coverage"]), 6),
            "avg_satisfaction": round(float(result["avg_satisfaction"]), 6),
            "total_profit": round(float(result["total_profit"]), 2),
            "total_subsidy": round(float(result["total_subsidy"]), 2),
            "min_profit_rate": round(float(result["min_profit_rate"]), 4),
            "max_profit_rate": round(float(result["max_profit_rate"]), 4),
        }

    summary["robustness_notes"] = [
        "人口增长率和失能转移概率变化会直接改变第 5 年需求结构，进而影响站点选址和规模组合。",
        "日固定运营成本上升会压缩利润率上限，可能迫使方案从大站点转向更小规模或更分散布局。",
        "预算变化会改变可选站点数量和服务半径覆盖范围，从而影响覆盖率和满意度的平衡。",
        "服务基准价格、居民消费上限和政府补贴规则的微调都可能让最优定价从可行变为不可行。",
    ]
    summary["mitigation"] = [
        "对关键参数做区间敏感性分析，而不是只看单点结果。",
        "保留多个备选站点布局和价格方案，保证预算或成本变化时能快速切换。",
        "对高需求站点优先预留容量冗余，减少利用率波动带来的服务中断风险。",
        "把补贴和定价分开监控，定期复核利润率是否仍落在 0% 到 8% 的约束区间内。",
    ]
    return summary


def main() -> None:
    results: dict[str, dict[str, object]] = {}
    for name, params in SCENARIOS.items():
        print(f"运行场景：{name}")
        results[name] = run_scenario(name, params)

    summary = build_summary(results)
    with open(OUT_DIR / "sensitivity_summary.json", "w", encoding="utf-8") as file:
        json.dump(summary, file, ensure_ascii=False, indent=2)
    print("灵敏度分析完成，汇总已写入 q4_output/sensitivity_summary.json")


if __name__ == "__main__":
    main()