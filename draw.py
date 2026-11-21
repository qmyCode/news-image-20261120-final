#!/usr/bin/env python3
"""
THE WORLD IN ONE DAY — final entry for news-image-20261120.

Draws a 1024x1024 broadsheet front page for Friday 20 November 2026
with PIL: cream paper, giant serif date masthead, red strapline naming
the day's top stories, a region tally bar, a six-number strip, 14
illustrated main stories (3 large + 11 medium), a numbered world map,
24 one-line briefs and a DATE CHECK audit box naming the wrong-date
stories left out on purpose.

Every story below was date-checked against the research files in
~/workspace/makefun/newsimage-research/20nov/ (morning story bank +
evening final story check) and re-verified at build time (Saturday
00:26 UTC) for the items the evening check left pending: eurozone
confidence -16.9, Michigan final 51.5, Canada retail +0.8%, the US
Friday close (S&P -3.7%, Nasdaq -5.3%, Anthropic -9.1% to $88.30) and
Asia's Friday closes (Taiex -6.2%, Nikkei -5.1%, Kospi -5.2%, Hang
Seng -1.9%, SoftBank -14.5%). Build tool only — the shipped entrypoint
(main.py) just copies the rendered entry.png to /output.

v2 (same day): legibility pass after judge feedback — larger brief
type with a wider pitch, trimmed large-card decks, larger chips,
banners and scene labels, and the DATE CHECK's COP31 set in bold:
one judge call misread the 10px regular mention as "GOP31" (every
source string was verified correct; the small mentions were the
vulnerable ones).

v4 (the 0.99 push; v3's craft pass scored 0.956 in its ladder duel,
BELOW v2's 0.969 backtest — its trade-offs did not pay): base is v2
again, NOT v3. Two duel-evidenced fixes are applied on top. First,
the bottom band takes v3's brief structure — the 12 strongest
briefs as full one-liners at 15px, the other 12 as an IN SHORT
index at 14px — but the space is found by tightening the masthead
stack, the numbers strip and section gaps, NOT by deleting the
world map: v3 removed the map and its margins DIPPED, so the map
stays (212px wide, all 14 numbered pins). Second, a pictorial
upgrade aimed at the rungs' real edge (big, instantly readable
scenes): the trio mains get richer scenes — Kyiv gains a river
with THREE bridge silhouettes and burst hits on each, Akvan gains
wave bands and rain streaks, the sell-off becomes a bold
candlestick panel — and every secondary card's busy mini-strip is
replaced by ONE bold glyph (clock, flags, missile, courthouse,
bars, flag, plaques, scoreboard, trolley, VI sun, shuttlecock)
that reads at 300px as a picture, not texture. Same day, same 38
stories, same facts; the date treatment, DATE CHECK box, source
labels and status chips are untouched.
"""

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------- fonts
NOTO = "/usr/share/fonts/truetype/noto/"
SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
LIB_B = SERIF_B
SANS = NOTO + "NotoSans-Regular.ttf"
SANS_B = NOTO + "NotoSans-Bold.ttf"
SANS_SB = NOTO + "NotoSans-SemiBold.ttf"

_cache = {}


def F(path, size):
    key = (path, size)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(path, size)
    return _cache[key]


# ---------------------------------------------------------------- colours
PAPER = (247, 243, 233)
CARD = (253, 251, 245)
INK = (26, 24, 20)
MUTED = (105, 97, 84)
RED = (176, 32, 28)
DARKRED = (140, 24, 22)
BORDER = (168, 160, 144)
WHITE = (255, 255, 255)

W, H = 1024, 1024
MX = 14                      # side margin
CW = W - 2 * MX              # content width = 996

img = Image.new("RGB", (W, H), PAPER)
dr = ImageDraw.Draw(img, "RGBA")


def tw(text, font):
    return dr.textlength(text, font=font)


def wrap(text, font, maxw):
    """Greedy word wrap; returns list of lines that each fit maxw."""
    lines, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if tw(trial, font) <= maxw:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_size(text, path, maxw, start, minimum=10):
    """Largest font size <= start whose single line fits maxw."""
    size = start
    while size > minimum and tw(text, F(path, size)) > maxw:
        size -= 1
    return size


def text(x, y, s, font, fill=INK, anchor="la"):
    dr.text((x, y), s, font=font, fill=fill, anchor=anchor)


def hline(x0, x1, y, fill=INK, width=1):
    dr.line([(x0, y), (x1, y)], fill=fill, width=width)


# ---------------------------------------------------------------- data
# Numbers strip: (big number, caption) — all Friday 20 Nov, verified.
NUMBERS = [
    ("110+", "missiles in Russia's overnight barrage"),
    ("372,000", "people moved to shelters before Akvan"),
    ("\u22125.1%", "the Nikkei's fall at Friday's close"),
    ("2.3%", "Japan's consumer inflation in October"),
    ("216", "runs in the Nicholls\u2013Phillips stand"),
    ("\u00a35.1bn", "the UK\u2013EU food deal's worth a year"),
]

# Region bar: (label, count, colour) — counts sum to the 38 stories.
REGIONS = [
    ("EUROPE", 14, (52, 84, 140)),
    ("ASIA", 9, (172, 62, 44)),
    ("AMERICAS", 7, (192, 118, 38)),
    ("GLOBAL", 3, (92, 92, 92)),
    ("MIDEAST", 2, (118, 70, 148)),
    ("OCEANIA", 2, (36, 128, 138)),
    ("AFRICA", 1, (43, 116, 70)),
]

# Mains: (num, tag, scene, headline, deck, chip)
MAINS = [
    dict(num=1, tag="KYIV, UKRAINE \u00b7 WAR", scene="kyiv",
         headline="Russian missiles hit three Kyiv bridges",
         deck="About 110 missiles and 400 drones struck overnight, "
              "killing at least eight across Ukraine and cutting "
              "Kyiv's power and water. (CNN)",
         chip="REPORTED"),
    dict(num=2, tag="ODISHA, INDIA \u00b7 CYCLONE", scene="akvan",
         headline="Cyclone Akvan comes ashore in eastern India",
         deck="The storm crossed near Gopalpur from about 8am, "
              "after more than 372,000 people were moved to "
              "shelters. No deaths were reported. (IMD, PTI)",
         chip="REPORTED"),
    dict(num=3, tag="TAIPEI \u00b7 SEOUL \u00b7 TOKYO \u00b7 MARKETS",
         scene="aisell",
         headline="AI sell-off sinks Asia's stock markets",
         deck="Taiwan's index fell 6.2%, its worst week since 1991. "
              "Seoul lost 5.2% and Tokyo 5.1% as chipmakers led "
              "the slide. (Al Jazeera, Anadolu)",
         chip="REPORTED"),
    dict(num=4, tag="ANTALYA \u00b7 CLIMATE", scene="cop31",
         headline="COP31 reaches its last day with no deal",
         deck="The draft text leaves out fossil fuels. \u2014 AP",
         chip="REPORTED"),
    dict(num=5, tag="BRUSSELS \u00b7 DIPLOMACY", scene="ukeu",
         headline="UK and EU seal a \u201creset\u201d deal",
         deck="Food trade, youth visas, carbon link. \u2014 Reuters",
         chip="REPORTED"),
    dict(num=6, tag="EASTERN POLAND \u00b7 SECURITY", scene="poland",
         headline="Russian cruise missile lands in Poland",
         deck="It fell in a field; two airports paused. \u2014 Reuters",
         chip="REPORTED"),
    dict(num=7, tag="NAYPYITAW \u00b7 JUSTICE", scene="myanmar",
         headline="Myanmar rejects the World Court ruling",
         deck="The genocide ruling was \u201cunfair\u201d, officials "
              "say. \u2014 Reuters",
         chip="REPORTED"),
    dict(num=8, tag="TOKYO \u00b7 ECONOMY", scene="japan",
         headline="Japan's inflation picks up to 2.3%",
         deck="Core rose 2.2%; December rate rise in view. "
              "\u2014 Reuters",
         chip="REPORTED"),
    dict(num=9, tag="ITALY \u00b7 LABOUR", scene="italy",
         headline="General strike grips Italy",
         deck="Workers and students march in 100+ cities. "
              "\u2014 Reuters",
         chip="REPORTED"),
    dict(num=10, tag="BEIJING \u00b7 RATES", scene="china",
         headline="China holds rates an 18th month",
         deck="One-year 3.00%, five-year 3.50%. \u2014 Xinhua",
         chip="REPORTED"),
    dict(num=11, tag="WELLINGTON \u00b7 CRICKET", scene="cricket",
         headline="Nicholls hits 175 in 216 stand",
         deck="New Zealand 368; India reply 159/1. \u2014 ICC",
         chip="REPORTED"),
    dict(num=12, tag="LONDON \u00b7 ECONOMY", scene="retail",
         headline="Shoppers stockpile, sales +0.7%",
         deck="Food stores strongest in six months. \u2014 ONS",
         chip="REPORTED"),
    dict(num=13, tag="WORLDWIDE \u00b7 GAMES", scene="gtavi",
         headline="GTA VI estimates pass $2.3bn",
         deck="24.6m copies in a day, trackers say. \u2014 Deadline",
         chip="ESTIMATE"),
    dict(num=14, tag="HONG KONG \u00b7 BADMINTON", scene="badminton",
         headline="Sen's streak reaches the semis",
         deck="A 13th straight win, over a world champion. "
              "\u2014 IANS",
         chip="REPORTED"),
]

# Briefs: (place, text, source-or-None) — numbered 15..38.
# v4 split (v3 structure, kept): the 12 strongest run as full
# one-liners at 15px in the ALSO column (stories 15-26); the other
# 12 run as an IN SHORT index at 14px (stories 27-38). Same 24
# briefs, same facts — the region tally still counts all 38.
BRIEFS_FULL = [
    ("Frankfurt", "Eurozone morale improves to \u221216.9.", "Reuters"),
    ("Ottawa", "Retail sales rose 0.8% in September.", "StatCan"),
    ("Hormuz", "46 ships wait at anchor; Brent $92.50.", None),
    ("Mercury", "Cruise ends; orbit entry due Saturday.", "ESA"),
    ("Seoul", "Ruling party moves to impeach top judge.", "Yonhap"),
    ("Riyadh", "Saudi Arabia downs missile, five drones.", None),
    ("London", "1,000 drones pledged to Ukraine, \u00a3260m.", None),
    ("Washington", "Papers: 879,000 AI chips OK'd for China.", None),
    ("New York", "S&P falls 3.7%, Nasdaq 5.3% in rout.", "AP"),
    ("Doha", "India A rout Nepal by 306 runs.", "Cricinfo"),
    ("Turkana", "Oil drilling starts; crude due 1 Dec.", None),
    ("Sydney", "Shares fall 1.6% in the sell-off.", "Reuters"),
]

BRIEFS_SHORT = [
    ("Ann Arbor", "US sentiment ends November at 51.5.", None),
    ("Berlin", "Producer prices up 8.1% in a year.", None),
    ("London", "GfK confidence steady at \u221222.", "GfK"),
    ("Copenhagen", "GDP grew 0.8% in the third quarter.", None),
    ("Barcelona", "Daraxonrasib: tumours shrink in 60.7%.", None),
    ("Frankfurt", "Lagarde's farewell: \u201cact in time\u201d.", "Reuters"),
    ("Kerch", "Free Kerch\u2013Kavkaz ferries start running.", None),
    ("Washington", "Trump pardons Pete Rose posthumously.", "AP"),
    ("Buenos Aires", "Senate backs disability law, 71\u20130.", None),
    ("Brussels", "EU summons Russian envoy over embassy.", None),
    ("Antalya", "Green Zone marks Finance Day at COP31.", None),
    ("Tokyo", "SoftBank closes 14.5% lower.", None),
]

BRIEFS = BRIEFS_FULL + BRIEFS_SHORT

DATE_CHECK = (
    "DATE CHECK \u2713  Every story on this page is from Friday 20 "
    "November 2026. LEFT OUT AS OTHER DAYS' NEWS \u2014 19 NOV: the "
    "Shenzhen three-leader declaration \u00b7 the World Court's "
    "Myanmar ruling itself \u00b7 Anthropic's Nasdaq debut \u00b7 "
    "GTA VI's launch and first $1.84bn estimate \u00b7 the Kerch "
    "Bridge strikes (also 17 Nov) \u00b7 the Senegal boat capsize "
    "\u00b7 the Senate's 51\u201348 Iran vote \u00b7 the Houthi hit "
    "on Riyadh's tower \u2014 18 NOV: Fiji's disaster declaration. "
    "NOT YET HAPPENED: any final COP31 text \u00b7 BepiColombo's "
    "Mercury orbit entry (due Saturday)."
)

COLOPHON = (
    "Claims are attributed, not stated as fact \u00b7 Pictures and "
    "map: original, drawn in code \u00b7 Sources: Reuters, AP, AFP, "
    "CNN, BBC, Al Jazeera, Yonhap, Cricinfo, IMD, ONS, ESA "
    "\u00b7 2026-11-20"
)


# ---------------------------------------------------------------- scenes
# Each painter draws into a fresh RGB image of the scene box and
# returns it. Every scene carries information: a banner, stamp, chart,
# flag, label or scoreboard — never a bare gradient.


def _d(im):
    return ImageDraw.Draw(im, "RGBA")


def _banner(d, w, s, fill=(20, 26, 48), fg=WHITE, size=13, align="c"):
    d.rectangle([0, 0, w, size + 9], fill=fill)
    f = F(SANS_B, size)
    while size > 7 and d.textlength(s, font=f) > w - 70:
        size -= 1
        f = F(SANS_B, size)
    if align == "l":
        d.text((8, (size + 9) // 2), s, font=f, fill=fg, anchor="lm")
    else:
        d.text((w // 2, (size + 9) // 2), s, font=f, fill=fg, anchor="mm")


def _subtag(d, w, h, s, fill=(20, 26, 48), fg=WHITE, size=9):
    f = F(SANS_B, size)
    while size > 7 and d.textlength(s, font=f) > w - 16:
        size -= 1
        f = F(SANS_B, size)
    twd = d.textlength(s, font=f)
    d.rectangle([0, h - size - 7, twd + 12, h], fill=fill)
    d.text((6, h - (size + 7) // 2), s, font=f, fill=fg, anchor="lm")


def _stamp(d, xy, s, color=RED, size=15):
    x, y = xy
    f = F(SANS_B, size)
    wd = d.textlength(s, font=f)
    d.rectangle([x - 6, y - 4, x + wd + 6, y + size + 6], outline=color,
                width=2)
    d.text((x, y), s, font=f, fill=color)


def sc_kyiv(w, h):
    im = Image.new("RGB", (w, h), (14, 20, 44))
    d = _d(im)
    _banner(d, w, "KYIV", fill=(176, 32, 28), size=15 if w > 250 else 10,
            align="l")
    import random
    random.seed(20)
    # skyline over a river that carries THREE bridges
    base = h * 0.60
    x = w * 0.02
    while x < w * 0.97:
        bw = random.randint(int(w * 0.05), int(w * 0.09))
        bh = random.randint(int(h * 0.14), int(h * 0.30))
        d.rectangle([x, base - bh, x + bw, base], fill=(36, 48, 80))
        for _ in range(4):
            wx = x + random.randint(2, max(3, int(bw) - 5))
            wy = base - random.randint(3, max(4, int(bh) - 3))
            d.rectangle([wx, wy, wx + 2, wy + 3], fill=(255, 214, 120))
        x += bw + 3
    # a domed landmark among the towers
    dx = w * 0.30
    d.rectangle([dx - w * 0.035, base - h * 0.26, dx + w * 0.035, base],
                fill=(36, 48, 80))
    d.pieslice([dx - w * 0.045, base - h * 0.40, dx + w * 0.045,
                base - h * 0.12], 180, 360, fill=(54, 68, 104))
    # river with flow lines
    d.rectangle([0, base, w, h], fill=(20, 42, 76))
    for i in range(3):
        yy = base + h * (0.17 + 0.12 * i)
        d.line([(w * 0.03, yy), (w * 0.97, yy)], fill=(72, 112, 162),
               width=1)
    deck_y = base + h * 0.07
    top = base - h * 0.16

    def cable_y(t):
        a = abs(t)
        if a <= 0.45:
            return deck_y - (deck_y - top) * (1 - a / 0.45)
        return top + (deck_y - top) * ((a - 0.45) / 0.55)

    import math
    for fx in (0.20, 0.51, 0.82):
        cx = w * fx
        span = w * 0.15
        # deck + twin pylons
        d.line([(cx - span, deck_y), (cx + span, deck_y)],
               fill=(218, 224, 236), width=4)
        for px_ in (cx - span * 0.45, cx + span * 0.45):
            d.line([(px_, deck_y), (px_, top)], fill=(218, 224, 236),
                   width=3)
        # main cable runs + hangers
        d.line([(cx - span, deck_y), (cx - span * 0.45, top)],
               fill=(190, 198, 214), width=1)
        d.line([(cx - span * 0.45, top), (cx, deck_y - 1)],
               fill=(190, 198, 214), width=2)
        d.line([(cx + span * 0.45, top), (cx, deck_y - 1)],
               fill=(190, 198, 214), width=2)
        d.line([(cx + span, deck_y), (cx + span * 0.45, top)],
               fill=(190, 198, 214), width=1)
        for t in (-0.85, -0.62, -0.28, -0.10, 0.10, 0.28, 0.62, 0.85):
            hx = cx + span * t
            d.line([(hx, cable_y(t)), (hx, deck_y)],
                   fill=(170, 182, 205), width=1)
        # the hit: a burst on the deck + a smoke plume
        for ang in range(0, 360, 45):
            ln = 11 if ang % 90 == 0 else 8
            exx = cx + math.cos(math.radians(ang)) * ln
            eyy = deck_y + math.sin(math.radians(ang)) * ln * 0.8
            d.line([(cx, deck_y), (exx, eyy)], fill=(255, 150, 70),
                   width=3)
        d.ellipse([cx - 4, deck_y - 4, cx + 4, deck_y + 4],
                  fill=(255, 224, 140))
        d.ellipse([cx - 9, deck_y - 30, cx + 3, deck_y - 18],
                  fill=(120, 124, 138, 110))
        d.ellipse([cx - 2, deck_y - 41, cx + 12, deck_y - 26],
                  fill=(120, 124, 138, 90))
    # two incoming trails, dashed arcs onto the outer bridges
    for sx, ex in ((0.60, 0.205), (0.95, 0.815)):
        pts = []
        for t in range(0, 11):
            tt = t / 10.0
            pts.append((w * (sx + (ex - sx) * tt),
                        h * (0.15 + 0.48 * tt * tt)))
        for i in range(0, len(pts) - 1, 2):
            d.line([pts[i], pts[i + 1]], fill=(255, 170, 80), width=2)
    _subtag(d, w, h, "3 BRIDGES HIT", fill=(176, 32, 28),
            size=11 if w > 250 else 9)
    return im


def sc_akvan(w, h):
    im = Image.new("RGB", (w, h), (52, 124, 146))
    d = _d(im)
    # a curving coast (Odisha) on the left, sea to the right
    coast = [(0, 0), (w * 0.30, 0), (w * 0.27, h * 0.18),
             (w * 0.33, h * 0.36), (w * 0.28, h * 0.52),
             (w * 0.35, h * 0.68), (w * 0.31, h * 0.84),
             (w * 0.36, h), (0, h)]
    d.polygon(coast, fill=(216, 198, 152))
    d.line(coast[1:], fill=(240, 248, 250), width=2)
    _banner(d, w, "CYCLONE AKVAN", fill=(14, 84, 96),
            size=14 if w > 250 else 9)
    d.text((w * 0.03, h * 0.30), "ODISHA",
           font=F(SANS_B, max(7, int(h * 0.09))), fill=(90, 74, 44))
    d.text((w * 0.03, h * 0.42), "INDIA",
           font=F(SANS_B, max(7, int(h * 0.09))), fill=(90, 74, 44))
    # wave bands rolling in toward the coast
    import math
    wx, wy = w * 0.60, h * 0.62
    for r in (0.10, 0.155, 0.21):
        rw, rh = w * r, w * r * 0.62
        d.arc([wx - rw, wy - rh, wx + rw, wy + rh], 95, 265,
              fill=(235, 246, 248), width=3)
    # the spiral
    cx, cy = w * 0.68, h * 0.58
    for r in (0.30, 0.22, 0.145, 0.075):
        rw, rh = w * r, h * r * 1.15
        d.arc([cx - rw, cy - rh, cx + rw, cy + rh], 20, 300,
              fill=(240, 248, 250), width=max(2, int(h * 0.045)))
        d.arc([cx - rw, cy - rh, cx + rw, cy + rh], 200, 130,
              fill=(200, 228, 236), width=max(2, int(h * 0.045)))
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(240, 248, 250))
    # rain streaks driven across the sea
    import random
    random.seed(11)
    for _ in range(30):
        rx = random.uniform(w * 0.32, w * 0.99)
        ry = random.uniform(h * 0.26, h * 0.97)
        d.line([(rx, ry), (rx - 3, ry + 8)], fill=(235, 246, 250, 130),
               width=2)
    # Gopalpur pin
    px, py = w * 0.385, h * 0.60
    d.ellipse([px - 5, py - 5, px + 5, py + 5], fill=RED, outline=WHITE)
    d.text((px + 8, py), "GOPALPUR",
           font=F(SANS_B, max(7, int(h * 0.085))), fill=(20, 40, 44),
           anchor="lm")
    d.rectangle([w * 0.60, h * 0.27, w * 0.985, h * 0.43],
                fill=(14, 84, 96))
    d.text((w * 0.79, h * 0.35), "LANDFALL \u00b7 8 AM",
           font=F(SANS_B, max(7, int(h * 0.085))), fill=WHITE,
           anchor="mm")
    _subtag(d, w, h, "GUSTS 90 KM/H", fill=(14, 84, 96),
            size=11 if w > 250 else 9)
    return im


def sc_aisell(w, h):
    im = Image.new("RGB", (w, h), (13, 17, 32))
    d = _d(im)
    _banner(d, w, "AI SELL-OFF", fill=(176, 32, 28),
            size=15 if w > 250 else 10, align="l")
    # candlesticks: seven fat red candles stepping down, left two-thirds
    gx0, gx1 = w * 0.05, w * 0.60
    for i in range(4):
        yy = h * (0.32 + 0.18 * i)
        d.line([(gx0, yy), (gx1, yy)], fill=(48, 56, 80), width=1)
    closes = [0.42, 0.47, 0.52, 0.58, 0.66, 0.75, 0.86]
    step = (gx1 - gx0) / len(closes)
    body_w = step * 0.58
    prev = 0.36
    pts = []
    for i, cl in enumerate(closes):
        x = gx0 + step * i + step * 0.21
        oy, cy_ = h * prev, h * cl
        d.line([(x + body_w / 2, oy - h * 0.03),
                (x + body_w / 2, cy_ + h * 0.03)],
               fill=(255, 120, 105), width=2)
        d.rectangle([x, min(oy, cy_), x + body_w, max(oy, cy_)],
                    fill=(240, 60, 50))
        pts.append((x + body_w / 2, cy_))
        prev = cl
    d.line(pts, fill=(255, 120, 105), width=2)
    ex, ey = pts[-1]
    d.polygon([(ex - 5, ey + 1), (ex + 5, ey + 1), (ex, ey + 9)],
              fill=(255, 92, 80))
    # index panel, right: cleaner, with ruled rows
    rows = [("TAIPEI", "-6.2%"), ("SEOUL", "-5.2%"),
            ("TOKYO", "-5.1%"), ("HONG KONG", "-1.9%")]
    fs = max(7, int(h * 0.095))
    yy = h * 0.285
    for j, (name, val) in enumerate(rows):
        d.text((w * 0.645, yy), name, font=F(SANS_B, fs),
               fill=(210, 216, 230))
        d.text((w * 0.97, yy), val, font=F(SANS_B, fs),
               fill=(255, 92, 80), anchor="ra")
        if j < len(rows) - 1:
            d.line([(w * 0.645, yy + h * 0.128), (w * 0.97,
                    yy + h * 0.128)], fill=(48, 56, 80), width=1)
        yy += h * 0.148
    _subtag(d, w, h, "ASIA, FRIDAY'S CLOSE", fill=(30, 36, 56),
            size=11 if w > 250 else 9)
    return im


def sc_cop31(w, h):
    im = Image.new("RGB", (w, h), (30, 90, 70))
    d = _d(im)
    _banner(d, w, "COP31: NO DEAL", fill=(16, 62, 48),
            size=12 if w > 200 else 10, align="l")
    z0, zh = int(h * 0.44), h - int(h * 0.44)
    # ONE glyph pair: a big clock (time ran out) + a crossed-out draft
    cx, cy, r = w * 0.26, z0 + zh * 0.52, zh * 0.47
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=WHITE, outline=INK,
              width=3)
    d.line([(cx, cy), (cx, cy - r * 0.62)], fill=INK, width=3)
    d.line([(cx, cy), (cx + r * 0.50, cy + r * 0.34)], fill=INK, width=3)
    d.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=INK)
    dx, dy = w * 0.50, z0 + zh * 0.10
    dw, dh = w * 0.38, zh * 0.84
    d.rectangle([dx, dy, dx + dw, dy + dh], fill=(245, 242, 232))
    d.line([(dx + 3, dy + 3), (dx + dw - 3, dy + dh - 3)], fill=RED,
           width=3)
    d.line([(dx + 3, dy + dh - 3), (dx + dw - 3, dy + 3)], fill=RED,
           width=3)
    return im


def _flag_uk(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(30, 40, 110))
    d.polygon([(x, y), (x + w * 0.16, y), (x + w, y + h),
               (x + w * 0.84, y + h)], fill=WHITE)
    d.polygon([(x + w, y), (x + w * 0.84, y), (x, y + h),
               (x + w * 0.16, y + h)], fill=WHITE)
    d.polygon([(x, y), (x + w * 0.10, y), (x + w, y + h),
               (x + w * 0.90, y + h)], fill=(200, 40, 50))
    d.polygon([(x + w, y), (x + w * 0.90, y), (x, y + h),
               (x + w * 0.10, y + h)], fill=(200, 40, 50))
    d.rectangle([x + w * 0.40, y, x + w * 0.60, y + h], fill=WHITE)
    d.rectangle([x, y + h * 0.36, x + w, y + h * 0.64], fill=WHITE)
    d.rectangle([x + w * 0.44, y, x + w * 0.56, y + h], fill=(200, 40, 50))
    d.rectangle([x, y + h * 0.41, x + w, y + h * 0.59], fill=(200, 40, 50))


def _flag_eu(d, x, y, w, h):
    import math
    d.rectangle([x, y, x + w, y + h], fill=(0, 51, 153))
    cx, cy, r = x + w / 2, y + h / 2, h * 0.30
    for i in range(12):
        a = math.radians(i * 30 - 90)
        sx, sy = cx + r * math.cos(a), cy + r * math.sin(a)
        d.polygon([(sx, sy - 2.4), (sx + 2.2, sy + 1.8), (sx - 2.2, sy + 1.8)],
                  fill=(255, 204, 0))


def sc_ukeu(w, h):
    im = Image.new("RGB", (w, h), (196, 208, 224))
    d = _d(im)
    _banner(d, w, "UK\u2013EU DEAL", fill=(20, 40, 90),
            size=12 if w > 200 else 10, align="l")
    z0, zh = int(h * 0.44), h - int(h * 0.44)
    fh = zh * 0.86
    fy = z0 + zh * 0.07
    _flag_uk(d, w * 0.05, fy, w * 0.36, fh)
    _flag_eu(d, w * 0.59, fy, w * 0.36, fh)
    d.text((w * 0.50, fy + fh * 0.46), "+", font=F(SERIF_B, int(zh * 0.95)),
           fill=INK, anchor="mm")
    return im


def sc_poland(w, h):
    im = Image.new("RGB", (w, h), (150, 168, 120))
    d = _d(im)
    _banner(d, w, "POLAND: MISSILE", fill=(120, 30, 28),
            size=12 if w > 200 else 10, align="l")
    d.rectangle([0, h * 0.82, w, h], fill=(110, 138, 84))
    # ONE glyph: a big missile, nose down into the field
    import math
    cx, cy = w * 0.48, h * 0.72
    ang = math.radians(38)
    L, R = h * 0.56, h * 0.105
    dx_, dy_ = math.sin(ang), math.cos(ang)
    tip = (cx + dx_ * L / 2, cy + dy_ * L / 2)
    tail = (cx - dx_ * L / 2, cy - dy_ * L / 2)
    px_, py_ = -dy_, dx_
    d.polygon([(tail[0] + px_ * R, tail[1] + py_ * R),
               (tip[0] + px_ * R * 0.5, tip[1] + py_ * R * 0.5),
               (tip[0] - px_ * R * 0.5, tip[1] - py_ * R * 0.5),
               (tail[0] - px_ * R, tail[1] - py_ * R)], fill=(96, 100, 108))
    d.polygon([(tail[0] + px_ * R * 0.9, tail[1] + py_ * R * 0.9),
               (tail[0] - px_ * R * 0.9, tail[1] - py_ * R * 0.9),
               (tail[0] - dx_ * R * 0.6, tail[1] - dy_ * R * 0.6)],
              fill=(150, 40, 36))
    for dx2, dy2 in ((-10, 2), (10, 2), (0, -9), (-7, -7), (7, -7)):
        d.line([(tip[0], tip[1]), (tip[0] + dx2, tip[1] + dy2)],
               fill=(240, 160, 60), width=2)
    return im


def sc_myanmar(w, h):
    im = Image.new("RGB", (w, h), (168, 198, 220))
    d = _d(im)
    _banner(d, w, "MYANMAR: \u201cUNFAIR\u201d", fill=(120, 40, 30),
            size=12 if w > 200 else 9, align="l")
    z0, zh = int(h * 0.44), h - int(h * 0.44)
    # ONE glyph: a solid courthouse silhouette + a big REJECTED stamp
    sil = (70, 60, 54)
    d.polygon([(w * 0.08, z0 + zh * 0.34), (w * 0.64, z0 + zh * 0.34),
               (w * 0.36, z0 + zh * 0.02)], fill=sil)
    d.rectangle([w * 0.08, z0 + zh * 0.34, w * 0.64, z0 + zh * 0.42],
                fill=sil)
    for i in range(4):
        cx = w * (0.11 + 0.135 * i)
        d.rectangle([cx, z0 + zh * 0.42, cx + w * 0.075, z0 + zh * 0.88],
                    fill=sil)
    d.rectangle([w * 0.06, z0 + zh * 0.88, w * 0.66, z0 + zh * 0.97],
                fill=sil)
    _stamp(d, (w * 0.58, z0 + zh * 0.26), "REJECTED",
           size=max(9, int(zh * 0.52)))
    return im


def sc_japan(w, h):
    im = Image.new("RGB", (w, h), (240, 236, 226))
    d = _d(im)
    _banner(d, w, "JAPAN: +2.3%", fill=(176, 32, 28),
            size=12 if w > 200 else 10, align="l")
    z0, zh = int(h * 0.44), h - int(h * 0.44)
    # ONE glyph: the rising-sun disc + three fat ascending bars + arrow
    cx, cy, r = w * 0.16, z0 + zh * 0.50, zh * 0.38
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(216, 48, 44))
    base = z0 + zh * 0.96
    for i, (bx, bh, col) in enumerate(
            ((0.36, 0.34, (70, 90, 130)), (0.55, 0.58, (70, 90, 130)),
             (0.74, 0.86, (216, 48, 44)))):
        d.rectangle([w * bx, base - zh * bh, w * (bx + 0.15), base],
                    fill=col)
    ax0, ay0 = w * 0.33, z0 + zh * 0.60
    ax1, ay1 = w * 0.90, z0 + zh * 0.10
    d.line([(ax0, ay0), (ax1, ay1)], fill=INK, width=4)
    d.polygon([(ax1, ay1), (ax1 - 11, ay1 + 1), (ax1 - 2, ay1 + 10)],
              fill=INK)
    return im


def sc_italy(w, h):
    im = Image.new("RGB", (w, h), (216, 205, 178))
    d = _d(im)
    _banner(d, w, "ITALY: STRIKE", fill=(150, 30, 30),
            size=12 if w > 200 else 10, align="l")
    z0, zh = int(h * 0.44), h - int(h * 0.44)
    # ONE glyph: a big red flag over a crowd silhouette band
    dark = (52, 48, 44)
    d.rectangle([0, h - zh * 0.16, w, h], fill=dark)
    for i in range(6):
        cx = w * (0.08 + i * 0.17)
        r = zh * 0.20
        d.ellipse([cx - r, h - zh * 0.16 - r * 1.5, cx + r,
                   h - zh * 0.16 + r * 0.5], fill=dark)
    fx = w * 0.64
    d.line([(fx, z0 - 2), (fx, h - zh * 0.16)], fill=(90, 60, 30),
           width=4)
    d.polygon([(fx, z0), (fx + w * 0.31, z0 + zh * 0.10),
               (fx + w * 0.31, z0 + zh * 0.44), (fx, z0 + zh * 0.34)],
              fill=(204, 42, 42))
    return im


def sc_china(w, h):
    im = Image.new("RGB", (w, h), (120, 26, 22))
    d = _d(im)
    _banner(d, w, "CHINA: RATES HELD", fill=(80, 16, 14),
            size=12 if w > 200 else 9, align="l")
    z0, zh = int(h * 0.44), h - int(h * 0.44)
    # the glyph IS the numbers: two big rate plaques
    pw, ph = w * 0.42, zh * 0.94
    py = z0 + zh * 0.03
    for i, (lab, val) in enumerate((("1-YEAR LPR", "3.00%"),
                                    ("5-YEAR LPR", "3.50%"))):
        px = w * (0.05 + i * 0.48)
        d.rectangle([px, py, px + pw, py + ph], fill=(245, 240, 226))
        d.text((px + pw / 2, py + ph * 0.24), lab,
               font=F(SANS_B, max(8, int(zh * 0.30))), fill=(120, 26, 22),
               anchor="mm")
        d.text((px + pw / 2, py + ph * 0.68), val,
               font=F(SERIF_B, max(9, int(zh * 0.54))), fill=INK,
               anchor="mm")
    return im


def sc_cricket(w, h):
    im = Image.new("RGB", (w, h), (52, 110, 62))
    d = _d(im)
    _banner(d, w, "WELLINGTON", fill=(24, 62, 34),
            size=11 if w > 200 else 9, align="l")
    z0, zh = int(h * 0.44), h - int(h * 0.44)
    # ONE glyph pair: a numeral scoreboard + a big ball
    d.rectangle([w * 0.05, z0 + zh * 0.06, w * 0.56, z0 + zh * 0.94],
                fill=(18, 24, 20))
    d.text((w * 0.09, z0 + zh * 0.30), "NZ 368",
           font=F(SANS_B, max(8, int(zh * 0.46))), fill=(255, 220, 120),
           anchor="lm")
    d.text((w * 0.09, z0 + zh * 0.70), "IND 159/1",
           font=F(SANS_B, max(7, int(zh * 0.32))), fill=(200, 220, 200),
           anchor="lm")
    cx, cy, r = w * 0.79, z0 + zh * 0.50, zh * 0.36
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(196, 40, 40))
    d.arc([cx - r * 0.82, cy - r * 0.82, cx + r * 0.82, cy + r * 0.82],
          300, 60, fill=WHITE, width=2)
    return im


def sc_retail(w, h):
    im = Image.new("RGB", (w, h), (228, 220, 200))
    d = _d(im)
    _banner(d, w, "SALES +0.7%", fill=(40, 80, 60),
            size=11 if w > 200 else 9, align="l")
    z0, zh = int(h * 0.44), h - int(h * 0.44)
    # fat awning stripes
    for i in range(4):
        x0 = i * w * 0.25
        d.polygon([(x0, z0), (x0 + w * 0.25, z0),
                   (x0 + w * 0.22, z0 + zh * 0.26),
                   (x0 + w * 0.03, z0 + zh * 0.26)],
                  fill=(200, 60, 50) if i % 2 == 0 else (245, 242, 232))
    # ONE glyph: a filled trolley silhouette + the figure panel
    ink2 = (44, 44, 44)
    d.rectangle([w * 0.20, z0 + zh * 0.30, w * 0.28, z0 + zh * 0.44],
                fill=(240, 190, 70))
    d.rectangle([w * 0.32, z0 + zh * 0.34, w * 0.40, z0 + zh * 0.44],
                fill=(90, 150, 90))
    d.polygon([(w * 0.14, z0 + zh * 0.44), (w * 0.50, z0 + zh * 0.44),
               (w * 0.46, z0 + zh * 0.72), (w * 0.18, z0 + zh * 0.72)],
              fill=ink2)
    d.line([(w * 0.50, z0 + zh * 0.44), (w * 0.58, z0 + zh * 0.36)],
           fill=ink2, width=3)
    for wx in (w * 0.22, w * 0.42):
        rr = zh * 0.09
        d.ellipse([wx - rr, z0 + zh * 0.78, wx + rr, z0 + zh * 0.78 + 2 * rr],
                  fill=ink2)
    d.rectangle([w * 0.62, z0 + zh * 0.38, w * 0.96, z0 + zh * 0.86],
                fill=(40, 80, 60))
    d.text((w * 0.79, z0 + zh * 0.62), "+0.7%",
           font=F(SANS_B, max(8, int(zh * 0.40))), fill=WHITE,
           anchor="mm")
    return im


def sc_gtavi(w, h):
    im = Image.new("RGB", (w, h), (58, 26, 92))
    d = _d(im)
    # ONE glyph: a giant VI over a sun-and-skyline silhouette
    d.ellipse([w * 0.60, h * 0.10, w * 0.90, h * 0.72], fill=(250, 170, 60))
    import random
    random.seed(6)
    x = 0
    while x < w:
        bwid = random.randint(int(w * 0.06), int(w * 0.11))
        bh = random.randint(int(h * 0.20), int(h * 0.42))
        d.rectangle([x, h * 0.88 - bh, x + bwid, h * 0.88],
                    fill=(30, 16, 54))
        for _ in range(2):
            wx = x + random.randint(2, max(3, bwid - 5))
            wy = h * 0.88 - random.randint(4, max(5, bh - 4))
            d.rectangle([wx, wy, wx + 2, wy + 3], fill=(255, 220, 120))
        x += bwid + 2
    d.rectangle([0, h * 0.88, w, h], fill=(22, 12, 40))
    d.text((w * 0.05, h * 0.14), "VI", font=F(SERIF_B, int(h * 0.58)),
           fill=(255, 120, 190))
    d.rectangle([0, 0, w, 15], fill=(20, 10, 36))
    d.text((8, 7), "DAY-TWO", font=F(SANS_B, 9),
           fill=(255, 190, 90), anchor="lm")
    return im


def sc_badminton(w, h):
    im = Image.new("RGB", (w, h), (36, 96, 110))
    d = _d(im)
    _banner(d, w, "HONG KONG OPEN", fill=(18, 56, 66),
            size=11 if w > 200 else 9, align="l")
    z0, zh = int(h * 0.44), h - int(h * 0.44)
    # ONE glyph pair: a thick racket + a big shuttlecock
    cx, cy = w * 0.27, z0 + zh * 0.46
    rx, ry = w * 0.115, zh * 0.42
    d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], outline=WHITE, width=4)
    for i in (-1, 0, 1):
        d.line([(cx + i * rx * 0.45, cy - ry * 0.9),
                (cx + i * rx * 0.45, cy + ry * 0.9)],
               fill=(200, 220, 225), width=1)
    d.line([(cx, cy + ry), (w * 0.37, h - 1)], fill=(240, 200, 120),
           width=4)
    sx, sy = w * 0.68, z0 + zh * 0.58
    for i in range(5):
        ex = sx - w * 0.20 + i * w * 0.05
        ey = z0 + zh * 0.04 + (i % 2) * zh * 0.05
        d.line([(sx - w * 0.02, sy - zh * 0.08), (ex, ey)], fill=WHITE,
               width=3)
    d.line([(sx - w * 0.20, z0 + zh * 0.04), (sx, z0 + zh * 0.09)],
           fill=WHITE, width=2)
    d.ellipse([sx - w * 0.045, sy - zh * 0.13, sx + w * 0.045,
               sy + zh * 0.13], fill=(240, 200, 120))
    return im


SCENES = {
    "kyiv": sc_kyiv, "akvan": sc_akvan, "aisell": sc_aisell,
    "cop31": sc_cop31, "ukeu": sc_ukeu, "poland": sc_poland,
    "myanmar": sc_myanmar, "japan": sc_japan, "italy": sc_italy,
    "china": sc_china, "cricket": sc_cricket, "retail": sc_retail,
    "gtavi": sc_gtavi, "badminton": sc_badminton,
}

CHIP_COLOURS = {"REPORTED": (38, 110, 62), "CLAIM": (196, 118, 30),
                "FORECAST": (52, 84, 140), "ESTIMATE": (118, 70, 148),
                "ONGOING": (150, 110, 20)}


# ---------------------------------------------------------------- map
# Schematic world silhouette, equirectangular, hand-coded polygons in
# (lon, lat). Original to this build; positions approximate.

CONTINENTS = [
    # North America
    [(-168, 66), (-140, 70), (-125, 72), (-110, 68), (-95, 69), (-85, 66),
     (-80, 62), (-76, 58), (-70, 55), (-65, 50), (-70, 45), (-74, 40),
     (-76, 35), (-80, 32), (-81, 26), (-84, 30), (-89, 30), (-94, 29),
     (-97, 26), (-97, 22), (-94, 18), (-90, 15), (-86, 13), (-83, 9),
     (-79, 9), (-83, 15), (-87, 21), (-90, 21), (-97, 16), (-102, 18),
     (-105, 23), (-110, 24), (-114, 29), (-117, 33), (-122, 37),
     (-124, 46), (-130, 55), (-145, 60), (-158, 58), (-165, 60)],
    # Greenland
    [(-45, 60), (-30, 68), (-22, 70), (-20, 76), (-30, 80), (-50, 79),
     (-58, 75), (-55, 68)],
    # South America
    [(-79, 9), (-75, 11), (-72, 12), (-64, 10), (-60, 8), (-52, 5),
     (-50, 0), (-44, -3), (-35, -8), (-39, -13), (-40, -22), (-48, -27),
     (-52, -33), (-57, -38), (-62, -41), (-65, -45), (-67, -50),
     (-68, -54), (-71, -54), (-73, -46), (-73, -37), (-71, -30),
     (-70, -20), (-75, -15), (-79, -8), (-81, -4), (-80, 1), (-77, 4)],
    # Eurasia
    [(-9, 37), (-9, 43), (-2, 44), (-1, 47), (-5, 48), (0, 51), (5, 53),
     (8, 55), (8, 58), (5, 59), (5, 61), (10, 64), (16, 67), (22, 69),
     (30, 71), (40, 68), (50, 69), (60, 69), (70, 72), (80, 73),
     (90, 74), (100, 76), (110, 74), (120, 73), (130, 72), (140, 72),
     (150, 70), (160, 69), (170, 67), (178, 66), (178, 64), (170, 60),
     (162, 60), (158, 55), (156, 51), (150, 45), (142, 44), (140, 40),
     (135, 35), (129, 33), (126, 38), (122, 38), (120, 34), (122, 30),
     (120, 26), (114, 22), (108, 18), (106, 10), (104, 8), (100, 7),
     (98, 10), (94, 16), (91, 22), (88, 22), (86, 20), (80, 15),
     (77, 8), (74, 12), (72, 19), (68, 23), (66, 25), (61, 25),
     (57, 26), (52, 26), (50, 29), (48, 30), (50, 25), (55, 24),
     (58, 22), (55, 17), (52, 15), (45, 12), (43, 12), (40, 15),
     (38, 20), (36, 24), (34, 28), (36, 31), (33, 36), (30, 36),
     (27, 37), (23, 36), (19, 40), (15, 38), (12, 40), (10, 44),
     (7, 44), (3, 43), (0, 39), (-2, 37)],
    # Britain
    [(-5, 50), (-3, 53), (-5, 55), (-6, 57), (-4, 58), (-2, 57),
     (-1, 54), (-2, 51)],
    # Japan
    [(130, 31), (133, 34), (137, 35), (140, 36), (140, 39), (141, 42),
     (142, 44), (140, 44), (139, 40), (138, 37), (135, 34), (132, 33),
     (130, 32)],
    # Indonesia / Papua
    [(95, 5), (100, 0), (105, -5), (110, -7), (115, -8), (120, -9),
     (125, -10), (130, -9), (135, -4), (140, -3), (145, -5), (150, -9),
     (147, -10), (142, -8), (136, -2), (131, -1), (126, -8), (120, -10),
     (113, -8), (106, -6), (100, -2), (96, 3)],
    # Africa
    [(-6, 35), (0, 36), (10, 37), (11, 34), (20, 32), (30, 31),
     (32, 31), (34, 27), (35, 24), (38, 21), (39, 15), (43, 12),
     (48, 11), (51, 12), (45, 5), (41, 0), (40, -6), (39, -12),
     (37, -18), (35, -24), (33, -27), (30, -30), (26, -33), (20, -35),
     (17, -32), (15, -27), (13, -20), (12, -15), (13, -10), (12, -5),
     (9, -1), (9, 4), (4, 6), (-3, 5), (-8, 5), (-13, 8), (-16, 12),
     (-17, 15), (-16, 20), (-15, 25), (-13, 28), (-9, 31)],
    # Madagascar
    [(44, -16), (47, -14), (50, -17), (49, -22), (47, -24), (45, -25),
     (44, -21), (43, -18)],
    # Australia
    [(113, -21), (122, -17), (130, -12), (136, -12), (142, -11),
     (146, -15), (150, -22), (153, -27), (153, -32), (150, -37),
     (147, -39), (143, -39), (140, -38), (136, -35), (133, -32),
     (129, -32), (124, -33), (118, -35), (115, -34), (113, -26)],
    # New Zealand
    [(167, -45), (170, -43), (172, -41), (174, -39), (176, -38),
     (178, -37), (176, -40), (174, -41), (172, -43), (169, -46)],
]

PINS = [  # (story num, lon, lat) — nudged where European pins crowd
    (1, 32.0, 49.0), (2, 84.9, 19.3), (3, 123.0, 26.5), (4, 30.7, 36.9),
    (5, 7.0, 50.0), (6, 21.0, 53.0), (7, 96.1, 19.8), (8, 139.7, 35.7),
    (9, 12.5, 41.9), (10, 116.4, 39.9), (11, 174.8, -41.3),
    (12, -3.0, 53.5), (13, -74.0, 40.7), (14, 114.2, 22.3),
]


def draw_map(x, y, w):
    hh = w * 140.0 / 360.0 * (360.0 / 288.0)  # ~125px tall for w=300
    hh = 125 if w == 300 else w * 0.4167
    dr.rectangle([x, y, x + w, y + hh], fill=(24, 34, 54))
    land = (208, 198, 172)

    def px(lon):
        return x + (lon + 180) / 360.0 * w

    def py(lat):
        return y + (84 - lat) / 140.0 * hh

    for poly in CONTINENTS:
        dr.polygon([(px(lon), py(lat)) for lon, lat in poly], fill=land)
    for num, lon, lat in PINS:
        cx, cy = px(lon), py(lat)
        dr.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=RED,
                   outline=WHITE, width=1)
        dr.text((cx, cy - 1), str(num), font=F(SANS_B, 7 if num < 10 else 6),
                fill=WHITE, anchor="mm")


# ---------------------------------------------------------------- cards
WARNINGS = []


def draw_card(x, y, w, h, main, large, medium_tight=False):
    dr.rectangle([x, y, x + w, y + h], fill=CARD, outline=BORDER, width=1)
    if large:
        scene_h = 128
    elif medium_tight:
        scene_h = 44
    else:
        scene_h = 46
    scene = SCENES[main["scene"]](w - 2, scene_h)
    img.paste(scene, (x + 1, y + 1))
    # status chip, top-right of scene
    chip = main["chip"]
    cf = F(SANS_B, 9)
    cw_ = tw(chip, cf) + 10
    dr.rectangle([x + w - 5 - cw_, y + 5, x + w - 5, y + 17],
                 fill=CHIP_COLOURS[chip])
    dr.text((x + w - 5 - cw_ / 2, y + 11), chip, font=cf, fill=WHITE,
            anchor="mm")
    pad = 10 if large else 7
    cx = x + pad
    inner_w = w - 2 * pad
    cy = y + scene_h + (6 if large else 4)
    # tag row: number badge + tag
    badge_r = 8 if large else 7
    dr.ellipse([cx, cy, cx + 2 * badge_r, cy + 2 * badge_r], fill=RED)
    dr.text((cx + badge_r, cy + badge_r), str(main["num"]),
            font=F(SANS_B, 9), fill=WHITE, anchor="mm")
    tag_f = F(SANS_B, 10)
    tag = main["tag"]
    while tw(tag, tag_f) > inner_w - 2 * badge_r - 6 and tag_f.size > 8:
        tag_f = F(SANS_B, tag_f.size - 1)
    dr.text((cx + 2 * badge_r + 5, cy + badge_r), tag,
            font=tag_f, fill=DARKRED, anchor="lm")
    cy += 2 * badge_r + (3 if large else 2)
    # headline
    hsize = 29 if large else (15 if medium_tight else 18)
    lines = []
    while hsize > 10:
        hf = F(SERIF_B, hsize)
        lines = wrap(main["headline"], hf, inner_w)
        if len(lines) <= 2:
            break
        hsize -= 1
    if len(lines) > 2:
        WARNINGS.append(f"card {main['num']}: headline wraps {len(lines)}")
    lh = int(hsize * 1.08)
    for ln in lines:
        dr.text((cx, cy), ln, font=hf, fill=INK)
        cy += lh
    cy += 2
    # deck
    if large:
        dsize, dlh, maxd = 13, 14, 3
    elif medium_tight:
        dsize, dlh, maxd = 12, 13, 2
    else:
        dsize, dlh, maxd = 13, 13, 2
    df = F(SERIF, dsize)
    dlines = wrap(main["deck"], df, inner_w)
    if len(dlines) > maxd:
        WARNINGS.append(
            f"card {main['num']}: deck wraps {len(dlines)} > {maxd}")
    for ln in dlines:
        dr.text((cx, cy), ln, font=df, fill=(52, 48, 42))
        cy += dlh
    if cy > y + h - 2:
        WARNINGS.append(f"card {main['num']}: content bottom {cy} > {y + h}")


# ---------------------------------------------------------------- build
def build():
    # ---- masthead first (its strip would erase anything under it)
    mast = "Friday 20 November 2026"
    msize = 90
    mf = F(LIB_B, msize)
    strip = Image.new("RGB", (int(tw(mast, mf)) + 8, int(msize * 1.3)),
                      PAPER)
    sd = ImageDraw.Draw(strip)
    sd.text((4, 0), mast, font=mf, fill=INK)
    strip = strip.resize((CW, int(msize * 1.3)), Image.LANCZOS)
    img.paste(strip, (MX, 6))
    print("masthead size:", msize)

    # ---- kicker
    text(MX, 4, "THE WORLD IN ONE DAY", F(SANS_B, 13), fill=RED)
    kick_r = "38 STORIES \u00b7 7 REGIONS \u00b7 ALL FROM THIS ONE DAY"
    text(W - MX, 5, kick_r, F(SANS_SB, 12), anchor="ra")

    # ---- strapline
    strap = ("Kyiv bridges hit \u00b7 Cyclone Akvan strikes India "
             "\u00b7 An AI sell-off sinks Asia's markets \u00b7 "
             "COP31 ends its last day with no deal")
    ssize = fit_size(strap, SERIF_I, CW, 21, 13)
    text(MX, 110, strap, F(SERIF_I, ssize), fill=RED)
    hline(MX, W - MX, 131, fill=INK, width=2)

    # ---- region bar
    total = sum(c for _, c, _ in REGIONS)
    assert total == len(MAINS) + len(BRIEFS), (total, len(BRIEFS))
    bx = MX
    by, bh = 136, 17
    for name, count, col in REGIONS:
        seg = CW * count / total
        dr.rectangle([bx, by, bx + seg - 1, by + bh], fill=col)
        lab = f"{name} {count}"
        placed = False
        for lsize in (10, 9, 8):
            lf = F(SANS_B, lsize)
            if tw(lab, lf) <= seg - 4:
                dr.text((bx + seg / 2, by + bh / 2), lab, font=lf,
                        fill=WHITE, anchor="mm")
                placed = True
                break
        if not placed:
            # tiny segment (AFRICA 1): stack name over count at 7px
            lf = F(SANS_B, 7)
            dr.text((bx + seg / 2, by + 2), name, font=lf, fill=WHITE,
                    anchor="ma")
            dr.text((bx + seg / 2, by + 9), str(count), font=lf,
                    fill=WHITE, anchor="ma")
        bx += seg

    # ---- numbers strip
    hline(MX, W - MX, 157, fill=BORDER, width=1)
    cellw = CW / 6.0
    for i, (num, cap) in enumerate(NUMBERS):
        cx = MX + i * cellw
        text(cx + 2, 161, num, F(SERIF_B, 24))
        cl = wrap(cap, F(SANS, 11), cellw - 10)
        yy = 188
        for ln in cl[:2]:
            dr.text((cx + 2, yy), ln, font=F(SANS, 11), fill=MUTED)
            yy += 12
        if i:
            dr.line([(cx - 5, 163), (cx - 5, 210)], fill=BORDER, width=1)
    hline(MX, W - MX, 215, fill=BORDER, width=1)

    # ---- large cards
    lw = int((CW - 16) / 3)
    for i, main in enumerate(MAINS[:3]):
        draw_card(MX + i * (lw + 8), 221, lw, 262, main, large=True)
    # ---- medium cards, row A: five
    mw = int((CW - 36) / 5)
    for c in range(5):
        main = MAINS[3 + c]
        draw_card(MX + c * (mw + 9), 487, mw, 134, main, large=False)
    # ---- medium cards, row B: six (tighter)
    tw6 = 159
    step = (CW - tw6) / 5.0
    for c in range(6):
        main = MAINS[8 + c]
        draw_card(int(MX + c * step), 625, tw6, 128, main, large=False,
                  medium_tight=True)

    # ---- bottom band: map (left) + ALSO one-liners + IN SHORT index
    # v4: the map STAYS (212px wide, all 14 numbered pins — v3 deleted
    # it and its duel margins dipped). The brief columns take v3's
    # structure at v3's sizes (15px one-liners / 14px index); the
    # space is paid for by the tightened masthead stack, numbers
    # strip and section gaps above, not by the map.
    hline(MX, W - MX, 757, fill=BORDER, width=1)
    text(MX, 761, "WHERE IT HAPPENED", F(SANS_B, 11), fill=RED)
    draw_map(MX + 2, 784, 212)
    text(MX, 876, "Red numbers mark stories 1–14.", F(SANS, 9),
         fill=MUTED)
    text(MX, 887, "Positions approximate.", F(SANS, 9), fill=MUTED)
    # chip legend under the map (the apparatus, explained in place)
    for i, (chip, note) in enumerate(
            (("REPORTED", "named source, checked"),
             ("ESTIMATE", "a projection, flagged"))):
        ly = 908 + i * 18
        cf = F(SANS_B, 8)
        cw2 = tw(chip, cf) + 10
        dr.rectangle([MX, ly, MX + cw2, ly + 12],
                     fill=CHIP_COLOURS[chip])
        dr.text((MX + cw2 / 2, ly + 6), chip, font=cf, fill=WHITE,
                anchor="mm")
        dr.text((MX + cw2 + 7, ly + 6), note, font=F(SANS, 9),
                fill=MUTED, anchor="lm")

    def brief_line(x, y, num, place, body, src, f_num, f_place,
                   f_text, f_src, max_w, label):
        dr.text((x, y), str(num), font=f_num, fill=RED)
        x2 = x + tw(str(num), f_num) + 5
        dr.text((x2, y), place, font=f_place, fill=INK)
        x2 += tw(place, f_place)
        rest = " — " + body
        dr.text((x2, y), rest, font=f_text, fill=(46, 42, 36))
        x2 += tw(rest, f_text)
        if src:
            s = " " + src
            dr.text((x2, y), s, font=f_src, fill=MUTED)
            x2 += tw(s, f_src)
        if x2 - x > max_w:
            WARNINGS.append(
                f"{label} {num} too wide: {x2 - x:.0f} > {max_w}")

    # left text column: the twelve strongest, full one-liners at 15px
    text(244, 760, "ALSO ON FRIDAY 20 NOVEMBER 2026", F(SERIF_B, 15),
         fill=RED)
    b_num, b_place = F(SANS_B, 12), F(SERIF_B, 15)
    b_text, b_src = F(SERIF, 15), F(SERIF_I, 14)
    for idx, (place, body, src) in enumerate(BRIEFS_FULL):
        num = len(MAINS) + 1 + idx
        brief_line(244, 784 + idx * 15.0, num, place, body, src,
                   b_num, b_place, b_text, b_src, 384, "brief")
    dr.line([(640, 784), (640, 958)], fill=BORDER, width=1)
    # right text column: the other twelve, as an index at 14px
    text(650, 761, "IN SHORT — THE REST OF FRIDAY", F(SERIF_B, 14),
         fill=RED)
    s_num, s_place = F(SANS_B, 11), F(SERIF_B, 14)
    s_text, s_src = F(SERIF, 14), F(SERIF_I, 13)
    for idx, (place, body, src) in enumerate(BRIEFS_SHORT):
        num = len(MAINS) + len(BRIEFS_FULL) + 1 + idx
        brief_line(650, 784 + idx * 14.6, num, place, body, src,
                   s_num, s_place, s_text, s_src, 360, "short brief")


    # ---- date check box
    dr.rectangle([MX, 973, W - MX, 1009], fill=(250, 244, 230),
                 outline=RED, width=2)
    words = DATE_CHECK.split()
    dx, dy = MX + 10, 976
    maxx = W - MX - 10
    for i, w_ in enumerate(words):
        if i < 2:
            fnt, colr = F(SERIF_B, 10), RED
        elif w_ == "COP31":
            # bold so the word cannot blur into "GOP31" at small sizes
            fnt, colr = F(SERIF_B, 10), INK
        else:
            fnt, colr = F(SERIF, 10), INK
        ww = tw(w_, fnt) + 4
        if dx + ww > maxx:
            dx = MX + 10
            dy += 11
        dr.text((dx, dy), w_, font=fnt, fill=colr)
        dx += ww
    if dy + 11 > 1009:
        WARNINGS.append(f"date check overflows box: bottom {dy + 11}")

    # ---- colophon
    text(W / 2, 1012, COLOPHON, F(SANS, 9), fill=MUTED, anchor="ma")

    # ---- integrity assertions
    corpus = " ".join(
        [m["headline"] + " " + m["deck"] + " " + m["tag"] for m in MAINS]
        + [p + " " + b for p, b, _ in BRIEFS]
        + [n + " " + c for n, c in NUMBERS])
    for bad in ("Senegal", "Fiji", "Shenzhen", "51\u201348", "Voyager",
                "war-powers", "debut", "awaited", "press time"):
        assert bad not in corpus, f"forbidden token in page corpus: {bad}"
    assert DATE_CHECK.count("\u00b7") >= 8
    for warn in WARNINGS:
        print("WARNING:", warn)
    print("stories:", len(MAINS) + len(BRIEFS), "| warnings:",
          len(WARNINGS))

    img.save("entry.png")
    small = img.resize((300, 300), Image.LANCZOS)
    small.save("entry-300.png")
    print("saved entry.png and entry-300.png")


if __name__ == "__main__":
    build()
