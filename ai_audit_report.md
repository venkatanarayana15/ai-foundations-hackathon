# 🔎 AI Audit Evidence Report — Samanantar

**For judges: the verifiable AI layer of the solution.**
**How to read this:** every AI decision in the classroom leaves a row in the `AI_AUDIT` log. Judges can inspect the repo and trace any diagnostic result back to its source: **LLM**, **fallback rule**, or **tap override**.

---

## 1. The one real LLM call, in four lines

```python
resp = client.messages.create(
    model=...,                        # e.g. claude-sonnet-4-5
    max_tokens=512,
    temperature=0,                    # deterministic, never random
    system=DIAGNOSTIC_SYSTEM,         # the contract the model must obey
    tools=[DIAGNOSTIC_TOOL],          # forced tool-use, structured output
    tool_choice={"type": "tool", "name": "record_diagnosis"},
    messages=[{"role": "user", "content": context}],
)
```

This is the **only** place `chat.completions.create` appears in the codebase. Everything else is deterministic, pure, unit-tested.

---

## 2. What the model is given (data input)

The diagnosis is a single structured JSON payload:

```json
{
  "item_id": "LIT-W-01",
  "domain": "literacy",
  "asked_level": "Word",
  "target_text": "बिल्ली",
  "expected_phonemes": ["bil", "li"],
  "prompt": "बिल्ली",
  "ncert_reference": "Rimjhim-1 page 24",
  "cbse_fln_skill": "FLN-L-2.1 Blending",
  "speech_recogniser_heard": "बिल्ल",
  "recogniser_confidence": 71,
  "teacher_override": false,
  "classroom_noise_db": 60
}
```

**No child name, no photo, no audio. Only the item, the transcript, and the context.** The only thing the model learns from a child is one scalar per item (Rasch difficulty) — there is no fine-tuning on children's speech.

---

## 3. What the model returns (output)

The tool schema forces the output into a fixed shape:

| Field | Type | Constraint |
|---|---|---|
| `level` | `enum` | Pre-Letter / Letter / Word / Paragraph / Story |
| `error_code` | `enum` | LIT-01 / LIT-02 / LIT-03 / MATH-01 / MATH-02 / MATH-03 |
| `misconception` | `string` | Free text but must cite the given NCERT page |
| `teacher_hint` | `string` | One sentence, Hindi, actional in <5 min |
| `cra_stage` | `enum` | concrete / representational / abstract |
| `confidence` | `number` | 0–1, must be ≤ 0.85 if no teacher override |

---

## 4. The guardrails, in code

```python
# DIAGNOSTIC_SYSTEM (abridged)
You may ONLY cite the NCERT book and page supplied to you.
The teacher hint must be actionable in under 5 minutes ...
If confidence is below 80 percent and there was no teacher override,
you must return a lower confidence and prefer the most conservative
(easiest) interpretation.
```

The tool schema (JSON Schema) enforces the output shape on the model itself:

```python
DIAGNOSTIC_TOOL = {
    "name": "record_diagnosis",
    "input_schema": {
        "type": "object",
        "properties": {
            "level": {"type": "string", "enum": ["Pre-Letter", "Letter", "Word", "Paragraph", "Story"]},
            "error_code": {"type": "string", "enum": ["LIT-01", "LIT-02", "LIT-03", "MATH-01", "MATH-02", "MATH-03"]},
            ...
        },
        "required": ["level", "error_code", "teacher_hint", "cra_stage", "confidence"],
    },
}
```

---

## 5. The audit trail: which path produced which result

Every diagnosis appends a row to `AI_AUDIT`:

```python
def _audit(component, path, detail=None):
    AI_AUDIT.append({
        "component": component,   # "diagnostic_llm"
        "path": path,             # "llm" | "fallback_after_error" | "fallback_conservative" | "fallback_rules"
        "detail": detail or {},
    })
```

| `path` | Meaning | Example |
|---|---|---|
| `"llm"` | The real Claude model returned a valid structured diagnosis. | `{"model": "claude-sonnet-4-5", "level": "Word"}` |
| `"fallback_after_error"` | Network failure or parse error → the rule path took over. | `{"error": "Timeout"}` |
| `"fallback_conservative"` | Unverified transcript, no override → conservative judgment. | `{"noise_db": 60}` |
| `"fallback_rules"` | Normal rule-path diagnosis, no LLM needed. | `{"override": false, "conf": 0.71}` |

**The honest framing:** in Build stage, most decisions come from the fallback path (no API key in the demo). That is a *feature*, not a bug — it means the product works without a network, and the audit log makes the LLM-versus-fallback rate measurable.

---

## 6. The non-LLM AI components

### 6.1 AsrScorer — the trust gate (real DSP)

```python
class AsrScorer:
    CONF_FLOOR = 0.80   # below this we do not judge the child on audio alone
    SIM_FLOOR = 0.75    # weighted similarity needed to count as "read it"

    def score(self, target, heard, asr_confidence, noise_db=50, teacher_override=None):
        ...
        # weighted levenshtein: vowel signs (matras) cost 3× consonants
        dist = _weighted_levenshtein(t, h)
        eff_conf = float(asr_confidence) * (1.0 - 0.004 * max(0, noise_db - 40))
        usable = eff_conf >= self.CONF_FLOOR
        ...
```

**Why this is AI:** a dropped vowel sign (`bili` → `billi`) changes the word. A naive character distance would score it at 83% and pass it. Weighting a matra three times a consonant is a linguistically-grounded decision, not a threshold tweak.

### 6.2 DifficultyModel — the Rasch adaptive ladder

```python
class DifficultyModel:
    def observe(self, item_id, was_correct, prior_weight=1.0):
        # 1PL IRT: P(correct | theta) = 1 / (1 + exp(+theta))
        # theta = difficulty (logits)
        # Every observation shrinks the standard error
        ...
```

The ladder is adaptive: two misses at a level → step down immediately. The Rasch estimate prevents oscillation between adjacent levels for borderline children.

---

## 7. How a judge verifies this

1. **`python ai.py`** → runs the self-test, shows the AI component checks pass.
2. **`python -X utf8 app.py`** → the app's **AI Lab** tab shows the model registry, a live diagnosis tester, the Rasch chart, and the full `AI_AUDIT` trail.
3. **Read `ai.py`** → the single `client.messages.create` call; the tool schema; the fallback paths; the audit function.
4. **Check `.github/workflows/ci.yml`** → CI runs the pack validation, engine tests, and compile check on every push.

---

## 8. What we will measure in the pilot (pre-registered, OSF)

| Endpoint | Type | Target |
|---|---|---|
| % children gaining ≥1 ASER level | Primary | Report d + 95% CI |
| Teacher minutes per child (stopwatch) | Co-primary | ≤5 min; paper 10–15 |
| TOST equivalence, app vs paper, ±0.2 SD | Fidelity | Pass = no loss |
| Quadratic-weighted κ vs blinded re-test | Agreement | κ ≥ 0.75 |
| Override rate, completion, usage days/week | Fidelity | Logged weekly, not recalled |
| Simulator (45 children, 60 dB, battery throttle) | Engineering | ≥90% stable ≤5 min, 0 crashes, resumes after kill |

**Honest power:** at ICC 0.15 with two classrooms per arm, the minimum detectable effect is ~0.40 SD. So we pre-commit to reporting effect sizes with confidence intervals — not claiming a 20-point difference we cannot detect.
