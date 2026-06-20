# Bug Report — `student_grades.html`
### KBTG Workshop · Bug Finding Agent · Definitive Report

> **Investigation method:** Full source read of [`student_grades.html`](student_grades.html) (494 lines),
> cross-referenced against findings from the Documentation Agent and Code Quality Critic Agent.
> Every bug below is confirmed with an exact line citation.

---

## Executive Summary

| Metric | Count |
|---|---|
| **Total bugs confirmed** | **9** |
| Injected / intentional logic bugs | 3 (BUG-01, BUG-02, BUG-03) |
| UI rendering bugs | 2 (BUG-04, BUG-06) |
| Security bugs | 2 (BUG-05, BUG-07) |
| Data-integrity / edge-case bugs | 2 (BUG-08, BUG-09) |
| **Bugs missed by prior agents** | **4** (BUG-06, BUG-07, BUG-08, BUG-09) |

---

## Bug Inventory

---

### BUG-01 — Off-by-one denominator in `calculateAverage`

| Field | Detail |
|---|---|
| **Category** | Logic |
| **File** | [`student_grades.html`](student_grades.html:296) |
| **Line** | 296 |
| **Severity** | 🔴 Critical |

**Actual code:**
```js
// line 296
return total / (scores.length + 1);
```

**What it does:** Divides the sum of scores by `length + 1` — always one higher than the number of scores.
For a student with 5 scores the divisor is 6 instead of 5, so every average is `(n/(n+1))` of the true value
(e.g., 5 scores → average is 83.3% of the real value).

**What it should do:** Divide by `scores.length`.

```js
return total / scores.length;
```

**User-visible symptom:** Every student's "Average" column shows a number lower than the correct "Sum ÷ Count"
column. The discrepancy is highlighted in red. Grade letters are systematically too low (e.g., a true B becomes
a C or lower). This is the **root cause** of BUG-02 and BUG-08 as well, since both call `calculateAverage`.

---

### BUG-02 — Off-by-one denominator in `getClassAverage`

| Field | Detail |
|---|---|
| **Category** | Logic |
| **File** | [`student_grades.html`](student_grades.html:314) |
| **Line** | 314 |
| **Severity** | 🔴 Critical |

**Actual code:**
```js
// line 314
return allAvgs.reduce((a, b) => a + b, 0) / (allAvgs.length - 1);
```

**What it does:** Divides the sum of per-student averages by `length - 1`. With exactly 1 student this produces
`Infinity` (division by zero). With multiple students the class average is always inflated — the fewer the
students, the larger the inflation (e.g., 2 students → divides by 1, effectively doubling the true mean).

**What it should do:** Divide by `allAvgs.length`.

```js
return allAvgs.reduce((a, b) => a + b, 0) / allAvgs.length;
```

**Compounding note:** `allAvgs` is built by mapping through the **buggy** `calculateAverage` (line 313), so the
Class Average stat is wrong in two independent ways simultaneously (see also BUG-08).

**User-visible symptom:** The "Class Average" stat is always inflated compared to "Simple Mean". With exactly
one student loaded the UI must special-case it (line 395) to avoid displaying `Infinity`.

---

### BUG-03 — `findTopStudent` uses `>=` instead of `>`

| Field | Detail |
|---|---|
| **Category** | Logic |
| **File** | [`student_grades.html`](student_grades.html:323) |
| **Line** | 323 |
| **Severity** | 🟠 High |

**Actual code:**
```js
// line 323
if (avg >= topAvg) {
```

**What it does:** Updates `topName` whenever the current average is **greater than or equal** to the running
maximum. On a tie the last student encountered in iteration order becomes the top student.

**What it should do:** Use strict `>` so the **first** student to reach the maximum keeps the title.

```js
if (avg > topAvg) {
```

**User-visible symptom:** With the pre-seeded data, Diana and Eve both have identical scores
`[100, 98, 97, 99, 100]`. The "Top Student" stat shows **Eve** (last in order), while the "Highest Scorer"
stat correctly shows **Diana** (first in order). The discrepancy is immediately visible in the Stats Bar.

---

### BUG-04 — `stat-avg` Class Average element is **always** styled red (`stat-mismatch`)

| Field | Detail |
|---|---|
| **Category** | UI/UX |
| **File** | [`student_grades.html`](student_grades.html:400) |
| **Line** | 400 |
| **Severity** | 🟠 High |

**Actual code:**
```js
// line 400
caEl.className = "stat-mismatch";
```

**What it does:** Unconditionally assigns the red `stat-mismatch` CSS class to the Class Average stat element
after every render, regardless of whether the displayed value actually differs from the correct value.

**What it should do:** Only apply `stat-mismatch` when the class average genuinely differs from the correct
value by more than a small epsilon (analogous to the per-row `avgClass` logic on line 366). When the bugs are
fixed, this element should revert to the default yellow `--yellow` colour, not remain permanently red.

```js
// Correct behaviour after bug-fixes are applied:
const correctClassAvg = /* correct computation */;
caEl.className = Math.abs(ca - correctClassAvg) > 0.001 ? "stat-mismatch" : "";
```

**User-visible symptom:** Even if a developer fixes BUG-01 and BUG-02, the Class Average stat will remain red,
giving a false alarm that the value is still wrong. This silently defeats the visual self-verification the UI
was designed to provide.

---

### BUG-05 — `escHtml` does not escape `"` or `'` — incomplete XSS protection

| Field | Detail |
|---|---|
| **Category** | Security |
| **File** | [`student_grades.html`](student_grades.html:425-427) |
| **Lines** | 425–427 |
| **Severity** | 🟠 High |

**Actual code:**
```js
// lines 425-427
function escHtml(str) {
  return str.replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");
}
```

**What it does:** Escapes `&`, `<`, and `>` but leaves **double-quotes `"`** and **single-quotes `'`**
unescaped. The escaped name is then injected into `tr.innerHTML` inside an attribute-less `<td>` context
(line 371), so for the current usage the missing quote escaping does not create an exploitable injection
path in isolation.

**What it should do:** Also escape `"` and `'` to be safe for use in HTML attributes — this is the standard
`escHtml` contract. If the function is ever reused in an attribute context (e.g.,
`<input value="${escHtml(name)}">`), the current implementation would be directly exploitable.

```js
function escHtml(str) {
  return str
    .replace(/&/g,  "&amp;")
    .replace(/</g,  "&lt;")
    .replace(/>/g,  "&gt;")
    .replace(/"/g,  "&quot;")
    .replace(/'/g,  "&#39;");
}
```

**User-visible symptom:** No visible symptom with current usage. Becomes a stored XSS vector if the function
is used in an attribute context in future code changes.

---

### BUG-06 — `getClassAverage` calls the buggy `calculateAverage` — double-compounding error *(missed by prior agents)*

| Field | Detail |
|---|---|
| **Category** | Logic |
| **File** | [`student_grades.html`](student_grades.html:313) |
| **Line** | 313 |
| **Severity** | 🟡 Medium |

**Actual code:**
```js
// line 313
const allAvgs = names.map(n => calculateAverage(students[n]));
```

**What it does:** Builds the list of per-student averages used in the class-average calculation by calling
`calculateAverage()` — the same function that carries BUG-01 (`length + 1`). The resulting class average is
therefore wrong in **two independent ways**:
1. Each individual average fed in is already under-reported (BUG-01).
2. The final division uses `length - 1` instead of `length` (BUG-02).

The prior agents identified BUG-01 and BUG-02 separately but did not flag that BUG-02's input data is
itself corrupted by BUG-01, meaning fixing only BUG-02 still leaves the Class Average wrong (and vice versa).
Both bugs must be fixed together.

**What it should do:** To compute a true class average (mean of per-student means), `calculateAverage` must
first be fixed (BUG-01), and then the divisor corrected (BUG-02). Alternatively, call the correct inline
formula `scores.reduce(…) / scores.length` instead of `calculateAverage()`.

**User-visible symptom:** Class Average is wrong by more than either BUG-01 or BUG-02 alone would cause.
Fixing only one of the two parent bugs leaves the stat partially incorrect with no visual feedback
(since BUG-04 always colours it red regardless).

---

### BUG-07 — `scores.join(", ")` is injected raw into `innerHTML` without sanitization *(missed by prior agents)*

| Field | Detail |
|---|---|
| **Category** | Security |
| **File** | [`student_grades.html`](student_grades.html:372) |
| **Line** | 372 |
| **Severity** | 🟡 Medium |

**Actual code:**
```js
// line 372
<td class="scores-cell">${scores.join(", ")}</td>
```

**What it does:** Joins the numeric `scores` array directly into an HTML string via `tr.innerHTML`. The scores
are the result of `parseFloat()` (line 446), which coerces input to IEEE-754 floats. For all finite,
non-NaN numbers `parseFloat` produces safe numeric strings. **However**, `parseFloat` does not filter
`Infinity` or `-Infinity` — entering `"Infinity"` as a score (which `parseFloat("Infinity")` returns as the
JS global `Infinity`) passes the `!isNaN` filter on line 447, is stored as `Infinity` in the scores array,
and is later joined into innerHTML as the literal string `"Infinity"`. While this specific case does not
produce an HTML injection, the broader pattern of unsanitized array content flowing into `innerHTML` without
an explicit escaping step is a latent injection risk.

Additionally, `Infinity` and `-Infinity` values stored as scores cause downstream computation issues:
- `calculateAverage` returns `Infinity`
- `getHighestScore` returns `Infinity`
- `getLowestScore` returns `-Infinity` if a negative-infinity score exists
- `avg.toFixed(2)` on `Infinity` returns `"Infinity"` (not an error, but semantically nonsensical)

**What it should do:** Either filter `isFinite` in the score parsing step (line 447), or escape each score
value before injecting. The minimal fix is to add `&& isFinite(n)` to the filter on line 447:

```js
// line 445-447
const scores = rawScr.split(",")
  .map(s => parseFloat(s.trim()))
  .filter(n => !isNaN(n) && isFinite(n));
```

**User-visible symptom:** Typing `Infinity` as a score is accepted silently and produces `Infinity` in all
average and max/min columns, which looks like an application crash to the user.

---

### BUG-08 — `stat-avg` with exactly 1 student still displays the **buggy** average *(missed by prior agents)*

| Field | Detail |
|---|---|
| **Category** | Logic / UI |
| **File** | [`student_grades.html`](student_grades.html:395-396) |
| **Lines** | 395–396 |
| **Severity** | 🟡 Medium |

**Actual code:**
```js
// lines 395-396
if (names.length === 1) {
  caEl.textContent = calculateAverage(Object.values(students)[0]).toFixed(2);
```

**What it does:** When exactly one student is in the store, `getClassAverage()` returns `Infinity` (because
BUG-02 divides by `allAvgs.length - 1 = 0`). The code correctly avoids displaying `Infinity` by special-casing
the single-student path and showing that student's individual average instead. However, it calls
**`calculateAverage()`** — the same buggy function from BUG-01 — so with one student the "Class Average" stat
displays a value that is still wrong (`n/(n+1)` of the true value) and permanently red (BUG-04).

The special-case workaround masks BUG-02 for the 1-student case without actually fixing it, and introduces
a dependency on BUG-01's broken output.

**What it should do:** After BUG-01 and BUG-02 are fixed, this special case can be removed entirely (since
`getClassAverage()` with 1 student would correctly return that student's true average). If the workaround
must remain, it should use the correct inline formula:

```js
if (names.length === 1) {
  const sc = Object.values(students)[0];
  caEl.textContent = (sc.reduce((a, b) => a + b, 0) / sc.length).toFixed(2);
}
```

**User-visible symptom:** With a single student, "Class Average" and "Simple Mean" show different values even
though for one student they should be identical. The "Class Average" is visually lower than "Simple Mean" and
always red.

---

### BUG-09 — Prototype pollution via reserved object key names in student names *(missed by prior agents)*

| Field | Detail |
|---|---|
| **Category** | Security / Data Integrity |
| **File** | [`student_grades.html`](student_grades.html:438) and [`student_grades.html`](student_grades.html:453) |
| **Lines** | 438, 453 |
| **Severity** | 🟡 Medium |

**Actual code:**
```js
// line 438 — duplicate check
if (students[name] !== undefined) {
  showToast("toast-add", `⚠ "${name}" already exists.`, "error"); return;
}

// line 453 — store assignment
students[name] = scores;
```

**What it does:** Uses a plain `{}` object as the data store keyed by student name. The duplicate-name guard
checks `students[name] !== undefined` using bracket notation, which **traverses the prototype chain**. This
means:

1. If a user enters `"constructor"` as a name, `students["constructor"]` is a function (inherited from
   `Object.prototype`), which is `!== undefined`, so the guard fires and the student appears to "already
   exist" — preventing legitimate use of that name with a confusing error.
2. If a user enters `"__proto__"` or `"toString"` as a name and the guard somehow passes (browser-dependent
   for `__proto__`), the assignment `students[name] = scores` could mutate the prototype, breaking
   `Object.keys()`, `flatMap()`, and every downstream computation.
3. Prototype property names like `"hasOwnProperty"`, `"toString"`, `"valueOf"` all fail the duplicate check
   spuriously.

**What it should do:** Use `Object.prototype.hasOwnProperty.call(students, name)` for the duplicate check,
and use `Object.create(null)` for the store to eliminate prototype inheritance entirely:

```js
// Safe store initialization
const students = Object.create(null);

// Safe duplicate check
if (Object.prototype.hasOwnProperty.call(students, name)) { ... }
```

**User-visible symptom:** Attempting to add a student named `constructor`, `toString`, `valueOf`,
`hasOwnProperty`, or similar JavaScript built-in names produces a spurious "already exists" error even when
no such student has been added.

---

## Bugs Missed by Prior Agents

| Bug ID | Title | Why It Was Missed |
|---|---|---|
| **BUG-06** | `getClassAverage` calls buggy `calculateAverage` — double compounding | Prior agents identified BUG-01 and BUG-02 as independent bugs; the interaction (compounding) was not flagged |
| **BUG-07** | `Infinity`/`-Infinity` accepted as valid scores — flows into innerHTML | Prior agents noted `Math.max(...scores)` stack-overflow risk but not the `isFinite` filtering gap |
| **BUG-08** | 1-student special-case uses buggy `calculateAverage` | The single-student workaround was documented as a correct mitigation; its reliance on the buggy function was not scrutinized |
| **BUG-09** | Prototype pollution via reserved property names as student names | Not flagged in either prior report |

---

## Prioritized Fix Plan

Ordered by: **Severity → Root-cause-first (fix dependencies before dependents)**

| Priority | Bug ID | Title | Rationale |
|---|---|---|---|
| **P1** | BUG-01 | Fix `calculateAverage` denominator (`+1` → none) | Root cause of BUG-02 (compound), BUG-06, and BUG-08; all other average bugs cascade from this |
| **P2** | BUG-02 | Fix `getClassAverage` denominator (`-1` → none) | Must be fixed after P1; fixing P1 alone leaves class average wrong |
| **P3** | BUG-08 | Remove / fix the 1-student `calculateAverage` workaround | After P1+P2 are fixed, the special case is both unnecessary and misleading; remove it |
| **P4** | BUG-04 | Make `stat-mismatch` conditional, not unconditional | Without this fix, the red indicator remains after P1+P2 are fixed, masking the repair |
| **P5** | BUG-03 | Change `findTopStudent` from `>=` to `>` | Correctness: tie-breaking gives wrong result; observable with pre-seeded Diana/Eve data |
| **P6** | BUG-06 | Document/test the compound error interaction | Awareness fix; resolved automatically when P1+P2 are applied |
| **P7** | BUG-05 | Add `"` and `'` escaping to `escHtml` | Security hardening; low risk in current usage, high risk if function is reused |
| **P8** | BUG-07 | Add `isFinite` filter to score parsing | Closes `Infinity` score injection; 1-line fix |
| **P9** | BUG-09 | Use `Object.create(null)` store + `hasOwnProperty` guard | Security hardening; closes prototype pollution; low exploitability in a single-page toy app |

---

## Detailed Fix Diffs

### P1 — BUG-01

```diff
- return total / (scores.length + 1);
+ return total / scores.length;
```
[`student_grades.html:296`](student_grades.html:296)

---

### P2 — BUG-02

```diff
- return allAvgs.reduce((a, b) => a + b, 0) / (allAvgs.length - 1);
+ return allAvgs.reduce((a, b) => a + b, 0) / allAvgs.length;
```
[`student_grades.html:314`](student_grades.html:314)

---

### P3 — BUG-08 (remove the now-unnecessary special case)

```diff
- if (names.length === 1) {
-   caEl.textContent = calculateAverage(Object.values(students)[0]).toFixed(2);
- } else {
    caEl.textContent = ca.toFixed(2);
- }
```
[`student_grades.html:395-399`](student_grades.html:395)

---

### P4 — BUG-04

```diff
- caEl.className = "stat-mismatch";
+ // Compute the correct class average for comparison
+ const correctClassAvg = names.map(n => {
+   const sc = students[n];
+   return sc.reduce((a, b) => a + b, 0) / sc.length;
+ }).reduce((a, b) => a + b, 0) / names.length;
+ caEl.className = Math.abs(ca - correctClassAvg) > 0.001 ? "stat-mismatch" : "";
```
[`student_grades.html:400`](student_grades.html:400)

---

### P5 — BUG-03

```diff
- if (avg >= topAvg) {
+ if (avg > topAvg) {
```
[`student_grades.html:323`](student_grades.html:323)

---

### P7 — BUG-05

```diff
  function escHtml(str) {
-   return str.replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");
+   return str
+     .replace(/&/g,  "&amp;")
+     .replace(/</g,  "&lt;")
+     .replace(/>/g,  "&gt;")
+     .replace(/"/g,  "&quot;")
+     .replace(/'/g,  "&#39;");
  }
```
[`student_grades.html:425-427`](student_grades.html:425)

---

### P8 — BUG-07

```diff
  const scores = rawScr.split(",")
    .map(s => parseFloat(s.trim()))
-   .filter(n => !isNaN(n));
+   .filter(n => !isNaN(n) && isFinite(n));
```
[`student_grades.html:447`](student_grades.html:447)

---

### P9 — BUG-09

```diff
- const students = {};
+ const students = Object.create(null);

  // line 438
- if (students[name] !== undefined) {
+ if (Object.prototype.hasOwnProperty.call(students, name)) {
```
[`student_grades.html:290`](student_grades.html:290), [`student_grades.html:438`](student_grades.html:438)

---

## Complete Bug Reference Table

| ID | Title | Category | File:Line | Severity | Prior Agent? |
|---|---|---|---|---|---|
| BUG-01 | `calculateAverage` denominator is `length+1` | Logic | [`:296`](student_grades.html:296) | 🔴 Critical | ✅ Both agents |
| BUG-02 | `getClassAverage` denominator is `length-1` | Logic | [`:314`](student_grades.html:314) | 🔴 Critical | ✅ Both agents |
| BUG-03 | `findTopStudent` uses `>=` instead of `>` | Logic | [`:323`](student_grades.html:323) | 🟠 High | ✅ Both agents |
| BUG-04 | `stat-mismatch` class applied unconditionally | UI/UX | [`:400`](student_grades.html:400) | 🟠 High | ✅ Code Quality Critic only |
| BUG-05 | `escHtml` missing `"` and `'` escaping | Security | [`:425`](student_grades.html:425) | 🟠 High | ✅ Code Quality Critic only |
| BUG-06 | `getClassAverage` calls buggy `calculateAverage` — double compounding | Logic | [`:313`](student_grades.html:313) | 🟡 Medium | ❌ **Newly found** |
| BUG-07 | `Infinity` accepted as valid score; flows into innerHTML | Security/Logic | [`:447`](student_grades.html:447) | 🟡 Medium | ❌ **Newly found** |
| BUG-08 | 1-student workaround calls buggy `calculateAverage` | Logic/UI | [`:396`](student_grades.html:396) | 🟡 Medium | ❌ **Newly found** |
| BUG-09 | Prototype pollution via JS reserved names as student names | Security | [`:290`](student_grades.html:290), [`:438`](student_grades.html:438) | 🟡 Medium | ❌ **Newly found** |

---

*Generated by Bug Finding Agent — Bob Workshop, KBTG.*
