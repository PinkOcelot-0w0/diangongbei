# AGENTS.md

## 协作规则

- 所有文件读写使用 UTF-8 编码。
- PowerShell 读取中文文件前先执行 `chcp 65001`，并设置 UTF-8 输入输出。
- 读取中文文件使用 `Get-Content -Encoding UTF8`，不要用 `sed`/`awk` 处理中文内容。
- 代码注释使用中文，保持简短、具体、可维护。
- 修改代码后必须同步更新相关文档和测试。

## 文档优先级

1. `README.md`、`AGENTS.md`、`docs/project_onboarding.md`
2. `docs/architecture.md`
3. `docs/requirements_traceability.md`
4. `docs/program_index.md`
5. `docs/cli_usage.md`
6. `docs/test_reference.md`
7. `docs/troubleshooting.md`
8. `docs/error_traceability.md`
9. `docs/config_reference.md`
10. `docs/api_reference.md`
11. `docs/data_schema_reference.md`
12. `docs/customization_guide.md`

## 链接规范

文档中的代码定位必须使用可点击行号链接：

```md
[说明 q1_solution.py:L36-L57](../q1_solution.py#L36-L57)
```

没有真实行号时使用 `TODO-LINES`，禁止编造行号。

## 验证命令

```bash
python q1_solution.py
python q2_solution.py
python q3_solution.py
python q4_solution.py
python -m unittest discover -s tests -v
```
