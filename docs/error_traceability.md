# Error Traceability

## ERR-0001 q4 输出负利润方案

### 错误现象

`q4_output/best_pricing_plan.csv` 中曾出现 C 站和 J 站年度利润为负，但脚本仍将其作为最优方案输出。

### 错误定位

| 类型 | 说明 | 跳转链接 |
|---|---|---|
| 原始约束 | 仅检查利润率是否超过上限 | [q4_solution.py:L125-L268](../q4_solution.py#L125-L268) |
| 修复位置 | 新增利润非负和利润率上限统一判断 | [q4_solution.py:L112-L122](../q4_solution.py#L112-L122) |
| 测试 | 负利润方案必须不可行 | [tests/test_project_improvements.py:L80-L84](../tests/test_project_improvements.py#L80-L84) |

### 修复方案

新增 `MIN_PROFIT = 0.0`，并通过 `is_station_financially_feasible()` 同时检查 `annual_profit >= 0` 和 `profit_rate <= 8`。

### 验证命令

```bash
python q4_solution.py
python -m unittest tests.test_project_improvements.ProjectImprovementTests.test_q4_rejects_negative_profit_even_when_profit_rate_is_under_limit -v
```
