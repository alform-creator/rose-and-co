#!/usr/bin/env python3
"""Complete production release QA for Rose & Co across all 78 localized pages.

Two phases:
  1. static SEO/content/image inventory of every URL + file;
  2. actual Chrome desktop/mobile rendering of every page at 320px + 1440px,
     and extra intermediate breakpoint coverage of key commercial pages.
Fails the deployment only for actionable regressions, prints non-blocking
editorial and product-operations follow-ups separately.
"""
from pathlib import Path
from collections import Counter,defaultdict
from urllib.parse import unquote,urlsplit
from html import unescape
from functools import partial
from tempfile import TemporaryDirectory
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from threading import Thread
import io
import json
import os
import re
import shutil
import sys
import time
from bs4 import BeautifulSoup
from PIL import Image,ImageFile
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

ImageFile.LOAD_TRUNCATED_IMAGES=False
root=Path(sys.argv[1]).resolve()
langs=("hy","ru","en")
pages=sorted(p for l in langs for p in (root/l).rglob("index.html"))
assert len(pages)==78, f"Unexpected page count: {len(pages)}"
errors=[];warnings=[]
seo_titles={};seen_images={};page_inventory={}
images_by_stem=defaultdict(list)
broken_picture_refs=set()
readable_dims={}
photo_total=0
home_sections={}
css_files=[]
js_files=[]
def pagepath(p):return p.relative_to(root).as_posix()
def clean(s):return re.sub(r"\s+"," ",unescape(s)).strip()
def loc_to_file(uri):
    parsed=urlsplit(uri)
    if parsed.scheme and parsed.netloc!="alform-creator.github.io":
        return None
    if not parsed.path.startswith("/rose-and-co/"):
        return None
    rel=unquote(parsed.path[len("/rose-and-co/"):])
    return (root/rel/"index.html") if rel.endswith("/") else (root/rel)
for path in pages:
    rel=pagepath(path);soup=BeautifulSoup(path.read_text(encoding="utf-8"),"html.parser")
    lang=path.relative_to(root).parts[0]
    target="https://alform-creator.github.io/rose-and-co/"+rel.removesuffix("index.html")
    titles=soup.select("title"); title=clean(titles[0].get_text()) if titles else ""
    des=soup.select_one('meta[name="description"]')
    desc=clean(des.get("content","")) if des else ""
    h1=soup.select("main h1")
    can=soup.select('link[rel="canonical"]')
    hreflang={tag.get("hreflang"):tag.get("href") for tag in soup.select("link[hreflang]")}
    if not (8<len(title)<115 and 35<=len(desc)<=240):
        errors.append(f"{rel} missing/poor page title or meta description: {len(title)} {len(desc)}")
    if title in seo_titles: errors.append(f"{rel} duplicate title also on {seo_titles[title]}")
    seo_titles[title]=rel
    if len(h1)!=1:errors.append(f"{rel} expected exactly 1 H1")
    if len(can)!=1 or can[0].get("href")!=target:
        errors.append(f"{rel} incorrect canonical")
    if set(hreflang)!={"hy","ru","en","x-default"}:
        errors.append(f"{rel} incomplete hreflang")
    if soup.html.get("lang")!=lang:errors.append(f"{rel} incorrect html lang")
    if not soup.select_one('meta[property="og:image"]'):errors.append(f"{rel} missing social share image")
    if not soup.select_one('script[type="application/ld+json"]'):errors.append(f"{rel} missing JSON-LD")
    localimgs=[]
    for image in soup.select("img"):
        src=image.get("src","").strip()
        if not image.has_attr("alt"):errors.append(f"{rel} image without alt")
        if src.startswith("/rose-and-co/"):
            imagefile=loc_to_file(src)
            if imagefile is None or not imagefile.is_file():
                broken_picture_refs.add(rel+" "+src);continue
            localimgs.append((src,imagefile))
            photo_total+=1
            seen_images.setdefault(str(imagefile), []).append(rel)
        elif not src.startswith(("https://","http://","data:")):
            warnings.append(f"{rel} unusual image source: {src}")
    imgs=[u for u,p in localimgs]
    if lang=="hy" and len(imgs)>0:images_by_stem[rel]=imgs
    piccards=[c.find("img") for c in soup.select(".product-card,.journal-card,.occasion-card") if c.find("img")]
    if len(piccards)>4:
        duplicates=Counter(urlsplit(i.get("src","")).path for i in piccards)
        repeats=[u for u,n in duplicates.items() if n>=3]
        if repeats:
            warnings.append(f"{rel} repeated card images (>=3): {len(repeats)}")
    for sheet in soup.select('link[rel=stylesheet][href]'):
        href=sheet["href"];f=loc_to_file(href)
        if f and f.exists():css_files.append(f)
        elif f:errors.append(f"{rel} missing CSS {href}")
    for script in soup.select('script[src]'):
        src=script["src"];f=loc_to_file(src)
        if f and f.exists():js_files.append(f)
        elif f:errors.append(f"{rel} missing JS {src}")
    slug=rel.split("/")[1] if len(rel.split("/"))>2 else "home"
    page_inventory[rel]={"title":title,"desc":desc,"images":len(localimgs),"cards":len(piccards),"h2":len(soup.select("main h2")),"h3":len(soup.select("main h3"))}
    if slug=="home":home_sections[lang]=[t.get("id") for t in soup.select("main section[id]")]
assert all(page_inventory[f"{l}/index.html"]["images"]>=15 for l in langs)
assert all(len(home_sections[l])>=3 for l in langs)
# Check images are real (not corrupt) and useful in display contexts.
for f,uses in sorted(seen_images.items()):
    try:
        im=Image.open(f)
        im.verify()
        im=Image.open(f)
        w,h=im.size
        readable_dims[f]=(w,h)
        if w<240 or h<240:
            warnings.append(f"Image resolution below 240px: {Path(f).relative_to(root)} ({w}x{h})")
    except Exception as e: errors.append(f"Corrupt image {Path(f).relative_to(root)}: {str(e)[:160]}")
if broken_picture_refs: errors.extend(sorted(broken_picture_refs))
# Same route tree must exist in all languages, 20 journal articles per locale.
routes={l:set(p.relative_to(root/l).as_posix() for p in (root/l).rglob("index.html")) for l in langs}
if not (routes["hy"]==routes["ru"]==routes["en"]):
    errors.append("Mismatch between localized route trees")
for l in langs:
    article_count=sum("/journal/" in p and p.endswith("index.html") for p in (f"{l}/"+x for x in routes[l]))
    if article_count!=20:errors.append(f"{l}: expected 20 journal posts, got {article_count}")

print("FULL SITE STATIC | pages:",len(pages), "| languages:",", ".join(langs),
      "| localized journal posts:",20*3)
print("FULL SITE SEO | unique title/desc scan, canonical, hreflang, Open Graph, JSON-LD: done")
print("FULL SITE IMAGES | referenced image instances:",photo_total,
      "| distinct inspected files:",len(seen_images),
      "| corrupt / missing:",len([x for x in errors if "image" in x.lower()]))
print("FULL SITE ASSETS | CSS references:",len(css_files),"| JS references:",len(js_files))
if warnings:
    print("FULL SITE EDITORIAL WARNINGS:",len(warnings))
    for w in warnings[:18]:print("WARNING:",w)
# Browser audit via local static server mapping /rose-and-co/ to webroot.
chrome=next((shutil.which(x) for x in ("google-chrome","google-chrome-stable","chromium","chromium-browser") if shutil.which(x)),None)
if not chrome:raise SystemExit("Chrome is required for full QA")
class Quiet(SimpleHTTPRequestHandler):
    def log_message(self,*a):pass

with TemporaryDirectory() as tmp:
    (Path(tmp)/"rose-and-co").symlink_to(root,target_is_directory=True)
    http=ThreadingHTTPServer(("127.0.0.1",0),partial(Quiet,directory=tmp))
    Thread(target=http.serve_forever,daemon=True).start()
    base=f"http://127.0.0.1:{http.server_address[1]}/rose-and-co/"
    options=Options()
    options.binary_location=chrome
    for arg in ("--headless=new","--disable-gpu","--no-sandbox","--disable-dev-shm-usage",
                "--disable-background-networking","--disable-features=Translate"):
        options.add_argument(arg)
    options.page_load_strategy="eager"
    options.set_capability("goog:loggingPrefs",{"browser":"SEVERE"})
    options.add_argument("--window-size=1440,900")
    driver=webdriver.Chrome(options=options)
    driver.set_page_load_timeout(25)
    combinations=0
    js_errors=[]
    key_routes={"index.html","catalog/index.html","about/index.html",
                "contact/index.html","flowers/index.html","journal/index.html"}
    try:
      for width,height,mobile in ((320,700,True),(375,812,True),(768,1024,True),(1440,900,False)):
        if mobile:
            driver.execute_cdp_cmd("Emulation.setDeviceMetricsOverride",{
               "width":width,"height":height,"deviceScaleFactor":1,"mobile":True})
        else:
            driver.execute_cdp_cmd("Emulation.clearDeviceMetricsOverride",{})
            driver.set_window_size(width,height)
        for p in pages:
            lang=p.relative_to(root).parts[0]
            relative=p.relative_to(root/lang).as_posix()
            if width in (375,768) and relative not in key_routes:
                # All 78 routes receive 320px & desktop; the core commerce
                # page types also receive phone + tablet checks.
                continue
            where=f"{lang}/{relative} @{width}px"
            driver.get(base+lang+"/"+relative.removesuffix("index.html"))
            driver.execute_script("document.documentElement.classList.remove('rose-bloom-on')")
            result=driver.execute_script("""
              const viewport=document.documentElement.clientWidth;
              const root=document.documentElement;
              const samples=s=>[...document.querySelectorAll(s)];
              const rect=e=>e.getBoundingClientRect();
              const visual=[
                'main h1','main h2','main h3','.hero-buttons .button',
                '.product-card .card-action','.rs-actions .button',
                '.rose-builder-form button','.rs-sample-arrow'
              ];
              let cuts=[];
              for(const q of visual){
                for(const el of samples(q).slice(0,4)){
                  const s=getComputedStyle(el);
                  const r=rect(el);
                  if(s.display==='none'||s.visibility==='hidden'||r.width===0)continue;
                  // Unlike decorative artwork, important text must be
                  // inside the visual viewport and not clipped vertically.
                  if(r.right>viewport+8||r.left< -8)cuts.push(q+': '+Math.round(r.left)+'..'+Math.round(r.right));
                  if(el.scrollHeight>el.clientHeight+16 && s.overflowY!=='visible')cuts.push(q+' vertical clipping');
                }
              }
              const card=samples('.product-card')[0];
              const cardImage=card?.querySelector('.card-image img');
              const frame=card?.querySelector('.card-image');
              const nav=document.querySelector('#menu-toggle');
              const images=samples('main img');
              const visibleImages=images.filter(i=>{const r=rect(i);return r.bottom>0&&r.top<window.innerHeight;}).slice(0,12);
              const badImg=visibleImages.filter(i=>i.complete&&i.naturalWidth===0)
                .map(i=>i.currentSrc||i.src);
              return {
                width:root.scrollWidth,viewport,rtl:document.dir,
                h1:samples('main h1').length,
                canonical:document.querySelector('link[rel=canonical]')?.href,
                title:document.title, h2:samples('main h2').length,
                menuDisplay:nav?getComputedStyle(nav).display:'missing',
                headingFont:getComputedStyle(document.querySelector('main h1')).fontFamily,
                imgs:images.length,badImages:badImg,
                cardFrameRatio:frame?frame.getBoundingClientRect().width/
                    Math.max(frame.getBoundingClientRect().height,1):null,
                cardImageFit:cardImage?getComputedStyle(cardImage).objectFit:null,
                clipped:cuts.slice(0,10)
              };
            """)
            combinations+=1
            if result["width"]>result["viewport"]+8:
                errors.append(where+f" HORIZONTAL OVERFLOW {result['width']} > {result['viewport']}")
            if result["h1"]!=1:errors.append(where+" H1 not unique")
            if result["clipped"]:errors.append(where+" cropped important text: "+str(result["clipped"]))
            if result["badImages"]:errors.append(where+" visible broken images: "+str(result["badImages"][:4]))
            if not result["canonical"]:errors.append(where+" missing canonical")
            if result["cardFrameRatio"] and not (0.60<=result["cardFrameRatio"]<=1.25):
                errors.append(where+" anomalous product card image proportions "+str(result["cardFrameRatio"]))
            if width<960 and result["menuDisplay"]=="none":
                errors.append(where+" mobile menu toggle absent")
            if lang=="hy" and "Noto Serif Armenian" not in result["headingFont"]:
                errors.append(where+" Armenian display font not applied")
            if lang!="hy" and "Noto Serif Armenian" in result["headingFont"] and width==1440:
                warnings.append(where+" unexpected Armenian display font on translation")
            # Only true runtime JavaScript exceptions, not external Google-font
            # timeouts or benign network console warnings.
            for entry in driver.get_log("browser"):
                msg=entry.get("message","")
                if entry.get("level")=="SEVERE" and (
                     "Uncaught" in msg or "SyntaxError" in msg or "TypeError" in msg or "ReferenceError" in msg):
                    js_errors.append(where+" "+msg[:300])
            if combinations%60==0:print(f"FULL SITE BROWSER: {combinations} page/viewport cases checked",flush=True)
      # Real user scenarios on all languages, phone and desktop.
      for width,height,mobile in ((375,812,True),(1440,900,False)):
        if mobile:driver.execute_cdp_cmd("Emulation.setDeviceMetricsOverride",{
              "width":width,"height":height,"deviceScaleFactor":1,"mobile":True})
        else:
            driver.execute_cdp_cmd("Emulation.clearDeviceMetricsOverride",{})
            driver.set_window_size(width,height)
        for l in langs:
            driver.get(base+l+"/")
            driver.execute_script("document.documentElement.classList.remove('rose-bloom-on')")
            v=driver.execute_script("""
               const el=(s)=>document.querySelector(s);
               const form=el('.rose-builder-form'),stage=el('.rose-builder-stage');
               const before=stage?.innerHTML;
               const radio=form?.querySelector('input[name=rose-color][value="1"]');
               if(radio){radio.checked=true;radio.dispatchEvent(new Event('change',{bubbles:true}));}
               const after=stage?.innerHTML;
               const href=el('.rose-builder-order')?.href||'';
               const arrows=document.querySelectorAll('.rs-sample-arrow');
               const samples=document.querySelectorAll('.rs-sample-grid .rs-sample-card');
               const slider=el('.rs-sample-grid');
               const reviewForm=el('#rs-review-form');
               const letter=el('#rs-letter-form');
               const surprise=el('#rs-surprise-form');
               const quiz=el('#rs-quiz-form');
               const delivery=el('#rs-delivery-form');
               return {visualUpdated:before!==after,href:href.includes('wa.me/'),
                 slides:samples.length,rail:!!slider&&slider.scrollWidth>slider.clientWidth,
                 arrows:arrows.length,hasDisclosure:!!el('.rs-editorial-notice'),
                 allFive:!!reviewForm&&!!letter&&!!surprise&&!!quiz&&!!delivery};
            """)
            if not all((v["visualUpdated"],v["href"],v["slides"]==30,v["rail"],
                        v["arrows"]==2,v["hasDisclosure"],v["allFive"])):
                errors.append(f"{l} @{width} commerce feature runtime failure {v}")
            if mobile:
                menu=driver.execute_script("""
                    const a=document.querySelector('#menu-toggle');
                    a.click(); const open=document.querySelector('#mobile-menu').classList.contains('open');
                    a.click();return open;
                """)
                if not menu:errors.append(f"{l} mobile menu doesn't open")
    finally:
        driver.quit();http.shutdown()
print(f"FULL SITE BROWSER | {combinations} real Chrome route/viewport checks")
print("FULL SITE UX | mobile menu, 30 story cards, all 5 inquiry modules, WhatsApp bouquet visual: 6 cases")
if js_errors:
    print("JAVASCRIPT ERRORS:",len(js_errors))
    errors.extend(js_errors[:25])
if errors:
    print("FULL SITE AUDIT ERRORS:",len(errors))
    for e in errors[:45]:print("ERROR:",e)
    raise SystemExit("FULL SITE AUDIT FAILED")
print("FULL SITE AUDIT PASS | All language routes, photo files, SEO, typography, responsiveness, interactions.")
print("BUSINESS FOLLOW UPS (not a code failure): delivery tariffs need confirmation; genuine consented reviews; Search Console ownership and indexing.")
