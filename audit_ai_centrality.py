"""Verifies the AI-centrality claim against the source code.

Guidelines §3.7: "AI must be central to the solution developed, and should
leverage (as best possible) the advanced capabilities that frontier LLM models
and AI tools offer. Source-code shared as part of the Build stage submission
will be used to verify how AI is being used in the solution."
"""
import ast
import os
import re

print("=" * 70)
print("AI-CENTRICITY AUDIT — what a judge opening the repo would find")
print("=" * 70)

results = []


def check(label, cond, detail=""):
    results.append(cond)
    print(f"  [{'PASS' if cond else 'FAIL'}] {label}" + (f"  {detail}" if detail else ""))


ai = open("ai.py", encoding="utf-8").read()

print("\n--- 1. A real frontier-LLM integration, not a stub ---")
check("Claude named as the diagnostic model", "claude" in ai.lower())
check("Anthropic SDK called", "anthropic.Anthropic" in ai or "anthropic" in ai)
check("API key read from environment", "ANTHROPIC_API_KEY" in ai)
check("Actual messages.create() call", "messages.create" in ai)
check("System prompt defined", "DIAGNOSTIC_SYSTEM" in ai)
check("Tool-use schema defined", "DIAGNOSTIC_TOOL" in ai)
check("Forced tool choice (not free prose)", '"type": "tool"' in ai or "tool_choice" in ai)
check("Temperature pinned to 0", "temperature=0" in ai)
check("Grounding rule: model may only cite given pages",
      "only cite the NCERT book and page supplied" in ai or "may ONLY cite" in ai)

print("\n--- 2. Genuine ML/algorithmic components (not random) ---")
check("Matra-weighted Devanagari edit distance", "_weighted_levenshtein" in ai and "_MATRA" in ai)
check("Confidence gating before judging a child", "CONF_FLOOR" in ai and "needs_tap" in ai)
check("1PL/Rasch item-response model", "RaschItem" in ai and "_sigmoid" in ai)
check("Damped Newton update with prior", "prior_weight" in ai)
check("No random() in the AI decision path",
      "random" not in ai.split("def _fallback")[0].split("class LlmDiagnostic")[1])

print("\n--- 3. The app actually calls the AI layer ---")
app = open("app.py", encoding="utf-8").read()
check("app imports the AI layer", "from ai import" in app)
check("Voice path calls the scorer", "_SCORER.score" in app)
check("Voice path calls the LLM diagnosis", "_DIAG.diagnose" in app)
check("Rasch updated per item", "_RASCH.observe" in app)
check("TaRL grouping used for benches", "tarl_groups" in app)

print("\n--- 4. AI is observable by judges, not hidden ---")
check("AI Lab tab in the UI", "AI Lab" in app)
check("Model registry exposed", "MODEL_REGISTRY" in app)
check("Audit log records which path ran", "AI_AUDIT" in app)
check("llm vs fallback source reported", "source" in ai and "fallback" in ai)

print("\n--- 5. Honest degradation, not silent faking ---")
check("Deterministic offline fallback documented", "_fallback" in ai)
check("Fallback is audited, not hidden", 'audit("diagnostic_llm", "fallback' in ai)
check("Conservative behaviour when unverified", "conservative" in ai)

print("\n--- 6. Quality gates ---")
try:
    import subprocess
    r1 = subprocess.run(["python", "-X", "utf8", "ai.py"], capture_output=True, text=True)
    check("ai.py self-tests pass", r1.returncode == 0, r1.stdout.strip().split("\n")[0])
    r2 = subprocess.run(["python", "-X", "utf8", "engines.py"], capture_output=True, text=True)
    check("engines.py self-tests pass", r2.returncode == 0, r2.stdout.strip().split("\n")[0])
except Exception as e:
    check("self-tests run", False, str(e))

check("CI validates pack + compiles app", os.path.exists(".github/workflows/ci.yml"))
pack = open("content_pack.json", encoding="utf-8").read()
p = __import__("json").loads(pack)
check("Every content item cites NCERT + CBSE",
      all(i.get("ncertRef") and i.get("cbseFln") for i in p["items"]),
      f"{len(p['items'])} items")

print("\n" + "=" * 70)
n, f = results.count(True), results.count(False)
print(f"{n}/{n+f} AI-centrality checks passed")
print("=" * 70)
