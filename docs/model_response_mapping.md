# Model Response Mapping

AI 回答项目问题时必须引用代码、配置、数据和测试证据。

## 回答模板

```md
## 结论

直接回答。

## 定位位置

| 类型 | 说明 | 跳转链接 |
|---|---|---|
| code | 关键实现 | [q2_solution.py:L99-L129](../q2_solution.py#L99-L129) |
| test | 回归测试 | [tests/test_project_improvements.py:L55-L63](../tests/test_project_improvements.py#L55-L63) |

## 验证命令

python -m unittest discover -s tests -v
```

## 常用证据映射

| 问题 | 首选证据 |
|---|---|
| q1 概率从哪里来 | [q1_solution.py:L18-L57](../q1_solution.py#L18-L57) |
| q2 是否完整枚举 | [q2_solution.py:L99-L129](../q2_solution.py#L99-L129) |
| q2 为什么仍可能过载 | [q2_solution.py:L426-L445](../q2_solution.py#L426-L445) |
| q4 为什么不输出负利润 | [q4_solution.py:L112-L122](../q4_solution.py#L112-L122) |
