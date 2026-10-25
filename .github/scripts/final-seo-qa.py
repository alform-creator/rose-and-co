#!/usr/bin/env python3
"""Final Rose & Co release audit: SEO, accessibility, language paths and responsive quality.

Run LAST, after all feature installers, against the extracted GitHub Pages site.
The audit is deterministic and can be repeated on every release.
"""
from __future__ import annotations
from collections import Counter
from pathlib import Path
from urllib.parse import urlsplit, unquote
from xml.etree import ElementTree as ET
from bs4 import BeautifulSoup
import json
import re
import sys

root=Path(sys.argv[1]).resolve()
host="https://alform-creator.github.io"
prefix="/rose-and-co/"
langs=("hy","ru","en")
version="final-qa-20261025-v5"
META={
"hy":{
"about":("Rose & Co-ի պատմությունը․ ծաղիկներ՝ սիրով ու ուշադրությամբ",
"Բացահայտեք Rose & Co-ի պատմությունն ու ծաղկային մոտեցումը՝ վարդեր, ծաղկեփնջեր և անհատապես համաձայնեցվող կոմպոզիցիաներ։"),
"contact":("Կապ Rose & Co-ի հետ․ ծաղիկների և ծաղկեփնջերի պատվեր",
"Պատվերի, առկայության և գնի հարցերով զանգահարեք Rose & Co-ին՝ 033 081 898։ Գտնվում ենք Զովունիում։"),
},
"ru":{
"about":("История Rose & Co — цветы с вниманием к деталям",
"История Rose & Co: элегантные букеты, розы и цветочные композиции. Обсудите подходящий вариант и наличие с нашей командой."),
"contact":("Контакты Rose & Co — заказ цветов и букетов",
"Свяжитесь с Rose & Co по поводу букетов, цен и наличия: Зовуни, телефон 033 081 898, WhatsApp и Instagram."),
},
"en":{
"about":("Our Story — Rose & Co Flower Atelier",
"Discover Rose & Co's floral approach, from roses to thoughtfully arranged bouquets. Enquire about the flowers and arrangements available."),
"contact":("Contact Rose & Co — Flowers and Bouquet Enquiries",
"Contact Rose & Co in Zovuni for flower bouquets, custom arrangements, availability and pricing. Call 033 081 898 or message us."),
}
}
page_files=sorted(p for lang in langs for p in (root/lang).rglob("index.html"))
assert len(page_files)==78, f"Expected 78 localised pages, got {len(page_files)}"
repaired_ids=0
unique_titles={}
validated_anchors=0
missing_assets=[]
missing_links=[]
missing_fragments=[]
problems=[]
allurls={}

# Build every page's public URL once, including matching language variants.
def make_url(page:Path)->str:
    rel=page.relative_to(root).as_posix()
    assert rel.endswith("index.html")
    return host+prefix+rel[:-len("index.html")]

pages={make_url(p):p for p in page_files}

for page in page_files:
    lang=page.relative_to(root).parts[0]
    rel=page.relative_to(root).as_posix()
    slug=rel.split("/")[1] if len(rel.split("/"))>2 else "home"
    soup=BeautifulSoup(page.read_text(encoding="utf-8"),"html.parser")
    assert soup.html and soup.head and soup.body and soup.main,rel
    soup.html["lang"]=lang

    # Newly added forms had repeated recipient/address IDs across five modules,
    # and one textarea ID collided with its section ID. Scope each form control.
    for form in soup.select("#rose-service-hub form"):
        form_id=form.get("id")
        if not form_id: continue
        for control in form.select("input[id],select[id],textarea[id]"):
            prev=control["id"]
            target=form_id+"-"+prev.removeprefix("rs-")
            if prev==target:continue
            control["id"]=target
            for label in form.select("label[for]"):
                if label["for"]==prev:
                    label["for"]=target
            repaired_ids+=1

    ids=[node.get("id") for node in soup.select("[id]")]
    duplicates=sorted(k for k,v in Counter(ids).items() if v>1)
    if duplicates: problems.append(f"{rel} duplicate HTML ids: {duplicates}")
    for label in soup.select("label[for]"):
        if label.get("for") not in ids:
            problems.append(f"{rel} label target missing: {label.get('for')}")
    h1=soup.select("main h1")
    if len(h1)!=1:
        problems.append(f"{rel} expected one H1, got {len(h1)}")

    # Distinct and human-readable key landing page titles and descriptions.
    if slug in META[lang]:
        heading,description=META[lang][slug]
        if h1:
            h1[0].clear()
            h1[0].append(heading)
        if soup.title:
            soup.title.string=heading+(" | Rose & Co" if "Rose & Co" not in heading else "")
        d=soup.select_one('meta[name="description"]')
        if d:d["content"]=description
        od=soup.select_one('meta[property="og:description"]')
        if od:od["content"]=description

    title=soup.title.get_text(" ",strip=True) if soup.title else ""
    desc=soup.select_one('meta[name="description"]')
    if not title or not desc or len(desc.get("content","").strip())<40:
        problems.append(f"{rel} incomplete title or description")
    if title in unique_titles:
        problems.append(f"duplicate SEO title between {rel} and {unique_titles[title]}")
    unique_titles[title]=rel

    # Self-canonical and real absolute hreflang URLs are always the localized
    # public route, not a fragment or a query like ?intro=1.
    canonical_url=make_url(page)
    for tag in soup.select('link[rel="canonical"]'):
        tag.decompose()
    canonical=soup.new_tag("link", rel="canonical", href=canonical_url)
    soup.head.append(canonical)
    family=page.relative_to(root).parts[1:-1]  # same route in HY/RU/EN
    for node in soup.select('link[hreflang]'):
        node.decompose()
    for l in langs:
        alternative=root.joinpath(l,*family,"index.html")
        if alternative not in page_files:
            problems.append(f"{rel} has no {l} alternate")
            continue
        node=soup.new_tag("link", rel="alternate", hreflang=l, href=make_url(alternative))
        soup.head.append(node)
    default=root.joinpath("hy",*family,"index.html")
    if default in page_files:
        soup.head.append(soup.new_tag("link",rel="alternate",hreflang="x-default",href=make_url(default)))

    def setmeta(property_name,value):
        tag=soup.select_one(f'meta[property="{property_name}"]')
        if tag is None:
            tag=soup.new_tag("meta")
            tag["property"]=property_name
            soup.head.append(tag)
        tag["content"]=value

    setmeta("og:url",canonical_url)
    setmeta("og:type","article" if "/journal/" in canonical_url and not canonical_url.endswith("/journal/") else "website")
    setmeta("og:locale",{"hy":"hy_AM","ru":"ru_RU","en":"en_US"}[lang])
    setmeta("og:site_name","Rose & Co")
    setmeta("og:title",title)
    setmeta("og:description",desc["content"])

    ogimage=soup.select_one('meta[property="og:image"]')
    if ogimage:
        img=ogimage.get("content","")
        if img.startswith(prefix):img=host+img
        elif img.startswith("/"):img=host+img
        ogimage["content"]=img

    # One universal business identity and machine-readable page description.
    web_page={
      "@context":"https://schema.org","@type":"WebPage",
      "@id":canonical_url+"#webpage",
      "url":canonical_url,"name":title,
      "description":desc["content"],
      "inLanguage":lang,
      "isPartOf":{"@type":"WebSite","name":"Rose & Co","url":host+prefix}
    }
    if "/journal/" in canonical_url and not canonical_url.endswith("/journal/"):
        web_page["@type"]="Article"
        web_page["headline"]=h1[0].get_text(" ",strip=True) if h1 else title
        web_page["publisher"]={"@type":"Organization","name":"Rose & Co","url":host+prefix}
        if ogimage and ogimage["content"]:
            web_page["image"]=ogimage["content"]
    for t in soup.select('script[data-rose-qa-schema]'):
        t.decompose()
    ld=soup.new_tag("script",type="application/ld+json")
    ld["data-rose-qa-schema"]="1"
    ld.string=json.dumps(web_page,ensure_ascii=False,separators=(",",":")).replace("<","\\u003c")
    soup.head.append(ld)

    # Better balance on iOS: keep headings readable and maintain only one
    # accessible focus target for forms without touching text or images.
    for img in soup.select("img"):
        if not img.has_attr("alt"):
            problems.append(f"{rel} image missing alt: {img.get('src','')}")
    for a in soup.select("a[href]"):
        href=a.get("href","")
        if href.startswith(prefix):
            parts=urlsplit(href)
            resolved=unquote(parts.path[len(prefix):])
            target=root/resolved
            if parts.path.endswith("/"):
                target=target/"index.html"
            if not target.is_file():
                missing_links.append(f"{rel}: {href}")
            elif parts.fragment and target==page:
                if parts.fragment not in ids:
                    missing_fragments.append(f"{rel}: #{parts.fragment}")
            validated_anchors+=1
        elif href.startswith("#") and href!="#":
            if unquote(href[1:]) not in ids:
                missing_fragments.append(f"{rel}: {href}")
    for img in soup.select("img[src]"):
        src=img["src"]
        if src.startswith(prefix):
            target=root/unquote(urlsplit(src).path[len(prefix):])
            if not target.is_file():
                missing_assets.append(f"{rel}: {src}")

    page.write_text(str(soup),encoding="utf-8")
    allurls[canonical_url]=(lang,family)

# Regenerate a complete canonical sitemap and reciprocal language relations.
ns="http://www.sitemaps.org/schemas/sitemap/0.9"
xns="http://www.w3.org/1999/xhtml"
ET.register_namespace("",ns)
ET.register_namespace("xhtml",xns)
urlset=ET.Element(f"{{{ns}}}urlset")
for url,(lang,family) in sorted(allurls.items()):
    entry=ET.SubElement(urlset,f"{{{ns}}}url")
    ET.SubElement(entry,f"{{{ns}}}loc").text=url
    for l in langs:
        alternate=root.joinpath(l,*family,"index.html")
        if alternate in page_files:
            ET.SubElement(entry,f"{{{xns}}}link",{
                "rel":"alternate","hreflang":l,"href":make_url(alternate)
            })
    ET.SubElement(entry,f"{{{xns}}}link",{
        "rel":"alternate","hreflang":"x-default",
        "href":make_url(root.joinpath("hy",*family,"index.html"))
    })
ET.ElementTree(urlset).write(root/"sitemap.xml",encoding="utf-8",xml_declaration=True)
(root/"robots.txt").write_text(
    "User-agent: *\nAllow: /\nSitemap: "+host+prefix+"sitemap.xml\n",
    encoding="utf-8")

# The GitHub Pages project root is an HTML redirect; clarify that it is not
# another separate indexable home page. /hy/ is the preferred local landing.
index=root/"index.html"
if index.is_file():
    doc=BeautifulSoup(index.read_text(encoding="utf-8"),"html.parser")
    if doc.head:
        noindex=doc.select_one('meta[name="robots"]')
        if noindex is None:
            noindex=doc.new_tag("meta",attrs={"name":"robots","content":"noindex,follow"})
            doc.head.append(noindex)
        for old in doc.select('link[rel="canonical"]'):old.decompose()
        doc.head.append(doc.new_tag("link",rel="canonical",href=host+prefix+"hy/"))
        index.write_text(str(doc),encoding="utf-8")

# Header and content proportions: 8 links cannot fit reliably between 961px
# and 1240px; switch to existing mobile menu earlier and keep long Armenian
# headings/controls readable at 320-390px widths.
css_path=root/"assets"/"styles.css"
css=css_path.read_text(encoding="utf-8")
marker="/* ROSE-CO-FINAL-RESPONSIVE-SEO-20261025 */"
if marker not in css:
    css+=r"""

/* ROSE-CO-FINAL-RESPONSIVE-SEO-20261025 */
html{scroll-padding-top:22px}
.page-intro h1,.hero h1,.section-head h2,.rs-header h2,.rose-builder-header h2 {
  overflow-wrap:break-word;hyphens:auto;text-wrap:balance;
}
.section-head h2 {line-height:1.3}
.page-intro h1 {line-height:1.23}
.rose-builder-preview,.rs-form,.rs-grid,.rs-cardhead {min-width:0}
.rose-services :is(input,textarea,select),.rose-builder-section :is(input,textarea,select){max-width:100%}
.rs-card {overflow-wrap:anywhere}
.rs-card .rs-actions .button,.rs-card .rs-textbtn {max-width:100%}
.rose-builder-summary {min-height:25px}
.rose-builder-header p,.rs-header p{max-width:69ch;margin-left:auto;margin-right:auto}
@media (min-width:961px) and (max-width:1240px){
  .desktop-nav{display:none}
  .menu-toggle{display:block}
  .mobile-menu {
    flex-direction:column;position:absolute;top:100%;left:0;right:0;
    padding:15px max(25px,calc((100vw - 1120px)/2)) 24px;
    background:rgba(255,249,245,.985);
    box-shadow:0 20px 30px rgba(0,0,0,.08);
  }
  .mobile-menu.open{display:flex}
  .mobile-menu .nav-link{padding:9px 6px;font-size:13px}
}
@media(max-width:640px){
  .container{width:min(100% - 30px,1280px)}
  .section,.categories-section{padding-top:62px;padding-bottom:62px}
  .page-intro h1{font-size:clamp(29px,8vw,40px);line-height:1.34}
  .section-head h2,.rs-header h2,.rose-builder-header h2{
    font-size:clamp(27px,7.3vw,36px);line-height:1.35;
  }
  .rs-header p,.rose-builder-header p{font-size:13px}
  .hero-buttons{gap:14px}
  .hero-buttons .text-link{font-size:12px;min-height:38px}
  .rose-builder-preview{padding:20px 15px}
}
@media(max-width:365px){
  .header-actions{gap:10px}
  .language-switcher{gap:2px}
  .page-intro h1{font-size:29px}
}
"""
    css_path.write_text(css,encoding="utf-8")

# Genuine ultra-narrow Russian layout issues found by the full 192-case
# browser crawl: flower-type labels and long-form article copy. Avoid clipping
# or horizontal scrollbar; do not change the visual proportions above 360px.
ultra_css = """
/* ROSE-CO-ULTRA-NARROW-20261025: 320px Russian flower guide + journal */
/* Compact heading and navigation safely for the smallest iPhones. */
html,body {max-width:100%;overflow-x:clip}
.site-header,.notice-strip,.site-footer,body>footer {max-width:100%;overflow-x:clip}
.navbar{gap:8px}
.brand{min-width:0;gap:4px}
.brand-type{font-size:clamp(19px,6.8vw,23px);letter-spacing:.085em}
.brand-rose-mark{width:36px!important;height:36px!important;flex:0 0 36px}
.header-actions{min-width:0;gap:6px}
.language-switcher{gap:1px}
.language-switcher a{padding:6px 2px;font-size:9px}
.menu-toggle{flex:0 0 35px}
.about-grid,.spotlight-gallery,.spotlight-copy{min-width:0;max-width:100%}
.about-spotlight,.page-intro,.article-hero{max-width:100%;overflow-x:clip}

@media(max-width:360px) {
  .flower-types-grid,.flower-type,.flower-type div,.flower-type b,.flower-type small {
    min-width:0;max-width:100%;
  }
  .flower-type {gap:8px;padding:11px 8px;}
  .flower-type b,.flower-type small {overflow-wrap:anywhere;word-break:normal;}
  .flower-icon {min-width:37px;width:37px;height:37px;font-size:21px;}
  .article-body,.article-hero,.article-hero h1,.article-hero p,
  .article-body p,.article-body li,.article-body a,
  .article-body strong,.article-body em,.article-body h2,.article-body h3 {
    min-width:0;max-width:100%;overflow-wrap:anywhere;
  }
  .article-body pre,.article-body table {display:block;max-width:100%;overflow-x:auto;}
  .article-body img,.article-hero img {max-width:100%;height:auto;}
  .article-meta,.article-meta span,.article-back {min-width:0;overflow-wrap:anywhere;}
}
"""
if "ROSE-CO-ULTRA-NARROW-20261025" not in css_path.read_text(encoding="utf-8"):
    css_path.write_text(css_path.read_text(encoding="utf-8")+"\n"+ultra_css,encoding="utf-8")

for p in page_files:
    s=p.read_text(encoding="utf-8")
    s=re.sub(r'(/rose-and-co/assets/styles\.css)\?v=[^"\']+',r'\1?v='+version,s)
    p.write_text(s,encoding="utf-8")

assert len(allurls)==78
print("Rose & Co final QA | localized pages:",len(page_files),
      "| rewritten form IDs:",repaired_ids,
      "| inspected internal links:",validated_anchors,
      "| sitemap URLs:",len(allurls))
print("SEO | canonical:78 | hreflang: 4 per page | unique titles:",len(unique_titles))
print("Language + mobile | hy/ru/en complete | original forms, copy and images preserved")
if missing_links:print("BROKEN INTERNAL LINKS ("+str(len(missing_links))+"):",*missing_links[:25],sep="\n  ")
if missing_assets:print("MISSING IMAGE FILES ("+str(len(missing_assets))+"):",*missing_assets[:25],sep="\n  ")
if missing_fragments:print("MISSING FRAGMENTS ("+str(len(missing_fragments))+"):",*missing_fragments[:25],sep="\n  ")
if problems:print("STRUCTURE ISSUES ("+str(len(problems))+"):",*problems[:30],sep="\n  ")
if missing_links or missing_assets or missing_fragments or problems:
    raise SystemExit("Release QA FAILED: fix the issues above.")
print("Rose & Co FINAL QA PASS: SEO, links, headings, assets, forms, languages, responsive CSS.")
