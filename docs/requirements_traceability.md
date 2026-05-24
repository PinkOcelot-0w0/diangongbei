# Requirements Traceability

## REQ-001 问题一人口与需求预测

### 用户场景

根据附件 1 和附件 2 预测未来五年各小区老人结构，并计算第 5 年末理论需求和消费约束后实际需求。

### 实现位置

| 类型 | 说明 | 跳转链接 |
|---|---|---|
| 数据读取 | 小区人口和转移概率 | [q1_solution.py:L32-L53](../q1_solution.py#L32-L53) |
| 概率校验 | 年度状态转移概率校验 | [q1_solution.py:L14-L29](../q1_solution.py#L14-L29) |
| 预测模型 | 五年状态递推 | [q1_solution.py:L84-L107](../q1_solution.py#L84-L107) |
| 需求模型 | 理论需求与消费约束需求 | [q1_solution.py:L110-L159](../q1_solution.py#L110-L159) |
| 测试 | 转移概率来自工作簿 | [tests/test_project_improvements.py:L18-L45](../tests/test_project_improvements.py#L18-L45) |

### 验证命令

```bash
python q1_solution.py
python -m unittest tests.test_project_improvements.ProjectImprovementTests.test_q1_reads_transition_probabilities_from_workbook -v
```

## REQ-002 问题二服务站选址与规模优化

### 用户场景

在建设预算下选择服务站位置和规模，分配各小区，计算覆盖率、满意度、利润和容量风险。

### 实现位置

| 类型 | 说明 | 跳转链接 |
|---|---|---|
| 距离矩阵 | 附件 4 读取 | [q2_solution.py:L37-L45](../q2_solution.py#L37-L45) |
| 候选点 | 默认完整枚举全部站点 | [q2_solution.py:L99-L129](../q2_solution.py#L99-L129) |
| 方案评估 | 分配、满意度、利润 | [q2_solution.py:L195-L369](../q2_solution.py#L195-L369) |
| 搜索入口 | 组合枚举与择优 | [q2_solution.py:L372-L423](../q2_solution.py#L372-L423) |
| 容量核查 | 软容量过载标记 | [q2_solution.py:L426-L445](../q2_solution.py#L426-L445) |
| 测试 | 距离、候选点、容量核查 | [tests/test_project_improvements.py:L47-L78](../tests/test_project_improvements.py#L47-L78) |

### 验证命令

```bash
python q1_solution.py
python q2_solution.py
python -m unittest tests.test_project_improvements.ProjectImprovementTests.test_q2_default_candidate_selection_uses_all_sites -v
```

## REQ-003 问题三服务定价与政府补贴优化

### 用户场景

在问题二站点方案给定后，为各站各服务搜索价格，使老人满意度高且机构满足保本微利约束。

### 实现位置

| 类型 | 说明 | 跳转链接 |
|---|---|---|
| 输入组装 | q1/q2 输出转为站点输入 | [q3_solution.py:L95-L145](../q3_solution.py#L95-L145) |
| 定价评估 | 服务价格、补贴、利润率 | [q3_solution.py:L148-L347](../q3_solution.py#L148-L347) |
| 运行入口 | 输出站点价格和小区满意度 | [q3_solution.py:L362-L412](../q3_solution.py#L362-L412) |

### 验证命令

```bash
python q1_solution.py
python q2_solution.py
python q3_solution.py
```

## REQ-004 问题四灵敏度分析与方案比较

### 用户场景

比较统一 markup 定价方案，保证利润率不超过上限且各站不亏损。

### 实现位置

| 类型 | 说明 | 跳转链接 |
|---|---|---|
| 可调参数 | markup、补贴上限、利润约束 | [q4_solution.py:L28-L42](../q4_solution.py#L28-L42) |
| 财务约束 | 利润非负和利润率上限 | [q4_solution.py:L112-L122](../q4_solution.py#L112-L122) |
| 方案评估 | 统一 markup 枚举 | [q4_solution.py:L125-L268](../q4_solution.py#L125-L268) |
| 输出入口 | 可行结果或不可行报告 | [q4_solution.py:L271-L322](../q4_solution.py#L271-L322) |
| 测试 | 负利润方案拒绝 | [tests/test_project_improvements.py:L80-L84](../tests/test_project_improvements.py#L80-L84) |

### 验证命令

```bash
python q4_solution.py
python -m unittest tests.test_project_improvements.ProjectImprovementTests.test_q4_rejects_negative_profit_even_when_profit_rate_is_under_limit -v
```
