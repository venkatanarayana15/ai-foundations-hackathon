"""Pure, testable engines — no Streamlit dependency."""
import random

LEVEL_ORDER = ["Pre-Letter","Letter","Word","Paragraph","Story"]

def level_to_idx(l: str) -> int:
    return LEVEL_ORDER.index(l) if l in LEVEL_ORDER else 0

def diagnose(results: list) -> tuple:
    """ASER thresholds. results: [{level, correct, error, cer, wer, conf}]"""
    if not results:
        return "Pre-Letter", [], 0
    correct = sum(1 for r in results if r.get("correct"))
    acc = correct / len(results)
    errs = [r["error"] for r in results if not r.get("correct") and r.get("error")]
    if acc >= 0.85:
        lvl = "Story" if "Story" in [r.get("level") for r in results] else "Paragraph"
    elif acc >= 0.70:
        lvl = "Word"
    elif acc >= 0.45:
        lvl = "Letter"
    else:
        lvl = "Pre-Letter"
    if acc >= 0.85 and lvl == "Word":
        lvl = "Paragraph"
    return lvl, errs, round(acc*100, 1)

def remediation_for(level: str, errors: list, pack: dict) -> dict:
    if errors and errors[0] in pack.get("errorCodes", {}):
        return pack["errorCodes"][errors[0]]
    mapping = {"Pre-Letter":"LIT-03","Letter":"LIT-01","Word":"LIT-02","Paragraph":"LIT-02","Story":"LIT-02"}
    return pack["errorCodes"][mapping.get(level,"LIT-01")]

def simulate_asr(level: str, noise_db: int, lang: str = "hi") -> dict:
    base_cer = {"Pre-Letter":6,"Letter":7,"Word":9,"Paragraph":14,"Story":18, "Concrete":7,"Representational":10,"Abstract":11}.get(level, 9)
    noise_penalty = {40:0,50:4,60:11}.get(noise_db, 4)
    cer = max(2, min(28, base_cer + noise_penalty + random.randint(-2,3)))
    wer = cer + random.randint(6,12)
    conf = max(52, 96 - cer*1.6 + random.randint(-4,4))
    p_correct = max(0.35, 0.92 - noise_db*0.008 - cer*0.012)
    is_correct = random.random() < p_correct
    # pick error
    err = None
    if not is_correct:
        # will be filled by caller with pack keys
        err = random.choice(["LIT-01","LIT-02","MATH-01","MATH-02"])
    return {"correct": is_correct, "error": err, "cer": cer, "wer": wer, "conf": round(conf,1)}

def validate_content_pack(pack: dict) -> list:
    """CI rule: every item must have ncertRef and cbseFln. Returns list of errors."""
    errs=[]
    for it in pack.get("items",[]):
        if not it.get("ncertRef"): errs.append(f"{it['id']} missing ncertRef")
        if not it.get("cbseFln"): errs.append(f"{it['id']} missing cbseFln")
    return errs

# --- Minimal unit tests (run: python engines.py) ---
if __name__ == "__main__":
    assert diagnose([])[0]=="Pre-Letter"
    assert diagnose([{"correct":True},{"correct":True},{"correct":True}], )[0] in LEVEL_ORDER
    assert level_to_idx("Word")==2
    pack = {"errorCodes":{"LIT-01":{"label":"x"},"LIT-03":{"label":"y"}},"items":[]}
    assert remediation_for("Letter", [], pack)["label"]=="x"
    assert remediation_for("Word", ["LIT-03"], pack)["label"]=="y"
    assert validate_content_pack({"items":[{"id":"A","ncertRef":None,"cbseFln":"x"}]})
    print("engines.py — all checks passed")
