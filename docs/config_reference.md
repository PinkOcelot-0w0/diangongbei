# Config Reference

本项目没有独立配置文件，配置来自 Excel 附件和脚本顶部常量。

| 字段 | 类型 | 默认值 | 使用位置 | 修改风险 | 测试方式 |
|---|---|---|---|---|---|
| 附件1 B3 自理转半失能概率 | float | 0.045 | [q1_solution.py:L32-L53](../q1_solution.py#L32-L53) | 影响五年人口结构和所有后续需求 | `python q1_solution.py` |
| 附件1 B4 半失能转失能概率 | float | 0.1 | [q1_solution.py:L32-L53](../q1_solution.py#L32-L53) | 影响失能需求和护理/助浴需求 | `python q1_solution.py` |
| `TOP_CANDIDATE_SITES` | int 或 None | None | [q2_solution.py:L23-L25](../q2_solution.py#L23-L25) | 设置为整数会截断候选点，可能漏全局最优 | `python -m unittest tests.test_project_improvements.ProjectImprovementTests.test_q2_default_candidate_selection_uses_all_sites -v` |
| `MAX_SELECTED_SITES` | int | 5 | [q2_solution.py:L23-L25](../q2_solution.py#L23-L25) | 限制服务站数量，影响覆盖率和成本 | `python q2_solution.py` |
| `MARKUP_OPTIONS` | list[float] | -0.3 到 0.3 | [q4_solution.py:L28-L30](../q4_solution.py#L28-L30) | 候选集过窄可能导致 q4 不可行 | `python q4_solution.py` |
| `PROFIT_RATE_LIMIT` | float | 8.0 | [q4_solution.py:L35-L42](../q4_solution.py#L35-L42) | 影响财务可行性筛选 | `python -m unittest tests.test_project_improvements.ProjectImprovementTests.test_q4_rejects_negative_profit_even_when_profit_rate_is_under_limit -v` |
| `MIN_PROFIT` | float | 0.0 | [q4_solution.py:L35-L42](../q4_solution.py#L35-L42) | 小于 0 会重新允许亏损站点 | `python -m unittest tests.test_project_improvements.ProjectImprovementTests.test_q4_rejects_negative_profit_even_when_profit_rate_is_under_limit -v` |
