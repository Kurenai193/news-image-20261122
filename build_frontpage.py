"""Build entry.png (v2): Sunday 22 November 2026 as a dense newspaper page.

Thirty-five dated stories in six regions, arranged the way the day's
best front pages are: a date-first masthead, a band of the day's big
numbers, a region tally, a UTC timeline, three illustrated lead cards,
twelve small illustrated cards, a pinned world map, a DATE CHECK box
listing older stories deliberately left out, and a numbered also-list.

Facts were checked on 23 November 2026 against that day's reporting:
COP31 in Antalya ends with no deal (Le Monde, AP); Ukraine's air force
counts 186 Russian drones fired overnight and 161 downed or jammed,
with a collapsed block in Dymer and 14 missing (Ukrinform); Iran's IRGC
claims two US Patriot radars struck in Bahrain while Bahrain reports a
civilian site fire in Sitra and two injured, and a US official reports
no US damage (Al Jazeera, Reuters) - labelled CLAIM; a suspected sea
drone hits a Russian corvette at Benghazi; Democrats reach 258 US House
seats after a North Carolina recount; cartel leader El Chapo Isidro is
captured in Sinaloa in a raid that left 11 dead (AP); BepiColombo
reaches Mercury; Liverpool beat ten-man Manchester United 4-0 at
Anfield (Reuters); Alcaraz beats Zverev 6-2 7-6 in the ATP Finals in
Turin (Reuters); a Banten candy factory fire leaves 3 dead and 36
missing; a Nigeria funeral boat toll rises to 24; South Korea's
education minister resigns over AI cheating; Gukesh opens his chess
title defence in Geneva; a Russian cargo ship burns in the Baltic;
settlers torch vehicles and homes in the West Bank. The twenty
also-list items are one-line versions of the same day's reporting.
Deterministic: the same bytes come out on every run.
"""

from pathlib import Path
import textwrap

from PIL import Image, ImageDraw, ImageFont

SIDE = 1024
EDGE = 28
WIDE = SIDE - 2 * EDGE
PAPER = (246, 241, 230)
NAVY = (19, 34, 58)
INK = (30, 30, 30)
RED = (176, 32, 48)
GOLD = (198, 148, 42)
TEAL = (38, 110, 110)
GREY = (105, 105, 100)
CARD = (255, 253, 247)
SKY = (24, 42, 74)

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")


def face(name: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONT_DIR / name), size)


def serif(size: int):
    return face("DejaVuSerif-Bold.ttf", size)


def bold(size: int):
    return face("DejaVuSans-Bold.ttf", size)


def plain(size: int):
    return face("DejaVuSans.ttf", size)


def wrap(text: str, font, width: int) -> list[str]:
    probe = ImageDraw.Draw(Image.new("RGB", (8, 8)))
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = f"{cur} {word}".strip()
        if probe.textlength(trial, font=font) <= width:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


# ---------------------------------------------------------------- icons
def icon(d: ImageDraw.ImageDraw, kind: str, x: int, y: int, s: int) -> None:
    """Tiny flat pictograms, one per small card, drawn from primitives."""
    c = NAVY
    if kind == "ship":
        d.polygon([(x + 4, y + s - 10), (x + s - 4, y + s - 10), (x + s - 12, y + s - 2), (x + 12, y + s - 2)], fill=c)
        d.rectangle([x + s // 2 - 2, y + 6, x + s // 2 + 2, y + s - 12], fill=c)
        d.polygon([(x + s // 2 + 4, y + 8), (x + s // 2 + 4, y + s - 14), (x + s - 10, y + s - 14)], fill=RED)
    elif kind == "capitol":
        d.polygon([(x + 4, y + 12), (x + s - 4, y + 12), (x + s // 2, y + 3)], fill=c)
        for i in range(4):
            cx = x + 9 + i * (s - 18) // 3
            d.rectangle([cx - 2, y + 15, cx + 2, y + s - 10], fill=c)
        d.rectangle([x + 4, y + s - 8, x + s - 4, y + s - 4], fill=c)
    elif kind == "badge":
        d.ellipse([x + 8, y + 4, x + s - 8, y + s - 12], outline=c, width=3)
        d.polygon([(x + s // 2, y + 12), (x + s // 2 + 5, y + 22), (x + s // 2 + 12, y + 22),
                   (x + s // 2 + 7, y + 28), (x + s // 2 + 9, y + 36), (x + s // 2, y + 31),
                   (x + s // 2 - 9, y + 36), (x + s // 2 - 7, y + 28), (x + s // 2 - 12, y + 22),
                   (x + s // 2 - 5, y + 22)], fill=GOLD)
    elif kind == "planet":
        d.ellipse([x + 10, y + 12, x + s - 10, y + s - 12], fill=TEAL)
        d.ellipse([x + 4, y + s // 2 - 3, x + s - 4, y + s // 2 + 3], outline=GOLD, width=3)
        d.ellipse([x + 18, y + 18, x + 26, y + 26], fill=PAPER)
    elif kind == "ball":
        d.ellipse([x + 6, y + 6, x + s - 6, y + s - 6], outline=c, width=3)
        d.polygon([(x + s // 2, y + 14), (x + s // 2 + 8, y + 22), (x + s // 2 + 5, y + 32),
                   (x + s // 2 - 5, y + 32), (x + s // 2 - 8, y + 22)], fill=c)
    elif kind == "trophy":
        d.polygon([(x + 14, y + 6), (x + s - 14, y + 6), (x + s - 18, y + 26), (x + 18, y + 26)], fill=GOLD)
        d.arc([x + 4, y + 6, x + 20, y + 24], 90, 270, fill=GOLD, width=3)
        d.arc([x + s - 20, y + 6, x + s - 4, y + 24], 270, 90, fill=GOLD, width=3)
        d.rectangle([x + s // 2 - 2, y + 26, x + s // 2 + 2, y + 34], fill=c)
        d.rectangle([x + 12, y + 34, x + s - 12, y + 38], fill=c)
    elif kind == "flame":
        d.polygon([(x + s // 2, y + 2), (x + s - 10, y + s - 14), (x + s - 16, y + s - 4),
                   (x + 16, y + s - 4), (x + 10, y + s - 14)], fill=RED)
        d.polygon([(x + s // 2, y + 18), (x + s - 18, y + s - 10), (x + 18, y + s - 10)], fill=GOLD)
    elif kind == "boat":
        d.polygon([(x + 4, y + s - 14), (x + s - 4, y + s - 14), (x + s - 12, y + s - 4), (x + 12, y + s - 4)], fill=c)
        d.rectangle([x + s // 2 - 2, y + 8, x + s // 2 + 2, y + s - 16], fill=c)
        d.polygon([(x + s // 2 + 4, y + 10), (x + s // 2 + 4, y + s - 18), (x + s - 12, y + s - 18)], fill=TEAL)
    elif kind == "book":
        d.rectangle([x + 8, y + 6, x + s // 2, y + s - 6], outline=c, width=3)
        d.rectangle([x + s // 2, y + 6, x + s - 8, y + s - 6], outline=c, width=3)
        d.line([x + 13, y + 14, x + s // 2 - 5, y + 14], fill=RED, width=2)
        d.line([x + s // 2 + 5, y + 22, x + s - 13, y + 22], fill=GREY, width=2)
    elif kind == "knight":
        d.polygon([(x + 14, y + s - 6), (x + 14, y + 22), (x + 20, y + 12), (x + 30, y + 6),
                   (x + 38, y + 12), (x + 32, y + 18), (x + 38, y + 26), (x + 30, y + 30),
                   (x + 30, y + s - 6)], fill=c)
        d.ellipse([x + 22, y + 10, x + 28, y + 16], fill=PAPER)
    elif kind == "waves":
        for r in range(3):
            yy = y + 14 + r * 10
            d.arc([x + 4, yy - 6, x + 24, yy + 6], 0, 180, fill=TEAL, width=3)
            d.arc([x + 22, yy - 6, x + 42, yy + 6], 180, 360, fill=TEAL, width=3)
    elif kind == "torch":
        d.polygon([(x + s // 2, y + 2), (x + s - 12, y + 20), (x + s // 2 + 4, y + 26),
                   (x + s // 2 - 4, y + 26), (x + 12, y + 20)], fill=RED)
        d.rectangle([x + s // 2 - 3, y + 26, x + s // 2 + 3, y + s - 4], fill=c)


# ------------------------------------------------------------- big art
def art_cop(d: ImageDraw.ImageDraw, x: int, y: int, w: int, h: int) -> None:
    d.rectangle([x, y, x + w, y + h], fill=(214, 226, 235))
    d.ellipse([x + w // 2 - 34, y + 8, x + w // 2 + 34, y + 76], fill=GOLD)
    d.ellipse([x + w // 2 - 34, y + 8, x + w // 2 + 34, y + 76], outline=TEAL, width=3)
    d.line([x + w // 2 - 34, y + 42, x + w // 2 + 34, y + 42], fill=TEAL, width=2)
    d.rectangle([x + 18, y + h - 34, x + w - 18, y + h - 20], fill=(122, 84, 50))
    flags = [RED, TEAL, GOLD, NAVY, (90, 140, 70), (150, 90, 160)]
    for i, col in enumerate(flags):
        fx = x + 30 + i * (w - 60) // 5
        d.line([fx, y + h - 58, fx, y + h - 34], fill=INK, width=2)
        d.polygon([(fx, y + h - 58), (fx + 14, y + h - 52), (fx, y + h - 46)], fill=col)
    d.line([x + 8, y + h - 8, x + w - 8, y + h - 8], fill=RED, width=4)


def art_ukr(d: ImageDraw.ImageDraw, x: int, y: int, w: int, h: int) -> None:
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    for sx, sy in [(30, 16), (90, 8), (170, 20), (250, 12), (290, 26)]:
        d.ellipse([x + sx, y + sy, x + sx + 3, y + sy + 3], fill=(240, 240, 220))
    for i in range(4):
        dx, dy = x + 36 + i * 62, y + 26 + (i % 2) * 16
        d.line([dx - 12, dy, dx + 12, dy], fill=(230, 230, 230), width=3)
        d.line([dx, dy - 6, dx, dy + 6], fill=(230, 230, 230), width=3)
        d.line([dx + 12, dy, dx + 26, dy + 22], fill=RED, width=2)
    d.polygon([(x + w - 74, y + h - 8), (x + w - 52, y + h - 44), (x + w - 30, y + h - 8)], outline=GOLD, width=3)
    d.rectangle([x + 10, y + h - 16, x + 120, y + h - 8], fill=(10, 20, 40))
    d.rectangle([x + 130, y + h - 22, x + 210, y + h - 8], fill=(10, 20, 40))


def art_bah(d: ImageDraw.ImageDraw, x: int, y: int, w: int, h: int) -> None:
    d.rectangle([x, y, x + w, y + h], fill=(233, 220, 196))
    cx, cy = x + 74, y + h - 18
    d.line([cx - 26, cy, cx, cy - 52], fill=NAVY, width=4)
    d.line([cx + 26, cy, cx, cy - 52], fill=NAVY, width=4)
    d.ellipse([cx - 30, cy - 78, cx + 30, cy - 46], fill=TEAL)
    for r in (16, 26, 36):
        d.arc([cx + 30, cy - 70 - r // 2, cx + 30 + r * 2, cy - 70 + r // 2 + r], -60, 60, fill=RED, width=3)
    d.line([x + w - 70, y + 12, cx + 44, cy - 62], fill=RED, width=3)
    d.polygon([(x + w - 78, y + 6), (x + w - 60, y + 10), (x + w - 70, y + 20)], fill=RED)
    d.rectangle([x, y + h - 10, x + w, y + h], fill=TEAL)


MAP_ROWS = [
    "                                                                      ",
    "      #####    #        #########   ################################  ",
    "    ##########           ##############################  ##########   ",
    "     ########     ##      ###################  #################      ",
    "      ######               ################    ##############  ##     ",
    "       #####   ###          #############       ###########           ",
    "        ###     ##           ##########          ########    ###      ",
    "        ##      #             ########            ######              ",
    "         #                     ######    ##        ####     #         ",
    "                                ####    ####       ##                 ",
    "                                 ##    ######     ###                 ",
    "                                      ########   ####                 ",
    "                                       ######     ##        #         ",
    "                                        ####                    ##    ",
    "                                        ###                            ",
    "                                         #                             ",
]

PINS = [(0.535, 0.24, "2"), (0.548, 0.35, "1"), (0.605, 0.44, "3"), (0.515, 0.42, "4"),
        (0.155, 0.30, "5"), (0.105, 0.44, "6"), (0.475, 0.27, "9"), (0.80, 0.33, "12")]


def world_map(d: ImageDraw.ImageDraw, x: int, y: int, w: int, h: int) -> None:
    d.rectangle([x, y, x + w, y + h], fill=(226, 233, 238))
    rows, cols = len(MAP_ROWS), len(MAP_ROWS[0])
    for r, row in enumerate(MAP_ROWS):
        for cidx, ch in enumerate(row):
            if ch == "#":
                px = x + 8 + cidx * (w - 16) // cols
                py = y + 6 + r * (h - 12) // rows
                d.ellipse([px, py, px + 4, py + 4], fill=(120, 140, 155))
    for fx, fy, num in PINS:
        px, py = x + int(fx * w), y + int(fy * h)
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED)
        d.text((px, py), num, font=bold(11), fill=(255, 255, 255), anchor="mm")


# ---------------------------------------------------------------- data
BIG = [
    ("ANTALYA · CLIMATE", "COP31 ENDS WITH NO DEAL",
     "The longest COP on record ran two days into overtime and still ended with no deal: the EU and 130 parties rejected a draft silent on fossil fuels.",
     "Le Monde · AP", "REPORTED", art_cop),
    ("KYIV · WAR", "186 DRONES IN ONE NIGHT",
     "Russia fired 186 attack drones overnight; Ukraine says 161 were downed or jammed, hits at 18 locations. In Dymer a block collapsed: 14 missing.",
     "Ukrinform · Air Force", "REPORTED", art_ukr),
    ("BAHRAIN · GULF", "IRAN CLAIMS RADAR HIT",
     "The IRGC says it struck two US Patriot radars at Al-Riffa and Awali. Bahrain reports a civilian fire in Sitra, two injured; the US says its forces were not hit.",
     "Al Jazeera · Reuters", "CLAIM", art_bah),
]

SMALL = [
    ("ship", "BENGHAZI, LIBYA", "Sea drone hits Russian corvette in port", "REPORTED"),
    ("capitol", "WASHINGTON", "Democrats reach 258 House seats", "REPORTED"),
    ("badge", "SINALOA, MEXICO", "Cartel boss 'El Chapo Isidro' captured", "REPORTED"),
    ("planet", "MERCURY", "BepiColombo arrives after 8-year cruise", "REPORTED"),
    ("ball", "ANFIELD", "Liverpool rout 10-man United 4-0", "REPORTED"),
    ("trophy", "TURIN", "Alcaraz beats Zverev for ATP Finals title", "REPORTED"),
    ("flame", "BANTEN, INDONESIA", "Candy factory fire: 3 dead, 36 missing", "REPORTED"),
    ("boat", "NIGERIA", "Funeral boat capsizes, toll rises to 24", "REPORTED"),
    ("book", "SEOUL", "Education minister quits over AI cheating", "REPORTED"),
    ("knight", "GENEVA", "Gukesh opens chess title defence", "REPORTED"),
    ("waves", "BALTIC SEA", "Russian cargo ship ablaze after strike", "REPORTED"),
    ("torch", "WEST BANK", "Settlers torch 12 vehicles and homes", "REPORTED"),
]

ALSO = [
    "EU & Indonesia sign trade deal; tariffs cut on 98.5% of goods",
    "Delta glitch delays hundreds of flights at Atlanta",
    "China eases margin rules: minimum ratio 100% to 80%",
    "US seeks answers on Nvidia AI chip sales to China",
    "Iran unveils underground 'missile city' facility",
    "Tankers struck and ablaze near Strait of Hormuz",
    "India: 11 dead, 180+ hospitalised after illicit alcohol",
    "France: sixth weekend of living-cost protests",
    "Brazil town clears rubble after deadly storm",
    "Istanbul: thousands march over seizure of Sozcu TV",
    "UK and EU seek closer ties in post-Brexit pact",
    "Delhi forum ends with no formal India-Pakistan talks",
    "US intel chief: Putin 'not America's friend'",
    "Myanmar junta calls ASEAN decision 'unfair'",
    "Trump's calls to Kim Jong Un go unanswered - report",
    "Youth Congress protests at Meta offices in India",
    "Taiwan cautions Canada over China economic ties",
    "Seoul Metro named among world's 18 best subways",
    "Russia claims 170 Ukrainian drones downed overnight",
    "Arribage & Olivetti take ATP Finals doubles crown",
]

NUMBERS = [("186", "drones fired at Ukraine"), ("161", "downed or jammed"),
           ("258", "US House seats, Democrats"), ("36", "missing after Banten fire"),
           ("11", "killed in Sinaloa raid"), ("8", "years BepiColombo travelled")]


def chip(d, x, y, text, fill):
    wpx = int(d.textlength(text, font=bold(10))) + 12
    d.rectangle([x, y, x + wpx, y + 16], fill=fill)
    d.text((x + 6, y + 2), text, font=bold(10), fill=(255, 255, 255))
    return wpx


def build() -> Path:
    img = Image.new("RGB", (SIDE, SIDE), PAPER)
    d = ImageDraw.Draw(img)

    d.rectangle([0, 0, SIDE, 26], fill=NAVY)
    d.text((EDGE, 5), "THE WORLD IN ONE DAY", font=bold(14), fill=(255, 255, 255))
    d.text((SIDE - EDGE, 5), "ONE PAGE · THE WHOLE PLANET", font=bold(14),
           fill=(255, 255, 255), anchor="ra")

    d.text((SIDE // 2, 34), "35 STORIES · 6 REGIONS · EVERY ONE DATED", font=bold(16),
           fill=RED, anchor="ma")
    d.text((SIDE // 2, 54), "SUNDAY 22 NOVEMBER 2026", font=serif(52), fill=NAVY, anchor="ma")
    d.line([EDGE, 122, SIDE - EDGE, 122], fill=RED, width=3)

    d.rectangle([EDGE, 130, SIDE - EDGE, 186], fill=NAVY)
    colw = WIDE // 6
    for i, (num, label) in enumerate(NUMBERS):
        cx = EDGE + i * colw + colw // 2
        d.text((cx, 136), num, font=serif(30), fill=(255, 255, 255), anchor="ma")
        for j, ln in enumerate(wrap(label, plain(10), colw - 10)):
            d.text((cx, 168 + j * 0), ln, font=plain(10), fill=(205, 215, 230), anchor="ma")
            break

    d.text((EDGE, 194), "EUROPE 11 · MIDDLE EAST 4 · AMERICAS 6 · ASIA-PACIFIC 10 · AFRICA 2 · WORLD 2",
           font=bold(14), fill=NAVY)
    d.text((EDGE, 216), "THE DAY IN UTC — 02:11 IRGC claims Bahrain radars · 06:00 Kyiv tally: 161 of 186 downed · 16:30 Liverpool 4-0 United · EVENING COP31 closes, no deal",
           font=plain(12), fill=GREY)

    # big three
    bw = (WIDE - 16) // 3
    by = 240
    for i, (kick, head, body, src, label, art) in enumerate(BIG):
        x = EDGE + i * (bw + 8)
        d.rectangle([x, by, x + bw, by + 238], fill=CARD, outline=NAVY, width=1)
        art(d, x + 6, by + 6, bw - 12, 92)
        d.text((x + 10, by + 104), kick, font=bold(11), fill=RED)
        for j, ln in enumerate(wrap(head, serif(19), bw - 20)):
            d.text((x + 10, by + 120 + j * 23), ln, font=serif(19), fill=NAVY)
        lines = wrap(body, plain(11), bw - 20)
        for j, ln in enumerate(lines[:4]):
            d.text((x + 10, by + 166 + j * 14), ln, font=plain(11), fill=INK)
        wpx = chip(d, x + 10, by + 214, label, RED if label == "CLAIM" else TEAL)
        d.text((x + 16 + wpx, by + 216), src, font=plain(10), fill=GREY)

    # small twelve
    sy = 490
    cw = (WIDE - 24) // 4
    for idx, (kind, place, head, label) in enumerate(SMALL):
        x = EDGE + (idx % 4) * (cw + 8)
        y = sy + (idx // 4) * 78
        d.rectangle([x, y, x + cw, y + 70], fill=CARD, outline=(190, 185, 170), width=1)
        icon(d, kind, x + 8, y + 10, 48)
        d.text((x + 64, y + 8), place, font=bold(10), fill=RED)
        for j, ln in enumerate(wrap(head, bold(12), cw - 72)[:3]):
            d.text((x + 64, y + 22 + j * 15), ln, font=bold(12), fill=INK)
        d.text((x + 64, y + 56), label, font=plain(9), fill=TEAL)

    # map + date check
    my = 730
    world_map(d, EDGE, my, 560, 108)
    d.text((EDGE + 6, my + 88), "WHERE IT HAPPENED — 1 Antalya 2 Kyiv 3 Bahrain 4 Benghazi 5 Washington 6 Sinaloa 9 Anfield 12 Seoul",
           font=plain(9), fill=NAVY)
    bx = EDGE + 572
    d.rectangle([bx, my, SIDE - EDGE, my + 108], fill=(252, 240, 238), outline=RED, width=2)
    d.text((bx + 10, my + 8), "DATE CHECK — LEFT OUT ON PURPOSE", font=bold(13), fill=RED)
    note = ("Shenzhen trilateral summit (19-20 Nov) · US stock correction (Fri 20 Nov) · "
            "148-drone attack (night 20-21 Nov). Every story on this page happened on, "
            "or was reported on, Sunday 22 November 2026.")
    for j, ln in enumerate(wrap(note, plain(11), SIDE - EDGE - bx - 20)):
        d.text((bx + 10, my + 30 + j * 15), ln, font=plain(11), fill=INK)

    # also list
    ay = 850
    d.rectangle([EDGE, ay, SIDE - EDGE, ay + 24], fill=NAVY)
    d.text((EDGE + 10, ay + 4), "ALSO ON SUNDAY 22 NOVEMBER — 20 MORE STORIES", font=bold(14),
           fill=(255, 255, 255))
    half = (len(ALSO) + 1) // 2
    for col in range(2):
        x = EDGE + col * (WIDE // 2 + 4)
        for r, item in enumerate(ALSO[col * half:(col + 1) * half]):
            num = col * half + r + 16
            d.text((x, ay + 29 + r * 12), f"{num}. {item}", font=plain(11), fill=INK)

    d.line([EDGE, 1002, SIDE - EDGE, 1002], fill=GREY, width=1)
    d.text((EDGE, 1006), "Sources: Reuters · AP · AFP · Al Jazeera · Ukrinform · Le Monde · ATP · LFC   |   REPORTED = reported that day by named outlets · CLAIM = one side's claim, not independently verified",
           font=plain(9), fill=GREY)

    out = Path(__file__).resolve().parent / "entry.png"
    img.save(out, optimize=True)
    print("saved", out, out.stat().st_size)
    small = img.quantize(colors=256, method=Image.MEDIANCUT)
    small.save(out, optimize=True)
    print("quantized", out.stat().st_size, img.size)
    return out


if __name__ == "__main__":
    build()
