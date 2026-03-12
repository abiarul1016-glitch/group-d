import { useState, useEffect, useRef } from "react";

const NEON_GREEN = "#39FF14";
const SOFT_GREEN = "#a8f5a2";

// ── Scoring + grouping logic (ported from Python) ──────────────────────────
function scoreGroups(groups, togetherPairs, notTogetherPairs) {
  let score = 0;
  for (const group of groups) {
    for (const [p1, p2] of togetherPairs) {
      const has1 = group.includes(p1);
      const has2 = group.includes(p2);
      if (has1 !== has2) score += 10;
    }
    for (const [p1, p2] of notTogetherPairs) {
      if (group.includes(p1) && group.includes(p2)) score += 50;
    }
  }
  return score;
}

function shuffle(arr) {
  const a = [...arr];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

function findBestGroups(students, numGroups, togetherPairs, notTogetherPairs, iterations = 5000) {
  let bestScore = Infinity;
  let bestAssignment = null;
  for (let i = 0; i < iterations; i++) {
    const shuffled = shuffle(students);
    const groups = Array.from({ length: numGroups }, () => []);
    shuffled.forEach((s, idx) => groups[idx % numGroups].push(s));
    const score = scoreGroups(groups, togetherPairs, notTogetherPairs);
    if (score < bestScore) {
      bestScore = score;
      bestAssignment = groups;
      if (bestScore === 0) break;
    }
  }
  return { groups: bestAssignment, score: bestScore };
}

// ── Green-family gradient palette ───────────────────────────────────────────
const GROUP_GRADIENTS = [
  "linear-gradient(135deg,#d4fcd4,#a8f5a2)",   // soft mint
  "linear-gradient(135deg,#b6f5d8,#7fffd4)",   // aqua-mint
  "linear-gradient(135deg,#e2fce2,#c0f0c0)",   // pale green
  "linear-gradient(135deg,#a8f0c6,#5dde9a)",   // emerald light
  "linear-gradient(135deg,#c8fce8,#90eec0)",   // seafoam
  "linear-gradient(135deg,#d8fef0,#a0f0d0)",   // glacier green
  "linear-gradient(135deg,#bbf7d0,#6ee7b7)",   // teal-green
  "linear-gradient(135deg,#e0fef0,#b8f5d8)",   // frosted mint
];

// ── Cryptex ring animation ──────────────────────────────────────────────────
function CryptexRings({ spinning }) {
  const RINGS = 5;
  const CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
  const [displayChars, setDisplayChars] = useState(Array(RINGS).fill("A"));
  const intervalRef = useRef(null);

  useEffect(() => {
    if (spinning) {
      intervalRef.current = setInterval(() => {
        setDisplayChars(prev =>
          prev.map(() => CHARS[Math.floor(Math.random() * CHARS.length)])
        );
      }, 60);
    } else {
      clearInterval(intervalRef.current);
      setDisplayChars(["G", "R", "O", "U", "P"]);
    }
    return () => clearInterval(intervalRef.current);
  }, [spinning]);

  return (
    <div style={{ display: "flex", gap: 8, justifyContent: "center", margin: "24px 0" }}>
      {displayChars.map((ch, i) => (
        <div
          key={i}
          style={{
            width: 52,
            height: 64,
            background: "rgba(255,255,255,0.08)",
            border: `2px solid ${spinning ? NEON_GREEN : "rgba(255,255,255,0.2)"}`,
            borderRadius: 10,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            fontSize: 28,
            fontFamily: "'SF Pro Display', -apple-system, BlinkMacSystemFont, sans-serif",
            fontWeight: 700,
            color: spinning ? NEON_GREEN : SOFT_GREEN,
            boxShadow: spinning ? `0 0 18px ${NEON_GREEN}55` : "none",
            transition: "box-shadow 0.3s, color 0.3s, border-color 0.3s",
            transform: spinning ? `translateY(${Math.sin(Date.now() / 200 + i) * 2}px)` : "none",
            letterSpacing: 0,
          }}
        >
          {ch}
        </div>
      ))}
    </div>
  );
}

// ── Tag chip ────────────────────────────────────────────────────────────────
function Tag({ label, onRemove, color = NEON_GREEN }) {
  return (
    <span style={{
      display: "inline-flex", alignItems: "center", gap: 6,
      background: "rgba(57,255,20,0.1)", border: `1px solid ${NEON_GREEN}55`,
      borderRadius: 999, padding: "3px 12px",
      fontSize: 13, color: SOFT_GREEN, fontFamily: "inherit",
    }}>
      {label}
      {onRemove && (
        <button onClick={onRemove} style={{
          background: "none", border: "none", color: "#ff6b6b",
          cursor: "pointer", padding: 0, fontSize: 14, lineHeight: 1,
        }}>×</button>
      )}
    </span>
  );
}

// ── Pair editor ─────────────────────────────────────────────────────────────
function PairEditor({ label, pairs, onAdd, onRemove, students, accent }) {
  const [a, setA] = useState("");
  const [b, setB] = useState("");
  const selectStyle = {
    background: "rgba(255,255,255,0.06)", border: "1px solid rgba(255,255,255,0.15)",
    borderRadius: 8, padding: "8px 12px", color: "#fff",
    fontSize: 14, fontFamily: "inherit", flex: 1, cursor: "pointer",
  };
  return (
    <div style={{ marginBottom: 20 }}>
      <label style={{ fontSize: 13, color: "rgba(255,255,255,0.5)", letterSpacing: 1, textTransform: "uppercase" }}>{label}</label>
      <div style={{ display: "flex", gap: 8, marginTop: 8 }}>
        <select value={a} onChange={e => setA(e.target.value)} style={selectStyle}>
          <option value="">Student A</option>
          {students.map(s => <option key={s} value={s}>{s}</option>)}
        </select>
        <select value={b} onChange={e => setB(e.target.value)} style={selectStyle}>
          <option value="">Student B</option>
          {students.map(s => <option key={s} value={s}>{s}</option>)}
        </select>
        <button onClick={() => { if (a && b && a !== b) { onAdd([a, b]); setA(""); setB(""); } }}
          style={{
            background: accent, border: "none", borderRadius: 8,
            padding: "8px 16px", cursor: "pointer", fontWeight: 700,
            fontSize: 14, color: "#000", fontFamily: "inherit",
          }}>+</button>
      </div>
      <div style={{ display: "flex", flexWrap: "wrap", gap: 6, marginTop: 8 }}>
        {pairs.map(([p1, p2], i) => (
          <Tag key={i} label={`${p1} + ${p2}`} onRemove={() => onRemove(i)} />
        ))}
      </div>
    </div>
  );
}

// ── Main App ────────────────────────────────────────────────────────────────
export default function App() {
  const [step, setStep] = useState("setup"); // setup | results
  const [rawStudents, setRawStudents] = useState("");
  const [numGroups, setNumGroups] = useState(3);
  const [togetherPairs, setTogetherPairs] = useState([]);
  const [notTogetherPairs, setNotTogetherPairs] = useState([]);
  const [results, setResults] = useState(null);
  const [spinning, setSpinning] = useState(false);
  const [error, setError] = useState("");

  const students = rawStudents
    .split("\n")
    .map(s => s.trim())
    .filter(Boolean);

  function generate() {
    setError("");
    if (students.length < 2) { setError("Please enter at least 2 students."); return; }
    if (numGroups < 1 || numGroups > students.length) { setError("Number of groups must be between 1 and the number of students."); return; }
    setSpinning(true);
    setStep("results");
    setTimeout(() => {
      const res = findBestGroups(students, numGroups, togetherPairs, notTogetherPairs);
      setResults(res);
      setSpinning(false);
      setResults(res);
      setSpinning(false);
      playRevealSound(); // 👈 add this
    }, 2200);
  }

  function playRevealSound() {
    const ctx = new AudioContext();

    // A little rising chime sweep
    [0, 100, 200, 350].forEach((delay, i) => {
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.connect(gain);
      gain.connect(ctx.destination);

      osc.frequency.value = [520, 660, 780, 1040][i];
      osc.type = "sine";

      const start = ctx.currentTime + delay / 1000;
      gain.gain.setValueAtTime(0, start);
      gain.gain.linearRampToValueAtTime(0.18, start + 0.05);
      gain.gain.exponentialRampToValueAtTime(0.001, start + 0.4);

      osc.start(start);
      osc.stop(start + 0.4);
    });
  }

  function reset() {
    setStep("setup");
    setResults(null);
    setSpinning(false);
  }

  const inputStyle = {
    width: "100%", background: "rgba(255,255,255,0.06)",
    border: "1px solid rgba(255,255,255,0.15)", borderRadius: 12,
    padding: "12px 16px", color: "#fff", fontSize: 15,
    fontFamily: "inherit", boxSizing: "border-box",
    outline: "none", resize: "vertical",
  };

  return (
    <div style={{
      minHeight: "100vh",
      background: "radial-gradient(ellipse at 20% 20%, #0d2e1a 0%, #070f0a 60%, #000 100%)",
      fontFamily: "'SF Pro Display', -apple-system, BlinkMacSystemFont, 'Helvetica Neue', sans-serif",
      color: "#fff",
      padding: "0 0 60px",
    }}>
      {/* Header */}
      <header style={{
        display: "flex", alignItems: "center", justifyContent: "space-between",
        padding: "28px 40px",
        borderBottom: "1px solid rgba(57,255,20,0.12)",
        backdropFilter: "blur(10px)",
        position: "sticky", top: 0, zIndex: 100,
        background: "rgba(7,15,10,0.7)",
      }}>
        <div style={{ display: "flex", alignItems: "baseline", gap: 2 }}>
          <span style={{
            fontSize: 28, fontWeight: 800, letterSpacing: -1,
            color: NEON_GREEN,
            textShadow: `0 0 24px ${NEON_GREEN}88`,
          }}>group'd</span>
        </div>
        <span style={{ fontSize: 13, color: "rgba(255,255,255,0.35)", letterSpacing: 1 }}>
          Smart group generator for educators
        </span>
        {step === "results" && (
          <button onClick={reset} style={{
            background: "rgba(57,255,20,0.1)", border: `1px solid ${NEON_GREEN}55`,
            color: NEON_GREEN, borderRadius: 999, padding: "8px 20px",
            cursor: "pointer", fontSize: 14, fontWeight: 600, fontFamily: "inherit",
          }}>← New Session</button>
        )}
      </header>

      <main style={{ maxWidth: 680, margin: "0 auto", padding: "48px 24px 0" }}>
        {step === "setup" && (
          <>
            <div style={{ textAlign: "center", marginBottom: 48 }}>
              <h1 style={{
                fontSize: 48, fontWeight: 800, letterSpacing: -2, margin: "0 0 12px",
                background: `linear-gradient(135deg, ${NEON_GREEN}, #a8f5a2, #7fffd4)`,
                WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent",
              }}>
                Build better groups.
              </h1>
              <p style={{ color: "rgba(255,255,255,0.45)", fontSize: 17, margin: 0 }}>
                Paste your class list, set your constraints, and let the algorithm do the rest.
              </p>
            </div>

            <div style={{
              background: "rgba(255,255,255,0.04)", border: "1px solid rgba(255,255,255,0.1)",
              borderRadius: 20, padding: 32, backdropFilter: "blur(20px)",
              boxShadow: "0 8px 40px rgba(0,0,0,0.4)",
            }}>

              {/* Students */}
              <div style={{ marginBottom: 24 }}>
                <label style={{ display: "block", fontSize: 13, color: "rgba(255,255,255,0.5)", letterSpacing: 1, textTransform: "uppercase", marginBottom: 8 }}>
                  Class List — one name per line
                </label>
                <textarea
                  rows={6}
                  placeholder={"Alice\nBob\nCarla\nDavid\n..."}
                  value={rawStudents}
                  onChange={e => setRawStudents(e.target.value)}
                  style={inputStyle}
                />
                {students.length > 0 && (
                  <div style={{ display: "flex", flexWrap: "wrap", gap: 6, marginTop: 10 }}>
                    {students.map(s => <Tag key={s} label={s} />)}
                  </div>
                )}
              </div>

              {/* Number of groups */}
              <div style={{ marginBottom: 28 }}>
                <label style={{ fontSize: 13, color: "rgba(255,255,255,0.5)", letterSpacing: 1, textTransform: "uppercase" }}>
                  Number of Groups
                </label>
                <div style={{ display: "flex", alignItems: "center", gap: 16, marginTop: 10 }}>
                  <button onClick={() => setNumGroups(g => Math.max(1, g - 1))} style={{
                    width: 36, height: 36, borderRadius: "50%",
                    background: "rgba(57,255,20,0.1)", border: `1px solid ${NEON_GREEN}44`,
                    color: NEON_GREEN, fontSize: 20, cursor: "pointer", lineHeight: 1, fontFamily: "inherit",
                  }}>−</button>
                  <span style={{ fontSize: 36, fontWeight: 800, color: NEON_GREEN, minWidth: 40, textAlign: "center",
                    textShadow: `0 0 20px ${NEON_GREEN}66`
                  }}>{numGroups}</span>
                  <button onClick={() => setNumGroups(g => g + 1)} style={{
                    width: 36, height: 36, borderRadius: "50%",
                    background: "rgba(57,255,20,0.1)", border: `1px solid ${NEON_GREEN}44`,
                    color: NEON_GREEN, fontSize: 20, cursor: "pointer", lineHeight: 1, fontFamily: "inherit",
                  }}>+</button>
                  <span style={{ color: "rgba(255,255,255,0.3)", fontSize: 14 }}>
                    {students.length > 0 ? `≈ ${Math.ceil(students.length / numGroups)} students/group` : "groups"}
                  </span>
                </div>
              </div>

              {/* Constraints */}
              {students.length >= 2 && (
                <>
                  <div style={{ height: 1, background: "rgba(255,255,255,0.07)", margin: "24px 0" }} />
                  <p style={{ fontSize: 13, color: "rgba(255,255,255,0.35)", letterSpacing: 1, textTransform: "uppercase", marginBottom: 20 }}>
                    Constraints (optional)
                  </p>
                  <PairEditor
                    label="✓ Work well together"
                    pairs={togetherPairs}
                    onAdd={p => setTogetherPairs(prev => [...prev, p])}
                    onRemove={i => setTogetherPairs(prev => prev.filter((_, idx) => idx !== i))}
                    students={students}
                    accent={NEON_GREEN}
                  />
                  <PairEditor
                    label="✗ Do NOT put together"
                    pairs={notTogetherPairs}
                    onAdd={p => setNotTogetherPairs(prev => [...prev, p])}
                    onRemove={i => setNotTogetherPairs(prev => prev.filter((_, idx) => idx !== i))}
                    students={students}
                    accent="#ff6b6b"
                  />
                </>
              )}

              {error && <p style={{ color: "#ff6b6b", fontSize: 14, marginBottom: 12 }}>{error}</p>}

              <button
                onClick={generate}
                style={{
                  width: "100%", padding: "16px 0",
                  background: `linear-gradient(135deg, ${NEON_GREEN}, #7fffd4)`,
                  border: "none", borderRadius: 14,
                  fontSize: 17, fontWeight: 800, letterSpacing: 0.5,
                  color: "#030f07", cursor: "pointer", fontFamily: "inherit",
                  boxShadow: `0 4px 30px ${NEON_GREEN}44`,
                  transition: "transform 0.1s, box-shadow 0.2s",
                  marginTop: 8,
                }}
                onMouseDown={e => e.currentTarget.style.transform = "scale(0.98)"}
                onMouseUp={e => e.currentTarget.style.transform = "scale(1)"}
              >
                Generate Groups →
              </button>
            </div>
          </>
        )}

        {step === "results" && (
          <div style={{ textAlign: "center" }}>
            <h2 style={{
              fontSize: 36, fontWeight: 800, letterSpacing: -1,
              color: NEON_GREEN, textShadow: `0 0 30px ${NEON_GREEN}55`,
              margin: "0 0 4px",
            }}>
              {spinning ? "Generating…" : "Your Groups"}
            </h2>
            <p style={{ color: "rgba(255,255,255,0.35)", fontSize: 14, marginBottom: 0 }}>
              {spinning ? "Finding the optimal arrangement…" : results && `Optimisation score: ${results.score} (lower is better)`}
            </p>

            <CryptexRings spinning={spinning} />

            {!spinning && results && (
              <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(200px, 1fr))", gap: 16, marginTop: 16, textAlign: "left" }}>
                {results.groups.map((group, gi) => (
                  <div key={gi} style={{
                    background: GROUP_GRADIENTS[gi % GROUP_GRADIENTS.length],
                    borderRadius: 18, padding: "20px 22px",
                    boxShadow: "0 4px 24px rgba(0,0,0,0.3)",
                    animation: `fadeUp 0.7s cubic-bezier(0.22, 1, 0.36, 1) ${gi * 0.15}s both`,
                  }}>
                    <div style={{ fontSize: 11, fontWeight: 700, letterSpacing: 2, textTransform: "uppercase", color: "rgba(0,0,0,0.45)", marginBottom: 12 }}>
                      Group {gi + 1}
                    </div>
                    {group.map(s => (
                      <div key={s} style={{
                        fontSize: 15, fontWeight: 600, color: "#111",
                        padding: "6px 0",
                        borderBottom: "1px solid rgba(0,0,0,0.08)",
                      }}>{s}</div>
                    ))}
                  </div>
                ))}
              </div>
            )}

            {!spinning && (
              <button onClick={generate} style={{
                marginTop: 32, padding: "13px 36px",
                background: "rgba(57,255,20,0.08)", border: `1.5px solid ${NEON_GREEN}66`,
                borderRadius: 999, color: NEON_GREEN, fontSize: 15,
                fontWeight: 700, cursor: "pointer", fontFamily: "inherit",
              }}>
                Regenerate ↺
              </button>
            )}
          </div>
        )}
      </main>

      <style>{`
        @keyframes fadeUp {
          from { opacity: 0; transform: translateY(28px) scale(0.97); }
          to   { opacity: 1; transform: translateY(0) scale(1); }
        }
        textarea:focus, select:focus { outline: none; border-color: ${NEON_GREEN}66 !important; }
        * { -webkit-font-smoothing: antialiased; }
      `}</style>
    </div>
  );
}
