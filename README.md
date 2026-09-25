# infographics

A Claude Code skill: page-level design principles for reports, dashboards and
infographics that busy, non-technical readers must grasp in five seconds.

Distilled from Tufte (data-ink, small multiples, sparklines), Few (single screen,
context beside every number), Knaflic (action titles, one highlight colour) and
Cairo (truthful before beautiful). Tool-agnostic: applies to HTML, slides, PDF,
Markdown, notebooks and BI dashboards.

It covers the page around the charts. For colour validation and mark specs inside
a single chart, use Claude's built-in `dataviz` skill alongside it.

## Install

As a plugin, with updates:

```
/plugin marketplace add Temikus/claude-plugins
/plugin install infographics@temikus
```

As a project skill, versioned with your repo:

```
git clone https://github.com/Temikus/claude-skill-infographics /tmp/infographics
cp -R /tmp/infographics/skills/infographics .claude/skills/
```

As a personal skill:

```
cp -R skills/infographics ~/.claude/skills/
```

## Use

Triggers on requests to make a report, dashboard or summary "scannable", "at a
glance", "for Finance", "for leadership" or infographic-like. Invoke directly with
`/infographics`.

## Layout

```
skills/infographics/
  SKILL.md                    procedure, chart-per-question table, checklist
  references/principles.md    the principles, how each was applied, sources
```

## License

Apache-2.0
