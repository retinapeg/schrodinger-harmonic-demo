"""Breaker check for the slide deck (no Keynote or PowerPoint needed).

    python scripts/check_slides.py

Opens slides/qho-demo.pptx with python-pptx and checks: 7 slides, every shape
inside the slide, every picture decodes, speaker notes present, and the deck's
text equals what scripts/make_slides.py would write from a fresh solve (so the
numbers and the pytest count are current). Exits non-zero on the first failure.
"""
import io
import re
import sys
from pathlib import Path

from PIL import Image
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import make_slides  # noqa: E402

TIMING = re.compile(r"~\d+ ms")


def slide_texts(prs):
    return [TIMING.sub("~? ms", "\n".join(sh.text_frame.text for sh in s.shapes if sh.has_text_frame))
            for s in prs.slides]


def main():
    deck = Presentation(str(make_slides.OUT))
    problems = []
    if len(deck.slides) != 7:
        problems.append(f"expected 7 slides, found {len(deck.slides)}")
    W, H = deck.slide_width, deck.slide_height
    pictures = 0
    for i, s in enumerate(deck.slides, 1):
        for sh in s.shapes:
            if sh.left < 0 or sh.top < 0 or sh.left + sh.width > W or sh.top + sh.height > H:
                problems.append(f"slide {i}: shape '{sh.name}' extends outside the slide")
            if sh.shape_type == MSO_SHAPE_TYPE.PICTURE:
                pictures += 1
                Image.open(io.BytesIO(sh.image.blob)).verify()
        if not s.has_notes_slide or not s.notes_slide.notes_text_frame.text.strip():
            problems.append(f"slide {i}: missing speaker notes")
    if pictures < 4:
        problems.append(f"expected >= 4 pictures, found {pictures}")

    expected = slide_texts(make_slides.build(make_slides.compute_stats()))
    for i, (have, want) in enumerate(zip(slide_texts(deck), expected), 1):
        if have != want:
            problems.append(f"slide {i}: text is stale; rerun python scripts/make_slides.py")

    if problems:
        print("FAIL:\n  " + "\n  ".join(problems))
        sys.exit(1)
    print(f"PASS: {len(deck.slides)} slides, {pictures} pictures, notes on every slide, numbers current")


if __name__ == "__main__":
    main()
