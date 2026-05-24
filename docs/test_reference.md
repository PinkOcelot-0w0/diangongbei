# Test Reference

## TEST-001 q1 转移概率读取

| 项目 | 内容 |
|---|---|
| 对应需求 | REQ-001 |
| 测试函数 | [tests/test_project_improvements.py:L18-L45](../tests/test_project_improvements.py#L18-L45) |
| 被测函数 | [q1_solution.py:L18-L57](../q1_solution.py#L18-L57) |

运行命令：

```bash
python -m unittest tests.test_project_improvements.ProjectImprovementTests.test_q1_reads_transition_probabilities_from_workbook -v
```

## TEST-002 距离矩阵校验

| 项目 | 内容 |
|---|---|
| 对应需求 | REQ-002 |
| 测试函数 | [tests/test_project_improvements.py:L47-L53](../tests/test_project_improvements.py#L47-L53) |
| 被测函数 | [q2_solution.py:L37-L45](../q2_solution.py#L37-L45) |

## TEST-003 q2 候选站点完整枚举

| 项目 | 内容 |
|---|---|
| 对应需求 | REQ-002 |
| 测试函数 | [tests/test_project_improvements.py:L55-L63](../tests/test_project_improvements.py#L55-L63) |
| 被测函数 | [q2_solution.py:L99-L129](../q2_solution.py#L99-L129) |

## TEST-004 q2 容量核查

| 项目 | 内容 |
|---|---|
| 对应需求 | REQ-002 |
| 测试函数 | [tests/test_project_improvements.py:L65-L78](../tests/test_project_improvements.py#L65-L78) |
| 被测函数 | [q2_solution.py:L426-L445](../q2_solution.py#L426-L445) |

## TEST-005 q4 财务约束

| 项目 | 内容 |
|---|---|
| 对应需求 | REQ-004 |
| 测试函数 | [tests/test_project_improvements.py:L80-L84](../tests/test_project_improvements.py#L80-L84) |
| 被测函数 | [q4_solution.py:L112-L122](../q4_solution.py#L112-L122) |

## 全量测试命令

```bash
python -m unittest discover -s tests -v
```
