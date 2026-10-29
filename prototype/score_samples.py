"""Illustrative deterministic scorer for the fictional sample set.

This is not a PDF parser and does not call an AI model. It assumes facts have
already been extracted and validated. Scoring bands are explicit design
assumptions because the assessment brief supplies weights but not score bands.
"""
from dataclasses import dataclass
import json

WEIGHTS = {
    "experience": 0.30,
    "price": 0.25,
    "timeline": 0.15,
    "warranty": 0.15,
    "team": 0.15,
}

def experience_score(installs):
    if installs >= 12: return 100
    if installs >= 9: return 80
    if installs >= 6: return 60
    return 40

def price_score(price):
    if price <= 220_000: return 100
    if price <= 235_000: return 90
    if price <= 250_000: return 80
    if price <= 260_000: return 60
    return 0

def timeline_score(weeks):
    if weeks <= 10: return 100
    if weeks <= 12: return 90
    if weeks <= 14: return 80
    if weeks <= 16: return 60
    return 0

def warranty_score(panel_years, workmanship_years):
    # Each warranty contributes half; cap each at 100.
    panel = 100 if panel_years >= 25 else 80 if panel_years >= 20 else 50
    work = 100 if workmanship_years >= 10 else 80 if workmanship_years >= 7 else 60
    return (panel + work) / 2

def team_score(named_lead, crew, safety, monitoring_months):
    score = 0
    score += 25 if named_lead else 0
    score += 25 if crew >= 5 else 15 if crew >= 3 else 0
    score += 25 if safety else 0
    score += 25 if monitoring_months >= 12 else 15 if monitoring_months > 0 else 0
    return score

SAMPLES = {
    "A": dict(installs=14, price=238000, weeks=12, panel=25, work=10,
              lead=True, crew=6, safety=True, monitoring=12),
    "C": dict(installs=9, price=244000, weeks=14, panel=25, work=10,
              lead=True, crew=5, safety=False, monitoring=0),
    "E": dict(installs=8, price=242500, weeks=13, panel=25, work=12,
              lead=True, crew=6, safety=True, monitoring=24),
}

def score(sample):
    parts = {
        "experience": experience_score(sample["installs"]),
        "price": price_score(sample["price"]),
        "timeline": timeline_score(sample["weeks"]),
        "warranty": warranty_score(sample["panel"], sample["work"]),
        "team": team_score(sample["lead"], sample["crew"], sample["safety"], sample["monitoring"]),
    }
    total = round(sum(parts[k] * WEIGHTS[k] for k in WEIGHTS), 1)
    return {"subscores": parts, "score": total}

if __name__ == "__main__":
    results = {letter: score(sample) for letter, sample in SAMPLES.items()}
    print(json.dumps(results, indent=2))
