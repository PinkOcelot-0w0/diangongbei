# Project Onboarding

## 1. 项目目标

本项目求解 B 题“嵌入式社区养老服务站的建设与优化问题”，产出未来五年老人数量与服务需求预测、社区养老服务站选址规模方案、服务定价和政府补贴方案、灵敏度分析结果。

## 2. 系统边界

当前包含：

- 人口状态转移和消费约束需求预测。
- 软容量服务站选址、规模、覆盖与满意度优化。
- 分服务定价和统一 markup 定价方案搜索。
- CSV 输出和基于 `unittest` 的回归测试。

当前不包含：

- HTTP API、数据库或前端页面。
- 默认硬容量选址重算。
- 论文 DOCX 自动改写。

## 3. 核心功能地图

| 功能 | 需求编号 | 代码入口 | 测试入口 |
|---|---|---|---|
| 人口与需求预测 | REQ-001 | [q1_solution.py:L166-L202](../q1_solution.py#L166-L202) | [tests/test_project_improvements.py:L18-L45](../tests/test_project_improvements.py#L18-L45) |
| 选址与规模优化 | REQ-002 | [q2_solution.py:L448-L486](../q2_solution.py#L448-L486) | [tests/test_project_improvements.py:L47-L78](../tests/test_project_improvements.py#L47-L78) |
| 定价与补贴优化 | REQ-003 | [q3_solution.py:L362-L412](../q3_solution.py#L362-L412) | [tests/test_project_improvements.py:L15-L84](../tests/test_project_improvements.py#L15-L84) |
| 灵敏度与统一定价 | REQ-004 | [q4_solution.py:L271-L322](../q4_solution.py#L271-L322) | [tests/test_project_improvements.py:L80-L84](../tests/test_project_improvements.py#L80-L84) |

## 4. 新同事阅读顺序

1. [架构说明](./architecture.md)
2. [需求追踪](./requirements_traceability.md)
3. [程序索引](./program_index.md)
4. [CLI 使用说明](./cli_usage.md)
5. [测试说明](./test_reference.md)
6. [常见问题排查](./troubleshooting.md)

## 5. 常见任务入口

| 任务 | 先看文档 | 代码入口 |
|---|---|---|
| 修改人口预测参数 | [config_reference.md](./config_reference.md) | [q1_solution.py:L18-L57](../q1_solution.py#L18-L57) |
| 修改选址搜索范围 | [requirements_traceability.md](./requirements_traceability.md#req-002-问题二服务站选址与规模优化) | [q2_solution.py:L99-L129](../q2_solution.py#L99-L129) |
| 排查 q4 不可行 | [troubleshooting.md](./troubleshooting.md#q4-未找到满足条件的方案) | [q4_solution.py:L271-L322](../q4_solution.py#L271-L322) |
