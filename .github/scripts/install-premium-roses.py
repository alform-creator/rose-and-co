#!/usr/bin/env python3
"""Install uploaded Rose & Co premium photos and synchronize the trilingual catalog."""
from pathlib import Path
from PIL import Image
import base64
import html
import json
import re
import sys

site = Path(sys.argv[1]).resolve()
repo = Path(__file__).resolve().parents[2]
photo_dir = site / "assets" / "images" / "rose50"
photo_dir.mkdir(parents=True, exist_ok=True)

# Reassemble GitHub-safe encoded chunks; verify the WebP before publishing.
chunks = sorted((repo / ".rose-premium" / "101").glob("part-*.b64"))
if len(chunks) != 21:
    raise RuntimeError(f"Expected 21 photo chunks, found {len(chunks)}")
binary = base64.b64decode("".join(p.read_text(encoding="ascii").strip() for p in chunks), validate=True)
photo = photo_dir / "premium-101.webp"
photo.write_bytes(binary)
with Image.open(photo) as image:
    image.verify()

changes = {
    "RC01": {
        "name": {"hy": "51 վարդ", "ru": "51 роза", "en": "51 Roses"},
        "desc": {
            "hy": "51 կարմիր վարդ՝ սովորական կամ երկար ցողուններով։ Ցողունների բարձրությունն ու առկայությունը ճշտեք պատվիրելիս։",
            "ru": "51 красная роза, со стандартными или длинными стеблями. Уточните высоту и наличие при заказе.",
            "en": "51 red roses, with standard or long stems. Enquire about available stem lengths when ordering."
        }
    },
    "RC07": {
        "name": {"hy": "101 վարդ", "ru": "101 роза", "en": "101 Roses"},
        "desc": {
            "hy": "101 կարմիր վարդ՝ սովորական կամ երկար ցողուններով։ Ցողունների բարձրությունն ու առկայությունը ճշտեք պատվիրելիս։",
            "ru": "101 красная роза, со стандартными или длинными стеблями. Уточните высоту и наличие при заказе.",
            "en": "101 red roses, with standard or long stems. Enquire about available stem lengths when ordering."
        },
        "img": "rose50/premium-101"
    },
    "RC21": {
        "name": {"hy": "Ծաղկեպսակ", "ru": "Венок", "en": "Wreath"}
    }
}
for filename in ("catalog.json", "catalog.js"):
    path = site / "assets" / filename
    raw = path.read_text(encoding="utf-8")
    prefix = "window.ROSE_DATA=" if filename.endswith(".js") else ""
    if prefix:
        assert raw.startswith(prefix)
        raw = raw[len(prefix):].strip().removesuffix(";")
    data = json.loads(raw)
    found = set()
    for product in data["products"]:
        pid = product["id"]
        if pid in changes:
            product.update(changes[pid])
            found.add(pid)
    if found != set(changes):
        raise RuntimeError(f"Missing catalog products: {set(changes)-found}")
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    path.write_text(prefix + payload + (";" if prefix else "") + "\n", encoding="utf-8")

labels = {
    "hy": "Դիտել կոմպոզիցիան: ",
    "ru": "Посмотреть композицию: ",
    "en": "View arrangement: "
}
for path in site.rglob("*.html"):
    locale = next((lang for lang in labels if lang in path.parts), None)
    if locale is None:
        continue
    text = path.read_text(encoding="utf-8")
    for pid, update in changes.items():
        title = update["name"][locale]
        allnames = " ".join(update["name"][lang] for lang in labels).lower()
        pattern = r'(<article\b[^>]*\bdata-item="' + re.escape(pid) + r'"[^>]*>)(.*?)(</article>)'
        def replace_card(m):
            attrs, body, close = m.groups()
            attrs = re.sub(r'aria-label="[^"]*"', 'aria-label="' + html.escape(labels[locale] + title, quote=True) + '"', attrs, count=1)
            attrs = re.sub(r'data-name="[^"]*"', 'data-name="' + html.escape(allnames, quote=True) + '"', attrs, count=1)
            body = re.sub(r'<h3>.*?</h3>', '<h3>' + html.escape(title) + '</h3>', body, count=1, flags=re.DOTALL)
            body = re.sub(r'(<img\b[^>]*\balt=")[^"]*(")', lambda a: a.group(1) + html.escape(title + " — Rose & Co", quote=True) + a.group(2), body, count=1)
            if "img" in update:
                newpath = "/rose-and-co/assets/images/" + update["img"] + ".webp?v=premium3"
                body = re.sub(r'(<img\b[^>]*\bsrc=")[^"]*(")', lambda a: a.group(1) + newpath + a.group(2), body, count=1)
            return attrs + body + close
        text = re.sub(pattern, replace_card, text, flags=re.DOTALL)
    path.write_text(text, encoding="utf-8")

manifest = photo_dir / "manifest.json"
if manifest.exists():
    data = json.loads(manifest.read_text(encoding="utf-8"))
    if not any(item.get("file") == photo.name for item in data):
        data.append({"file": photo.name, "category": "flowers", "label": "101 վարդ / 101 Roses",
                     "origin": "original single generated photo", "width": 640, "height": 800})
    manifest.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"Installed {photo.name}: {len(binary)} bytes, synchronized HY/RU/EN product labels.")
