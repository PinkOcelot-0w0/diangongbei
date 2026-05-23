# Project Improvement Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Improve the project according to the provided paper while keeping current baseline results reproducible.

**Architecture:** Keep the four existing scripts as the runnable entrypoints. Add small helper functions, regression tests, and traceability documents around the current data flow instead of restructuring the repository.

**Tech Stack:** Python 3, pandas, openpyxl, standard-library unittest, Markdown documentation.

---

### Task 1: Baseline Tests

**Files:**
- Create: `tests/test_project_improvements.py`
- Modify: no production files in this task

- [ ] **Step 1: Write failing tests**

Create tests that assert q1 reads transition probabilities from the workbook, q2 uses all candidate sites by default, the distance matrix is symmetric, q2 capacity rows can mark overload, and q4 rejects negative profit.

- [ ] **Step 2: Run tests to verify failures**

Run:

```bash
python -m unittest discover -s tests -v
```

Expected before implementation: at least one failure because q2 still truncates candidates and q4 does not expose a reusable negative-profit check.

### Task 2: q1/q2/q4 Minimal Fixes

**Files:**
- Modify: `q1_solution.py`
- Modify: `q2_solution.py`
- Modify: `q4_solution.py`
- Test: `tests/test_project_improvements.py`

- [ ] **Step 1: Implement q1 workbook probability parsing**

Read `self_to_semi` and `semi_to_disabled` from attachment 1 sheet 2 cells B3 and B4, validate that each value is numeric and between 0 and 1, then return them.

- [ ] **Step 2: Implement q2 full candidate enumeration and capacity check output**

Set default candidate limit to no limit, derive candidate sites from the full distance matrix, and write `q2_output/capacity_check.csv` from the selected station rows.

- [ ] **Step 3: Implement q4 profit nonnegative feasibility**

Add `MIN_PROFIT = 0.0`, reject any station with `annual_profit < MIN_PROFIT`, and write an infeasibility report if no candidate is feasible.

- [ ] **Step 4: Run focused tests**

Run:

```bash
python -m unittest tests.test_project_improvements -v
```

Expected after implementation: all tests pass.

### Task 3: Traceability Documentation

**Files:**
- Create: `README.md`
- Create: `AGENTS.md`
- Create: `docs/project_onboarding.md`
- Create: `docs/architecture.md`
- Create: `docs/requirements_traceability.md`
- Create: `docs/program_index.md`
- Create: `docs/cli_usage.md`
- Create: `docs/test_reference.md`
- Create: `docs/troubleshooting.md`
- Create: `docs/question_traceability.md`
- Create: `docs/error_traceability.md`
- Create: `docs/config_reference.md`
- Create: `docs/api_reference.md`
- Create: `docs/data_schema_reference.md`
- Create: `docs/customization_guide.md`
- Create: `docs/model_response_mapping.md`
- Create: `docs/link_policy.md`
- Create directory: `docs/decision_records/`
- Create directory: `docs/handoffs/`

- [ ] **Step 1: Add concise project docs**

Write the project goal, data flow, command sequence, output files, known model limits, and clickable code line links.

- [ ] **Step 2: Add test references**

Document `python -m unittest discover -s tests -v` and map each new test to its requirement.

### Task 4: End-to-End Verification

**Files:**
- Read/verify generated CSV files in `q1_output/`, `q2_output/`, `q3_output/`, and `q4_output/`

- [ ] **Step 1: Run q1 to q4**

Run:

```bash
python q1_solution.py
python q2_solution.py
python q3_solution.py
python q4_solution.py
```

- [ ] **Step 2: Run all tests**

Run:

```bash
python -m unittest discover -s tests -v
```

- [ ] **Step 3: Inspect git diff**

Run:

```bash
git status --short
git diff --stat
```

Expected: code, tests, docs, and regenerated output files reflect scheme A only.
