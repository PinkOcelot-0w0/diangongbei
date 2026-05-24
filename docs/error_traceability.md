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

## ERR-0002 同步后 q1 附件路径读取失败

### 错误现象

同步 `origin/main` 到 `79e3191` 后，`python -m pytest -q` 出现 2 个失败，核心错误为：

```text
FileNotFoundError: 附件1_小区基础数据.xlsx
```

### 错误定位

| 类型 | 说明 | 跳转链接 |
|---|---|---|
| 触发位置 | 问题一读取附件 1 | [q1_solution.py:L32-L53](../q1_solution.py#L32-L53) |
| 同类位置 | 问题一读取附件 2 | [q1_solution.py:L56-L81](../q1_solution.py#L56-L81) |
| 概率校验 | 从附件 1 B3/B4 读取并校验转移概率 | [q1_solution.py:L14-L29](../q1_solution.py#L14-L29) |
| 回归测试 | 覆盖附件路径和概率读取 | [tests/test_project_improvements.py:L18-L45](../tests/test_project_improvements.py#L18-L45) |

### 原因分析

仓库实际附件文件名使用全角冒号，例如 `附件1：小区基础数据.xlsx`；同步后的 `q1_solution.py` 使用了不存在的下划线文件名 `附件1_小区基础数据.xlsx` 和 `附件2_服务需求数据.xlsx`。同时，附件 1 第二个工作表的 B3/B4 转移概率读取逻辑被硬编码替代，导致测试无法验证题面数据来源。

### 修复方案

恢复附件 1、附件 2 的真实文件名；恢复 `read_probability_cell()`，继续从附件 1 第二个工作表 B3/B4 读取转移概率。保留 `79e3191` 中已确认正确的第一问年度递推计算顺序。

### 验证命令

```bash
python -m pytest -q
```
