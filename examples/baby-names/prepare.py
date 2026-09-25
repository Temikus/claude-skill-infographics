#!/usr/bin/env python3
"""Aggregate the SSA baby-names CSV (via hadley/data-baby-names) into data.json.

Source rows: year, name, percent (share of births of that sex), sex. Top 1,000
names per sex per year, 1880-2008. Rerun only to refresh data.json.
"""
import csv, json, sys, urllib.request
from collections import defaultdict
from pathlib import Path

URL = "https://raw.githubusercontent.com/hadley/data-baby-names/master/baby-names.csv"
HERE = Path(__file__).parent
CACHE = HERE / ".cache" / "baby-names.csv"
TRACKED = ["Mary", "Jennifer", "Emma", "John", "Michael", "Jacob"]

def load():
    if not CACHE.exists():
        CACHE.parent.mkdir(exist_ok=True)
        urllib.request.urlretrieve(URL, CACHE)
    by = defaultdict(list)
    with CACHE.open() as f:
        for r in csv.DictReader(f):
            by[(int(r["year"]), r["sex"])].append((r["name"], float(r["percent"])))
    for k in by:
        by[k].sort(key=lambda x: -x[1])
    return by

def main():
    by = load()
    years = sorted({y for y, _ in by})
    out = {"years": years, "source": URL, "series": {}, "top10": {}, "tracked": {}}
    for sex in ("boy", "girl"):
        out["series"][sex] = {
            "top1": [round(by[(y, sex)][0][1] * 100, 3) for y in years],
            "top1_name": [by[(y, sex)][0][0] for y in years],
            "top10": [round(sum(p for _, p in by[(y, sex)][:10]) * 100, 2) for y in years],
            "top1000": [round(sum(p for _, p in by[(y, sex)]) * 100, 2) for y in years],
        }
        for y in (1950, 1998, 2008):
            out["top10"][f"{sex}_{y}"] = [(n, round(p * 100, 2)) for n, p in by[(y, sex)][:10]]
    for name in TRACKED:
        for sex in ("boy", "girl"):
            vals = [dict(by[(y, sex)]).get(name, 0.0) * 100 for y in years]
            if max(vals) > 0.5:
                out["tracked"][name] = {"sex": sex, "share": [round(v, 3) for v in vals]}
    (HERE / "data.json").write_text(json.dumps(out, separators=(",", ":")) + "\n")
    print(f"wrote data.json ({len(years)} years)", file=sys.stderr)

if __name__ == "__main__":
    main()
