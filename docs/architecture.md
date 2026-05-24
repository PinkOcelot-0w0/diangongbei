# Architecture

## 1. 总体架构

项目采用四个顺序执行的脚本，不引入服务端、数据库或前端框架。

```text
附件1/附件2
  -> q1_solution.py
  -> q1_output/*.csv
  -> q2_solution.py + 附件4
  -> q2_output/*.csv
  -> q3_solution.py + 附件2
  -> q3_output/*.csv
  -> q4_solution.py
  -> q4_output/*.csv
```

## 2. 模块边界

| 模块 | 职责 | 入口 |
|---|---|---|
| 问题一 | 读取人口、转移概率、需求频次和消费上限，生成五年预测和第 5 年需求 | [q1_solution.py:L162-L202](../q1_solution.py#L162-L202) |
| 问题二 | 读取 q1 需求和距离矩阵，枚举服务站位置与规模，输出分配和容量核查 | [q2_solution.py:L448-L486](../q2_solution.py#L448-L486) |
| 问题三 | 基于 q2 站点分配，搜索分站分服务价格和补贴方案 | [q3_solution.py:L148-L347](../q3_solution.py#L148-L347) |
| 问题四 | 基于 q1/q2 输出搜索统一 markup，并加入利润非负约束 | [q4_solution.py:L125-L268](../q4_solution.py#L125-L268) |

## 3. 关键设计决策

- q2 保留软容量模型：过载不剔除方案，但会降低响应满意度并输出核查表：[q2_solution.py:L426-L445](../q2_solution.py#L426-L445)。
- q2 默认不再截断候选点，完整枚举 10 个小区：[q2_solution.py:L99-L129](../q2_solution.py#L99-L129)。
- q4 同时约束利润率上限和利润非负：[q4_solution.py:L112-L122](../q4_solution.py#L112-L122)。
