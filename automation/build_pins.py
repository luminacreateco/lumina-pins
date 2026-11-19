#!/usr/bin/env python3
"""Build Pinterest image pins + bulk-upload CSV from a picks file.

Usage:  python3 build_pins.py picks.json OUT_CSV_NAME
picks.json = list of objects:
  {"listing_id": "4619823562", "image_url": "https://i.etsystatic.com/...il_fullxfull...jpg",
   "slug": "monster-truck-red-5x7-main", "title": "...<=100", "description": "...<=500",
   "board": "Boy Birthday Party Ideas", "keywords": ["DIY Birthday Invitations", ...],
   "publish": "2026-12-03T16:00:00"   # UTC, Pinterest reads it as UTC
  }
Writes pins/auto/<slug>-pin.jpg (1000x1500, photo full width centred on black, as the
owner's rule for pins with badges) and OUT_CSV_NAME in the repo root of automation/csv/.
Checks: title<=100, description<=500, no 'evite', no 'Monster Jam', image downloads OK.
"""
import json, os, re, sys, io, urllib.request
from PIL import Image

ROOT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(ROOT)
OUTDIR = os.path.join(REPO, "pins", "auto")
CSVDIR = os.path.join(ROOT, "csv")
RAW = "https://raw.githubusercontent.com/luminacreateco/lumina-pins/main/pins/auto/"
BAN = re.compile(r"\be[\s-]?vites?\b|monster\s*jam", re.I)

def make_pin(url, dest):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    data = urllib.request.urlopen(req, timeout=60).read()
    im = Image.open(io.BytesIO(data)).convert("RGB")
    W, H = 1000, 1500
    canvas = Image.new("RGB", (W, H), (0, 0, 0))
    scale = W / im.width
    nh = int(im.height * scale)
    if nh > H:  # tall source: fit by height
        scale = H / im.height
    im2 = im.resize((int(im.width * scale), int(im.height * scale)), Image.LANCZOS)
    canvas.paste(im2, ((W - im2.width) // 2, (H - im2.height) // 2))
    canvas.save(dest, "JPEG", quality=88, optimize=True, progressive=True)

def q(s):
    return '"' + str(s).replace('"', '""') + '"'

def main():
    picks = json.load(open(sys.argv[1]))
    name = sys.argv[2]
    os.makedirs(OUTDIR, exist_ok=True); os.makedirs(CSVDIR, exist_ok=True)
    rows = ["Title,Media URL,Pinterest board,Thumbnail,Description,Link,Publish date,Keywords"]
    for p in picks:
        t, d = p["title"].strip(), p["description"].strip()
        assert len(t) <= 100, ("title too long", t)
        assert len(d) <= 500, ("description too long", len(d), t)
        for s in (t, d, " ".join(p["keywords"])):
            assert not BAN.search(s), ("banned word", s)
        slug = re.sub(r"[^a-z0-9-]+", "-", p["slug"].lower()).strip("-")
        make_pin(p["image_url"], os.path.join(OUTDIR, slug + "-pin.jpg"))
        link = "https://www.etsy.com/listing/%s" % p["listing_id"]
        rows.append(",".join([q(t), RAW + slug + "-pin.jpg", p["board"], "", q(d), link,
                              p["publish"], q(", ".join(p["keywords"]))]))
    out = os.path.join(CSVDIR, name)
    open(out, "w", encoding="utf-8").write("\n".join(rows) + "\n")
    print("wrote", out, len(picks), "pins")

if __name__ == "__main__":
    main()
