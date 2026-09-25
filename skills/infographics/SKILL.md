---
name: infographics
description: Page-level design principles for reports, dashboards, one-pagers and infographics that busy non-technical readers (Finance, execs, leadership) must grasp in five seconds. Use whenever asked to make a report, summary, dashboard, forecast write-up, metrics page, slide or document "easy to read", "scannable", "at a glance", "for Finance", "for leadership", "nicer", "more visual", or infographic-like, in any medium: HTML, slides, PDF, Markdown, notebook, BI tool. Covers reading order (lede, hero number, takeaways, action titles, collapsed detail), chart choice per question (waterfall, sorted bars, small multiples, sparklines), typography hierarchy, the one-highlight-colour rule, honesty about uncertainty, and a render-and-check pass. Complements the built-in dataviz skill, which covers colour validation and mark specs inside a single chart; this skill covers the page around the charts.
---

# Infographics

A report is read top-down, once, by someone busy. The page must give up its main
number and its main message before the reader scrolls. Everything else is support.

Distilled from Tufte (data-ink, small multiples, sparklines), Few (single screen,
context beside every number), Knaflic (action titles, preattentive attributes) and
Cairo (truthful before beautiful). Sources and detail in `references/principles.md`.
Nothing here depends on a tool. The same rules hold for HTML, slides, PDF or a BI
dashboard.

## Procedure

Do these in order. Message before layout, layout before charts, charts before colour.

1. **Write the lede first.** One or two sentences: the headline number, its
   direction, and the one caveat that changes a decision. If you cannot write it,
   you do not yet know what the page is about. Emphasise at most two numbers in it.
2. **Pick the hero.** One number, largest on the page, top-left. Give it context in
   the same block: change vs a comparison period, and a range or confidence. At most
   three supporting numbers, same layout, visibly smaller.
3. **Show "is this normal?" beside each number.** A word-sized trend of the last
   two years, last point marked, no axes. Tufte's sparkline. It replaces a chart the
   reader would otherwise have to find.
4. **Three takeaways, numbered.** Headline on its own line, one or two plain
   sentences under it. Each carries a number. Nothing that is not in the data.
5. **Title every section with its finding, not its topic.** "Hosting cost grew
   12% a year", not "Cost over time". Topic, period and units go in a smaller
   subtitle. A reader who only reads headings should get the whole story.
6. **One chart per question.** Match the question to the form (table below). Two
   things that must be compared share one scale side by side, never one big chart
   and one hidden chart.
7. **Label directly, drop the legend.** Series name and end value at the line end.
   One highlight colour for the thing that matters, greys for context, black for
   actuals. Validate new categorical colours with the dataviz skill; grey may fail
   its chroma check when it is meant to read as background.
8. **One type scale, two weights.** Pick about six sizes and use only those.
   Regular and one bold. Labels above numbers take a fixed height so values align
   across blocks. Charts use the page font.
9. **Collapse what a decision does not need.** Method, backtests, monthly tables,
   reconciliation tables, secondary charts go below the fold or behind a toggle.
   The above-the-fold view fits one screen.
10. **State reliability plainly.** One sentence: how it was tested, typical miss,
    worst miss, and what caused the worst miss. A range that is wide on purpose gets
    a one-line explanation beside the chart, not a footnote.
11. **Render and look.** View the output as the reader will, at their screen size.
    Check the list under "Before shipping". Fix, re-render, look again.

## Chart per question

| Question | Form | Notes |
|---|---|---|
| How did the total become this number? | Waterfall | Start and end in highlight colour, steps grey, value on every bar, axis hidden |
| Which parts are big? | Horizontal bars, sorted, labelled | Top one or two in highlight colour, rest grey. Put the pattern or date in the label text |
| Trend plus forecast | Line with shaded range | Actuals black, forecast highlight, cross-check dotted grey, divider where actuals end |
| Two scenarios | Small multiples, shared scale | Same axes, same size, side by side |
| Is this normal? | Sparkline inside the number block | No axes, last point marked |
| One number | Stat block | Not a one-bar chart, not a two-slice pie |
| Composition over time | Stacked area with event markers | Only when the stack itself is the story; otherwise the waterfall |

## Numbers

- Short form in charts and headlines: `$1.2k`, `$3.4M`. Exact figures only in detail tables.
- Round to what changes a decision. Percentages to whole numbers.
- Every number carries its comparison: vs prior period, range, share of total.
- Negative growth reads badly as "rose -1%". Write "moved -1%" or "was flat".
- Indicative totals that mix forecast and contract run-rates are labelled indicative,
  with the composition spelled out.

## Before shipping

Look at a rendered screenshot, then hover or interact once, and check:

- Values in number blocks align horizontally. Labels wrap to the same line count.
- No label sits on top of a line. End labels are not clipped at the edge.
- Series drawn as lines are lines, not chains of markers.
- Paired panels share the same scale and the same width.
- Tooltips or callouts are opaque and readable over the chart.
- One font family throughout, including inside charts.
- Headings state findings. Read only the headings: does the story hold?
- The lede, hero, takeaways and first chart fit one screen at a typical laptop width.
- The reliability sentence and the range explanation are present and honest.

## Skeleton

```
Title
  run date · data through · units
Lede: one or two sentences, the answer
Hero block + three supporting blocks, each with sparkline and comparison
Three numbered takeaways
Finding as heading            (topic · period · units)
  chart
  one-line note on the range
Finding as heading
  table or chart
...
How reliable is this          one paragraph
Collapsed: secondary charts, tables, method
Source line
```
