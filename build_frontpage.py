"""Build THE WORLD TODAY front page for 22 Nov 2026, entirely with PIL.

Stories verified fresh on 2026-11-23 against 22 Nov 2026 reporting:
- Centre: COP31 in Antalya ends with no deal on Sunday 22 Nov, the
  longest COP on record, two days into overtime. The EU, Panama and
  about 130 parties rejected a draft that never mentioned fossil
  fuels. UN chief Guterres: no ambiguity in the science.
- Ukraine: a Russian drone partly destroyed a five-storey block in
  Dymer, north of Kyiv, on Sunday. Ukraine said at least six were
  killed across the Kyiv region; Zelensky said 14 were missing in
  Dymer and rescuers evacuated nine, including a child.
- Libya: eastern authorities said a Russian corvette docked at
  Benghazi was hit by a suspected Ukrainian sea drone on Sunday;
  reports said it sank. A second, Maltese-flagged ship was targeted.
- United States: Democrat Chuck Hubbard beat Virginia Foxx in North
  Carolina after a recount, giving Democrats at least 258 House
  seats, their largest majority since 1992.
- Mexico: special forces captured Fausto Isidro Meza Flores,
  'El Chapo Isidro', an FBI ten-most-wanted fugitive who led the
  Beltran Leyva cartel, in Sinaloa.
- Space: the Europe-Japan BepiColombo probe entered orbit around
  Mercury after an eight-year journey launched in 2018.
- Indonesia: a candy factory fire in Banten left 3 dead and dozens
  missing; rescuers searched the burnt-out plant for workers.
Ticker: Iran strike on a Bahrain civilian site wounds two, Gulf
states condemn; Nigeria funeral boat capsizes, 24 dead; South
Korea education minister resigns over an AI cheating scandal;
Gukesh opens his world chess title defence against Sindarov.
"""
from PIL import Image, ImageDraw, ImageFont
import os

W = H = 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
FD = "/usr/share/fonts/truetype/dejavu"
def F(name, size): return ImageFont.truetype(os.path.join(FD, name), size)
SERIF_B = lambda s: F("DejaVuSerif-Bold.ttf", s)
SANS_B = lambda s: F("DejaVuSans-Bold.ttf", s)
SANS = lambda s: F("DejaVuSans.ttf", s)

img = Image.new("RGB", (W, H), "white")
d = ImageDraw.Draw(img)

# Masthead
d.rectangle([0, 0, W, 118], fill=(15, 23, 42))
d.text((W//2, 14), "THE WORLD TODAY", font=SERIF_B(58), fill="white", anchor="ma")
d.text((W//2, 84), "Sunday  22 November 2026  -  The day in one page", font=SANS(20), fill=(203, 213, 225), anchor="ma")
d.line([24, 130, W-24, 130], fill=(15, 23, 42), width=3)

def wrap(draw, text, font, width):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if draw.textlength(t, font=font) <= width: cur = t
        else: lines.append(cur); cur = w_
    if cur: lines.append(cur)
    return lines

def story(x, y, w, h, colour, kicker, headline, body, font_h=25):
    d.rectangle([x, y, x+w, y+h], outline=(100, 116, 139), width=2)
    d.rectangle([x, y, x+w, y+34], fill=colour)
    d.text((x+12, y+6), kicker, font=SANS_B(19), fill="white")
    cy = y + 46
    for ln in wrap(d, headline, SANS_B(font_h), w-24):
        d.text((x+12, cy), ln, font=SANS_B(font_h), fill=(15, 23, 42)); cy += font_h + 5
    cy += 2
    for ln in wrap(d, body, SANS(18), w-24):
        d.text((x+12, cy), ln, font=SANS(18), fill=(51, 65, 85)); cy += 23
    return cy

# Centre story - COP31 collapse on Sunday 22 Nov
d.rectangle([24, 142, W-24, 430], fill=(254, 242, 242), outline=(185, 28, 28), width=3)
d.text((W//2, 154), "CLIMATE SUMMIT COLLAPSES", font=SANS_B(21), fill=(185, 28, 28), anchor="ma")
d.text((W//2, 184), "COP31 ends with", font=SERIF_B(52), fill=(15, 23, 42), anchor="ma")
d.text((W//2, 242), "NO DEAL AT ALL", font=SERIF_B(58), fill=(185, 28, 28), anchor="ma")
body = ("Antalya, Turkiye - The longest COP on record ended on Sunday with no agreement, "
        "two days into overtime. The EU, Panama and about 130 parties rejected a draft "
        "that never mentioned fossil fuels. UN chief Guterres: no ambiguity in the science.")
cy = 312
for ln in wrap(d, body, SANS(20), W-96):
    d.text((W//2, cy), ln, font=SANS(20), fill=(51, 65, 85), anchor="ma"); cy += 26

# Grid of four
story(24, 442, 488, 178, (30, 64, 175), "UKRAINE  -  WAR",
      "Drone hits Kyiv block: 14 missing",
      "A Russian drone partly destroyed a five-storey block in Dymer, north of Kyiv. At least six died across the region; nine were rescued.")
story(512, 442, 488, 178, (194, 65, 12), "LIBYA  -  WAR AT SEA",
      "Russian warship hit at Benghazi",
      "A Russian corvette docked at Benghazi was hit by a suspected Ukrainian sea drone and reportedly sank. A second ship was then targeted off the port.")
story(24, 632, 488, 178, (71, 85, 105), "UNITED STATES  -  POLITICS",
      "Democrats win 258 House seats",
      "A North Carolina recount gave Democrats at least 258 seats, their largest House majority since 1992. Incoming Speaker Jeffries pledges focus on costs and health care.")
story(512, 632, 488, 178, (4, 120, 87), "MEXICO  -  CARTEL ARREST",
      "Cartel boss 'El Chapo Isidro' captured",
      "Special forces seized Fausto Isidro Meza Flores, an FBI ten-most-wanted fugitive and Beltran Leyva cartel leader, in a Sinaloa operation.")
# Wide story
story(24, 822, 976, 108, (8, 145, 178), "SPACE  -  GOOD NEWS",
      "BepiColombo enters orbit around Mercury",
      "After an eight-year journey, the Europe-Japan probe slipped into orbit around Mercury.", font_h=23)

# Ticker
d.rectangle([0, 942, W, H], fill=(15, 23, 42))
ticker = "ALSO TODAY:  Iran strike on a Bahrain civilian site wounds 2 - Gulf states condemn  |  Nigeria funeral boat capsizes: 24 dead  |  South Korea education minister quits over AI cheating  |  Indonesia candy factory fire: 3 dead, dozens missing  |  Gukesh opens world chess title defence in Geneva"
cy = 950
for ln in wrap(d, ticker, SANS_B(17), W-40):
    d.text((20, cy), ln, font=SANS_B(17), fill=(253, 224, 71)); cy += 22

img.save(OUT)
print("saved", OUT, os.path.getsize(OUT))
q = img.quantize(colors=256, method=Image.MEDIANCUT)
q.save(OUT, optimize=True)
print("quantized", os.path.getsize(OUT), Image.open(OUT).size)
