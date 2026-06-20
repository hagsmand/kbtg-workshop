# 🐛 Bug Cheat Sheet — Student Grade Tracker

> All 4 bugs live inside the `<script>` block of [`student_grades.html`](student_grades.html).

---

## Bug 1 — Wrong average divisor

| | |
|---|---|
| **File** | [`student_grades.html`](student_grades.html) · line 282 |
| **Function** | `calculateAverage()` |
| **Effect** | Every student's average is lower than it should be |

```js
// ❌ BUG — divides by length+1
return total / (scores.length + 1);

// ✅ FIX
return total / scores.length;
```

**Example:** Alice's scores `[95, 88, 92, 100, 85]`
- Buggy → `76.67`
- Correct → `92.00`

---

## Bug 2 — Class average divides by wrong count

| | |
|---|---|
| **File** | [`student_grades.html`](student_grades.html) · line 301 |
| **Function** | `getClassAverage()` |
| **Effect** | Class average is wildly inflated |

```js
// ❌ BUG — divides by (count - 1)
return allAvgs.reduce((a, b) => a + b, 0) / (allAvgs.length - 1);

// ✅ FIX
return allAvgs.reduce((a, b) => a + b, 0) / allAvgs.length;
```

**Example:** With 4 students the sum of averages is divided by `3` instead of `4`, inflating the result.

---

## Bug 3 — Top student uses `>=` instead of `>`

| | |
|---|---|
| **File** | [`student_grades.html`](student_grades.html) · line 311 |
| **Function** | `findTopStudent()` |
| **Effect** | On equal averages the *last* student in the list always wins instead of the *first* |

```js
// ❌ BUG — replaces top on tie, keeps iterating
if (avg >= topAvg) {

// ✅ FIX
if (avg > topAvg) {
```

> Combined with Bug 1 producing wrong averages, this can surface the completely wrong winner.

---

## Bug 4 — No existence check before delete

| | |
|---|---|
| **File** | [`student_grades.html`](student_grades.html) · line 320–323 |
| **Function** | `removeStudent()` |
| **Triggered** | Remove panel → type a name that doesn't exist → hit Remove |
| **Effect** | Throws `KeyError: 'Eve'` (mimicking Python's `KeyError`) |

```js
// ❌ BUG — throws if student doesn't exist
function removeStudent(name) {
  if (students[name] === undefined) {
    throw new Error(`KeyError: '${name}'`);
  }
  delete students[name];
}

// ✅ FIX
function removeStudent(name) {
  if (students[name] === undefined) {
    console.warn(`Student "${name}" not found.`);
    return;
  }
  delete students[name];
}
```

---

## Summary table

| # | Function | Line | Buggy code | Fix |
|---|---|---|---|---|
| 1 | `calculateAverage()` | 282 | `scores.length + 1` | `scores.length` |
| 2 | `getClassAverage()` | 301 | `allAvgs.length - 1` | `allAvgs.length` |
| 3 | `findTopStudent()` | 311 | `avg >= topAvg` | `avg > topAvg` |
| 4 | `removeStudent()` | 320 | throws on missing key | return/warn instead |
