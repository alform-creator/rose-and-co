#!/usr/bin/env python3
"""Refresh Rose & Co catalog photography, keeping just one authentic-looking wreath."""
import json
import re
import sys
from pathlib import Path
from PIL import Image, ImageEnhance, ImageFilter, ImageOps

site = Path(sys.argv[1]).resolve()
assets = site / 'assets'
photos = assets / 'images' / 'rose50'
assert (site / 'hy' / 'index.html').is_file(), 'Expected Rose & Co site root'

# Keep the one original, complete studio photograph of a floral wreath.
KEEP_WREATH = 'RC21'
for filename in ('catalog.json', 'catalog.js'):
    path = assets / filename
    raw = path.read_text(encoding='utf-8')
    prefix = 'window.ROSE_DATA=' if filename.endswith('.js') else ''
    if prefix:
        assert raw.startswith(prefix), 'Unexpected catalog JS format'
        raw = raw[len(prefix):].rstrip().removesuffix(';')
    data = json.loads(raw)
    data['products'] = [p for p in data['products']
                        if p.get('cat') != 'wreaths' or p.get('id') == KEEP_WREATH]
    assert sum(p.get('cat') == 'wreaths' for p in data['products']) == 1
    encoded = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
    path.write_text(prefix + encoded + (';' if prefix else '') + '\n', encoding='utf-8')

# The product grid is pre-rendered for search engines; fix every locale and view.
removed = 0
notices = 0
for page in site.rglob('*.html'):
    html = page.read_text(encoding='utf-8')
    html, n = re.subn(r'<div\s+class="notice-strip"\s*>.*?</div>', '', html,
                      flags=re.DOTALL)
    notices += n

    def keep_only_one_wreath(m):
        global removed
        card = m.group(0)
        if 'data-item="' + KEEP_WREATH + '"' in card:
            return card
        removed += 1
        return ''

    html = re.sub(r'<article\b[^>]*\bdata-category="wreaths"[^>]*>.*?</article>',
                  keep_only_one_wreath, html, flags=re.DOTALL)
    page.write_text(html, encoding='utf-8')

# Keep all existing unique images; refine contrast, focus, and encoding quality.
# Upscaling improves presentation on high-density phones, but it cannot recreate
# photographic detail absent in the source crops.
updated = 0
for image_path in sorted(photos.glob('flowers-*.webp')) + [photos / 'wreaths-01.webp']:
    with Image.open(image_path) as source:
        img = ImageOps.exif_transpose(source).convert('RGB')
    img = ImageEnhance.Contrast(img).enhance(1.055)
    img = ImageEnhance.Color(img).enhance(1.035)
    img = img.filter(ImageFilter.UnsharpMask(radius=1.15, percent=125, threshold=2))
    if img.width < 1100:
        factor = 1100 / img.width
        img = img.resize((1100, round(img.height * factor)), Image.Resampling.LANCZOS)
    img = img.filter(ImageFilter.UnsharpMask(radius=0.8, percent=65, threshold=2))
    img.save(image_path, format='WEBP', quality=91, method=6)
    updated += 1

# Remove only the five artificial/montage wreath assets, never the real wreath.
for image_path in photos.glob('wreaths-*.webp'):
    if image_path.name != 'wreaths-01.webp':
        image_path.unlink()

# Cache-busting ensures devices don't keep old blurred thumbnails.
for page in site.rglob('*.html'):
    html = page.read_text(encoding='utf-8')
    html = re.sub(r'(/rose-and-co/assets/images/rose50/(?:flowers-\d+|wreaths-01)\.webp)(?:\?v=photo2)?',
                  r'\1?v=photo2', html)
    page.write_text(html, encoding='utf-8')

js = assets / 'app.js'
script = js.read_text(encoding='utf-8')
script = script.replace('${esc(p.img)}.webp"', '${esc(p.img)}.webp?v=photo2"')
js.write_text(script, encoding='utf-8')

print(f'Rose & Co updated: {updated} photographs refined, {removed} duplicate wreath cards removed across pages, {notices} announcement strips removed.')