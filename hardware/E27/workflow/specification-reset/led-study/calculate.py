"""Preliminary optical screening; no manufacturing or lifetime qualification."""
import json
from itertools import product

CREE = {
    "2700": {"mpn": "JE2835BWT-N-H27GA0000-N0000001", "count": 14, "lm25": 70.7, "lm85": 63.8, "min25": 69.0},
    "4000": {"mpn": "JE2835BWT-N-H40GA0000-N0000001", "count": 13, "lm25": 78.1, "lm85": 70.5, "min25": 75.0},
    "6500": {"mpn": "JE2835BWT-N-H65GA0000-N0000001", "count": 13, "lm25": 77.1, "lm85": 69.6, "min25": 75.0},
}
LUMILEDS = {
    "2700": {"mpn": "L128-2780SA35A00D1", "count": 30, "lm25": 34.0, "min25": 31.6},
    "4000": {"mpn": "L128-4080SA35A00D1", "count": 28, "lm25": 36.3, "min25": 33.8},
    "6500": {"mpn": "L128-6580SA35A00D1", "count": 28, "lm25": 36.3, "min25": 33.8},
}

def classify(fluxes):
    ratio = max(fluxes) / min(fluxes)
    return {"ratio": round(ratio, 5), "nominal_criteria_met": all(750 <= x <= 850 for x in fluxes) and ratio <= 1.10}

def calculate():
    tau = 0.87  # Unmeasured optical transmission assumption, not a part specification.
    out = {"scope": "calculation only; candidate counts/currents, not approved electrical interface", "cree": {}, "lumileds": {}, "sensitivity": []}
    for cct, p in CREE.items():
        n=p["count"]
        out["cree"][cct] = {"count": n, "current_ma": 150, "flux_lm": round(n*p["lm85"]*tau, 2), "typical_string_v_25C": round(n*2.86, 2), "typical_led_electrical_w_25C": round(n*2.86*.15, 3), "low_bin_hot_proxy_lm_not_guaranteed": round(n*p["min25"]*p["lm85"]/p["lm25"]*tau, 2)}
    for cct,p in LUMILEDS.items():
        # Temperature multiplier 0.90 is an assumed sensitivity, not a hot specification.
        out["lumileds"][cct] = {"count": p["count"], "current_ma": 65, "flux_lm_assuming_hot_factor_0_90": round(p["count"]*p["lm25"]*tau*.90,2), "lower_flux_assuming_same_hot_factor":round(p["count"]*p["min25"]*tau*.90,2), "illustrative_electrical_w_at_assumed_2_8V_each":round(p["count"]*2.8*.065,3)}
    out["cree_nominal"] = classify([p["flux_lm"] for p in out["cree"].values()])
    out["lumileds_nominal_assumed_hot"] = classify([p["flux_lm_assuming_hot_factor_0_90"] for p in out["lumileds"].values()])
    # Independent per-colour deviations: equal/common factors would hide matching risk.
    for source, p in [("cree", CREE),("lumileds",LUMILEDS)]:
        bad=0; cases=0; low=1e9; high=0; worst=0
        for t in [.80,.87,.90]:
            for factors in product([.93,1.0,1.07], repeat=3):
                fs=[]
                for (_,v), factor in zip(p.items(),factors):
                    base=v["lm85"] if source=="cree" else v["lm25"]*.90
                    fs.append(v["count"]*base*t*factor)
                result=classify(fs);cases+=1;bad+=not result["nominal_criteria_met"]
                low=min(low,min(fs));high=max(high,max(fs));worst=max(worst,result["ratio"])
        out["sensitivity"].append({"family":source,"cases":cases,"failing_criteria":bad,"min_lm":round(low,2),"max_lm":round(high,2),"max_ratio":round(worst,5),"meaning":"assumed independent +/-7% deviations; not a statistical or manufacturer tolerance guarantee"})
    # Simple equal-count comparison deliberately isolates the CCT mismatch.
    equal=[14*p["lm85"]*tau for p in CREE.values()]
    out["cree_equal_count_14"]={"flux_lm":[round(x,2) for x in equal], **classify(equal)}
    # Panel electrical power is a conservative upper-bound heat budget, not measured heat.
    out["power_sensitivity"]=[{"panel_electrical_w":p,"assumed_driver_efficiency":eff,"input_w":round(p/eff,3),"base_conversion_loss_w":round(p/eff-p,3)} for p in [5.5,6.0] for eff in [.80,.85,.90]]
    return out

if __name__ == "__main__":
    print(json.dumps(calculate(), indent=2))
