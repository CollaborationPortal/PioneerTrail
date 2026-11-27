#!/usr/bin/env python3
"""Build an Apps Script-ready Index.html from game-src.html.

Leaves pioneer-trail.html (the GitHub Pages build) untouched. Run from anywhere:
    python3 apps-script/build.py
"""
import base64
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = Path(__file__).resolve().parent / "Index.html"

MUSIC_SRC = 'src="assets/music/campfire-loop.mp3"'
FULLSCREEN_CHECK = "if (!request || !exit) {"

html = (ROOT / "game-src.html").read_text()
assets = (ROOT / "assets" / "embedded.js").read_text().rstrip("\n")
html = html.replace("/* ASSETS_PLACEHOLDER */", assets)

# Apps Script can't serve loose files, so inline the music as a data URI.
mp3 = base64.b64encode((ROOT / "assets" / "music" / "campfire-loop.mp3").read_bytes()).decode()
assert MUSIC_SRC in html, "music <audio> tag not found"
html = html.replace(MUSIC_SRC, f'src="data:audio/mpeg;base64,{mp3}"')

# The Sites/Apps Script iframes may not allow fullscreen; hide the button when blocked.
assert FULLSCREEN_CHECK in html, "fullscreen check not found"
html = html.replace(FULLSCREEN_CHECK, "if (!request || !exit || document.fullscreenEnabled === false) {")

assert not re.search(r'(src=|href=|url\()["\']?assets/', html), "a relative asset path is still referenced"
OUT.write_text(html)
print(f"Wrote {OUT} ({OUT.stat().st_size / 1e6:.2f} MB)")
