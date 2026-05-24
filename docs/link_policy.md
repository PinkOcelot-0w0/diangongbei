# 链接规范

## 相对路径链接

用于本地 Markdown 文档：

```md
[函数名 q1_solution.py:L36-L57](../q1_solution.py#L36-L57)
```

## 根目录文档链接

根目录 `README.md` 使用：

```md
[q1_solution.py:L36-L57](q1_solution.py#L36-L57)
```

## TODO-LINES

无法读取真实行号时使用：

```md
[说明 q1_solution.py:TODO-LINES](../q1_solution.py)
```

写入 `TODO-LINES` 后必须在后续扫描中补齐真实行号。禁止编造行号，禁止把文件路径和行号拆成两段文本。
