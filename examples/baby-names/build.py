#!/usr/bin/env python3
"""Render two HTML pages from data.json: with-skill.html and without-skill.html.

Both use the same numbers and inline SVG. Only the page design differs.
"""
import json
from datetime import date
from pathlib import Path

HERE = Path(__file__).parent
D = json.loads((HERE / "data.json").read_text())
YEARS = D["years"]
Y0, Y1 = YEARS[0], YEARS[-1]
FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"

def idx(year):
    return YEARS.index(year)

def pct(v, nd=1):
    return f"{v:.{nd}f}%"

# --- SVG helpers ---------------------------------------------------------------

def scale(lo, hi, a, b):
    return lambda v: a + (v - lo) / (hi - lo) * (b - a)

def spread(ys, gap):
    """Push end-label y positions apart so none sit closer than gap."""
    order = sorted(range(len(ys)), key=lambda i: ys[i])
    out = list(ys)
    for a, b in zip(order, order[1:]):
        if out[b] - out[a] < gap:
            out[b] = out[a] + gap
    return out

def polyline(xs, ys, **attrs):
    pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in zip(xs, ys))
    a = " ".join(f'{k.replace("_", "-")}="{v}"' for k, v in attrs.items())
    return f'<polyline points="{pts}" fill="none" {a}/>'

def sparkline(vals, w=140, h=32, color="#1a1a1a"):
    sx = scale(0, len(vals) - 1, 0, w - 4)
    sy = scale(min(vals), max(vals), h - 3, 3)
    xs = [sx(i) for i in range(len(vals))]
    ys = [sy(v) for v in vals]
    return (f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" aria-hidden="true">'
            + polyline(xs, ys, stroke=color, stroke_width=1.5)
            + f'<circle cx="{xs[-1]:.1f}" cy="{ys[-1]:.1f}" r="2.5" fill="#1f5fbf"/></svg>')

def line_chart(series, w=1000, h=340, ymax=None, xticks=(), yticks=(), yfmt=pct,
               font=FONT, end_labels=True, legend=False, grid=False, colors=None):
    """series: list of dict(name, values, color, width). Shared x = YEARS."""
    m = dict(l=48, r=170 if end_labels else 24, t=16, b=60 if legend else 36)
    ymax = ymax or max(max(s["values"]) for s in series) * 1.05
    sx = scale(Y0, Y1, m["l"], w - m["r"])
    sy = scale(0, ymax, h - m["b"], m["t"])
    out = [f'<svg width="100%" viewBox="0 0 {w} {h}" font-family="{font}" font-size="13">']
    for t in yticks:
        y = sy(t)
        if grid:
            out.append(f'<line x1="{m["l"]}" x2="{w-m["r"]}" y1="{y:.1f}" y2="{y:.1f}" stroke="#e5e5e5"/>')
        out.append(f'<text x="{m["l"]-8}" y="{y+4:.1f}" text-anchor="end" fill="#666">{yfmt(t, 0)}</text>')
    for t in xticks:
        out.append(f'<text x="{sx(t):.1f}" y="{h-10}" text-anchor="middle" fill="#666">{t}</text>')
    out.append(f'<line x1="{m["l"]}" x2="{w-m["r"]}" y1="{sy(0):.1f}" y2="{sy(0):.1f}" stroke="#bbb"/>')
    label_y = spread([sy(s["values"][-1]) for s in series], 16)
    for s, ly in zip(series, label_y):
        xs = [sx(y) for y in YEARS]
        ys = [sy(v) for v in s["values"]]
        out.append(polyline(xs, ys, stroke=s["color"], stroke_width=s.get("width", 2)))
        if end_labels:
            out.append(f'<text x="{xs[-1]+8:.1f}" y="{ly+4:.1f}" fill="{s["color"]}" font-weight="600">'
                       f'{s["name"]} {pct(s["values"][-1])}</text>')
        if "start_label" in s:
            out.append(f'<text x="{xs[0]:.1f}" y="{ys[0]-8:.1f}" fill="{s["color"]}">{s["start_label"]}</text>')
    if legend:
        x = m["l"]
        for s in series:
            out.append(f'<rect x="{x}" y="{h-4}" width="12" height="3" fill="{s["color"]}"/>'
                       f'<text x="{x+16}" y="{h}" fill="#333">{s["name"]}</text>')
            x += 16 + 8 * len(s["name"]) + 24
    out.append("</svg>")
    return "".join(out)

def hbars(items, highlight, xmax, w=480, font=FONT, note=None):
    """items: [(label, value, sublabel)], sorted by caller. highlight: set of labels."""
    rh, gap, lw = 22, 8, 150
    h = len(items) * (rh + gap) + 8
    sx = scale(0, xmax, lw, w - 60)
    out = [f'<svg width="100%" viewBox="0 0 {w} {h}" font-family="{font}" font-size="13">']
    for i, (label, v, sub) in enumerate(items):
        y = i * (rh + gap) + 4
        hl = label in highlight
        out.append(f'<text x="{lw-10}" y="{y+15}" text-anchor="end" fill="#1a1a1a" font-weight="{600 if hl else 400}">{label}</text>')
        out.append(f'<rect x="{lw}" y="{y}" width="{sx(v)-lw:.1f}" height="{rh}" fill="{"#1f5fbf" if hl else "#c7c9cc"}"/>')
        out.append(f'<text x="{sx(v)+6:.1f}" y="{y+15}" fill="#1a1a1a">{pct(v, 2)}</text>')
        if sub:
            out.append(f'<text x="{lw+6}" y="{y+15}" fill="{"#fff" if hl else "#444"}" font-size="11">{sub}</text>')
    out.append("</svg>")
    return "".join(out)

def small_multiple(name, vals, ymax, w=320, h=150, font=FONT):
    m = dict(l=8, r=8, t=28, b=22)
    sx = scale(Y0, Y1, m["l"], w - m["r"])
    sy = scale(0, ymax, h - m["b"], m["t"])
    xs = [sx(y) for y in YEARS]
    ys = [sy(v) for v in vals]
    pk = max(range(len(vals)), key=lambda i: vals[i])
    out = [f'<svg width="100%" viewBox="0 0 {w} {h}" font-family="{font}" font-size="12">',
           f'<text x="{m["l"]}" y="16" font-size="14" font-weight="600" fill="#1a1a1a">{name}</text>',
           f'<text x="{w-m["r"]}" y="16" text-anchor="end" fill="#444">peak {pct(vals[pk])} in {YEARS[pk]}</text>',
           f'<line x1="{m["l"]}" x2="{w-m["r"]}" y1="{sy(0):.1f}" y2="{sy(0):.1f}" stroke="#bbb"/>',
           polyline(xs, ys, stroke="#1a1a1a", stroke_width=1.8),
           f'<circle cx="{xs[pk]:.1f}" cy="{ys[pk]:.1f}" r="3" fill="#1f5fbf"/>',
           f'<text x="{m["l"]}" y="{h-6}" fill="#666">{Y0}</text>',
           f'<text x="{w-m["r"]}" y="{h-6}" text-anchor="end" fill="#666">{Y1}</text></svg>']
    return "".join(out)

def pie(items, w=560, h=300, font=FONT):
    import math
    colors = ["#4e79a7", "#f28e2b", "#e15759", "#76b7b2", "#59a14f", "#edc948", "#b07aa1", "#ff9da7", "#9c755f", "#bab0ab"]
    cx, cy, r = 150, 150, 120
    total = sum(v for _, v in items)
    a0 = -math.pi / 2
    out = [f'<svg width="100%" viewBox="0 0 {w} {h}" font-family="{font}" font-size="13">']
    for i, (label, v) in enumerate(items):
        a1 = a0 + 2 * math.pi * v / total
        x0, y0 = cx + r * math.cos(a0), cy + r * math.sin(a0)
        x1, y1 = cx + r * math.cos(a1), cy + r * math.sin(a1)
        out.append(f'<path d="M{cx},{cy} L{x0:.1f},{y0:.1f} A{r},{r} 0 0 1 {x1:.1f},{y1:.1f} Z" fill="{colors[i]}" stroke="#fff"/>')
        out.append(f'<rect x="320" y="{30+i*26}" width="14" height="14" fill="{colors[i]}"/>'
                   f'<text x="342" y="{42+i*26}" fill="#333">{label} ({pct(v, 2)})</text>')
        a0 = a1
    out.append("</svg>")
    return "".join(out)

def vbars(items, w=560, h=300, font=FONT):
    colors = ["#4e79a7", "#f28e2b", "#e15759", "#76b7b2", "#59a14f", "#edc948", "#b07aa1", "#ff9da7", "#9c755f", "#bab0ab"]
    m = dict(l=50, r=10, t=10, b=60)
    ymax = max(v for _, v in items) * 1.1
    sy = scale(0, ymax, h - m["b"], m["t"])
    bw = (w - m["l"] - m["r"]) / len(items)
    out = [f'<svg width="100%" viewBox="0 0 {w} {h}" font-family="{font}" font-size="12">']
    for t in (0, 0.25, 0.5, 0.75, 1.0):
        out.append(f'<line x1="{m["l"]}" x2="{w-m["r"]}" y1="{sy(t):.1f}" y2="{sy(t):.1f}" stroke="#e5e5e5"/>'
                   f'<text x="{m["l"]-6}" y="{sy(t)+4:.1f}" text-anchor="end" fill="#666">{t:.2f}%</text>')
    for i, (label, v) in enumerate(items):
        x = m["l"] + i * bw + bw * 0.15
        out.append(f'<rect x="{x:.1f}" y="{sy(v):.1f}" width="{bw*0.7:.1f}" height="{sy(0)-sy(v):.1f}" fill="{colors[i]}"/>')
        out.append(f'<text x="{x+bw*0.35:.1f}" y="{h-m["b"]+14}" text-anchor="middle" fill="#333" transform="rotate(-35 {x+bw*0.35:.1f},{h-m["b"]+14})">{label}</text>')
    out.append("</svg>")
    return "".join(out)

# --- numbers used on both pages ------------------------------------------------

boy, girl = D["series"]["boy"], D["series"]["girl"]
i08, i00, i50, i80 = idx(2008), idx(2000), idx(1950), idx(1880)
boy_top10_08, boy_top10_00, boy_top10_80 = boy["top10"][i08], boy["top10"][i00], boy["top10"][i80]
girl_top10_08, girl_top10_00, girl_top10_80 = girl["top10"][i08], girl["top10"][i00], girl["top10"][i80]
girl_out_08 = 100 - girl["top1000"][i08]
girl_out_80 = 100 - girl["top1000"][i80]
boy_out_08 = 100 - boy["top1000"][i08]
boy_top1_08, boy_top1_name_08 = boy["top1"][i08], boy["top1_name"][i08]
boy_top1_80, boy_top1_name_80 = boy["top1"][i80], boy["top1_name"][i80]
top10 = {k: D["top10"][k] for k in D["top10"]}
new_boys = {n for n, _ in top10["boy_2008"]} - {n for n, _ in top10["boy_1998"]}
new_girls = {n for n, _ in top10["girl_2008"]} - {n for n, _ in top10["girl_1998"]}
gone_boys = {n for n, _ in top10["boy_1998"]} - {n for n, _ in top10["boy_2008"]}
rank98 = {s: {n: i + 1 for i, (n, _) in enumerate(top10[f"{s}_1998"])} for s in ("boy", "girl")}
share_ten_years_ago = lambda s, n: dict(top10[f"{s}_1998"]).get(n)

def names(s):
    s = sorted(s)
    return ", ".join(s[:-1]) + " and " + s[-1]

def sub_label(sex, name):
    r = rank98[sex].get(name)
    return f"#{r} in 1998" if r else "not in 1998 top 10"

peak = {n: max(t["share"]) for n, t in D["tracked"].items()}
tracked_order = ["Mary", "John", "Jennifer", "Michael", "Jacob", "Emma"]
run = date.today().isoformat()

# --- with skill ------------------------------------------------------------------

CSS_SKILL = f"""
*{{box-sizing:border-box}} body{{margin:0;background:#fff;color:#1a1a1a;font-family:{FONT};font-size:15px;line-height:1.45}}
main{{max-width:1100px;margin:0 auto;padding:28px 32px 48px}}
h1{{font-size:28px;font-weight:600;margin:0 0 2px;letter-spacing:-.01em}}
.meta{{font-size:13px;color:#666;margin:0 0 14px}}
.lede{{font-size:17px;max-width:900px;margin:0 0 22px}} .lede b{{font-weight:600}}
.tiles{{display:grid;grid-template-columns:1.35fr 1fr 1fr 1fr;gap:14px;margin-bottom:22px}}
.tile{{border:1px solid #e2e2e2;border-radius:6px;padding:14px 16px 12px}}
.tile .label{{font-size:13px;color:#555;height:36px;line-height:18px}}
.tile .value{{font-size:28px;font-weight:600;line-height:1;margin:4px 0 6px;font-variant-numeric:tabular-nums}}
.tile.hero .value{{font-size:40px}}
.tile .cmp{{font-size:13px;color:#555;height:36px;line-height:18px}} .tile .cmp b{{color:#1a1a1a;font-weight:600}}
.tile svg{{display:block;margin-top:6px}}
ol.take{{list-style:none;counter-reset:t;padding:0;margin:0 0 30px;display:grid;grid-template-columns:repeat(3,1fr);gap:20px}}
ol.take li{{counter-increment:t;padding-left:34px;position:relative}}
ol.take li::before{{content:counter(t);position:absolute;left:0;top:0;width:24px;height:24px;border-radius:50%;background:#1f5fbf;color:#fff;font-weight:600;font-size:13px;text-align:center;line-height:24px}}
ol.take h3{{margin:0 0 4px;font-size:17px;font-weight:600;line-height:1.3}} ol.take p{{margin:0;color:#333;font-size:15px}}
section{{margin:0 0 34px}}
h2{{font-size:22px;font-weight:600;margin:0 0 2px;letter-spacing:-.01em}}
.sub{{font-size:13px;color:#666;margin:0 0 12px}}
.note{{font-size:13px;color:#555;margin:6px 0 0}}
.pair{{display:grid;grid-template-columns:1fr 1fr;gap:28px}} .pair h4{{margin:0 0 6px;font-size:15px;font-weight:600}}
.multi{{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}}
details{{border-top:1px solid #e2e2e2;padding:12px 0}} summary{{cursor:pointer;font-weight:600;font-size:15px}}
table{{border-collapse:collapse;font-size:13px;margin:10px 0;font-variant-numeric:tabular-nums}} th,td{{padding:4px 12px 4px 0;text-align:left;border-bottom:1px solid #eee}} td.n{{text-align:right}}
.source{{font-size:13px;color:#666;margin-top:24px}}
"""

def tile(label, value, cmp, spark, hero=False):
    return (f'<div class="tile{" hero" if hero else ""}"><div class="label">{label}</div>'
            f'<div class="value">{value}</div><div class="cmp">{cmp}</div>{spark}</div>')

def top10_table(sex, year):
    rows = "".join(f"<tr><td>{i+1}</td><td>{n}</td><td class='n'>{pct(p, 2)}</td></tr>"
                   for i, (n, p) in enumerate(top10[f"{sex}_{year}"]))
    return f"<table><thead><tr><th>#</th><th>{sex.title()}s {year}</th><th>Share</th></tr></thead><tbody>{rows}</tbody></table>"

def with_skill():
    boys_bars = hbars([(n, p, sub_label("boy", n)) for n, p in top10["boy_2008"]], new_boys, 1.25)
    girls_bars = hbars([(n, p, sub_label("girl", n)) for n, p in top10["girl_2008"]], new_girls, 1.25)
    multis = "".join(small_multiple(n, D["tracked"][n]["share"], 8.5) for n in tracked_order)
    trend = line_chart([
        dict(name="Boys", values=boy["top10"], color="#1f5fbf", start_label=f"Boys {pct(boy_top10_80, 0)}"),
        dict(name="Girls", values=girl["top10"], color="#444", start_label=f"Girls {pct(girl_top10_80, 0)}"),
    ], ymax=45, xticks=(1880, 1900, 1920, 1940, 1960, 1980, 2000), yticks=(0, 10, 20, 30, 40))
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><title>US baby names are fragmenting</title>
<meta name="viewport" content="width=device-width,initial-scale=1"><style>{CSS_SKILL}</style></head><body><main>
<h1>US baby names are fragmenting</h1>
<p class="meta">Run {run} · Social Security Administration data {Y0}–{Y1} · share of births by sex</p>
<p class="lede">In 2008 fewer than <b>one in ten</b> US babies got a top-10 name, down from one in three boys and one in four girls in 1950.
Names outside the top 1,000 now cover <b>{pct(girl_out_08, 0)} of girls</b>, so a name says less about when someone was born.</p>

<div class="tiles">
{tile("Boys given a top-10 name, 2008", pct(boy_top10_08), f"<b>{pct(boy_top10_00)}</b> in 2000 · peak <b>{pct(boy_top10_80, 0)}</b> in 1880", sparkline(boy["top10"], 200, 40), hero=True)}
{tile("Girls given a top-10 name, 2008", pct(girl_top10_08), f"<b>{pct(girl_top10_00)}</b> in 2000 · <b>{pct(girl_top10_80, 0)}</b> in 1880", sparkline(girl["top10"]))}
{tile("Girls with a name outside the top 1,000", pct(girl_out_08, 0), f"<b>{pct(girl_out_80, 0)}</b> in 1880 · boys <b>{pct(boy_out_08, 0)}</b>", sparkline([100 - v for v in girl["top1000"]]))}
{tile("Share of boys with the #1 name", pct(boy_top1_08), f"<b>{boy_top1_name_08}</b> · was {boy_top1_name_80} at <b>{pct(boy_top1_80)}</b> in 1880", sparkline(boy["top1"]))}
</div>

<ol class="take">
<li><h3>The top-10 share fell every decade since 1950</h3><p>Boys went from {pct(boy["top10"][i50], 0)} to {pct(boy_top10_08, 0)}, girls from {pct(girl["top10"][i50], 0)} to {pct(girl_top10_08, 0)}. Boys' names were always more concentrated, and the gap has now almost closed.</p></li>
<li><h3>Most of the 2008 top ten was new within a decade</h3><p>{len(new_boys)} of the top-10 boys' names and {len(new_girls)} of the girls' names were outside the top ten in 1998. {names(new_boys)} displaced {names(gone_boys)}.</p></li>
<li><h3>A #1 name today is a tenth as common as in 1880</h3><p>{boy_top1_name_80} was given to {pct(boy_top1_80)} of boys in 1880. {boy_top1_name_08}, the 2008 leader, got {pct(boy_top1_08)}. Mary peaked at {pct(peak["Mary"])}; Emma peaked at {pct(peak["Emma"])}.</p></li>
</ol>

<section>
<h2>Top-10 names covered {pct(boy_top10_80, 0)} of boys in 1880 and {pct(boy_top10_08, 0)} in 2008</h2>
<p class="sub">Share of births given one of that year's ten most common names · by sex · {Y0}–{Y1}</p>
{trend}
<p class="note">The decline is steady rather than a single break. The dip in the early 1900s reflects fewer Social Security registrations for people born then, not a change in naming.</p>
</section>

<section>
<h2>Most of the 2008 top ten was not in the top ten in 1998</h2>
<p class="sub">2008 top-10 names by share of births · blue marks names outside the 1998 top ten · shared scale</p>
<div class="pair"><div><h4>Boys</h4>{boys_bars}</div><div><h4>Girls</h4>{girls_bars}</div></div>
</section>

<section>
<h2>Names now peak lower and fade faster</h2>
<p class="sub">Share of births by sex for six #1 names · same scale on every panel · {Y0}–{Y1}</p>
<div class="multi">{multis}</div>
<p class="note">Mary held #1 for most years until 1961. Jennifer took about 15 years to rise and 15 to fall. Jacob led for a decade without ever passing {pct(peak["Jacob"])}. Emma's 2008 peak is a revival: it first peaked in 1881.</p>
</section>

<section>
<h2>How reliable is this</h2>
<p>The data counts Social Security card applications, not births. Registration was voluntary before 1937 and many people born earlier never applied, so shares before about 1920 rest on smaller counts and the early-1900s dip should not be read as a naming trend. The source lists only the top 1,000 names per sex per year, so "outside the top 1,000" is the remainder, and includes names given to fewer than five children, which SSA withholds. The series stops at 2008.</p>
</section>

<details><summary>Top-10 tables, 1950 · 1998 · 2008</summary>
<div class="pair">
<div>{top10_table("boy", 1950)}{top10_table("boy", 1998)}{top10_table("boy", 2008)}</div>
<div>{top10_table("girl", 1950)}{top10_table("girl", 1998)}{top10_table("girl", 2008)}</div>
</div></details>
<details><summary>Method</summary>
<p>Each row of the source is a name, sex, year and share of that sex's births. Top-10 share is the sum of the ten largest shares in a year. Top-1,000 share is the sum of all listed shares. Sparklines show {Y0}–{Y1}, last point marked. Charts are inline SVG generated by <code>build.py</code> from <code>data.json</code>.</p>
</details>
<p class="source">Source: SSA national baby names via hadley/data-baby-names, top 1,000 names per sex per year, {Y0}–{Y1}.</p>
</main></body></html>"""

# --- without skill ---------------------------------------------------------------

CSS_PLAIN = f"""
*{{box-sizing:border-box}} body{{margin:0;background:#f4f6f9;color:#222;font-family:{FONT};font-size:16px;line-height:1.6}}
header{{background:linear-gradient(135deg,#1e3a8a,#3b82f6);color:#fff;text-align:center;padding:40px 20px}}
header h1{{margin:0 0 8px;font-size:38px}} header p{{margin:0;opacity:.9}}
main{{max-width:1000px;margin:0 auto;padding:30px 20px 60px}}
.card{{background:#fff;border-radius:12px;box-shadow:0 2px 10px rgba(0,0,0,.08);padding:24px 28px;margin-bottom:24px}}
h2{{margin:0 0 12px;font-size:24px;color:#1e3a8a;border-bottom:2px solid #e5e7eb;padding-bottom:8px}}
.stats{{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}}
.stat{{background:#f8fafc;border-radius:10px;padding:18px;text-align:center}}
.stat .v{{font-size:32px;font-weight:700;color:#3b82f6}} .stat .l{{color:#64748b;font-size:14px}}
.charts{{display:grid;grid-template-columns:1fr 1fr;gap:24px}}
table{{width:100%;border-collapse:collapse}} th{{background:#1e3a8a;color:#fff;padding:10px;text-align:left}} td{{padding:10px;border-bottom:1px solid #e5e7eb}}
tr:nth-child(even) td{{background:#f8fafc}}
footer{{text-align:center;color:#64748b;font-size:14px;padding:20px}}
"""

def without_skill():
    six = [dict(name=n, values=D["tracked"][n]["share"], color=c) for n, c in
           zip(tracked_order, ["#4e79a7", "#f28e2b", "#e15759", "#76b7b2", "#59a14f", "#b07aa1"])]
    trend = line_chart(six, w=940, h=360, ymax=8.5, xticks=(1880, 1900, 1920, 1940, 1960, 1980, 2000),
                       yticks=(0, 2, 4, 6, 8), end_labels=False, legend=True, grid=True)
    rows = "".join(f"<tr><td>{i+1}</td><td>{b}</td><td>{pct(bp, 2)}</td><td>{g}</td><td>{pct(gp, 2)}</td></tr>"
                   for i, ((b, bp), (g, gp)) in enumerate(zip(top10["boy_2008"], top10["girl_2008"])))
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Baby Names Report</title>
<meta name="viewport" content="width=device-width,initial-scale=1"><style>{CSS_PLAIN}</style></head><body>
<header><h1>📊 US Baby Names Report</h1><p>An analysis of naming trends from {Y0} to {Y1} based on Social Security Administration data</p></header>
<main>
<div class="card"><h2>Overview</h2>
<p>This report analyzes baby name data from the United States Social Security Administration covering the period from {Y0} to {Y1}. The dataset contains the top 1,000 names for each sex in each year, along with the percentage of births that received each name. Below we explore the most popular names, how naming diversity has changed over time, and long-term trends for selected names.</p>
<div class="stats">
<div class="stat"><div class="v">{len(YEARS)}</div><div class="l">Years of data</div></div>
<div class="stat"><div class="v">{boy_top1_name_08}</div><div class="l">Top boys' name {Y1}</div></div>
<div class="stat"><div class="v">{top10["girl_2008"][0][0]}</div><div class="l">Top girls' name {Y1}</div></div>
<div class="stat"><div class="v">{pct(boy_top10_08)}</div><div class="l">Boys with a top-10 name</div></div>
</div></div>

<div class="card"><h2>Top 10 Names in {Y1}</h2>
<div class="charts">
<div><h3>Girls</h3>{pie(top10["girl_2008"])}</div>
<div><h3>Boys</h3>{vbars(top10["boy_2008"])}</div>
</div></div>

<div class="card"><h2>Trends Over Time</h2>
<p>The chart below shows the popularity of six selected names over the full period. Some names such as Mary and John were extremely popular in the late 19th and early 20th centuries, while others such as Jennifer and Michael rose to prominence in the mid-20th century. More recent names like Jacob and Emma have become popular in the 2000s.</p>
{trend}
</div>

<div class="card"><h2>Key Findings</h2>
<ul>
<li>Naming diversity has increased significantly over time.</li>
<li>Traditional names such as Mary and John have declined in popularity.</li>
<li>Boys' names have historically been more concentrated than girls' names.</li>
<li>Several new names entered the top 10 in recent years.</li>
<li>The share of births covered by the top 1,000 names has decreased.</li>
</ul></div>

<div class="card"><h2>Data Table: Top 10 Names ({Y1})</h2>
<table><thead><tr><th>Rank</th><th>Boys</th><th>Share</th><th>Girls</th><th>Share</th></tr></thead><tbody>{rows}</tbody></table>
</div>

<div class="card"><h2>Conclusion</h2>
<p>American naming practices have changed considerably over the past century. Parents today choose from a much wider range of names than their grandparents did, and the dominance of a small number of traditional names has given way to a more diverse landscape. This trend is likely to continue as cultural influences become more varied.</p>
</div>
</main>
<footer>Data source: Social Security Administration via hadley/data-baby-names · Generated {run}</footer>
</body></html>"""

if __name__ == "__main__":
    (HERE / "with-skill.html").write_text(with_skill())
    (HERE / "without-skill.html").write_text(without_skill())
    print("wrote with-skill.html, without-skill.html")
