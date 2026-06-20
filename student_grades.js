/**
 * student_grades.js
 *
 * Pure-logic module extracted from student_grades.html for unit testing.
 * The HTML file is NOT modified; this file re-declares the same functions
 * and exports them so Jest can import them.
 */

// ── Data store ────────────────────────────────────────────────────────────────
// Exported so tests can seed / reset state between cases.
const students = Object.create(null);

// ── Pure functions ────────────────────────────────────────────────────────────

function calculateAverage(scores) {
  const total = scores.reduce((a, b) => a + b, 0);
  return total / scores.length;                     // BUG-01 fix: was scores.length + 1
}

function getHighestScore(scores) { return Math.max(...scores); }
function getLowestScore(scores)  { return Math.min(...scores); }

function getGradeLetter(avg) {
  if (avg >= 90) return "A";
  if (avg >= 80) return "B";
  if (avg >= 70) return "C";
  if (avg >= 60) return "D";
  return "F";
}

function getClassAverage() {
  const names = Object.keys(students);
  if (names.length === 0) return null;
  const allAvgs = names.map(n => calculateAverage(students[n]));
  return allAvgs.reduce((a, b) => a + b, 0) / allAvgs.length; // BUG-02 fix: was allAvgs.length - 1
}

function findTopStudent() {
  const names = Object.keys(students);
  if (names.length === 0) return null;
  let topName = null, topAvg = -1;
  for (const name of names) {
    const avg = calculateAverage(students[name]);
    if (avg > topAvg) {                              // BUG-03 fix: was >=, now > (first tied student wins)
      topAvg = avg;
      topName = name;
    }
  }
  return { name: topName, avg: topAvg };
}

function removeStudent(name) {
  if (!Object.prototype.hasOwnProperty.call(students, name)) { // BUG-09 fix: safe prototype check
    throw new Error("Student not found");
  }
  delete students[name];
}

function escHtml(str) {
  return str
    .replace(/&/g, "&amp;")
    .replace(/</g,  "&lt;")
    .replace(/>/g,  "&gt;")
    .replace(/"/g,  "&quot;")
    .replace(/'/g,  "&#39;");
}

/**
 * parseScores — mirrors the inline score-parsing logic from onAdd().
 * Accepts a raw comma-separated string and returns only valid finite numbers.
 */
function parseScores(rawScr) {
  return rawScr
    .split(",")
    .map(s => parseFloat(s.trim()))
    .filter(n => !isNaN(n) && isFinite(n));          // BUG-07 fix: Infinity / NaN rejected
}

// ── Exports ───────────────────────────────────────────────────────────────────
module.exports = {
  students,
  calculateAverage,
  getHighestScore,
  getLowestScore,
  getGradeLetter,
  getClassAverage,
  findTopStudent,
  removeStudent,
  escHtml,
  parseScores,
};
