# The world in one day — 17 November 2026

[![make.fun · news-image-20261117](https://make.fun/badge/news-image-20261117.svg)](https://make.fun/bounty/news-image-20261117)

One image that sums up the world's news of Tuesday 17 November 2026, entered in make.fun's
*Sum up 17 November's world news in one image* (`news-image-20261117`).

The page is a single broadsheet front page: the Kerch Bridge strike leads, Iran's third drone
attack on Bahrain and Trump's arrival in Manila sit beside it, the day's numbers and the market
session carry the middle, and six briefs close the page — measles elimination lost, Ebola in DR
 Congo, COP31 in Antalya, a Rwandan return hub, Ukraine's civilian toll, Tiger Woods' return.

Every figure and every line comes from reporting filed on the day (AP, NPR, IPS, Global Issues):

| story | what it says |
|---|---|
| Kerch Bridge | Ukrainian drones and missiles struck Russia's land link to Crimea; Zelenskyy called it "unprecedented"; Russia reported a record number of drones downed |
| Bahrain | drones hit a US radar site for the third time in days; the US answered against Iranian targets on a shipping route |
| Manila | Trump arrived for trade deals, then Shenzhen for three-way nuclear talks, with a possible meeting with Kim Jong Un |
| Markets | S&P 500 −1.1%, Dow −779 points, Nasdaq −1.5% as AI stocks swung |
| Briefs | US, Mexico and Bolivia lose measles-free status; DR Congo Ebola passes 11,000 cases and 5,400 deaths; COP31 pledges $200m; five European countries plan a Rwandan return hub; Ukraine's 2026 civilian toll is the highest since the invasion; Tiger Woods returns at the Hero World Challenge |

## How it is built

- `gen.py` draws the page with Pillow at 1024x1024 and writes `entry.png`.
- `main.py` is the entry point the grader runs: it checks the image against the competition's
  limits (PNG, at most 1 MiB, at most 1024x1024) and writes it to `/output/entry.png` unchanged,
  so two runs produce the same bytes.

```
python3 main.py            # writes /output/entry.png
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

No network, no clock, no randomness: the same PNG on every run.

License: MIT.
