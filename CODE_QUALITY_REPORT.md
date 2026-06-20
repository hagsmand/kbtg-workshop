# Code Quality Report — `student_grades.html`

**Reviewer:** Code Quality Critic Agent  
**File reviewed:** `student_grades.html` (494 lines, single-file HTML + CSS + JS)  
**Review date:** 2025  

---

## Executive Summary

| Severity | Count |
|----------|-------|
| 🔴 Critical | 3 |
| 🟠 High | 3 |
| 🟡 Medium | 5 |
| 🔵 Low | 4 |
| **Total** | **15** |

| Pillar | Count |
|--------|-------|
| Correctness | 5 |
| Maintainability | 4 |
| Robustness | 3 |
| Best Practices | 3 |

---

## Detailed Issues

---

### BUG-01 — Off-by-one denominator in `calculateAverage`

| Attribute | Detail |
|-----------|--------|
| **Pillar** | Correctness |
| **File / Line** | `student_grades.html` line 296 |
| **Severity** | 🔴 Critical |
| **Type** | Bug (objectively wrong behavior) |

**What the code does:**
```js
// line 296
return total / (scores.length + 1);
```
The denominator is `scores.length + 1`. For a student with 5 scores the divisor becomes 6, not 5, producing a systematically low average. Every downstream value that calls `calculateAverage` — the per-row average cell, `getClassAverage`, and `findTopStudent` — is wrong.

**What it should do:**
```js
return total / scores.length;
```

**Impact chain:** `calculateAverage` → `getGradeLetter` (wrong grade assigned) → `getClassAverage` → `findTopStudent` → stats bar display.

---

### BUG-02 — Off-by-one denominator in `getClassAverage`

| Attribute | Detail |
|-----------|--------|
| **Pillar** | Correctness |
| **File / Line** | `student_grades.html` line 314 |
| **Severity** | 🔴 Critical |
| **Type** | Bug (objectively wrong behavior) |

**What the code does:**
```js
// line 314
return allAvgs.reduce((a, b) => a + b, 0) / (allAvgs.length - 1);
```
The denominator is `allAvgs.length - 1`. For 5 students the divisor is 4, inflating the class average by 25 %. When there is exactly **one** student this produces a division by zero (`0`), returning `Infinity` or `NaN`.

**What it should do:**
```js
return allAvgs.reduce((a, b) => a + b, 0) / allAvgs.length;
```

**Edge case also broken:** The caller in `refreshTable` already special-cases `names.length === 1` (line 395–397) to avoid calling `getClassAverage`, but this is a symptom-patch, not a fix. The function itself is wrong.

---

### BUG-03 — `findTopStudent` uses `>=` instead of `>`

| Attribute | Detail |
|-----------|--------|
| **Pillar** | Correctness |
| **File / Line** | `student_grades.html` line 323 |
| **Severity** | 🟠 High |
| **Type** | Bug (wrong behavior for tied scores) |

**What the code does:**
```js
// line 323
if (avg >= topAvg) {
```
`>=` means every student whose average equals the current maximum overwrites `topName`. Because the demo data has Diana and Eve with identical scores, whichever comes last in iteration order (Eve) wins. Correct semantics for "top student" should be strict `>` so the **first** student encountered with the maximum is kept.

**What it should do:**
```js
if (avg > topAvg) {
```

**Note:** The comment on line 409 (`// buggy (>=) vs correct (first highest)`) acknowledges the bug intentionally. This must still be fixed in a real deployment.

---

### BUG-04 — `stat-avg` is always styled as `stat-mismatch` (red)

| Attribute | Detail |
|-----------|--------|
| **Pillar** | Correctness |
| **File / Line** | `student_grades.html` line 400 |
| **Severity** | 🟠 High |
| **Type** | Bug (misleading UI, unconditional red highlight) |

**What the code does:**
```js
// line 400
caEl.className = "stat-mismatch";
```
The "Class Average" stat element is **always** assigned the `stat-mismatch` (red) class, even if `getClassAverage` were fixed and returned the correct value. There is no conditional logic comparing the buggy vs. correct value.

**What it should do:**
```js
// Only highlight red when the value genuinely differs from the correct mean
const correctClassAvg = allScores.reduce((a, b) => a + b, 0) / allScores.length;
caEl.className = Math.abs(ca - correctClassAvg) > 0.001 ? "stat-mismatch" : "";
```

---

### BUG-05 — `escHtml` does not escape quotes — partial XSS protection

| Attribute | Detail |
|-----------|--------|
| **Pillar** | Correctness / Best Practices |
| **File / Line** | `student_grades.html` lines 425–427 |
| **Severity** | 🟠 High |
| **Type** | Bug / Security |

**What the code does:**
```js
function escHtml(str) {
  return str.replace(/&/g,"&amp;")
            .replace(/</g,"&lt;")
            .replace(/>/g,"&gt;");
}
```
`"` and `'` are not escaped. The escaped name is injected directly into an attribute-free text node (`<td>${escHtml(name)}</td>`), which is safe **today**, but the function gives a false sense of completeness. If `escHtml` were reused in a context where the string lands inside an HTML attribute (e.g., `title="${escHtml(name)}"`) a name like `" onmouseover="alert(1)` would break out.

**What it should do:**
```js
function escHtml(str) {
  return str
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}
```

---

### MAINT-01 — Scores-per-student are out-of-range scores silently accepted

| Attribute | Detail |
|-----------|--------|
| **Pillar** | Robustness |
| **File / Line** | `student_grades.html` lines 445–451 |
| **Severity** | 🟡 Medium |
| **Type** | Quality / Robustness |

**What the code does:**
```js
const scores = rawScr.split(",")
  .map(s => parseFloat(s.trim()))
  .filter(n => !isNaN(n));
```
Scores such as `-50`, `200`, or `999` pass validation silently. Negative or >100 scores produce nonsensical averages and grades.

**What it should do:**
Add a range check after parsing:
```js
const scores = rawScr.split(",")
  .map(s => parseFloat(s.trim()))
  .filter(n => !isNaN(n) && n >= 0 && n <= 100);

if (scores.length === 0) {
  showToast("toast-add", "⚠ Scores must be numbers between 0 and 100.", "error");
  return;
}
```

---

### MAINT-02 — Duplicate average-calculation logic scattered across four locations

| Attribute | Detail |
|-----------|--------|
| **Pillar** | Maintainability |
| **File / Line** | `student_grades.html` lines 296, 313–314, 365, 417 |
| **Severity** | 🟡 Medium |
| **Type** | Style / Quality |

**What the code does:**
The expression `scores.reduce((a, b) => a + b, 0) / scores.length` is written inline at lines 365 and 417, and a deliberately-broken version is in `calculateAverage` (line 296) and `getClassAverage` (line 314). Four separate implementations of the same mean formula.

**What it should do:**
Have one canonical helper and call it everywhere:
```js
function correctAverage(scores) {
  return scores.reduce((a, b) => a + b, 0) / scores.length;
}
```
Then replace all four call sites with `correctAverage(scores)`.

---

### MAINT-03 — Magic numbers for grade thresholds are not named

| Attribute | Detail |
|-----------|--------|
| **Pillar** | Maintainability |
| **File / Line** | `student_grades.html` lines 303–307 |
| **Severity** | 🔵 Low |
| **Type** | Style / Quality |

**What the code does:**
```js
if (avg >= 90) return "A";
if (avg >= 80) return "B";
if (avg >= 70) return "C";
if (avg >= 60) return "D";
```
Grade boundaries are hard-coded. Any change (e.g., a different grading scale) requires touching multiple lines with no single source of truth.

**What it should do:**
```js
const GRADE_THRESHOLDS = [
  { min: 90, letter: "A" },
  { min: 80, letter: "B" },
  { min: 70, letter: "C" },
  { min: 60, letter: "D" },
];

function getGradeLetter(avg) {
  for (const { min, letter } of GRADE_THRESHOLDS) {
    if (avg >= min) return letter;
  }
  return "F";
}
```

---

### MAINT-04 — Global mutable object `students` doubles as both store and UI state

| Attribute | Detail |
|-----------|--------|
| **Pillar** | Maintainability |
| **File / Line** | `student_grades.html` line 290 |
| **Severity** | 🔵 Low |
| **Type** | Style / Quality |

**What the code does:**
```js
const students = {};
```
All data lives in a single module-level plain object. Any script on the page (or future script) can mutate it directly, bypassing all validation in `onAdd`.

**What it should do:**
Encapsulate data access behind functions or a class:
```js
const studentStore = (() => {
  const _data = {};
  return {
    add(name, scores)   { _data[name] = scores; },
    remove(name)        { delete _data[name]; },
    has(name)           { return name in _data; },
    getAll()            { return { ..._data }; },
  };
})();
```

---

### MAINT-05 — `inline onclick` handlers instead of `addEventListener`

| Attribute | Detail |
|-----------|--------|
| **Pillar** | Best Practices |
| **File / Line** | `student_grades.html` lines 218, 229 |
| **Severity** | 🔵 Low |
| **Type** | Style / Quality |

**What the code does:**
```html
<button class="btn btn-add" onclick="onAdd()">➕ Add Student</button>
<button class="btn btn-remove" onclick="onRemove()">🗑 Remove Student</button>
```
Inline `onclick` attributes mix HTML structure with JS behavior. They require the handler to be in global scope and cannot be easily removed or replaced.

**What it should do:**
```js
document.getElementById("btn-add").addEventListener("click", onAdd);
document.getElementById("btn-remove").addEventListener("click", onRemove);
```
Add corresponding `id` attributes to the buttons.

---

### MAINT-06 — `Enter` key only wired to scores input, not to name input

| Attribute | Detail |
|-----------|--------|
| **Pillar** | Robustness |
| **File / Line** | `student_grades.html` lines 476–481 |
| **Severity** | 🟡 Medium |
| **Type** | Quality / UX |

**What the code does:**
```js
document.getElementById("inp-scores").addEventListener("keydown", e => {
  if (e.key === "Enter") onAdd();
});
```
`Enter` on the **name** field (`inp-name`) does nothing; the user must tab to the scores field first or click the button. The `inp-name` input has no `keydown` listener.

**What it should do:**
```js
document.getElementById("inp-name").addEventListener("keydown", e => {
  if (e.key === "Enter") onAdd();
});
```

---

### ROBUST-01 — `refreshTable` uses `innerHTML` for empty-state row

| Attribute | Detail |
|-----------|--------|
| **Pillar** | Best Practices |
| **File / Line** | `student_grades.html` lines 355–356 |
| **Severity** | 🟡 Medium |
| **Type** | Quality / Security |

**What the code does:**
```js
tbody.innerHTML =
  `<tr class="empty-row"><td colspan="7">No students yet. Add one on the left.</td></tr>`;
```
This specific string is static, so it is not exploitable today. However, the surrounding pattern (line 370 sets `tr.innerHTML` with interpolated data) establishes a risky convention. The `tr.innerHTML` on line 370 injects `scores.join(", ")` directly without escaping. Integer scores are safe, but if the data source ever changes to include strings the injection surface widens.

**Fix for `tr.innerHTML` on line 370:**  
All interpolated values that aren't already numbers should be escaped. At minimum, `scores` should be validated as numeric-only before storage (see MAINT-01) so the cell remains safe.

---

### ROBUST-02 — No maximum score-count limit; `Math.max(...scores)` can stack-overflow

| Attribute | Detail |
|-----------|--------|
| **Pillar** | Robustness |
| **File / Line** | `student_grades.html` lines 299–300 |
| **Severity** | 🟡 Medium |
| **Type** | Robustness |

**What the code does:**
```js
function getHighestScore(scores) { return Math.max(...scores); }
function getLowestScore(scores)  { return Math.min(...scores); }
```
Spreading a very large array into `Math.max()` or `Math.min()` can throw a `RangeError: Maximum call stack size exceeded` when the array has tens of thousands of elements. While unlikely for a grade tracker, no cap exists.

**What it should do:**
```js
function getHighestScore(scores) {
  return scores.reduce((m, v) => v > m ? v : m, -Infinity);
}
function getLowestScore(scores) {
  return scores.reduce((m, v) => v < m ? v : m, Infinity);
}
```

---

### ROBUST-03 — No `<form>` / `novalidate` — browser may block non-number keys inconsistently

| Attribute | Detail |
|-----------|--------|
| **Pillar** | Robustness |
| **File / Line** | `student_grades.html` lines 210–217 |
| **Severity** | 🔵 Low |
| **Type** | Quality / UX |

**What the code does:**
The scores input is `type="text"`. This is actually fine (scores are parsed manually), but the name input has no `maxlength` attribute. A very long name will overflow the table cell and break the layout.

**What it should do:**
```html
<input id="inp-name" type="text" placeholder="e.g. Alice" maxlength="60" />
```

---

### A11Y-01 — No `aria-live` region for toast notifications

| Attribute | Detail |
|-----------|--------|
| **Pillar** | Best Practices / Accessibility |
| **File / Line** | `student_grades.html` lines 220, 231 |
| **Severity** | 🟡 Medium |
| **Type** | Quality / Accessibility |

**What the code does:**
```html
<div id="toast-add" class="toast"></div>
<div id="toast-remove" class="toast"></div>
```
Toast messages appear and disappear visually but are invisible to screen readers because neither `aria-live` nor `role="alert"` is set.

**What it should do:**
```html
<div id="toast-add" class="toast" role="alert" aria-live="polite"></div>
<div id="toast-remove" class="toast" role="alert" aria-live="polite"></div>
```

---

## Prioritized Action Plan

### 🔴 Critical — Fix First (Bugs with incorrect output)

| ID | Issue | Line | Fix Summary |
|----|-------|------|-------------|
| BUG-01 | `calculateAverage` divides by `length + 1` | 296 | Change to `/ scores.length` |
| BUG-02 | `getClassAverage` divides by `length - 1` | 314 | Change to `/ allAvgs.length` |

These two bugs corrupt every numerical output in the app. Fix them before anything else.

---

### 🟠 High — Fix Soon (Bugs with visible wrong behavior or security risk)

| ID | Issue | Line | Fix Summary |
|----|-------|------|-------------|
| BUG-03 | `findTopStudent` uses `>=` — last tie wins | 323 | Change to `> topAvg` |
| BUG-04 | Class Average always shown red | 400 | Conditionally assign `stat-mismatch` |
| BUG-05 | `escHtml` missing quote escaping | 425–427 | Add `"` and `'` replacements |

---

### 🟡 Medium — Improve Soon (Correctness edge cases and UX gaps)

| ID | Issue | Line | Fix Summary |
|----|-------|------|-------------|
| MAINT-01 | No score range validation (0–100) | 445–451 | Add `n >= 0 && n <= 100` filter |
| MAINT-02 | Duplicated average logic in 4 places | 296, 313, 365, 417 | Extract single `correctAverage()` helper |
| MAINT-06 | `Enter` key not wired to name input | 476–481 | Add `keydown` listener to `inp-name` |
| ROBUST-01 | `tr.innerHTML` injects un-escaped data | 370 | Ensure all interpolated values are safe |
| ROBUST-02 | Spread into `Math.max/min` risks stack overflow | 299–300 | Use `reduce` instead |
| A11Y-01 | Toast has no `aria-live`/`role="alert"` | 220, 231 | Add `role="alert" aria-live="polite"` |

---

### 🔵 Low — Quality Improvements (Style, maintainability, UX polish)

| ID | Issue | Line | Fix Summary |
|----|-------|------|-------------|
| MAINT-03 | Magic numbers for grade thresholds | 303–307 | Extract `GRADE_THRESHOLDS` constant array |
| MAINT-04 | Global mutable `students` object | 290 | Encapsulate in IIFE or module |
| MAINT-05 | `onclick` inline handlers | 218, 229 | Use `addEventListener` |
| ROBUST-03 | No `maxlength` on name input | 212 | Add `maxlength="60"` |

---

## Bug vs. Style Classification

### Bugs (objectively wrong behavior)
- **BUG-01** — wrong average computed for every student
- **BUG-02** — wrong class average; division-by-zero with one student in function body
- **BUG-03** — wrong top-student when scores are tied
- **BUG-04** — "Class Average" always displayed in red regardless of correctness

### Style / Quality Suggestions
- **BUG-05** — incomplete `escHtml` (dangerous pattern, not currently exploitable)
- **MAINT-01** through **MAINT-06** — validation, duplication, naming, coupling
- **ROBUST-01** through **ROBUST-03** — defensive coding, edge cases
- **A11Y-01** — accessibility

---

## Quick-Fix Diff Summary

```js
// BUG-01 fix (line 296)
- return total / (scores.length + 1);
+ return total / scores.length;

// BUG-02 fix (line 314)
- return allAvgs.reduce((a, b) => a + b, 0) / (allAvgs.length - 1);
+ return allAvgs.reduce((a, b) => a + b, 0) / allAvgs.length;

// BUG-03 fix (line 323)
- if (avg >= topAvg) {
+ if (avg > topAvg) {

// BUG-04 fix (line 400)
- caEl.className = "stat-mismatch";
+ // only mark red if value actually differs from the correct mean
+ const correctClassMean = allScores.reduce((a,b) => a+b, 0) / allScores.length;
+ caEl.className = Math.abs(ca - correctClassMean) > 0.001 ? "stat-mismatch" : "";

// BUG-05 fix (lines 425-427)
  function escHtml(str) {
    return str.replace(/&/g,"&amp;")
              .replace(/</g,"&lt;")
              .replace(/>/g,"&gt;")
+             .replace(/"/g,"&quot;")
+             .replace(/'/g,"&#39;");
  }
```
