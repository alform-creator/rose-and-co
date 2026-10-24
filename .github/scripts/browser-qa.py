#!/usr/bin/env python3
"""Browser-based Rose & Co smoke tests at 375px and 1440px via local Chrome."""
from __future__ import annotations
from pathlib import Path
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from tempfile import TemporaryDirectory
from threading import Thread
from urllib.parse import quote
import os
import shutil
import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

site=Path(sys.argv[1]).resolve()
assert (site/"hy/index.html").is_file()
chrome=next((shutil.which(x) for x in (
  "google-chrome","google-chrome-stable","chromium","chromium-browser"
) if shutil.which(x)), None)
if not chrome:
    raise SystemExit("Browser QA requires Chrome/Chromium in GitHub Actions.")

errors=[]
class Quiet(SimpleHTTPRequestHandler):
    def log_message(self,*args):pass

with TemporaryDirectory() as temp:
    base=Path(temp)
    (base/"rose-and-co").symlink_to(site,target_is_directory=True)
    http=ThreadingHTTPServer(("127.0.0.1",0),partial(Quiet,directory=temp))
    thread=Thread(target=http.serve_forever,daemon=True)
    thread.start()
    urlroot=f"http://127.0.0.1:{http.server_address[1]}/rose-and-co"
    options=Options()
    options.binary_location=chrome
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-background-networking")
    options.add_argument("--window-size=1440,900")
    options.page_load_strategy="eager"
    driver=webdriver.Chrome(options=options)
    driver.set_page_load_timeout(25)
    try:
      tested=0
      for mobile in (True,False):
        if mobile:
            driver.execute_cdp_cmd("Emulation.setDeviceMetricsOverride",{
                "width":375,"height":812,"deviceScaleFactor":1,"mobile":True
            })
        else:
            driver.execute_cdp_cmd("Emulation.clearDeviceMetricsOverride",{})
            driver.set_window_size(1440,900)
        for lang in ("hy","ru","en"):
          for path in ("/","/catalog/","/about/","/journal/flower-care/"):
            driver.get(urlroot+"/"+lang+path)
            # Opening intro is intentionally decorative and isn't relevant to
            # geometry. Let site JavaScript load and render before inspection.
            driver.execute_script("document.documentElement.classList.remove('rose-bloom-on')")
            time.sleep(.12)
            result=driver.execute_script("""
                const main=document.querySelector('main'),h1=document.querySelectorAll('main h1');
                const viewport=document.documentElement.clientWidth;
                const width=document.documentElement.scrollWidth;
                const root=window.location.pathname;
                const nav=document.querySelector('.desktop-nav');
                const menu=document.querySelector('.menu-toggle');
                const fav=document.querySelector('#rose-bouquet-builder');
                return {
                  h1:h1.length,main:!!main,viewport,width,
                  canonical:document.querySelector('link[rel=canonical]')?.href,
                  mainWidth:main?.getBoundingClientRect().width,
                  menuVisible:menu?getComputedStyle(menu).display!=='none':false,
                  builder:!!fav,fonts:document.fonts.status
                };
            """)
            tested+=1
            where=f"{lang}{path} {'mobile' if mobile else 'desktop'}"
            if not result["main"] or result["h1"]!=1:
                errors.append(where+" incorrect document structure")
            if not result["canonical"] or not result["canonical"].startswith("https://alform-creator.github.io/rose-and-co/"):
                errors.append(where+" canonical URL missing")
            if result["width"]>result["viewport"]+8:
                errors.append(where+f" horizontal overflow: {result['width']} > {result['viewport']}")
            if mobile and not result["menuVisible"]:
                errors.append(where+" menu toggle invisible")
            if path=="/" and not result["builder"]:
                errors.append(where+" custom bouquet builder missing")
            # Verify browser rendering and form interactivity, not merely HTML.
            if path=="/":
                state=driver.execute_script("""
                    const form=document.querySelector('.rose-builder-form');
                    const svg=document.querySelector('.rose-builder-stage');
                    const before=svg?.innerHTML||'';
                    const inp=form?.querySelector('[name=rose-color][value="1"]');
                    if(inp){inp.checked=true;inp.dispatchEvent(new Event('change',{bubbles:true}));}
                    const after=svg?.innerHTML||'';
                    const href=document.querySelector('.rose-builder-order')?.href||'';
                    const letter=document.querySelector('#rs-letter-form');
                    const label=letter?.querySelector('label[for]');
                    return {svgChanged:before!==after,whatsapp:href.includes('wa.me/'),
                      uniqueLabel:!!label&&!!letter.querySelector('#'+CSS.escape(label.htmlFor)),
                      quiz:!!document.querySelector('#rs-quiz-send'),
                      forms:document.querySelectorAll('.rs-form').length}
                """)
                if not all([state["svgChanged"],state["whatsapp"],state["uniqueLabel"],state["quiz"]]):
                    errors.append(where+" interactive form check failed: "+str(state))
                if mobile:
                    menu=driver.execute_script("""
                        const btn=document.querySelector('#menu-toggle');
                        btn.click();
                        const shown=document.querySelector('#mobile-menu').classList.contains('open');
                        btn.click();
                        return shown;
                    """)
                    if not menu:errors.append(where+" mobile menu not opening")
      print(f"Rose & Co Chrome QA: checked {tested} page/viewport combinations,")
      print("375px mobile, 1440px desktop, 3 languages, 4 major routes.")
      print("Bouquet previews, WhatsApp links, label focus and mobile navigation checked.")
      if errors:
          print("Browser QA issues:",*errors,sep="\n- ")
          raise SystemExit("Browser QA FAILED.")
      print("Rose & Co BROWSER QA PASS.")
    finally:
      driver.quit()
      http.shutdown()
