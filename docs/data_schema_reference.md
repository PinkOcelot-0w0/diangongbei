# Data Schema Reference

## 输入数据

| 文件 | 用途 | 使用位置 |
|---|---|---|
| `附件1：小区基础数据.xlsx` | 人口结构和转移概率 | [q1_solution.py:L36-L57](../q1_solution.py#L36-L57) |
| `附件2：服务需求数据.xlsx` | 服务频次、价格、成本、消费上限 | [q1_solution.py:L60-L85](../q1_solution.py#L60-L85) |
| `附件4：小区间距离矩阵.xlsx` | 社区到候选站点距离 | [q2_solution.py:L37-L45](../q2_solution.py#L37-L45) |

## 输出数据

| 文件 | 字段 | 生成位置 |
|---|---|---|
| `q1_output/year5_population.csv` | 小区、60岁以上人口、自理、半失能、失能 | [q1_solution.py:L166-L202](../q1_solution.py#L166-L202) |
| `q1_output/year5_actual_demand.csv` | 小区、老人类型、服务项目、消费约束缩放系数、实际月均需求次数 | [q1_solution.py:L114-L163](../q1_solution.py#L114-L163) |
| `q2_output/best_station_plan.csv` | 站点、规模、分配社区、覆盖社区数、日容量、利用率、响应满意度S2、年度利润 | [q2_solution.py:L195-L369](../q2_solution.py#L195-L369) |
| `q2_output/capacity_check.csv` | 站点、规模、日容量、估计日有效服务人次、利用率、是否过载、容量模型说明 | [q2_solution.py:L426-L445](../q2_solution.py#L426-L445) |
| `q3_output/best_pricing_plan.csv` | 站点、规模、服务价格、满意度、补贴、利润、利润率 | [q3_solution.py:L362-L412](../q3_solution.py#L362-L412) |
| `q4_output/best_pricing_plan.csv` | 站点、统一markup、站点满意度、年利润 | [q4_solution.py:L271-L322](../q4_solution.py#L271-L322) |
