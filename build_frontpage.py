"""Compose the 22 November 2026 front page with Pillow.

The page is a newspaper grid drawn from the STORIES table below.
Every fact was checked on 23 November 2026 against reporting dated
22 November 2026 (the day itself, Sunday):

* Antalya: COP31, the longest climate summit on record, closed two
  days late with no agreement after a draft that omitted any mention
  of fossil fuels was rejected by the EU, Panama and roughly 130
  other parties; the UN climate chief's boss, Secretary-General
  Guterres, pointed to the science.
* Dymer, Kyiv region: a Russian drone wrecked part of a five-storey
  housing block; six deaths were reported across the region and
  fourteen people were listed missing in Dymer, nine were rescued.
* Benghazi: a docked Russian corvette was struck, apparently by a
  Ukrainian sea drone, and was reported sunk; a second vessel was
  attacked afterwards off the same port.
* Washington: a recount in North Carolina pushed the Democratic
  House total to at least 258 seats, a majority unseen since 1992.
* Sinaloa: Mexican special forces arrested Fausto Isidro Meza
  Flores, called El Chapo Isidro, a fugitive on the FBI most-wanted
  list who headed the Beltran Leyva organisation.
* Mercury: BepiColombo, flown jointly by Europe and Japan, arrived
  in orbit eight years after launch.
* The ticker adds Bahrain, Nigeria, South Korea, Indonesia and the
  world chess championship opener in Geneva.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

SIDE = 1024
HERE = Path(__file__).resolve().parent
FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")
INK = (21, 28, 43)
GREY = (71, 85, 105)
PAPER = (255, 255, 255)


def font(filename: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONT_DIR / filename), size)


def serif(size: int):
    return font("DejaVuSerif-Bold.ttf", size)


def bold(size: int):
    return font("DejaVuSans-Bold.ttf", size)


def plain(size: int):
    return font("DejaVuSans.ttf", size)


def lines_for(draw: ImageDraw.ImageDraw, text: str, fnt, max_width: int) -> list:
    """Split text into lines that each fit inside max_width pixels."""
    result: list = []
    current = ""
    for word in text.split(" "):
        trial = word if not current else current + " " + word
        if fnt.getlength(trial) <= max_width:
            current = trial
        else:
            result.append(current)
            current = word
    if current:
        result.append(current)
    return result


def panel(draw, box, colour, kicker, headline, body, headline_size=25):
    """Draw one story: coloured kicker band, headline, then body text."""
    left, top, right, bottom = box
    draw.rectangle(box, outline=(110, 125, 145), width=2)
    draw.rectangle([left, top, right, top + 34], fill=colour)
    draw.text((left + 12, top + 6), kicker, font=bold(19), fill="white")
    y = top + 47
    for row in lines_for(draw, headline, bold(headline_size), right - left - 24):
        draw.text((left + 12, y), row, font=bold(headline_size), fill=INK)
        y += headline_size + 5
    y += 2
    for row in lines_for(draw, body, plain(18), right - left - 24):
        draw.text((left + 12, y), row, font=plain(18), fill=GREY)
        y += 23


STORIES = [
    ((24, 442, 512, 620), (30, 64, 175), "UKRAINE  -  WAR",
     "Drone hits Kyiv block: 14 missing",
     "A Russian drone partly destroyed a five-storey block in Dymer, north of Kyiv. At least six died across the region; nine were rescued."),
    ((512, 442, 1000, 620), (194, 65, 12), "LIBYA  -  WAR AT SEA",
     "Russian warship hit at Benghazi",
     "A Russian corvette docked at Benghazi was hit by a suspected Ukrainian sea drone and reportedly sank. A second ship was then targeted off the port."),
    ((24, 632, 512, 810), (71, 85, 105), "UNITED STATES  -  POLITICS",
     "Democrats win 258 House seats",
     "A North Carolina recount gave Democrats at least 258 seats, their largest House majority since 1992. Incoming Speaker Jeffries pledges focus on costs and health care."),
    ((512, 632, 1000, 810), (4, 120, 87), "MEXICO  -  CARTEL ARREST",
     "Cartel boss 'El Chapo Isidro' captured",
     "Special forces seized Fausto Isidro Meza Flores, an FBI ten-most-wanted fugitive and Beltran Leyva cartel leader, in a Sinaloa operation."),
    ((24, 822, 1000, 930), (8, 145, 178), "SPACE  -  GOOD NEWS",
     "BepiColombo enters orbit around Mercury",
     "After an eight-year journey, the Europe-Japan probe slipped into orbit around Mercury."),
]

TICKER = (
    "ALSO TODAY:  Iran strike on a Bahrain civilian site wounds 2 - Gulf states condemn  |  "
    "Nigeria funeral boat capsizes: 24 dead  |  South Korea education minister quits over AI cheating  |  "
    "Indonesia candy factory fire: 3 dead, dozens missing  |  Gukesh opens world chess title defence in Geneva"
)


def build() -> Path:
    canvas = Image.new("RGB", (SIDE, SIDE), PAPER)
    draw = ImageDraw.Draw(canvas)

    draw.rectangle([0, 0, SIDE, 118], fill=INK)
    draw.text((SIDE // 2, 14), "THE WORLD TODAY", font=serif(58), fill="white", anchor="ma")
    draw.text((SIDE // 2, 84), "Sunday  22 November 2026  -  The whole day in one page",
              font=plain(20), fill=(203, 213, 225), anchor="ma")
    draw.line([24, 130, SIDE - 24, 130], fill=INK, width=3)

    draw.rectangle([24, 142, SIDE - 24, 430], fill=(254, 242, 242), outline=(185, 28, 28), width=3)
    draw.text((SIDE // 2, 154), "CLIMATE SUMMIT COLLAPSES", font=bold(21), fill=(185, 28, 28), anchor="ma")
    draw.text((SIDE // 2, 184), "COP31 ends with", font=serif(52), fill=INK, anchor="ma")
    draw.text((SIDE // 2, 242), "NO DEAL AT ALL", font=serif(58), fill=(185, 28, 28), anchor="ma")
    lead = ("Antalya, Turkiye - The longest COP on record ended on Sunday with no agreement, "
            "two days into overtime. The EU, Panama and about 130 parties rejected a draft "
            "that never mentioned fossil fuels. UN chief Guterres: no ambiguity in the science.")
    y = 312
    for row in lines_for(draw, lead, plain(20), SIDE - 96):
        draw.text((SIDE // 2, y), row, font=plain(20), fill=GREY, anchor="ma")
        y += 26

    for box, colour, kicker, headline, body in STORIES:
        size = 23 if box[2] - box[0] > 600 else 25
        panel(draw, box, colour, kicker, headline, body, headline_size=size)

    draw.rectangle([0, 942, SIDE, SIDE], fill=INK)
    y = 950
    for row in lines_for(draw, TICKER, bold(17), SIDE - 40):
        draw.text((20, y), row, font=bold(17), fill=(253, 224, 71))
        y += 22

    target = HERE / "entry.png"
    canvas.save(target)
    print("saved", target, target.stat().st_size)
    small = canvas.quantize(colors=256, method=Image.MEDIANCUT)
    small.save(target, optimize=True)
    print("quantized", target.stat().st_size, Image.open(target).size)
    return target


if __name__ == "__main__":
    build()
