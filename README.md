# 🎓 Student Grade Tracker — KBTG Workshop

> **Workshop context:** This project is a deliberately buggy single-page web application used as a hands-on training exercise. Participants practise manual bug hunting, then build specialised AI agents to automate code review, documentation, bug finding, and test generation.

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [File Structure](#2-file-structure)
3. [How to Run the App](#3-how-to-run-the-app)
4. [Feature Walkthrough](#4-feature-walkthrough)
   - 4.1 [Add Student](#41-add-student)
   - 4.2 [Remove Student](#42-remove-student)
   - 4.3 [Stats Bar](#43-stats-bar)
   - 4.4 [Grade Table](#44-grade-table)
5. [JavaScript Function Reference](#5-javascript-function-reference)
6. [Known Intentional Bugs](#6-known-intentional-bugs)
7. [Lab Guide Summary](#7-lab-guide-summary)

---

## 1. Project Overview

**Student Grade Tracker** is a zero-dependency, single-file web application that lets a user manage a list of students and their exam scores. It calculates averages, assigns letter grades, and surfaces class-level statistics in real time.

The application is intentionally seeded with **four bugs** in the JavaScript logic layer. The buggy outputs are rendered **side-by-side with correct outputs** so that discrepancies are immediately visible in the UI — the design choice that makes the app useful as a training artefact. The footer explicitly warns: *"Averages may look wrong — that's intentional! Find & fix the bugs in the JS."*

**Primary purpose:** Serve as a realistic but compact codebase for the KBTG workshop's AI-agent skill lab (see [Lab Guide Summary](#7-lab-guide-summary)).

---

## 2. File Structure

```
kbtg-workshop/
├── student_grades.html   # The entire application — HTML, CSS, and JS in one file
├── lab_guide.md          # Workshop lab instructions
└── README.md             # This document
```

| File | Description |
|---|---|
| `student_grades.html` | Self-contained SPA. No build step, no dependencies, no server required. |
| `lab_guide.md` | Step-by-step lab guide for the KBTG Bob Workshop (Lab 1: Agent Skill). |
| `README.md` | Project documentation (this file). |

---

## 3. How to Run the App

Because the application has **no external dependencies and no build step**, running it is trivial:

### Option A — Open directly in a browser (simplest)

```bash
# From the project root
open student_grades.html          # macOS
start student_grades.html         # Windows
xdg-open student_grades.html      # Linux
```

Or simply double-click `student_grades.html` in your file explorer.

### Option B — Serve over HTTP (recommended for development)

Any static file server works:

```bash
# Python 3
python -m http.server 8080
# then visit http://localhost:8080/student_grades.html

# Node.js (npx)
npx serve .
```

### Requirements

| Requirement | Details |
|---|---|
| Browser | Any modern browser (Chrome, Firefox, Edge, Safari) |
| Internet | Not required — no CDN assets are loaded |
| Build tools | None |
| Runtime / server | None (Option A) |

---

## 4. Feature Walkthrough

The layout is split into two panels inside a dark-themed (`#1e1e2e` background) Catppuccin-inspired colour scheme.

### 4.1 Add Student

**Location:** Left panel, top section.

| Field | Description |
|---|---|
| **Name** | Free-text student name. Must be unique. |
| **Scores** | Comma-separated numeric scores, e.g. `85, 90, 78`. Non-numeric tokens are silently dropped. |

**Behaviour:**
- Pressing **➕ Add Student** or hitting `Enter` while focused on the Scores field calls `onAdd()`.
- Validation prevents empty names, duplicate names, and completely non-numeric score strings.
- On success, both inputs are cleared and a green toast (`✓ Added <name>`) appears for 3 seconds.
- On failure, a red toast describes the specific error.
- The table and stats bar refresh immediately after a successful add.

**Demo data pre-loaded on startup:**

| Name | Scores |
|---|---|
| Alice | 95, 88, 92, 100, 85 |
| Bob | 70, 65, 80, 75, 60 |
| Charlie | 55, 60, 58, 62, 70 |
| Diana | 100, 98, 97, 99, 100 |
| Eve | 100, 98, 97, 99, 100 *(tied with Diana — intentional)* |

---

### 4.2 Remove Student

**Location:** Left panel, bottom section.

| Field | Description |
|---|---|
| **Name** | The exact name of the student to remove (case-sensitive). |

**Behaviour:**
- Pressing **🗑 Remove Student** or hitting `Enter` inside the name field calls `onRemove()`.
- If the name is found, the student is deleted from the in-memory store and the table refreshes.
- If the name is not found, `removeStudent()` throws a `KeyError`-style exception, and a red toast displays the message.
- The input is cleared only on success.

---

### 4.3 Stats Bar

**Location:** Top of the right panel, always visible.

| Stat | Element ID | Description |
|---|---|---|
| **Total Students** | `stat-count` | Count of students currently in the store. |
| **Class Average** | `stat-avg` | Average of each student's individual (buggy) average. Rendered in **red** to signal it is computed with buggy logic. |
| **Simple Mean** | `stat-avg-simple` | Correct grand mean: sum of every individual score divided by total score count. Rendered in **green**. |
| **Top Student** | `stat-top` | Student with the highest buggy average (uses `>=` comparison, so a tie always resolves to the *last* equal entry). Rendered in default yellow. |
| **Highest Scorer** | `stat-top-correct` | Student with the highest correct average (uses strict `>`, so a tie resolves to the *first* entry). Rendered in **green**. |

The intentional contrast between the red/buggy column and the green/correct column is the visual learning cue.

---

### 4.4 Grade Table

**Location:** Right panel, below the stats bar.

| Column | Description |
|---|---|
| **Name** | Student name (HTML-escaped). |
| **Scores** | All raw scores as a comma-separated list. |
| **Average** | Buggy average from `calculateAverage()`. Highlighted **red** when it differs from the correct average by more than 0.001. |
| **Sum ÷ Count** | Correct average: `sum / scores.length`. Always shown in **green**. |
| **Grade** | Letter grade badge derived from the *buggy* average via `getGradeLetter()`. |
| **Highest** | Highest single score via `Math.max`. |
| **Lowest** | Lowest single score via `Math.min`. |

Grade badge colour coding:

| Grade | Threshold | Colour |
|---|---|---|
| A | avg ≥ 90 | Green |
| B | avg ≥ 80 | Blue |
| C | avg ≥ 70 | Yellow |
| D | avg ≥ 60 | Orange |
| F | avg < 60 | Red |

When the store is empty, a full-width italic placeholder row reads *"No students yet. Add one on the left."*

---

## 5. JavaScript Function Reference

All logic lives inside a single `<script>` block at the bottom of `student_grades.html`. There is no module system; all symbols are global.

### Data Store

```js
const students = {};   // { [name: string]: number[] }
```

A plain object keyed by student name, with an array of numeric scores as each value.

---

### Logic Functions

#### `calculateAverage(scores)`

```js
function calculateAverage(scores) {
    const total = scores.reduce((a, b) => a + b, 0);
    return total / (scores.length + 1);   // ← BUG 1: divides by length+1
}
```

| | |
|---|---|
| **Input** | `scores` — `number[]` |
| **Returns** | `number` — the mean of `scores` |
| **Bug** | Divides by `scores.length + 1` instead of `scores.length`, producing a result that is always **smaller than the true average**. |

---

#### `getHighestScore(scores)`

```js
function getHighestScore(scores) { return Math.max(...scores); }
```

| | |
|---|---|
| **Input** | `scores` — `number[]` |
| **Returns** | `number` — the maximum value in `scores` |
| **Status** | ✅ Correct |

---

#### `getLowestScore(scores)`

```js
function getLowestScore(scores) { return Math.min(...scores); }
```

| | |
|---|---|
| **Input** | `scores` — `number[]` |
| **Returns** | `number` — the minimum value in `scores` |
| **Status** | ✅ Correct |

---

#### `getGradeLetter(avg)`

```js
function getGradeLetter(avg) {
    if (avg >= 90) return "A";
    if (avg >= 80) return "B";
    if (avg >= 70) return "C";
    if (avg >= 60) return "D";
    return "F";
}
```

| | |
|---|---|
| **Input** | `avg` — `number` (the result of `calculateAverage`) |
| **Returns** | `"A"` \| `"B"` \| `"C"` \| `"D"` \| `"F"` |
| **Status** | ✅ Correct logic; however it receives the *buggy* average, so the letter grade may be wrong as a downstream consequence of Bug 1. |

---

#### `getClassAverage()`

```js
function getClassAverage() {
    const names = Object.keys(students);
    if (names.length === 0) return null;
    const allAvgs = names.map(n => calculateAverage(students[n]));
    return allAvgs.reduce((a, b) => a + b, 0) / (allAvgs.length - 1);  // ← BUG 2
}
```

| | |
|---|---|
| **Input** | *(none — reads global `students`)* |
| **Returns** | `number \| null` — mean of all per-student averages, or `null` when empty |
| **Bug** | Divides by `allAvgs.length - 1` instead of `allAvgs.length`. With a single student the result is `Infinity` (division by zero), which is why the UI special-cases `names.length === 1`. With multiple students the class average is **always inflated**. |

---

#### `findTopStudent()`

```js
function findTopStudent() {
    ...
    if (avg >= topAvg) {   // ← BUG 3: >= instead of >
        topAvg = avg;
        topName = name;
    }
    ...
}
```

| | |
|---|---|
| **Input** | *(none — reads global `students`)* |
| **Returns** | `{ name: string, avg: number } \| null` |
| **Bug** | Uses `>=` in the comparison, so when two students share the same highest average the **last** one encountered wins. The correct implementation uses strict `>` so the **first** one wins. This is observable with the pre-loaded Diana/Eve tie. |

---

#### `removeStudent(name)`

```js
function removeStudent(name) {
    if (students[name] === undefined) {
        throw new Error(`KeyError: '${name}'`);
    }
    delete students[name];
}
```

| | |
|---|---|
| **Input** | `name` — `string` |
| **Returns** | `void` |
| **Throws** | `Error` with a `KeyError`-style message if the name is not found |
| **Status** | ✅ Correct |

---

### UI Helper Functions

#### `showToast(id, msg, type)`

Displays a feedback message inside the element with the given `id`.

| Parameter | Type | Description |
|---|---|---|
| `id` | `string` | DOM element ID (`"toast-add"` or `"toast-remove"`) |
| `msg` | `string` | Message text to display |
| `type` | `"success"` \| `"error"` | Controls CSS class and therefore background/text colour |

The toast auto-dismisses after **3 seconds** via `setTimeout`.

---

#### `refreshTable()`

The central render function. Called after every add or remove operation.

1. Clears `<tbody id="table-body">`.
2. Iterates over all students and appends a `<tr>` per student with all seven columns.
3. Computes both the buggy average and the correct average inline; applies `avg-mismatch` (red) CSS class when they differ by more than 0.001.
4. Updates all five stat-bar elements (`stat-count`, `stat-avg`, `stat-avg-simple`, `stat-top`, `stat-top-correct`).
5. Renders the empty-state placeholder row when `students` is empty.

---

#### `escHtml(str)`

Sanitises a string for safe HTML insertion by replacing `&`, `<`, and `>` with their HTML entities.

| Parameter | Type | Description |
|---|---|---|
| `str` | `string` | Raw user input (student name) |
| **Returns** | `string` | HTML-safe string |

---

### Event Handlers

#### `onAdd()`

Triggered by the **➕ Add Student** button or `Enter` on the Scores input.

1. Reads and trims `inp-name` and `inp-scores`.
2. Validates: non-empty name, unique name, non-empty scores, at least one parseable number.
3. Stores the parsed score array in `students[name]`.
4. Clears inputs, shows a success toast, calls `refreshTable()`.

---

#### `onRemove()`

Triggered by the **🗑 Remove Student** button or `Enter` on the Remove input.

1. Reads and trims `inp-remove`.
2. Validates non-empty input.
3. Delegates to `removeStudent(name)`; catches its `Error` for the not-found case.
4. On success: clears the input, shows a success toast, calls `refreshTable()`.
5. On failure: shows an error toast with the exception message.

---

## 6. Known Intentional Bugs

The footer states: *"⚠️ Averages may look wrong — that's intentional! Find & fix the bugs in the JS."*

The source comment also reads: `// ── Logic (bugs preserved from student_grades.py) ──`

There are **four injected bugs**, all in the JavaScript logic functions:

| # | Function | Line (approx.) | Bug Description | Effect |
|---|---|---|---|---|
| **Bug 1** | `calculateAverage()` | `return total / (scores.length + 1)` | Denominator is `length + 1` instead of `length` | Every student's average is under-reported; grade letters may be one tier too low |
| **Bug 2** | `getClassAverage()` | `/ (allAvgs.length - 1)` | Denominator is `length - 1` instead of `length` | Class Average stat is inflated; with exactly one student it produces `Infinity` |
| **Bug 3** | `findTopStudent()` | `if (avg >= topAvg)` | Uses `>=` instead of `>` | When students tie, the *last* one in iteration order is reported as Top Student instead of the first |
| **Bug 4** | `removeStudent()` (caller) | `onRemove()` comment | Not a code bug per se — the function correctly throws on a missing key, which the comment flags as the expected error path | Observed as an error toast; the behaviour is actually correct but noted in the code comments as a callout |

> **Note:** The UI is designed to self-expose Bugs 1–3 by rendering the buggy values in **red** and the correct values in **green** in the same view, allowing immediate visual comparison without needing to inspect the source.

---

## 7. Lab Guide Summary

The workshop is titled **"Bob Workshop — Lab 1: Agent Skill"** and is documented in [`lab_guide.md`](lab_guide.md).

### Goals

The lab teaches participants how to leverage AI agents for software engineering tasks, using `student_grades.html` as the target codebase.

### Steps

```
Step 1 ── Manual bug hunt
          Open student_grades.html and find the 4 injected bugs WITHOUT AI assistance.

Step 2 ── Design AI helpers (4 specialised agents)
          2.1  Documentation Agent   — onboards new contributors faster
          2.2  Code Quality Critic   — reviews code for style/correctness issues
          2.3  Bug Finding Agent     — systematically identifies defects
          2.4  Tester Agent          — generates and runs test cases

Step 3 ── Reflection
          Consider the cumulative time cost of consulting each agent sequentially.
          Explore whether agents can be orchestrated in parallel to reduce total time.
```

### Key Takeaway

The lab uses the four-bug app as a controlled environment where the answer is already known (bugs are visible in the UI), making it easy to evaluate each agent's accuracy. The final reflection nudges participants toward **multi-agent parallelism** as a productivity pattern.

---

*Generated by Documentation Agent — Bob Workshop, KBTG.*
