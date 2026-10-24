#!/usr/bin/env python3
"""The final editorial polish for Rose & Co (after brand, SEO, blog, font installers).
Preserve verified original catalog photographs, home hero, copy, navigation and contacts.
"""
from pathlib import Path
from bs4 import BeautifulSoup
import re
import sys

root=Path(sys.argv[1]).resolve()
logo="/rose-and-co/assets/brand-rose.svg?v=brand1"
updated=0
for lang in ("hy","ru","en"):
    for file in (root/lang).rglob("*.html"):
        html=file.read_text(encoding="utf-8")
        soup=BeautifulSoup(html,"html.parser")
        changed=False

        # Replace the unrelated 'R ✧ CO' circle with the actual bespoke logo.
        for badge in soup.select(".about-stamp"):
            badge.clear()
            badge["role"]="img"
            badge["aria-label"]={"hy":"Rose & Co վարդի լոգո","ru":"Логотип Rose & Co с розой","en":"Rose & Co rose logo"}[lang]
            badge["class"]=["about-stamp","about-stamp-rose"]
            badge.append(soup.new_tag("img",src=logo,alt="",width="124",height="124",
                                      decoding="async"))
            changed=True

        # Remove accidental visual blank gap in the story section on mobile:
        # prefer the customer's own flower photos over an editorial toy display.
        for gallery in soup.select(".about-spotlight .spotlight-gallery"):
            large=gallery.select_one(".spotlight-large img")
            small=gallery.select_one(".spotlight-small img")
            if large:
                large["src"]="/rose-and-co/assets/images/real-2026/flowers-39.webp?v=story20261025"
                large["alt"]={"hy":"Վարդերով և ծաղիկներով կոմպոզիցիա զամբյուղում","ru":"Композиция из роз в корзине","en":"Real rose basket arrangement"}[lang]
                large["loading"]="eager"
                large["decoding"]="async"
                changed=True
            if small:
                small["src"]="/rose-and-co/assets/images/real-2026/flowers-26.webp?v=story20261025"
                small["alt"]={"hy":"Կարմիր վարդերի իրական փունջ","ru":"Букет красных роз","en":"Real bouquet of red roses"}[lang]
                small["loading"]="eager"
                small["decoding"]="async"
                changed=True

        # Search engines and social sharing should see the correct real wreath.
        if "memorial-wreaths" in file.parts:
            m=soup.select_one('meta[property="og:image"]')
            if m:
                m["content"]="https://alform-creator.github.io/rose-and-co/assets/images/real-2026/wreaths-05.webp"
                changed=True

        # Existing hero is still exactly the same approved image, only
        # change loading priority for perceived performance.
        if file == root/lang/"index.html":
            hero=soup.select_one(".hero-image")
            if hero:
                assert "hero-bouquet.webp" in hero.get("src",""),"Original hero must be preserved"
                hero["loading"]="eager"
                hero["fetchpriority"]="high"
                changed=True

        # Keep font and detail CSS fresh on mobile Safari after a deploy.
        link=soup.select_one('link[href*="/rose-and-co/assets/styles.css"]')
        if link:
            link["href"]="/rose-and-co/assets/styles.css?v=atelier-final-20261025"
            changed=True
        if changed:
            file.write_text(str(soup),encoding="utf-8")
            updated+=1

css_file=root/"assets"/"styles.css"
css=css_file.read_text(encoding="utf-8")
marker="/* ROSE-CO-FINAL-ATELIER-20261025 */"
if marker not in css:
    css+=r'''

/* ROSE-CO-FINAL-ATELIER-20261025 */
/* A restrained couture-florist visual system, with no dependency on scripts. */
:root {
  --atelier-cream:#faf6f3;
  --atelier-rose:#ead5d4;
  --atelier-wine:#61253e;
  --atelier-ease:cubic-bezier(.22,1,.36,1);
}
html { scroll-padding-top: 15px; }
body { text-rendering: optimizeLegibility; }
.section { padding-block:clamp(70px,7vw,106px); }
.container { max-width:1280px; }
.section-head h2 { text-wrap:balance; }
.button { border-radius:3px; transition:background .3s ease,color .3s ease,transform .4s var(--atelier-ease),box-shadow .4s ease; }
.button:focus-visible, .nav-link:focus-visible, .filter-chip:focus-visible,
.product-card:focus-visible, .journal-card:focus-visible {outline:2px solid #a46f7d;outline-offset:3px}
.hero { background-color:#f9eeea; }
.hero-grid { gap:clamp(16px,3vw,50px); }
.hero-copy>p { max-width:55ch; }
.hero-image-wrap { box-shadow:0 25px 85px rgba(77,32,46,.14); }
.hero-float-tag { box-shadow:0 7px 34px rgba(73,29,43,.10); }
.occasion-card { border-radius:3px; }
.occasion-card:focus-visible { outline-offset:3px; }
.occasion-caption {text-shadow:0 1px 4px rgba(26,13,19,.32)}
.product-card { overflow:hidden; border-radius:3px; }
.product-card .card-action { gap:8px; }
.product-card .card-action span { flex:none; }
.product-meta h3, .product-meta p { overflow-wrap:anywhere; }
.product-meta p { min-height:3em; }
.catalog-count { gap:14px; }
.filter-chip { border-radius:3px; }
.about-spotlight {
  background:linear-gradient(145deg,#f3e2e0 0%,#f5e7e3 55%,#f0dddc 100%);
  padding:clamp(60px,7vw,100px) 0;
  overflow:hidden;
}
.about-grid {
  grid-template-columns:minmax(0,1.08fr) minmax(0,.92fr);
  gap:clamp(32px,6vw,96px);
  align-items:center;
}
.spotlight-gallery {
  position:relative; min-width:0;
  padding:22px 57px 50px 6px;
  isolation:isolate;
}
/* Never let reveal state hide the main story images on iOS/WebKit. */
html.rose-motion-on .spotlight-gallery[data-rose-reveal],
html.rose-motion-on .spotlight-gallery[data-rose-reveal]:not(.rose-in-view) {
  opacity:1 !important;
  transform:none !important;
}
.spotlight-large {
  height:clamp(390px,43vw,545px);
  border-radius:210px 210px 4px 4px;
  background:#e4c4bc;
  overflow:hidden;
  box-shadow:0 22px 50px rgba(89,42,54,.11);
}
.spotlight-large img {
  width:100%; height:100%; display:block; object-fit:cover;
  object-position:center 44%;opacity:1 !important;
}
.spotlight-small {
  width:clamp(155px,15vw,214px);
  height:clamp(174px,18vw,245px);
  right:0; bottom:0;
  border:7px solid #f4e5e2;
  border-radius:3px; overflow:hidden;
  box-shadow:0 12px 35px rgba(89,42,54,.10);
}
.spotlight-small img {width:100%;height:100%;object-fit:cover;object-position:center;opacity:1 !important}
.about-stamp.about-stamp-rose {
  position:absolute;right:25px;top:-1px;z-index:4;
  width:clamp(90px,10vw,126px);height:clamp(90px,10vw,126px);
  border:0;background:transparent;box-shadow:none;
  border-radius:50%;padding:0;display:block;
  overflow:visible;transform:rotate(-9deg);
  filter:drop-shadow(0 7px 10px rgba(86,41,54,.18));
}
.about-stamp.about-stamp-rose img {
  width:100%;height:100%;object-fit:contain;display:block;
}
.spotlight-copy {max-width:560px;min-width:0;}
.spotlight-copy .eyebrow { color:#8c5164; }
.spotlight-copy h2 {text-wrap:balance; font-size:clamp(34px,3.7vw,53px);line-height:1.32;max-width:16ch;letter-spacing:-.025em;margin:17px 0}
.spotlight-copy p {margin:20px 0 29px;max-width:53ch;font-size:14px;line-height:1.95}
.ornament {color:#af8291}
.journal-grid {
  display:grid;
  grid-template-columns:repeat(3,minmax(0,1fr));
  gap:36px 25px;
  align-items:stretch;
}
.journal-card {
  display:flex;flex-direction:column;min-width:0;gap:0;
  padding-bottom:6px;border-bottom:1px solid #e9ddda;
  transition:border-color .3s ease;
}
.journal-card:hover,.journal-card:focus-visible { border-color:#b98999; }
.journal-photo {
  aspect-ratio:1.22/1;
  border-radius:3px;background:#f0e6e2;margin-bottom:17px;
}
.journal-photo img {
  width:100%;height:100%;object-fit:contain;object-position:center;
  background:#eee5e1;
}
.journal-photo img[src*="wreaths-"] {
  background:#18171a;
  object-fit:contain;
}
.journal-card h3 {
  font-size:clamp(21px,2.1vw,27px);
  line-height:1.4;min-width:0;text-wrap:pretty;
  margin:12px 0;
}
.journal-card p {font-size:13px;line-height:1.86;margin:0 0 18px;}
.journal-read {margin-top:auto;display:inline-flex;align-items:center;padding-bottom:8px;}
.journal-card .eyebrow {font-size:9px;letter-spacing:.20em;}
.article-photo {height:auto;aspect-ratio:1.85/1;border-radius:3px;background:#f0e9e5;overflow:hidden;}
.article-photo img {width:100%;height:100%;object-fit:contain;}
.article-photo img[src*="wreaths-"] {object-fit:contain;background:#18171a;}
.article-body h2,.article-body h3 {max-width:65ch}
.article-body p {max-width:72ch}
.journal-article-cta {
  margin:38px 0 4px;padding:30px 32px;
  background:linear-gradient(130deg,#fffaf5,#f5e7e5);
  border-left:2px solid #b17a8d;
  border-radius:2px;
}
.journal-article-cta .eyebrow {font-size:9px}
.journal-article-cta p {font-size:14px;line-height:1.75;margin:14px 0 20px}
.journal-article-cta .button {min-height:45px;padding:12px 19px;white-space:normal;text-align:center;}
.footer-main .brand {display:inline-flex}
.footer-main .brand-type small {font-size:8px}
@media(min-width:1000px) {
  .journal-grid .journal-card:nth-child(5),
  .journal-grid .journal-card:nth-child(9) { position:relative; }
  .journal-grid .journal-card:nth-child(5)::before {
    content:"";width:32px;height:1px;background:#ad8390;
    position:absolute;top:-19px;left:0;pointer-events:none;
  }
}
@media(max-width:960px){
  .about-grid {grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:30px;}
  .spotlight-gallery {padding:22px 35px 38px 0;}
  .spotlight-large {height:420px;}
  .spotlight-small {width:156px;height:180px;}
  .about-stamp.about-stamp-rose {right:1px;}
  .journal-grid {grid-template-columns:repeat(2,minmax(0,1fr));}
}
@media(max-width:640px) {
  .section {padding-block:65px;}
  .about-spotlight {padding:56px 0 62px;}
  .about-grid {grid-template-columns:minmax(0,1fr);gap:21px;}
  .spotlight-gallery {padding:18px 32px 40px 0;min-height:0;}
  .spotlight-large {height:clamp(265px,77vw,370px);border-radius:165px 165px 3px 3px;}
  .spotlight-small {width:clamp(110px,29vw,143px);height:clamp(128px,34vw,164px);border-width:6px;}
  .about-stamp.about-stamp-rose {width:87px;height:87px;top:0;right:-5px;}
  .spotlight-copy h2 {font-size:clamp(30px,7.6vw,40px);max-width:100%;line-height:1.32;margin:13px 0;}
  html[lang="hy"] .spotlight-copy h2 {font-size:clamp(30px,7.5vw,39px)}
  .spotlight-copy p {font-size:13px;margin:17px 0 20px;line-height:1.85;}
  .journal-grid {grid-template-columns:minmax(0,1fr);gap:31px;}
  .journal-photo {aspect-ratio:1.3/1;}
  .journal-card h3,html[lang="hy"] .journal-card h3 {font-size:23px;line-height:1.4;}
  .journal-card p {font-size:13px;}
  .article-photo {aspect-ratio:1.18/1;}
  .article-hero > p {margin-bottom:22px;}
  .article-body {padding-top:32px;}
  .article-body h2 {font-size:26px;}
  .article-body h3 {font-size:21px;}
  .article-body p {margin-bottom:21px;}
  .journal-article-cta {padding:24px 18px;}
  .catalog-count {flex-direction:column;align-items:flex-start;}
  .footer-main {gap:24px;}
}
@media(max-width:360px){
  .spotlight-large {height:262px;}
  .about-stamp.about-stamp-rose {width:75px;height:75px;}
  .journal-card h3 {font-size:21px;}
}
'''
    css_file.write_text(css,encoding="utf-8")

# Successful build must retain 71 distinct catalog products, original home image,
# all published blog pages and brand photos.
for lang in ("hy","ru","en"):
    home=(root/lang/"index.html").read_text(encoding="utf-8")
    assert "hero-bouquet.webp" in home
    assert "about-stamp-rose" in home
    assert "brand-rose.svg" in home
    assert (root/lang/"journal"/"ordering-flowers-guide"/"index.html").exists()
    assert len(list((root/lang/"journal").rglob("index.html")))==11  # journal + 10 posts
    assert "wreaths-05.webp" in (root/lang/"journal"/"memorial-wreaths"/"index.html").read_text(encoding="utf-8")
print(f"Final Rose & Co editorial styling installed across {updated} localized pages")
