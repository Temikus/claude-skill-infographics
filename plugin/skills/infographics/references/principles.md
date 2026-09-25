# Principles and where they come from

## Tufte, The Visual Display of Quantitative Information; Envisioning Information; Beautiful Evidence

- **Data-ink ratio.** Ink that does not carry data is noise. Erase non-data ink, then erase redundant data ink. Applied: no legend when lines can be labelled at their ends, no chart border, grid faint or gone, axis hidden on a waterfall where every bar carries its value.
- **Chartjunk.** Decoration, 3D, gradients, heavy frames. Applied: tiles have one hairline border, charts have none inside the tile.
- **Small multiples.** Same design repeated across slices, same scale, side by side. The eye compares without re-learning the axes. Applied: two scenarios on one shared y axis.
- **Sparklines.** Word-sized graphics inside text or tiles. "Is this normal?" answered in the space of a word. Applied: 24-period sparkline under every hero value.
- **Graphical integrity.** Representation proportional to the numbers, labelled clearly, show data variation not design variation. Applied: same scale on paired panels, bars start at zero, ranges shown as ranges.

Sources: https://jtr13.github.io/cc19/tuftes-principles-of-data-ink.html, https://chartbuddy.io/blog/tuftes-principles-for-graphical-integrity, https://thedoublethink.com/tuftes-principles-for-visualizing-quantitative-information/

## Few, Information Dashboard Design

- A dashboard is what must be monitored to achieve an objective, on a single screen, at a glance. Applied: hero, takeaways, main chart fit one screen; the rest collapses.
- Context beside every number. A number without a comparison is not information. Applied: every tile shows change vs a period, a range, or a composition.
- Preattentive attributes (size, position, colour intensity) carry hierarchy. Applied: one hero at 40 px, three at 28 px, one highlight colour.
- The 13 mistakes worth remembering here: exceeding one screen, inadequate context, excessive detail, wrong chart type, meaningless variety, arranging data poorly, misusing colour, cluttering with decoration.

Sources: https://www.uxmatters.com/mt/archives/2007/04/book-review-information-dashboard-design.php, https://www.perceptualedge.com/library.php

## Knaflic, Storytelling with Data

- Know the audience and what decision they make. Applied: the lede names the decision-relevant number.
- Action titles. The title states the takeaway; the chart proves it. Applied: every h2 is a finding.
- Declutter, then focus attention with one colour. Grey is the default; colour marks the one thing to look at. Applied: black actuals, blue forecast, grey cross-check; top two bars blue, rest grey.
- Text is part of the chart. Annotate directly. Applied: end labels, divider label, note beside the chart.

Sources: https://medium.com/analytics-vidhya/key-points-from-the-book-storytelling-with-data-by-cole-nussbaumer-knaflic-8c0a7b08960, https://readingraphics.com/book-summary-storytelling-with-data/

## Cairo, The Truthful Art

- Truthful, functional, beautiful, insightful, enlightening, in that order. Applied: state the range and the worst miss up front; do not hide the ugly number.

Source: https://www.oreilly.com/library/view/the-truthful-art/9780133440492/

## Infographic and dashboard practice

- Five-second test: a reader must get the key message in five seconds. Applied: the lede.
- Inverted pyramid: most important top-left, detail down the page.
- Round numbers, one message per block, consistent styling.

Sources: https://venngage.com/blog/infographic-design/, https://visme.co/blog/infographic-layout/, https://www.przntperfect.com/post/infographic-design-for-executives, https://blog.bismart.com/en/data-storytelling-cuadros-de-mando, https://www.uxpin.com/studio/blog/dashboard-design-principles/, https://metapraxis.com/blog/financial-kpis-dashboards-for-the-board
