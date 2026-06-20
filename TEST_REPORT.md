# TEST_REPORT.md

> Generated after `npm test` — all tests pass.

---

## Summary

| Metric | Value |
|---|---|
| Test suites | 1 |
| **Total tests** | **63** |
| **Passed** | **63** |
| **Failed** | **0** |
| Test runner | Jest 29 (Node.js) |
| Source module | `student_grades.js` |
| Test file | `student_grades.test.js` |

---

## Test run output (condensed)

```
PASS ./student_grades.test.js
Tests: 63 passed, 63 total
Time:  ~3.9 s
```

---

## Coverage areas

### `calculateAverage` — 6 tests

| Test | Verifies |
|---|---|
| Single score returns that score | baseline correctness |
| Multiple integer scores | normal operation |
| Floating-point scores | decimal precision |
| **BUG-01 fix** — `sum/length`, NOT `sum/(length+1)` | regression guard for BUG-01 |
| All zeros returns 0 | edge case |
| Scores summing to non-integer average | arithmetic correctness |

### `getHighestScore` — 4 tests

| Test | Verifies |
|---|---|
| Max from a normal array | normal operation |
| Single element | edge case |
| All equal values | tie handling |
| Negative scores | sign correctness |

### `getLowestScore` — 4 tests

| Test | Verifies |
|---|---|
| Min from a normal array | normal operation |
| Single element | edge case |
| All equal values | tie handling |
| Negative scores | sign correctness |

### `getGradeLetter` — 15 tests

| Test | Verifies |
|---|---|
| Exact boundary hits (90, 80, 70, 60, 59) | boundary correctness |
| Interior values (100, 95, 85, 75, 65, 0) | grade band coverage |
| One-below-boundary (89.9, 79.9, 69.9, 59.9) | off-by-one guard |

### `getClassAverage` — 5 tests

| Test | Verifies |
|---|---|
| Empty store → `null` | empty state |
| **BUG-08 fix** — 1 student gives correct result | regression guard for BUG-08 |
| **BUG-02 fix** — 2 students: divides by `length` not `length-1` | regression guard for BUG-02 |
| 3 students with known averages | multi-student correctness |
| Students with multi-score arrays | integration with `calculateAverage` |

### `findTopStudent` — 5 tests

| Test | Verifies |
|---|---|
| Empty store → `null` | empty state |
| Single student is the top | baseline |
| Clear winner across multiple students | normal operation |
| **BUG-03 fix** — TIE: first-inserted student wins (not last) | regression guard for BUG-03 |
| Returns correct `avg` value alongside name | return-shape correctness |

### `removeStudent` — 7 tests

| Test | Verifies |
|---|---|
| Removes an existing student | normal operation |
| Throws on non-existent student | error path |
| Store is empty after removing only student | post-delete state |
| **BUG-09 fix** — `"constructor"` key doesn't crash | prototype-pollution safety |
| **BUG-09 fix** — `"__proto__"` key doesn't crash | prototype-pollution safety |
| **BUG-09 fix** — `"toString"` key doesn't crash | prototype-pollution safety |
| **BUG-09 fix** — prototype-pollution name can be added & removed safely | full round-trip |

### `escHtml` — 8 tests  *(BUG-07 / BUG-05 sanitisation)*

| Test | Verifies |
|---|---|
| Escapes `&` → `&amp;` | ampersand |
| Escapes `<` → `&lt;` | less-than |
| Escapes `>` → `&gt;` | greater-than |
| Escapes `"` → `&quot;` | double-quote |
| Escapes `'` → `&#39;` | single-quote |
| All special chars in one string | combined XSS payload |
| Plain text unchanged | no false positives |
| Empty string → empty string | edge case |

### `parseScores` — 9 tests  *(BUG-07 input filter)*

| Test | Verifies |
|---|---|
| Accepts valid integers | normal operation |
| Accepts valid floats | decimal input |
| Rejects `NaN` entries | invalid token |
| Rejects `Infinity` | `isFinite` guard |
| Rejects `-Infinity` | `isFinite` guard |
| Rejects whitespace-only tokens | empty-token safety |
| All invalid input → `[]` | full rejection |
| Single valid number | minimal input |
| Trims whitespace around scores | input normalisation |

---

## Bug regression map

| Bug ID | Description | Test(s) that guard the fix |
|---|---|---|
| BUG-01 | `calculateAverage` divided by `length + 1` | `calculateAverage › BUG-01 fix` |
| BUG-02 | `getClassAverage` divided by `length - 1` | `getClassAverage › BUG-02 fix` |
| BUG-03 | `findTopStudent` used `>=` (last tied student won) | `findTopStudent › BUG-03 fix — TIE` |
| BUG-05 | `onRemove` exposed raw error message | `removeStudent › throws on non-existent student` |
| BUG-07 | Scores / names injected raw into innerHTML | `escHtml › *` (8 tests) + `parseScores › *` (9 tests) |
| BUG-08 | 1-student special-case called buggy average | `getClassAverage › BUG-08 fix` |
| BUG-09 | `{}` store + `!== undefined` check vulnerable to prototype pollution | `removeStudent › BUG-09 fix` (4 tests) |

> **BUG-04** (stat-avg always red) is a pure UI/DOM concern and is not exercisable in a Node.js unit-test context. It is the only tested-bug path that remains outside this suite.

---

## Untested paths

| Path | Reason |
|---|---|
| `BUG-04` — `stat-avg` conditional CSS class | DOM-only; requires a browser or jsdom integration test |
| `showToast`, `refreshTable`, `onAdd`, `onRemove` | UI/DOM event handlers; not exported from the logic module |
| `document.getElementById` interactions | Require a DOM environment (jsdom/Playwright) |
| `students` seed data (`Alice`, `Bob`, …) | Live in the HTML `<script>` block; not part of the module |

---

*All 63 tests passed. No bugs were found in the extracted logic module.*
