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
            if lang=="hy":
                fontcheck=driver.execute_script("""
                  const family=s=>{const el=document.querySelector(s);return el?getComputedStyle(el).fontFamily:'';};
                  return {
                    loaded:!!document.querySelector('link[href*="armenian-elegance.css"]'),
                    body:family('body'),
                    h1:family('main h1'),
                    builder:family('.rose-builder-header h2'),
                    service:family('.rs-cardhead h3'),
                    form:family('.rs-form input')
                  };
                """)
                if not fontcheck["loaded"] or "Noto Sans Armenian" not in fontcheck["body"] or "Noto Serif Armenian" not in fontcheck["h1"]:
                    errors.append(lang+path+" Armenian typography stylesheet and family test failed: "+str(fontcheck))
                if path=="/" and not all("Noto Serif Armenian" in fontcheck[key] for key in ("builder","service")):
                    errors.append(lang+path+" Armenian services display fonts failed: "+str(fontcheck))
                if path=="/" and "Noto Sans Armenian" not in fontcheck["form"]:
                    errors.append(lang+path+" Armenian form font failed: "+str(fontcheck))
            elif driver.execute_script("return Array.from(document.querySelectorAll('link[rel=stylesheet]')).some(x=>x.href.includes('armenian-elegance.css'))"):
                errors.append(lang+path+" Armenian-only stylesheet leaked into another locale")
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
                      forms:document.querySelectorAll('.rs-form').length,
                      sampleCount:document.querySelectorAll('.rs-sample-grid .rs-sample-card').length,
                      sampleScrollable:(()=>{
                        const rail=document.querySelector('.rs-sample-grid');
                        return !!rail&&getComputedStyle(rail).gridAutoFlow==='column'&&
                          rail.scrollWidth>rail.clientWidth+50;})(),
                      sampleNotice:!!document.querySelector('.rs-editorial-notice'),
                      sampleArrows:document.querySelectorAll('.rs-sample-arrow').length,
                      samplePerCardLabels:document.querySelectorAll('.rs-sample-card small').length}
                """)
                if not all([state["svgChanged"],state["whatsapp"],state["uniqueLabel"],state["quiz"]]):
                    errors.append(where+" interactive form check failed: "+str(state))
                if state["sampleCount"]!=30 or not state["sampleScrollable"] or not state["sampleNotice"] or state["sampleArrows"]!=2 or state["samplePerCardLabels"]!=0:
                    errors.append(where+" editorial carousel check failed: "+str(state))
                if mobile:
                    menu=driver.execute_script("""
                        const btn=document.querySelector('#menu-toggle');
                        btn.click();
                        const shown=document.querySelector('#mobile-menu').classList.contains('open');
                        btn.click();
                        return shown;
                    """)
                    if not menu:errors.append(where+" mobile menu not opening")
      # Small-phone check: long Armenian headings should never force a
      # sideways page scroll on 320px devices.
      driver.execute_cdp_cmd("Emulation.setDeviceMetricsOverride",{
        "width":320,"height":700,"deviceScaleFactor":1,"mobile":True
      })
      for lang in ("hy","ru","en"):
          for route in ("/","/catalog/"):
              driver.get(urlroot+"/"+lang+route)
              driver.execute_script("document.documentElement.classList.remove('rose-bloom-on')")
              dim=driver.execute_script("""
                  const r=document.documentElement;
                  return {width:r.scrollWidth,viewport:r.clientWidth,
                    title:getComputedStyle(document.querySelector('main h1')).fontFamily};
              """)
              tested+=1
              if dim["width"]>dim["viewport"]+8:
                  errors.append(lang+route+" 320px device horizontal overflow: "+str(dim))
      # Test encrypted first-time credential setup, recurring password
      # login, and GitHub publishing; mock all external writes.
      import base64
      fixture=base64.b64encode((Path(__file__).resolve().parents[2]/".github/admin-data.json").read_bytes()).decode("ascii")
      for admin_mobile in (True,False):
          if admin_mobile:
              driver.execute_cdp_cmd("Emulation.setDeviceMetricsOverride",{
                  "width":375,"height":812,"deviceScaleFactor":1,"mobile":True
              })
          else:
              driver.execute_cdp_cmd("Emulation.clearDeviceMetricsOverride",{})
              driver.set_window_size(1440,900)
          driver.get(urlroot+"/admin/")
          driver.execute_script("localStorage.removeItem('rose_co_admin_encrypted_v1')")
          driver.refresh()
          driver.execute_script("""
            window.__savedAdminData=null;
            window.confirm=()=>true;
            const fixture=arguments[0];
            window.fetch=async (url,opts={})=>{
              if(url.includes('/contents/.github/admin-data.json')){
                if(opts.method==='PUT'){
                  const req=JSON.parse(opts.body);
                  const bytes=Uint8Array.from(atob(req.content),x=>x.charCodeAt(0));
                  window.__savedAdminData=JSON.parse(new TextDecoder().decode(bytes));
                  return {ok:true,json:async()=>({content:{sha:'mock-new-sha'}})};
                }
                return {ok:true,json:async()=>({sha:'mock-old-sha',content:fixture})};
              }
              throw Error('Unexpected test network request: '+url);
            };
            document.querySelector('#setup-user').value='roseowner';
            document.querySelector('#setup-password').value='strong-test-password-1234';
            document.querySelector('#setup-confirm').value='strong-test-password-1234';
            document.querySelector('#setup-token').value='github_pat_test_no_permissions';
            document.querySelector('#setup-form').dispatchEvent(new Event('submit',{bubbles:true,cancelable:true}));
          """,fixture)
          from selenium.webdriver.support.ui import WebDriverWait
          WebDriverWait(driver,9).until(lambda x:x.execute_script("return !document.querySelector('#workspace').hidden && !!localStorage.getItem('rose_co_admin_encrypted_v1') && document.querySelector('#setup-token').value===''"))
          logged=driver.execute_script("""
             const vault=localStorage.getItem('rose_co_admin_encrypted_v1')||'';
             return {workspace:!document.querySelector('#workspace').hidden,
               list:document.querySelectorAll('.item').length,
               editor:!document.querySelector('#product-fields').hidden,
               width:document.documentElement.scrollWidth,
               viewport:document.documentElement.clientWidth,
               vault:!!vault,
               safe:!vault.includes('github_pat_test')&&!vault.includes('strong-test-password'),
               tokenField:document.querySelector('#setup-token').value};
          """)
          if not all([logged["workspace"],logged["list"]>=60,logged["editor"],
                      logged["width"]<=logged["viewport"]+8,
                      logged["vault"],logged["safe"],not logged["tokenField"]]):
              errors.append("Encrypted admin account setup failed: "+str(logged))
              continue
          # Password-only login on the same browser after sign out.
          driver.execute_script("""
            document.querySelector('#disconnect').click();
            document.querySelector('#login-user').value='roseowner';
            document.querySelector('#login-password').value='strong-test-password-1234';
            document.querySelector('#login-form').dispatchEvent(new Event('submit',{bubbles:true,cancelable:true}));
          """)
          WebDriverWait(driver,9).until(lambda x:x.execute_script("return !document.querySelector('#workspace').hidden"))
          driver.execute_script("""
              const price=document.querySelector('#product-price');
              price.value='12999';
              price.dispatchEvent(new Event('input',{bubbles:true}));
              document.querySelector('#publish').click();
          """)
          WebDriverWait(driver,6).until(lambda x:x.execute_script("return !!window.__savedAdminData"))
          output=driver.execute_script("""
            return {saved:!!window.__savedAdminData,
              price:window.__savedAdminData?.products[0]?.price_amd,
              hidden:document.querySelector('#auth').hidden};
          """)
          if not output["saved"] or output["price"]!=12999 or not output["hidden"]:
              errors.append("Admin password login & publish test failed: "+str(output))
      print("Rose & Co Admin QA: encrypted first-time setup, password-only sign-in and GitHub mock publish passed on phone and desktop.")
      print(f"Rose & Co Chrome QA: checked {tested} page/viewport combinations,")
      print("320px and 375px mobile, 1440px desktop, 3 languages, 4 major routes.")
      print("Bouquet previews, WhatsApp links, label focus and mobile navigation checked.")
      if errors:
          print("Browser QA issues:",*errors,sep="\n- ")
          raise SystemExit("Browser QA FAILED.")
      print("Rose & Co BROWSER QA PASS.")
    finally:
      driver.quit()
      http.shutdown()
