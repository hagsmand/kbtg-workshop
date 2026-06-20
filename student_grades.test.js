/**
 * student_grades.test.js
 *
 * Jest test suite for the pure-logic functions in student_grades.js.
 * Each beforeEach wipes the shared `students` store so tests are isolated.
 */

"use strict";

const {
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
} = require("./student_grades");

// Helper: reset the shared students store before every test
beforeEach(() => {
  // Delete all own keys so the null-prototype object is empty again
  for (const key of Object.keys(students)) {
    delete students[key];
  }
});

// ─────────────────────────────────────────────────────────────────────────────
// calculateAverage
// ─────────────────────────────────────────────────────────────────────────────
describe("calculateAverage", () => {
  test("single score returns that score", () => {
    expect(calculateAverage([75])).toBe(75);
  });

  test("multiple integer scores", () => {
    expect(calculateAverage([80, 90, 100])).toBeCloseTo(90, 5);
  });

  test("floating-point scores", () => {
    expect(calculateAverage([88.5, 91.5])).toBeCloseTo(90, 5);
  });

  test("BUG-01 fix — result is sum/length, NOT sum/(length+1)", () => {
    // [60, 80] → sum=140, length=2 → correct=70, buggy-was=140/3≈46.67
    const result = calculateAverage([60, 80]);
    expect(result).toBeCloseTo(70, 5);
    expect(result).not.toBeCloseTo(46.67, 1);
  });

  test("all zeros returns 0", () => {
    expect(calculateAverage([0, 0, 0])).toBe(0);
  });

  test("scores summing to non-integer average", () => {
    // [10, 20, 30] → 60/3 = 20 exactly
    expect(calculateAverage([10, 20, 30])).toBeCloseTo(20, 5);
  });
});

// ─────────────────────────────────────────────────────────────────────────────
// getHighestScore
// ─────────────────────────────────────────────────────────────────────────────
describe("getHighestScore", () => {
  test("returns max from a normal array", () => {
    expect(getHighestScore([55, 100, 72, 88])).toBe(100);
  });

  test("single element returns that element", () => {
    expect(getHighestScore([42])).toBe(42);
  });

  test("all equal values returns that value", () => {
    expect(getHighestScore([77, 77, 77])).toBe(77);
  });

  test("handles negative scores", () => {
    expect(getHighestScore([-10, -5, -20])).toBe(-5);
  });
});

// ─────────────────────────────────────────────────────────────────────────────
// getLowestScore
// ─────────────────────────────────────────────────────────────────────────────
describe("getLowestScore", () => {
  test("returns min from a normal array", () => {
    expect(getLowestScore([55, 100, 72, 88])).toBe(55);
  });

  test("single element returns that element", () => {
    expect(getLowestScore([42])).toBe(42);
  });

  test("all equal values returns that value", () => {
    expect(getLowestScore([77, 77, 77])).toBe(77);
  });

  test("handles negative scores", () => {
    expect(getLowestScore([-10, -5, -20])).toBe(-20);
  });
});

// ─────────────────────────────────────────────────────────────────────────────
// getGradeLetter
// ─────────────────────────────────────────────────────────────────────────────
describe("getGradeLetter", () => {
  // Exact boundary hits
  test("90 → A (exact boundary)", () => expect(getGradeLetter(90)).toBe("A"));
  test("80 → B (exact boundary)", () => expect(getGradeLetter(80)).toBe("B"));
  test("70 → C (exact boundary)", () => expect(getGradeLetter(70)).toBe("C"));
  test("60 → D (exact boundary)", () => expect(getGradeLetter(60)).toBe("D"));
  test("59 → F (just below D)", () => expect(getGradeLetter(59)).toBe("F"));

  // Interior values
  test("100 → A", () => expect(getGradeLetter(100)).toBe("A"));
  test("95  → A", () => expect(getGradeLetter(95)).toBe("A"));
  test("85  → B", () => expect(getGradeLetter(85)).toBe("B"));
  test("75  → C", () => expect(getGradeLetter(75)).toBe("C"));
  test("65  → D", () => expect(getGradeLetter(65)).toBe("D"));
  test("0   → F", () => expect(getGradeLetter(0)).toBe("F"));

  // One-below-boundary checks (guards against off-by-one)
  test("89.9 → B (just below A)", () => expect(getGradeLetter(89.9)).toBe("B"));
  test("79.9 → C (just below B)", () => expect(getGradeLetter(79.9)).toBe("C"));
  test("69.9 → D (just below C)", () => expect(getGradeLetter(69.9)).toBe("D"));
  test("59.9 → F (just below D)", () => expect(getGradeLetter(59.9)).toBe("F"));
});

// ─────────────────────────────────────────────────────────────────────────────
// getClassAverage
// ─────────────────────────────────────────────────────────────────────────────
describe("getClassAverage", () => {
  test("empty store returns null", () => {
    expect(getClassAverage()).toBeNull();
  });

  test("BUG-08 fix — one student returns correct average (not crashing)", () => {
    students["Alice"] = [80, 90, 100];
    // calculateAverage([80,90,100]) = 90 exactly
    expect(getClassAverage()).toBeCloseTo(90, 5);
  });

  test("BUG-02 fix — two students: divides by length not length-1", () => {
    // Alice avg=90, Bob avg=70 → class avg should be (90+70)/2 = 80
    // buggy version would be (90+70)/1 = 160
    students["Alice"] = [90];
    students["Bob"]   = [70];
    expect(getClassAverage()).toBeCloseTo(80, 5);
    expect(getClassAverage()).not.toBeCloseTo(160, 1);
  });

  test("three students with known averages", () => {
    students["A"] = [100];         // avg 100
    students["B"] = [80];          // avg  80
    students["C"] = [60];          // avg  60
    // class avg = (100+80+60)/3 = 80
    expect(getClassAverage()).toBeCloseTo(80, 5);
  });

  test("students with multi-score arrays", () => {
    students["Alice"] = [80, 90, 100]; // avg 90
    students["Bob"]   = [60, 70, 80];  // avg 70
    // class avg = (90+70)/2 = 80
    expect(getClassAverage()).toBeCloseTo(80, 5);
  });
});

// ─────────────────────────────────────────────────────────────────────────────
// findTopStudent
// ─────────────────────────────────────────────────────────────────────────────
describe("findTopStudent", () => {
  test("empty store returns null", () => {
    expect(findTopStudent()).toBeNull();
  });

  test("single student is the top student", () => {
    students["Alice"] = [85, 90];
    const top = findTopStudent();
    expect(top.name).toBe("Alice");
    expect(top.avg).toBeCloseTo(87.5, 5);
  });

  test("clear winner across multiple students", () => {
    students["Alice"]   = [70];
    students["Bob"]     = [95];
    students["Charlie"] = [60];
    expect(findTopStudent().name).toBe("Bob");
    expect(findTopStudent().avg).toBeCloseTo(95, 5);
  });

  test("BUG-03 fix — TIE: first-inserted student wins (not last)", () => {
    // Both have avg=100; Diana is inserted first → should win
    students["Diana"] = [100, 100];
    students["Eve"]   = [100, 100];
    const top = findTopStudent();
    expect(top.name).toBe("Diana");   // first wins, not Eve
    expect(top.avg).toBeCloseTo(100, 5);
  });

  test("returns correct avg value alongside name", () => {
    students["Alice"] = [80, 90, 100]; // avg 90
    students["Bob"]   = [60, 70];      // avg 65
    const top = findTopStudent();
    expect(top.name).toBe("Alice");
    expect(top.avg).toBeCloseTo(90, 5);
  });
});

// ─────────────────────────────────────────────────────────────────────────────
// removeStudent
// ─────────────────────────────────────────────────────────────────────────────
describe("removeStudent", () => {
  test("removes an existing student", () => {
    students["Alice"] = [90];
    removeStudent("Alice");
    expect(Object.prototype.hasOwnProperty.call(students, "Alice")).toBe(false);
  });

  test("throws on non-existent student", () => {
    expect(() => removeStudent("Ghost")).toThrow("Student not found");
  });

  test("store is empty after removing only student", () => {
    students["Solo"] = [55];
    removeStudent("Solo");
    expect(Object.keys(students).length).toBe(0);
  });

  test("BUG-09 fix — 'constructor' key does not crash or mis-fire", () => {
    // 'constructor' is not an own-prop of the null-prototype store
    expect(() => removeStudent("constructor")).toThrow("Student not found");
  });

  test("BUG-09 fix — '__proto__' key does not crash or mis-fire", () => {
    expect(() => removeStudent("__proto__")).toThrow("Student not found");
  });

  test("BUG-09 fix — 'toString' key does not crash or mis-fire", () => {
    expect(() => removeStudent("toString")).toThrow("Student not found");
  });

  test("BUG-09 fix — prototype-pollution name can actually be added and removed safely", () => {
    // Simulate adding via direct property assignment on the null-proto store
    students["constructor"] = [80];
    expect(() => removeStudent("constructor")).not.toThrow();
    expect(Object.prototype.hasOwnProperty.call(students, "constructor")).toBe(false);
  });
});

// ─────────────────────────────────────────────────────────────────────────────
// escHtml  (BUG-07 / BUG-05 related sanitisation)
// ─────────────────────────────────────────────────────────────────────────────
describe("escHtml", () => {
  test("escapes ampersand &", () => {
    expect(escHtml("a & b")).toBe("a &amp; b");
  });

  test("escapes less-than <", () => {
    expect(escHtml("<script>")).toBe("&lt;script&gt;");
  });

  test("escapes greater-than >", () => {
    expect(escHtml("a > b")).toBe("a &gt; b");
  });

  test("escapes double-quote \"", () => {
    expect(escHtml('say "hello"')).toBe("say &quot;hello&quot;");
  });

  test("escapes single-quote '", () => {
    expect(escHtml("it's")).toBe("it&#39;s");
  });

  test("escapes all special chars in one string", () => {
    expect(escHtml(`<a href="/" onclick='alert(1)'>R&D</a>`)).toBe(
      "&lt;a href=&quot;/&quot; onclick=&#39;alert(1)&#39;&gt;R&amp;D&lt;/a&gt;"
    );
  });

  test("plain text is returned unchanged", () => {
    expect(escHtml("HelloWorld")).toBe("HelloWorld");
  });

  test("empty string returns empty string", () => {
    expect(escHtml("")).toBe("");
  });
});

// ─────────────────────────────────────────────────────────────────────────────
// parseScores — score-input filter  (BUG-07 fix)
// ─────────────────────────────────────────────────────────────────────────────
describe("parseScores", () => {
  test("accepts valid integers", () => {
    expect(parseScores("85, 90, 78")).toEqual([85, 90, 78]);
  });

  test("accepts valid floats", () => {
    expect(parseScores("88.5, 91.5")).toEqual([88.5, 91.5]);
  });

  test("rejects NaN entries", () => {
    expect(parseScores("abc, 90")).toEqual([90]);
  });

  test("rejects Infinity", () => {
    expect(parseScores("Infinity, 80")).toEqual([80]);
  });

  test("rejects -Infinity", () => {
    expect(parseScores("-Infinity, 70")).toEqual([70]);
  });

  test("rejects empty-string tokens (whitespace only)", () => {
    // "85, , 90" — the middle token parses as NaN
    expect(parseScores("85, , 90")).toEqual([85, 90]);
  });

  test("all invalid input returns empty array", () => {
    expect(parseScores("abc, Infinity, -Infinity, NaN")).toEqual([]);
  });

  test("single valid number", () => {
    expect(parseScores("100")).toEqual([100]);
  });

  test("trims whitespace around scores", () => {
    expect(parseScores("  70 ,  80 ,  90  ")).toEqual([70, 80, 90]);
  });
});
