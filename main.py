"""news-image-20261122 entry: copy the bundled front-page image to the output.

The image (entry.png, beside this file) sums up the world news of Sunday
22 November 2026 in one front page: COP31 ends with no deal in Antalya
(centre), a Russian drone strike on a Dymer apartment block near Kyiv,
a Russian warship hit at Benghazi, Democrats winning 258 US House
seats, the capture of cartel boss El Chapo Isidro in Mexico, and
BepiColombo entering orbit around Mercury, with a ticker for the
Iran-Bahrain strike, the Nigeria boat disaster, South Korea's
AI-cheating resignation and the Indonesia factory fire.
"""

import os
import shutil


def main() -> None:
    here = os.path.dirname(os.path.abspath(__file__))
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(here, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    # Copy byte-for-byte so repeated runs write identical bytes,
    # as the competition rules require (no network, deterministic).
    shutil.copyfile(src, dst)
    assert os.path.getsize(dst) == os.path.getsize(src)


if __name__ == "__main__":
    main()
