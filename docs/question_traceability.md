# Question Traceability

## Q-0001 如何基于论文完善项目？

### 用户原始问题

“请你基于这个文档，去帮我完善这个项目”

### 回答摘要

根据论文第七节，项目需要补齐 README/docs/tests，并修复 q1 转移概率硬编码、q2 候选点截断、q2 容量核查缺失、q4 负利润仍被输出的问题。

### 对应实现位置

| 类型 | 说明 | 跳转链接 |
|---|---|---|
| q1 | 转移概率从附件读取 | [q1_solution.py:L18-L57](../q1_solution.py#L18-L57) |
| q2 | 候选站点完整枚举 | [q2_solution.py:L99-L129](../q2_solution.py#L99-L129) |
| q2 | 容量核查输出 | [q2_solution.py:L426-L445](../q2_solution.py#L426-L445) |
| q4 | 利润非负约束 | [q4_solution.py:L112-L122](../q4_solution.py#L112-L122) |
| test | 回归测试 | [tests/test_project_improvements.py:L15-L84](../tests/test_project_improvements.py#L15-L84) |

### 验证命令

```bash
python -m unittest discover -s tests -v
```
