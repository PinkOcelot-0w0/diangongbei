# 嵌入式社区养老服务站建设与优化

本项目用于复现 B 题“嵌入式社区养老服务站的建设与优化问题”的四问建模流程：人口与服务需求预测、服务站选址与规模优化、服务定价与补贴优化、灵敏度与统一定价方案比较。

## 快速启动

```bash
python -m pip install -r requirements.txt
python q1_solution.py
python q2_solution.py
python q3_solution.py
python q4_solution.py
python -m unittest discover -s tests -v
```

## 程序入口

| 问题 | 程序 | 主要输出 |
|---|---|---|
| 问题一 | [q1_solution.py:L166-L202](q1_solution.py#L166-L202) | `q1_output/year5_population.csv`、`q1_output/year5_actual_demand.csv` |
| 问题二 | [q2_solution.py:L448-L486](q2_solution.py#L448-L486) | `q2_output/best_station_plan.csv`、`q2_output/capacity_check.csv` |
| 问题三 | [q3_solution.py:L362-L412](q3_solution.py#L362-L412) | `q3_output/best_pricing_plan.csv` |
| 问题四 | [q4_solution.py:L271-L322](q4_solution.py#L271-L322) | `q4_output/best_pricing_plan.csv`、`q4_output/infeasibility_report.txt` |

## 本次完善点

- 问题一转移概率改为从附件 1 第二个工作表读取：[q1_solution.py:L18-L57](q1_solution.py#L18-L57)。
- 问题二默认完整枚举 10 个候选站点：[q2_solution.py:L99-L129](q2_solution.py#L99-L129)。
- 问题二保留软容量模型，并新增容量核查输出：[q2_solution.py:L426-L445](q2_solution.py#L426-L445)。
- 问题四新增利润非负约束：[q4_solution.py:L112-L122](q4_solution.py#L112-L122)。
- 新增回归测试：[tests/test_project_improvements.py:L15-L84](tests/test_project_improvements.py#L15-L84)。

## 文档入口

先读 [docs/project_onboarding.md](docs/project_onboarding.md)，再按需查看架构、需求追踪、程序索引、CLI、测试和排错文档。
