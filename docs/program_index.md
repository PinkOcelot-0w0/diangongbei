# Program Index

## q1_solution.py

### 文件职责

问题一入口，负责人口状态转移预测、服务需求频次读取、消费约束计算和 q1 输出。

### 核心符号

| 符号 | 类型 | 跳转链接 | 说明 |
|---|---|---|---|
| `read_probability_cell` | function | [q1_solution.py:L18-L33](../q1_solution.py#L18-L33) | 校验年度转移概率 |
| `load_community_data` | function | [q1_solution.py:L36-L57](../q1_solution.py#L36-L57) | 读取人口结构和转移概率 |
| `forecast_five_years` | function | [q1_solution.py:L88-L111](../q1_solution.py#L88-L111) | 预测五年老人结构 |
| `build_service_tables` | function | [q1_solution.py:L114-L163](../q1_solution.py#L114-L163) | 计算理论和实际需求 |
| `main` | function | [q1_solution.py:L166-L202](../q1_solution.py#L166-L202) | 输出 q1 CSV |

## q2_solution.py

### 文件职责

问题二入口，负责读取距离矩阵、完整候选站点枚举、服务站选址规模优化和容量核查。

### 核心符号

| 符号 | 类型 | 跳转链接 | 说明 |
|---|---|---|---|
| `select_candidate_sites` | function | [q2_solution.py:L99-L129](../q2_solution.py#L99-L129) | 默认完整选择候选站点 |
| `solve_station_s2` | function | [q2_solution.py:L152-L192](../q2_solution.py#L152-L192) | 求响应满意度固定点 |
| `evaluate_plan` | function | [q2_solution.py:L195-L369](../q2_solution.py#L195-L369) | 评估选址规模方案 |
| `search_best_plan` | function | [q2_solution.py:L372-L423](../q2_solution.py#L372-L423) | 枚举并选择最优方案 |
| `build_capacity_check` | function | [q2_solution.py:L426-L445](../q2_solution.py#L426-L445) | 输出软容量核查 |

## q3_solution.py

### 文件职责

问题三入口，负责分站、分服务价格搜索和政府补贴核算。

### 核心符号

| 符号 | 类型 | 跳转链接 | 说明 |
|---|---|---|---|
| `build_station_inputs` | function | [q3_solution.py:L95-L145](../q3_solution.py#L95-L145) | 组装站点输入 |
| `evaluate_station_prices` | function | [q3_solution.py:L148-L347](../q3_solution.py#L148-L347) | 搜索站点价格 |
| `main` | function | [q3_solution.py:L362-L412](../q3_solution.py#L362-L412) | 输出 q3 CSV |

## q4_solution.py

### 文件职责

问题四入口，负责统一 markup 方案搜索、利润约束检查和不可行报告输出。

### 核心符号

| 符号 | 类型 | 跳转链接 | 说明 |
|---|---|---|---|
| `is_station_financially_feasible` | function | [q4_solution.py:L112-L122](../q4_solution.py#L112-L122) | 检查利润非负和利润率上限 |
| `evaluate_markups` | function | [q4_solution.py:L125-L268](../q4_solution.py#L125-L268) | 搜索统一 markup 方案 |
| `main` | function | [q4_solution.py:L271-L322](../q4_solution.py#L271-L322) | 输出 q4 CSV 或不可行报告 |
