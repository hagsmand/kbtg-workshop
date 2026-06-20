---
name: onboard-and-test
description: Use when the user wants to onboard a new project with AI agents — runs Documentation Agent and Code Quality Critic in parallel, passes their findings to Bug Finder, fixes all discovered bugs, then hands off to Tester Agent to write and run tests.
---

# Project Onboarding & Test Workflow

Follow these steps in order. Each step depends on the output of the previous one.

## Step 1 — Explore the project

Before spawning any agents, read enough of the project to brief them accurately:

1. Use `list_files` (recursive) to map the full file structure.
2. Read every source file that contains logic (JS, Python, etc.) and any existing docs.
3. Read `.bob/custom_modes.yaml` to confirm the four agent modes exist:
   `docs-writer`, `code-quality-critic`, `bug-finder`, `tester-agent`.

## Step 2 — Run Documentation Agent and Code Quality Critic in parallel

Call `spawn_subagent` **twice in the same tool-call block** (no dependencies between them):

**Documentation Agent subagent brief:**
- Role: `docs-writer` persona — reads code, writes Markdown only.
- Task: Read all source files and produce a `README.md` covering: project overview, file structure, how to run, feature walkthrough, function reference, and a Known Bugs section.
- Output file: `README.md` in the workspace root.
- Return: summary of what was documented and any notable observations.

**Code Quality Critic subagent brief:**
- Role: `code-quality-critic` persona — reviews across Correctness, Maintainability, Robustness, Best Practices.
- Task: Read all source files. For every issue found report: Issue ID, Pillar, file+line, what the code does, what it should do, Severity, and a before/after fix recommendation.
- Output file: `CODE_QUALITY_REPORT.md` in the workspace root.
- Return: total issues by severity and pillar, list of confirmed bugs.

Wait for both subagents to finish before proceeding.

## Step 3 — Run Bug Finder using both reports as context

Read `README.md` and `CODE_QUALITY_REPORT.md` fully, then call `spawn_subagent` once:

**Bug Finder subagent brief:**
- Role: `bug-finder` persona — covers Logic bugs AND UI/UX presentation bugs (including catch blocks that re-expose raw internal error strings or backend terminology to the user).
- Context to pass in: the complete findings from Step 2 (confirmed bugs, quality issues, code observations).
- Task:
  1. Read the source files in full.
  2. Confirm every bug identified by the prior two agents with exact file:line citations.
  3. Trace every data-flow path (user input → validation → computation → render) to find bugs the prior agents missed.
  4. For each bug report: Bug ID, Category (Logic / UI-UX / Security), file+line, what the code does, what it should do, Severity, user-visible symptom.
  5. Produce a prioritized fix plan ordered by severity.
- Output file: `BUG_REPORT.md` in the workspace root.
- Return: total bugs (confirmed + new), any newly discovered bugs, fix priority order.

Wait for the subagent to finish before proceeding.

## Step 4 — Fix all bugs

Read `BUG_REPORT.md` in full. Then apply every fix directly using `apply_diff` or `search_and_replace`:

1. Use `update_todo_list` to track each bug: pending → in-progress → fixed.
2. Apply all independent fixes in a **single `apply_diff` call** using multiple SEARCH/REPLACE blocks.
3. For each fix make the minimal targeted change — no refactors, no new features.
4. After applying, read back the changed file to verify correctness.
5. Mark all todos complete.

## Step 5 — Run Tester Agent

Read the fully fixed source file(s), then call `spawn_subagent` once:

**Tester Agent subagent brief:**
- Role: `tester-agent` persona — writes, runs, and diagnoses tests.
- Context to pass in: the complete fixed logic functions (copy the actual source), the full bug list with what each bug was and what fix was applied (all bugs become mandatory regression tests).
- Task:
  1. Check whether a test framework already exists (`package.json`, test files). If not, scaffold **Jest** for JS projects (or pytest for Python): create `package.json` and a dedicated logic module that exports pure functions (do NOT modify the original source file).
  2. Write tests covering: all happy paths, all edge cases, all boundary conditions, and a dedicated regression test for every bug that was fixed.
  3. Run the tests immediately using `execute_command`. Report full output: pass count, fail count, error messages.
  4. If any test fails, diagnose (bug in source vs wrong assertion), fix, and re-run.
  5. After all tests pass, write `TEST_REPORT.md`: total tests, pass count, coverage areas, any untested paths and why.
- Return: pass/fail counts, regression coverage, any untested paths.

## Step 6 — Report completion

Summarise the full pipeline result to the user in a single response:

- **Documentation Agent** → what was documented, any notable observations
- **Code Quality Critic** → total issues by severity and pillar
- **Bug Finder** → total bugs, how many were new vs confirmed, fix priority
- **Bug Fixes** → each bug ID, one-line description of the change made
- **Tester Agent** → total tests written, pass count, regression bugs covered, any untested paths
