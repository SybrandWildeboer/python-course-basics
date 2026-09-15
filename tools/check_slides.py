"""Open every deck in a headless browser and report layout problems.

A slide deck is only finished when nothing is cut off. This script loads each
slides/session-*.html at exactly 1280x720, walks every slide, and reports:

  * content taller than the slide body (something is scrolled out of view)
  * horizontal overflow inside code blocks
  * slides with no speaker notes
  * JavaScript errors raised while the deck boots

Usage:
    pip install playwright && playwright install chromium
    python tools/check_slides.py                 # check all decks
    python tools/check_slides.py 3 --shots       # check session 3, save PNGs
"""

from __future__ import annotations

import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

# Use whichever Chromium is already on the machine when the bundled build is
# missing (common in containers that pre-install browsers).
CHROMIUM_CANDIDATES = [
    "/opt/pw-browsers/chromium",
    "/usr/bin/chromium",
    "/usr/bin/chromium-browser",
    "/usr/bin/google-chrome",
]


def launch(pw):
    try:
        return pw.chromium.launch()
    except Exception:
        for path in CHROMIUM_CANDIDATES:
            if Path(path).exists():
                return pw.chromium.launch(executable_path=path)
        raise

ROOT = Path(__file__).resolve().parents[1]
SLIDES = ROOT / "slides"
SHOT_DIR = ROOT / "tools" / ".shots"

PROBE = """
() => {
  const out = [];
  document.querySelectorAll('.slide').forEach((slide, i) => {
    const prev = slide.className;
    slide.classList.add('is-active');
    const body = slide.querySelector('.slide-body');
    const issues = [];
    if (body && body.scrollHeight - body.clientHeight > 4) {
      issues.push(`body overflows by ${body.scrollHeight - body.clientHeight}px`);
    }
    slide.querySelectorAll('pre').forEach(pre => {
      if (pre.scrollWidth - pre.clientWidth > 4) {
        issues.push(`code line too wide by ${pre.scrollWidth - pre.clientWidth}px`);
      }
    });
    const needsNotes = !slide.matches('.slide--section, .slide--title');
    if (needsNotes && !slide.querySelector('aside.notes')) issues.push('no speaker notes');
    if (issues.length) out.push({ n: i + 1, title: slide.dataset.title || '', issues });
    slide.className = prev;
  });
  return out;
}
"""


def check(deck: Path, browser, shots: bool) -> int:
    page = browser.new_page(viewport={"width": 1280, "height": 720})
    errors: list[str] = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.goto(deck.as_uri())
    page.wait_for_timeout(280)

    total = page.eval_on_selector_all(".slide", "els => els.length")
    problems = page.evaluate(PROBE)

    print(f"\n{deck.name}  —  {total} slides")
    for err in errors:
        print(f"  ! javascript error: {err}")
    for item in problems:
        label = f"slide {item['n']:>2} ({item['title']})"
        for issue in item["issues"]:
            print(f"  - {label}: {issue}")
    if not problems and not errors:
        print("  all slides fit, notes present")

    if shots:
        SHOT_DIR.mkdir(parents=True, exist_ok=True)
        for n in range(1, total + 1):
            page.evaluate(f"() => location.hash = '{n}'")
            page.reload()
            page.wait_for_timeout(160)
            page.screenshot(path=str(SHOT_DIR / f"{deck.stem}-{n:02d}.png"))
        print(f"  screenshots -> {SHOT_DIR.relative_to(ROOT)}")

    page.close()
    return len(problems) + len(errors)


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    shots = "--shots" in sys.argv

    if args:
        decks = [SLIDES / f"session-{int(a):02d}.html" for a in args]
    else:
        decks = sorted(SLIDES.glob("session-*.html"))

    missing = [d for d in decks if not d.exists()]
    for d in missing:
        print(f"missing: {d}")
    decks = [d for d in decks if d.exists()]

    bad = 0
    with sync_playwright() as pw:
        browser = launch(pw)
        for deck in decks:
            bad += check(deck, browser, shots)
        browser.close()

    print(f"\n{'problems found: ' + str(bad) if bad else 'clean'}")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
