# Troubleshooting

## 启动失败

| 项目 | 内容 |
|---|---|
| 错误现象 | `ModuleNotFoundError` 或依赖导入失败 |
| 常见原因 | 未安装 `requirements.txt` |
| 定位文件 | [requirements.txt:L1-L10](../requirements.txt#L1-L10) |
| 验证命令 | `python -m pip install -r requirements.txt` |

## q1 转移概率读取失败

| 项目 | 内容 |
|---|---|
| 错误现象 | `ValueError: 自理转半失能概率 必须...` |
| 常见原因 | 附件 1 第二个工作表 B3/B4 为空、非数值或不在 0 到 1 |
| 定位文件 | [q1_solution.py:L14-L53](../q1_solution.py#L14-L53) |
| 验证命令 | `python q1_solution.py` |

## q2 容量过载

| 项目 | 内容 |
|---|---|
| 错误现象 | `q2_output/capacity_check.csv` 中“是否过载”为“是” |
| 常见原因 | 当前方案采用软容量模型，过载会降低响应满意度但不剔除方案 |
| 定位文件 | [q2_solution.py:L426-L445](../q2_solution.py#L426-L445) |
| 修复方式 | 若要严格容量可行，需要新增硬容量约束并同步修改论文结果 |
| 验证命令 | `python q2_solution.py` |

## q4 未找到满足条件的方案

| 项目 | 内容 |
|---|---|
| 错误现象 | 控制台输出“未找到满足条件的方案” |
| 常见原因 | 统一 markup 方案无法同时满足利润非负和利润率不超过 8% |
| 定位文件 | [q4_solution.py:L271-L322](../q4_solution.py#L271-L322) |
| 输出文件 | `q4_output/infeasibility_report.txt` |
| 修复方式 | 扩大 markup 候选集、提高补贴上限、调整站点规模或改用 q3 分服务定价 |
