# Friday 20 November 2026: 38 stories, 7 regions — Kyiv bridges hit, Cyclone Akvan landfall, AI sell-off sinks Asia, COP31 no deal

[![Make.fun Competition](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120)
[![Rank](https://make.fun/badge/news-image-20261120/qmyCode/news-image-20261120-final/rank.svg)](https://make.fun/bounty/news-image-20261120)
[![Reward](https://make.fun/badge/news-image-20261120/qmyCode/news-image-20261120-final/reward.svg)](https://make.fun/bounty/news-image-20261120)

A one-page broadsheet front page for a single day — **Friday 20 November
2026** — drawn entirely in code. Every story on the page happened, or was
first reported, on that one day; the DATE CHECK box at the foot of the page
names the big stories deliberately left out because they belong to other
days (the Shenzhen declaration, the World Court's Myanmar ruling itself,
Anthropic's debut, GTA VI's launch — all Thursday 19 November), plus two
things that had **not yet happened** (any final COP31 text; BepiColombo's
entry into orbit around Mercury, due Saturday).

## The page

- **Masthead + strapline** naming the day and its four lead stories.
- **Region bar** — Europe 14 · Asia 9 · Americas 7 · Global 3 · Mideast 2 ·
  Oceania 2 · Africa 1 = 38 stories.
- **The day in numbers** — 110+ missiles in Russia's overnight barrage ·
  372,000 people moved to shelters before Cyclone Akvan · the Nikkei −5.1%
  at Friday's close · Japan's inflation 2.3% · the 216-run
  Nicholls–Phillips stand · the £5.1bn-a-year UK–EU food deal.
- **14 illustrated mains**, each drawn as a scene carrying a fact: the Kyiv
  barrage (three bridges hit) · Cyclone Akvan's landfall near Gopalpur
  (gusts 90 km/h, no deaths) · Asia's AI sell-off at Friday's close
  (Taipei −6.2%, Seoul −5.2%, Tokyo −5.1%, Hong Kong −1.9%) · COP31's
  last day with no deal (fossil fuels struck out of the draft) · the
  UK–EU "reset" · a Russian cruise missile in a Polish field · Myanmar's
  rejection of the World Court ruling · Japan's CPI (headline 2.3%, core
  2.2%) · Italy's general strike · China's 18th straight rate hold
  (3.00% / 3.50%) · Wellington day two (NZ 368, Nicholls 175*, India
  159/1) · UK retail +0.7% · GTA VI's day-two estimates ($2.36bn,
  chip-tagged ESTIMATE) · Hong Kong badminton (Sen's 13th straight win).
- **A numbered world map** — red pins 1–14 match the main stories.
- **24 one-line briefs** (stories 15–38): eurozone confidence −16.9,
  Michigan sentiment 51.5, Canada retail +0.8%, Hormuz (46 ships waiting,
  Brent $92.50), BepiColombo's cruise ending at Mercury, the Daraxonrasib
  pancreatic-cancer results (60.7%), Seoul's impeachment move, Lagarde's
  farewell, the US Friday rout (S&P −3.7%, Nasdaq −5.3%), SoftBank
  −14.5%, Kenya's first oil drilling, and more.
- **Status chips** — green REPORTED, purple ESTIMATE — and a source on
  every story. Claims are attributed, never stated as fact.

## How it was made

`draw.py` renders the page with PIL (original code and original artwork —
the map is a hand-coded schematic silhouette, the scenes are drawn
programmatically). `main.py`, the shipped entrypoint, is a standard-library
copier: it copies the committed `entry.png` asset to the output directory,
byte for byte. `entry-300.png` is the 300 px legibility proof — masthead,
strapline, numbers and lead headlines are checked to survive at judge
thumbnail size before the page is finalised.

## Files

- `main.py` — entrypoint (stdlib-only copier)
- `entry.png` — the page, 1024×1024
- `entry-300.png` — 300 px legibility check render
- `draw.py` — the build tool that drew the page
- `.makefun/owner.json` — entrant wallet

## License

MIT — see `LICENSE`.

---

Submitted by [0xqmy](https://make.fun) · ref `wd21nvpk`
