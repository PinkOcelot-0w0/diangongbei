# CLI Usage

## 运行顺序

```bash
python q1_solution.py
python q2_solution.py
python q3_solution.py
python q4_solution.py
```

## 命令说明

| 命令 | 说明 | 入口链接 | 主要输出 |
|---|---|---|---|
| `python q1_solution.py` | 预测第 1 年至第 5 年人口和第 5 年需求 | [q1_solution.py:L162-L202](../q1_solution.py#L162-L202) | `q1_output/*.csv` |
| `python q2_solution.py` | 搜索服务站位置、规模和小区分配 | [q2_solution.py:L448-L486](../q2_solution.py#L448-L486) | `q2_output/*.csv` |
| `python q3_solution.py` | 搜索分站分服务定价方案 | [q3_solution.py:L362-L412](../q3_solution.py#L362-L412) | `q3_output/*.csv` |
| `python q4_solution.py` | 搜索统一 markup 方案 | [q4_solution.py:L271-L322](../q4_solution.py#L271-L322) | `q4_output/*.csv` |

## 示例命令

```bash
python q1_solution.py
python q1_solution.py && python q2_solution.py && python q3_solution.py
python -m unittest discover -s tests -v
```

## 输入输出

- 输入：根目录下的题面 PDF 和 5 个 Excel 附件。
- 输出：`q1_output/`、`q2_output/`、`q3_output/`、`q4_output/` 下的 CSV 和可选说明文件。

## 错误码

脚本未自定义错误码。若 Excel 缺失、字段非法或模型无可行解，Python 进程会以非 0 状态退出或输出不可行报告。
