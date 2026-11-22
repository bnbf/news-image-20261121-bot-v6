#!/usr/bin/env python3
"""The World - Saturday 21 November 2026: 35 stories, one front page.

Self-contained PIL generator. Draws a newspaper front page for 21 Nov 2026
(3 heroes, 12 picture cards, 20 ALSO briefs, 7 regions, UTC timeline,
world map with numbered pins, DATE CHECK footer). Deterministic: same input
always renders the same PNG bytes. Run: python3 main.py -> entry.png
(or $MAKEFUN_OUTPUT_DIR/entry.png).
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.environ.get("MAKEFUN_OUTPUT_DIR", ".")
PAPER = (247, 241, 222)
INK = (22, 20, 17)
INK2 = (74, 68, 58)
RED = (163, 29, 29)
NAVY = (29, 58, 95)
GOLD = (176, 124, 22)
GREEN = (46, 110, 58)
TEAL = (18, 102, 102)
RULE = (180, 170, 145)
CARD = (255, 252, 244)
SKY = (214, 228, 238)

FD = "/usr/share/fonts/truetype/dejavu"


def F(name, size):
    try:
        return ImageFont.truetype(os.path.join(FD, name), size)
    except OSError:
        return ImageFont.load_default()


def serif_b(s):
    return F("DejaVuSerif-Bold.ttf", s)


def serif(s):
    return F("DejaVuSerif.ttf", s)


def sans(s):
    return F("DejaVuSans.ttf", s)


def sans_b(s):
    return F("DejaVuSans-Bold.ttf", s)


def wrap(d, text, font, maxw):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text(d, x, y, s, font, fill=INK, anchor="la"):
    d.text((x, y), s, font=font, fill=fill, anchor=anchor)


def centre(d, x, y, s, font, fill=INK):
    d.text((x, y), s, font=font, fill=fill, anchor="ma")


def rule(d, x0, y, x1, w=2, fill=RULE):
    d.line([(x0, y), (x1, y)], fill=fill, width=w)


def tag(d, x, y, s, fill):
    f = sans_b(9)
    w = int(d.textlength(s, font=f)) + 10
    d.rounded_rectangle([x, y, x + w, y + 14], radius=3, fill=fill)
    d.text((x + 5, y + 2), s, font=f, fill=(255, 255, 255))
    return w


# ---------------------------------------------------------------- data
# Every figure below was checked against live reporting on 22 Nov 2026:
# USGS (Peru M6.7, 00:09 UTC), Zelensky / Ukraine Air Force (404 drones,
# 110 missiles, 27 ballistic), NYSE closes (Nasdaq -5.28%, S&P -3.7%),
# Reuters (Nikkei -5.06%, COP31 deadlock, Cikande fire), ESA (BepiColombo
# orbit insertion 18:24 UTC), Guardian (daraxonrasib trial, 1 in 12).
HEROES = [
    dict(num=1, region="LATIN AMERICA", colour=(150, 60, 20),
         head="M6.7 QUAKE SHAKES PERU'S ANDES",
         deck="00:09 UTC, 9 km NE of Carhuamayo, 108 km deep. "
              "Felt in Lima; 1 dead, 16 injured, homes damaged.",
         conf="CONFIRMED", src="USGS", pic="quake"),
    dict(num=2, region="EUROPE", colour=RED,
         head="400 DRONES, 110 MISSILES: KYIV STILL BURNING",
         deck="Overnight barrage, 27 ballistic; 3 Dnipro bridges hit. "
              "21 Nov: missile strikes Kryvyi Rih, 2 dead; one lands in Poland.",
         conf="CONFIRMED", src="Zelensky / Ukr. Air Force", pic="kyiv"),
    dict(num=3, region="NORTH AMERICA", colour=NAVY,
         head="NASDAQ -5.3%: THE AI TRADE MELTS DOWN",
         deck="Friday close 22,617.73, down 1,261 pts; S&P -3.7% into "
              "correction. Nvidia -14% on SEC probe report.",
         conf="CONFIRMED", src="NYSE closes", pic="nasdaq"),
]

CARDS = [
    dict(num=4, region="GLOBAL", colour=TEAL,
         head="COP31: NO DEAL IN ANTALYA",
         deck="Draft drops fossil fuels, $120bn target. "
              "EU: \u201cgood deal or no deal\u201d.",
         conf="CONFIRMED", src="Reuters", pic="cop"),
    dict(num=5, region="MIDDLE EAST", colour=RED,
         head="IRAN HITS US BASES IN BAHRAIN",
         deck="Two bases struck; fire at a plant, no injuries. "
              "US drone downed near Qeshm: CLAIM.",
         conf="CONFIRMED", src="IRGC", pic="missile"),
    dict(num=6, region="LATIN AMERICA", colour=(150, 60, 20),
         head="CHAPO ISIDRO SEIZED; 11 DEAD",
         deck="FBI most-wanted cartel boss captured in Sinaloa. "
              "Gunfights and roadblocks follow.",
         conf="CONFIRMED", src="BBC", pic="badge"),
    dict(num=7, region="EUROPE", colour=NAVY,
         head="DRONES HIT RUSSIAN SHIP SPARTA II",
         deck="Blaze in the Gulf of Finland. Ukraine likely "
              "behind it, Finland says.",
         conf="REPORTED", src="Finland", pic="ship"),
    dict(num=8, region="ASIA-PACIFIC", colour=GREEN,
         head="EU-INDONESIA DEAL, 10 YEARS ON",
         deck="Trade pact sealed after a decade of talks. "
              "EU's biggest deal in Asia in years.",
         conf="CONFIRMED", src="France 24", pic="flags"),
    dict(num=9, region="LATIN AMERICA", colour=(150, 60, 20),
         head="BOLSONARO RUSHED TO HOSPITAL",
         deck="Brazil's ex-president taken in over abdominal pain. "
              "Condition stable, aides say.",
         conf="CONFIRMED", src="DW", pic="cross"),
    dict(num=10, region="GLOBAL", colour=TEAL,
         head="BEPICOLOMBO REACHES MERCURY",
         deck="8 years on, twin orbiters enter orbit at 18:24 UTC. "
              "Only the 2nd ever.",
         conf="CONFIRMED", src="ESA", pic="planet"),
    dict(num=11, region="GLOBAL", colour=(120, 40, 110),
         head="THE PILL THAT ERASED TUMOURS",
         deck="Daraxonrasib: tumours undetectable in 1 in 12 "
              "in an early trial.",
         conf="CONFIRMED", src="Guardian", pic="pill"),
    dict(num=12, region="ASIA-PACIFIC", colour=(150, 60, 20),
         head="36 MISSING IN FACTORY FIRE",
         deck="Cikande candy factory blaze kills 3; 36 missing, "
              "search under way.",
         conf="CONFIRMED", src="Reuters", pic="factory"),
    dict(num=13, region="EUROPE", colour=NAVY,
         head="DENMARK: PLOT TO KILL RAPPER",
         deck="Copenhagen accuses Russia of plotting to assassinate "
              "a US-Ukrainian rapper.",
         conf="REPORTED", src="BBC", pic="mic"),
    dict(num=14, region="NORTH AMERICA", colour=RED,
         head="FBI PROBES HACK OF ITS DATABASE",
         deck="Apparent breach of the key crime database; "
              "USDA also hit.",
         conf="REPORTED", src="AP", pic="lock"),
    dict(num=15, region="GLOBAL", colour=TEAL,
         head="NASA HALTS MARS SCIENCE",
         deck="Perseverance and Mars Odyssey paused amid hardware "
              "troubles, agency says.",
         conf="CONFIRMED", src="NASA", pic="rover"),
]

ALSO = [
    ("EUROPE", "Trump defends Putin; Zelensky: \u201cPutin is a killer\u201d."),
    ("EUROPE", "Missile lands in Poland; allies rally to Warsaw."),
    ("N. AMERICA", "Harden 51, passes Kobe; Cavs beat Pacers 128-119."),
    ("N. AMERICA", "Cavalry FC win Canadian Premier League, 3-2."),
    ("N. AMERICA", "Palisades arsonist convicted; fire killed 12."),
    ("N. AMERICA", "Mamdani: close Rikers Island jail by 2032."),
    ("MIDDLE EAST", "Israel plans new West Bank city of 200,000."),
    ("N. AMERICA", "19 years for Indian in Pannun murder plot."),
    ("ASIA-PAC.", "Illicit alcohol kills 11, poisons 180 in Manipur."),
    ("EUROPE", "Trafalgar tree felled in Norway."),
    ("EUROPE", "Spain frees activist Chambers on bail."),
    ("AFRICA", "ANC fights to hold South Africa's big cities."),
    ("EUROPE", "Harry Kane out \u201ca few months\u201d; Bayern draw."),
    ("GLOBAL", "FIFA: Infantino re-election backed by CONMEBOL."),
    ("MIDDLE EAST", "Lebanon demands Israel withdraw."),
    ("EUROPE", "France braces for fresh protests, week six."),
    ("GLOBAL", "US declassifies more UFO footage."),
    ("ASIA-PAC.", "Quad, ASEAN summits: takeaways from Manila."),
    ("N. AMERICA", "$811m fines didn't stop migrant-detention scams."),
    ("ASIA-PAC.", "Veteran NSW MP Fred Nile dies, aged 92."),
]

REGIONS = [
    ("EUROPE", 9, NAVY), ("N. AMERICA", 8, RED), ("GLOBAL", 6, TEAL),
    ("ASIA-PAC.", 5, GREEN), ("LATIN AM.", 3, (150, 60, 20)),
    ("MIDDLE EAST", 3, (120, 40, 110)), ("AFRICA", 1, GOLD),
]

NUMBERS = [
    ("6.7", "Peru quake magnitude (USGS)"),
    ("400+", "drones over Ukraine"),
    ("110", "missiles fired at Ukraine"),
    ("-5.3%", "Nasdaq, Friday close"),
    ("3", "Kyiv bridges hit"),
    ("1 in 12", "pill-trial patients, tumours gone"),
]

TIMELINE = [
    ("00:09", "Peru quake M6.7"),
    ("06:00", "Nikkei closes -5.1%"),
    ("08:00", "COP31 past deadline"),
    ("14:36", "EU: \u201cgood deal or no deal\u201d"),
    ("18:24", "BepiColombo enters Mercury orbit"),
    ("21:00", "Nasdaq closes -5.3%"),
    ("NIGHT", "Kyiv's fires still burn"),
]

# map pins: (number, label, x, y) on a 474x114 map box; LAB offsets badges
# for the four colliding European pins (dot stays true, badge moves out)
PINS = [
    (1, "Jun\u00edn, Peru", 128, 87), (2, "Kyiv", 266, 32),
    (3, "New York", 122, 42), (4, "Antalya", 278, 40),
    (5, "Bahrain", 318, 56), (6, "Sinaloa", 78, 56),
    (7, "Gulf of Finland", 278, 18), (8, "Jakarta", 392, 80),
    (9, "Brazil", 158, 83), (12, "Cikande", 388, 71),
    (13, "Copenhagen", 256, 20), (14, "Washington", 108, 45),
    (15, "Mars *", 452, 95),
]
LAB = {2: (250, 52), 4: (294, 56), 7: (294, 8), 12: (368, 94), 13: (236, 32)}


# ---------------------------------------------------------------- header
def draw_header(d):
    centre(d, W // 2, 6,
           "SATURDAY 21 NOVEMBER 2026  \u00b7  35 STORIES  \u00b7  7 REGIONS  \u00b7  ALL FROM THIS DAY",
           sans_b(13), INK)
    rule(d, 26, 28, W - 26, 2, INK)
    centre(d, W // 2, 34, "THE WORLD", serif_b(74), INK)
    centre(d, W // 2, 112,
           "A quake in the Andes, a barrage over Kyiv, a meltdown on Wall Street \u2014 and a pill that erased tumours.",
           serif(15), INK2)
    rule(d, 26, 134, W - 26, 2, INK)


def draw_region_bar(d, y=142):
    x = 26
    total = 35
    names = {"EUROPE": "EUROPE", "N. AMERICA": "N. AMERICA", "GLOBAL": "GLOBAL",
             "ASIA-PAC.": "ASIA-PAC.", "LATIN AM.": "LATIN AM", "MIDDLE EAST": "MID EAST",
             "AFRICA": "AFRICA"}
    for name, n, col in REGIONS:
        w = int(972 * n / total)
        d.rectangle([x, y, x + w - 2, y + 20], fill=col)
        lab = f"{names[name]} {n}"
        f = sans_b(9)
        tw = d.textlength(lab, font=f)
        if tw < w - 6:
            d.text((x + (w - 2 - tw) / 2, y + 5), lab, font=f, fill=(255, 255, 255))
        else:
            d.text((x + (w - 2 - 6) / 2, y + 5), str(n), font=f, fill=(255, 255, 255))
            d.text((x + (w - 2 - d.textlength(names[name], font=f)) / 2, y + 22),
                   names[name], font=f, fill=INK)
        x += w


def draw_numbers(d, y=182):
    text(d, 26, y, "THE DAY IN NUMBERS", sans_b(12), RED)
    rule(d, 26, y + 17, W - 26, 1)
    cw = 972 // 6
    for i, (num, lab) in enumerate(NUMBERS):
        x = 26 + i * cw
        centre(d, x + cw // 2, y + 22, num, serif_b(26), INK)
        for j, ln in enumerate(wrap(d, lab, sans(9), cw - 14)):
            centre(d, x + cw // 2, y + 52 + j * 11, ln, sans(9), INK2)
        if i:
            d.line([(x, y + 22), (x, y + 76)], fill=RULE, width=1)


def draw_timeline(d, y=264):
    text(d, 26, y, "THE DAY IN UTC", sans_b(12), RED)
    rule(d, 26, y + 17, W - 26, 1)
    cw = 972 // 7
    for i, (t, ev) in enumerate(TIMELINE):
        x = 26 + i * cw
        d.ellipse([x + 4, y + 24, x + 12, y + 32], fill=RED)
        text(d, x + 16, y + 22, t, sans_b(11), INK)
        for j, ln in enumerate(wrap(d, ev, sans(9), cw - 12)):
            text(d, x + 4, y + 38 + j * 11, ln, sans(9), INK2)


# ---------------------------------------------------------------- pictures
def pic_quake(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(233, 220, 196))
    d.polygon([(x0, y1), (x0 + 60, y0 + 18), (x0 + 120, y1)], fill=(96, 84, 62))
    d.polygon([(x0 + 90, y1), (x0 + 165, y0 + 8), (x0 + 240, y1)], fill=(70, 60, 44))
    d.polygon([(x0 + 200, y1), (x0 + 260, y0 + 26), (x1, y1)], fill=(120, 104, 74))
    d.line([(x0 + 165, y0 + 8), (x0 + 158, y0 + 30), (x0 + 170, y0 + 48),
            (x0 + 160, y0 + 66), (x0 + 168, y1)], fill=(40, 30, 20), width=3)
    for hx in (x0 + 20, x0 + 52, x0 + 250):
        d.rectangle([hx, y1 - 14, hx + 18, y1], fill=(163, 29, 29))
    d.ellipse([x0 + 285, y0 + 8, x0 + 305, y0 + 28], fill=(240, 200, 90))


def pic_kyiv(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(16, 22, 44))
    for sx, sy in ((30, 12), (90, 26), (150, 8), (210, 20), (260, 12), (120, 34)):
        d.ellipse([x0 + sx, y0 + sy, x0 + sx + 3, y0 + sy + 3], fill=(255, 255, 255))
    for dx, dy in ((40, 40), (110, 30), (180, 44), (240, 34), (290, 48)):
        d.ellipse([x0 + dx, y0 + dy, x0 + dx + 5, y0 + dy + 5], fill=(255, 200, 60))
        d.line([(x0 + dx, y0 + dy + 2), (x0 + dx - 14, y0 + dy + 6)], fill=(255, 120, 40), width=2)
    d.arc([x0 + 20, y1 - 34, x1 - 20, y1], 180, 360, fill=(120, 120, 130), width=4)
    for bx in (60, 130, 200, 260):
        d.line([(x0 + bx, y1 - 22), (x0 + bx, y1)], fill=(120, 120, 130), width=3)
    for fx, fh in ((50, 22), (150, 30), (250, 18)):
        d.polygon([(x0 + fx, y1), (x0 + fx + 10, y1 - fh), (x0 + fx + 20, y1)],
                  fill=(230, 110, 30))
        d.polygon([(x0 + fx + 5, y1), (x0 + fx + 10, y1 - fh + 8), (x0 + fx + 15, y1)],
                  fill=(250, 200, 60))


def pic_nasdaq(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(255, 252, 244))
    for gy in range(y0 + 16, y1, 18):
        d.line([(x0 + 8, gy), (x1 - 8, gy)], fill=(225, 220, 205), width=1)
    pts = [(x0 + 14, y0 + 14), (x0 + 70, y0 + 22), (x0 + 120, y0 + 18),
           (x0 + 170, y0 + 38), (x0 + 220, y0 + 52), (x0 + 265, y0 + 62),
           (x0 + 300, y0 + 78)]
    d.line(pts, fill=RED, width=4)
    d.polygon([(x0 + 300, y0 + 78), (x0 + 288, y0 + 70), (x0 + 290, y0 + 84)],
              fill=RED)


def pic_cop(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=SKY)
    cx, cy, r = (x0 + x1) // 2, (y0 + y1) // 2, 20
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(70, 130, 190))
    d.ellipse([cx - 12, cy - 8, cx - 1, cy + 1], fill=(90, 160, 90))
    d.ellipse([cx + 3, cy + 4, cx + 13, cy + 12], fill=(90, 160, 90))
    d.arc([cx - r, cy - r, cx + r, cy + r], 90, 270, fill=(255, 255, 255), width=2)
    d.line([(cx, cy - r), (cx, cy + r)], fill=(255, 255, 255), width=2)
    d.line([(x0 + 6, y0 + 5), (x1 - 6, y0 + 5)], fill=RED, width=2)


def pic_missile(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(240, 226, 200))
    d.line([(x0 + 10, y1 - 10), (x0 + 38, y0 + 12)], fill=(60, 60, 60), width=4)
    d.polygon([(x0 + 38, y0 + 12), (x0 + 45, y0 + 22), (x0 + 30, y0 + 22)], fill=RED)
    d.rectangle([x0 + 6, y1 - 20, x0 + 46, y1 - 8], fill=(90, 80, 60))
    d.polygon([(x0 + 38, y0 + 26), (x0 + 42, y0 + 16), (x0 + 46, y0 + 26)],
              fill=(250, 180, 40))


def pic_badge(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(238, 232, 214))
    cx, cy = (x0 + x1) // 2 - 4, (y0 + y1) // 2 - 4
    d.polygon([(cx, cy - 18), (cx + 5, cy - 5), (cx + 19, cy - 4), (cx + 8, cy + 5),
               (cx + 12, cy + 18), (cx, cy + 10), (cx - 12, cy + 18), (cx - 8, cy + 5),
               (cx - 19, cy - 4), (cx - 5, cy - 5)], fill=GOLD)
    d.ellipse([x0 + 10, y1 - 14, x0 + 21, y1 - 3], outline=INK, width=2)
    d.ellipse([x0 + 23, y1 - 14, x0 + 34, y1 - 3], outline=INK, width=2)
    d.line([(x0 + 21, y1 - 8), (x0 + 23, y1 - 8)], fill=INK, width=2)


def pic_ship(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=SKY)
    d.rectangle([x0, y0 + 40, x1, y1], fill=(60, 110, 160))
    d.polygon([(x0 + 6, y0 + 38), (x0 + 46, y0 + 38), (x0 + 40, y0 + 50),
               (x0 + 12, y0 + 50)], fill=(40, 40, 50))
    d.rectangle([x0 + 18, y0 + 26, x0 + 34, y0 + 38], fill=(40, 40, 50))
    for sx, sy in ((22, 10), (38, 14), (30, 6)):
        d.ellipse([x0 + sx, y0 + sy, x0 + sx + 7, y0 + sy + 7], fill=(200, 200, 200))
    d.ellipse([x0 + 44, y0 + 6, x0 + 48, y0 + 10], fill=(255, 200, 60))
    d.polygon([(x0 + 44, y0 + 28), (x0 + 47, y0 + 18), (x0 + 50, y0 + 28)],
              fill=(230, 110, 30))


def pic_flags(d, x0, y0, x1, y1):
    import math
    d.rectangle([x0, y0, x1, y1], fill=(238, 232, 214))
    d.rectangle([x0 + 6, y0 + 12, x0 + 24, y0 + 32], fill=(20, 60, 140))
    for a in range(8):
        ax = x0 + 15 + 6 * math.cos(a * 0.785)
        ay = y0 + 22 + 6 * math.sin(a * 0.785)
        d.ellipse([ax - 1, ay - 1, ax + 1, ay + 1], fill=(255, 210, 60))
    d.rectangle([x0 + 30, y0 + 12, x0 + 48, y0 + 22], fill=RED)
    d.rectangle([x0 + 30, y0 + 22, x0 + 48, y0 + 32], fill=(255, 255, 255))
    d.line([(x0 + 15, y0 + 32), (x0 + 15, y0 + 48)], fill=INK, width=2)
    d.line([(x0 + 39, y0 + 32), (x0 + 39, y0 + 48)], fill=INK, width=2)


def pic_cross(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(255, 252, 244))
    d.rectangle([x0 + 20, y0 + 8, x0 + 32, y0 + 46], fill=RED)
    d.rectangle([x0 + 12, y0 + 18, x0 + 42, y0 + 34], fill=RED)


def pic_planet(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(18, 20, 40))
    d.ellipse([x0 + 4, y0 + 4, x0 + 10, y0 + 10], fill=(255, 255, 255))
    d.ellipse([x0 + 44, y0 + 6, x0 + 48, y0 + 10], fill=(255, 255, 255))
    d.ellipse([x0 + 14, y0 + 14, x0 + 40, y0 + 40], fill=(150, 120, 95))
    for cx, cy, cr in ((22, 24, 3), (32, 20, 2), (26, 34, 4), (34, 30, 2)):
        d.ellipse([x0 + cx - cr, y0 + cy - cr, x0 + cx + cr, y0 + cy + cr],
                  fill=(110, 85, 65))
    d.ellipse([x0 + 6, y0 + 8, x0 + 48, y0 + 46], outline=(200, 180, 120), width=1)
    d.rectangle([x0 + 44, y0 + 10, x0 + 49, y0 + 15], fill=(230, 200, 80))


def pic_pill(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(238, 232, 214))
    d.rounded_rectangle([x0 + 6, y0 + 18, x0 + 48, y0 + 38], radius=10, fill=RED)
    d.rounded_rectangle([x0 + 27, y0 + 18, x0 + 48, y0 + 38], radius=10,
                        fill=(255, 255, 255))
    d.rounded_rectangle([x0 + 6, y0 + 18, x0 + 27, y0 + 38], radius=10, fill=RED)
    for dx, dy in ((10, 44), (20, 47), (34, 45)):
        d.ellipse([x0 + dx, y0 + dy, x0 + dx + 3, y0 + dy + 3], fill=(120, 40, 110))


def pic_factory(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(240, 226, 200))
    d.rectangle([x0 + 6, y0 + 28, x0 + 46, y1 - 6], fill=(70, 60, 50))
    d.polygon([(x0 + 6, y0 + 28), (x0 + 16, y0 + 18), (x0 + 26, y0 + 28),
               (x0 + 36, y0 + 18), (x0 + 46, y0 + 28)], fill=(70, 60, 50))
    d.rectangle([x0 + 38, y0 + 8, x0 + 44, y0 + 28], fill=(70, 60, 50))
    for sx, sy in ((38, 2), (43, 5), (34, 6)):
        d.ellipse([x0 + sx, y0 + sy, x0 + sx + 6, y0 + sy + 6], fill=(180, 180, 180))
    d.polygon([(x0 + 18, y1 - 6), (x0 + 23, y1 - 22), (x0 + 28, y1 - 6)],
              fill=(230, 110, 30))


def pic_mic(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(238, 232, 214))
    d.ellipse([x0 + 10, y0 + 8, x0 + 46, y0 + 44], outline=RED, width=2)
    d.ellipse([x0 + 17, y0 + 15, x0 + 39, y0 + 37], outline=RED, width=1)
    d.rounded_rectangle([x0 + 22, y0 + 8, x0 + 36, y0 + 30], radius=7, fill=INK)
    d.line([(x0 + 29, y0 + 30), (x0 + 29, y0 + 44)], fill=INK, width=3)
    d.line([(x0 + 21, y0 + 48), (x0 + 37, y0 + 48)], fill=INK, width=3)


def pic_lock(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(238, 232, 214))
    d.arc([x0 + 18, y0 + 8, x0 + 40, y0 + 30], 180, 360, fill=INK, width=4)
    d.rounded_rectangle([x0 + 13, y0 + 24, x0 + 45, y0 + 48], radius=4, fill=GOLD)
    d.ellipse([x0 + 25, y0 + 31, x0 + 32, y0 + 38], fill=INK)
    d.line([(x0 + 28, y0 + 38), (x0 + 28, y0 + 44)], fill=INK, width=3)


def pic_rover(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(20, 18, 36))
    d.ellipse([x0 + 2, y0 + 34, x0 + 52, y0 + 56], fill=(170, 80, 50))
    d.rectangle([x0 + 16, y0 + 18, x0 + 38, y0 + 32], fill=(200, 200, 200))
    d.line([(x0 + 34, y0 + 18), (x0 + 34, y0 + 10)], fill=(200, 200, 200), width=2)
    d.ellipse([x0 + 32, y0 + 7, x0 + 37, y0 + 12], fill=(200, 200, 200))
    for wx in (18, 28, 38):
        d.ellipse([x0 + wx, y0 + 32, x0 + wx + 7, y0 + 39], fill=(40, 40, 40))


PICS = dict(quake=pic_quake, kyiv=pic_kyiv, nasdaq=pic_nasdaq, cop=pic_cop,
            missile=pic_missile, badge=pic_badge, ship=pic_ship,
            flags=pic_flags, cross=pic_cross, planet=pic_planet,
            pill=pic_pill, factory=pic_factory, mic=pic_mic,
            lock=pic_lock, rover=pic_rover)


# ---------------------------------------------------------------- heroes
def draw_hero(d, h, x, y, w=316, hh=168):
    PICS[h["pic"]](d, x, y, x + w, y + 80)
    d.rectangle([x, y + 80, x + w, y + 80], fill=INK)
    text(d, x, y + 86, f"No. {h['num']}  \u00b7  {h['region']}", sans_b(9), h["colour"])
    ct = f"{h['conf']} \u2013 {h['src']}"
    tw = d.textlength(ct, font=sans(9))
    text(d, x + w - tw, y + 86, ct, sans(9), INK2)
    yy = y + 102
    for ln in wrap(d, h["head"], serif_b(15), w)[:2]:
        text(d, x, yy, ln, serif_b(15), INK)
        yy += 18
    for ln in wrap(d, h["deck"], sans(10), w)[:2]:
        text(d, x, yy, ln, sans(10), INK2)
        yy += 13


def draw_heroes(d, y=332):
    for i, h in enumerate(HEROES):
        draw_hero(d, h, 26 + i * 328, y)
    rule(d, 26, y + 174, W - 26, 1)


# ---------------------------------------------------------------- cards
def draw_card(d, c, x, y, w=237, hh=60):
    d.rectangle([x, y, x + w, y + hh], fill=CARD, outline=RULE)
    PICS[c["pic"]](d, x + 4, y + 4, x + 56, y + 56)
    tx = x + 62
    text(d, tx, y + 3, f"{c['num']}. {c['region']}", sans_b(8), c["colour"])
    ct = f"{c['conf']} \u2013 {c['src']}"
    tw = d.textlength(ct, font=sans(7))
    text(d, x + w - 4 - tw, y + 3, ct, sans(7), INK2)
    yy = y + 15
    for ln in wrap(d, c["head"], sans_b(10), w - 68)[:2]:
        text(d, tx, yy, ln, sans_b(10), INK)
        yy += 12
    for ln in wrap(d, c["deck"], sans(8), w - 68)[:2]:
        text(d, tx, yy, ln, sans(8), INK2)
        yy += 10


def draw_cards(d, y=514):
    for i, c in enumerate(CARDS):
        draw_card(d, c, 26 + (i % 4) * 245, y + (i // 4) * 68)


# ---------------------------------------------------------------- map
CONTINENTS = [
    [(28, 14), (95, 8), (128, 18), (118, 38), (88, 46), (55, 40), (30, 26)],
    [(128, 6), (142, 4), (146, 11), (134, 14)],
    [(105, 60), (132, 56), (146, 68), (138, 92), (120, 100), (108, 78)],
    [(222, 17), (246, 11), (262, 19), (252, 30), (232, 28), (220, 23)],
    [(232, 40), (258, 36), (276, 47), (272, 68), (256, 84), (238, 71), (228, 53)],
    [(268, 12), (360, 6), (420, 15), (432, 29), (405, 45), (360, 51),
     (320, 45), (290, 34), (268, 23)],
    [(385, 60), (405, 59), (408, 67), (388, 69)],
    [(360, 65), (372, 63), (374, 70), (362, 72)],
    [(392, 78), (420, 74), (428, 84), (410, 92), (394, 88)],
]
LAND = (222, 205, 160)


def draw_map(d, x=26, y=736, w=474, hh=114):
    d.rectangle([x, y, x + w, y + hh], fill=(216, 230, 238), outline=RULE)
    for poly in CONTINENTS:
        d.polygon([(x + px, y + py) for px, py in poly], fill=LAND, outline=INK)
    for num, label, px, py in PINS:
        lx, ly = LAB.get(num, (px, py))
        if (lx, ly) != (px, py):
            d.line([(x + px, y + py), (x + lx, y + ly)], fill=INK, width=1)
        d.ellipse([x + px - 2, y + py - 2, x + px + 2, y + py + 2], fill=RED)
        bx, by = x + lx, y + ly
        d.ellipse([bx - 7, by - 7, bx + 7, by + 7], fill=RED, outline=(255, 255, 255))
        centre(d, bx, by - 5, str(num), sans_b(8), (255, 255, 255))
    leg1 = ("1 Jun\u00edn \u00b7 2 Kyiv \u00b7 3 New York \u00b7 4 Antalya \u00b7 5 Bahrain \u00b7 "
            "6 Sinaloa \u00b7 7 Finland \u00b7 8 Jakarta")
    leg2 = ("9 Brazil \u00b7 12 Cikande \u00b7 13 Copenhagen \u00b7 14 Washington \u00b7 15 Mars *")
    text(d, x, y + hh + 4, leg1, sans(8), INK2)
    text(d, x, y + hh + 14, leg2, sans(8), INK2)
    text(d, x, y + hh + 24, "* off-world. 10 BepiColombo + 11 pill trial are global: no pin.",
         sans(8), INK2)


# ---------------------------------------------------------------- also
def draw_also(d, x=512, y=736, w=486, hh=148):
    cols = [ALSO[:10], ALSO[10:]]
    cw = (w - 8) // 2
    for ci, col in enumerate(cols):
        cx = x + ci * (cw + 8)
        yy = y
        for region, item in col:
            lines = wrap(d, item, sans(9), cw - 4)
            text(d, cx, yy, "\u2022", sans_b(9), RED)
            for ln in lines:
                text(d, cx + 10, yy, ln, sans(9), INK)
                yy += 11
            yy += 2


# ---------------------------------------------------------------- bottom
def draw_bottom(d, y=892):
    d.rectangle([26, y, W - 26, y + 72], fill=(238, 228, 200), outline=INK)
    text(d, 36, y + 6, "DATE CHECK \u2014 WHAT WE LEFT OUT ON PURPOSE", sans_b(11), RED)
    left = ("NOT 21 NOV: PIF strike (19 Nov) \u00b7 Nvidia results (17 Nov) \u00b7 "
            "Voyager 1 light-day (18 Nov) \u00b7 Anthropic $81.3bn IPO (19 Nov) \u00b7 "
            "EU \u20ac45bn Ukraine loan (19 Nov).")
    for j, ln in enumerate(wrap(d, left, sans(9), 940)):
        text(d, 36, y + 22 + j * 11, ln, sans(9), INK)
    text(d, 36, y + 48,
         "NOT YET: COP31 final deal (talks run on) \u00b7 Spain votes 29 Nov.",
         sans_b(9), INK)
    text(d, 36, y + 80,
         "Sources: Reuters, AP, AFP, BBC, USGS, ESA, NYSE, France 24, DW, Guardian, NASA.",
         sans(9), INK2)
    text(d, 36, y + 92,
         "CONFIRMED = reported by the named source \u00b7 REPORTED = one side's account, not yet confirmed \u00b7 "
         "CLAIM = an unverified claim.",
         sans(9), INK2)
    centre(d, W // 2, y + 106,
           "Drawn in code \u00b7 35 stories: 3 leads, 12 pictures, 20 briefs \u00b7 7 regions \u00b7 UTC timeline \u00b7 date-checked",
           sans(8), INK2)


# ---------------------------------------------------------------- main
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    draw_header(d)
    draw_region_bar(d)
    draw_numbers(d)
    draw_timeline(d)
    draw_heroes(d)
    draw_cards(d)
    text(d, 26, 718, "WHERE IT HAPPENED \u2014 13 PINS", sans_b(12), RED)
    text(d, 512, 718, "ALSO \u2014 20 MORE STORIES", sans_b(12), RED)
    rule(d, 26, 734, W - 26, 1)
    draw_map(d)
    draw_also(d)
    draw_bottom(d)
    path = os.path.join(OUT, "entry.png")
    img.save(path, "PNG")
    print("wrote", path, img.size, os.path.getsize(path), "bytes")


if __name__ == "__main__":
    main()
