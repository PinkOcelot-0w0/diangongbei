# Customization Guide

## 修改问题一转移概率

优先修改附件 1 第二个工作表 B3/B4。读取与校验逻辑在 [q1_solution.py:L18-L57](../q1_solution.py#L18-L57)。

验证：

```bash
python q1_solution.py
python -m unittest tests.test_project_improvements.ProjectImprovementTests.test_q1_reads_transition_probabilities_from_workbook -v
```

## 修改问题二候选站点范围

默认完整枚举全部站点。若确实需要快速试算，可修改 `TOP_CANDIDATE_SITES`，对应位置为 [q2_solution.py:L23-L25](../q2_solution.py#L23-L25)，候选筛选逻辑为 [q2_solution.py:L99-L129](../q2_solution.py#L99-L129)。

## 改为硬容量约束

当前 q2 是软容量模型，容量核查在 [q2_solution.py:L426-L445](../q2_solution.py#L426-L445)。若改为硬容量，应在 [q2_solution.py:L195-L369](../q2_solution.py#L195-L369) 中剔除利用率大于 1 的方案，并同步更新论文结果。

## 修改 q4 财务约束

统一 markup 的可行性由 [q4_solution.py:L112-L122](../q4_solution.py#L112-L122) 控制。若提高利润率上限，修改 [q4_solution.py:L35-L42](../q4_solution.py#L35-L42)。
