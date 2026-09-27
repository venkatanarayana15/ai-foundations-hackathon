"""Pre-written analysis script — frozen before post-test (preregistration.md)"""
import pandas as pd, json, statistics
LEVEL_ORDER=["Pre-Letter","Letter","Word","Paragraph","Story"]
def level_to_idx(l): return LEVEL_ORDER.index(l) if l in LEVEL_ORDER else 0
def cohens_d(group_t, group_c):
    # simple pooled SD
    mt=sum(group_t)/len(group_t); mc=sum(group_c)/len(group_c)
    vt=statistics.pvariance(group_t) if len(group_t)>1 else 0
    vc=statistics.pvariance(group_c) if len(group_c)>1 else 0
    pooled=( (vt+vc)/2 )**0.5 or 1
    return (mt-mc)/pooled
# Example: load assessments CSV exported from app
# df=pd.read_csv("samanantar_assessments.csv")
# map levels to idx for gain
# df["idx"]=df["level"].map(level_to_idx)
# Compute κ and TOST externally (requires blinded re-test)
print("analysis.py — mixed-effects placeholder: use lme4/brms with (1|classroom). MDES 0.40 SD at ICC 0.15")
