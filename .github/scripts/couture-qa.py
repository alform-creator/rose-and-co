#!/usr/bin/env python3
"""Independent 78-page localization, data integrity, SEO and UX gates."""
from pathlib import Path
from bs4 import BeautifulSoup
from collections import Counter
from urllib.parse import urlsplit
import json,re,sys
root=Path(sys.argv[1]).resolve()
langs=("hy","ru","en")
pages=sorted(p for l in langs for p in (root/l).rglob("index.html"))
assert len(pages)==96,("Unexpected page count",len(pages))
config=json.loads(Path(".github/admin-data.json").read_text(encoding="utf-8"))
products=[p for p in config["products"] if p.get("enabled",True)]
expected_ids={"product-"+p["id"] for p in products}
assert products and all(p["img"] and p["name"]["hy"] and p["name"]["ru"] and p["name"]["en"] for p in products)
for page in pages:
    name=page.relative_to(root).as_posix()
    language=page.relative_to(root).parts[0]
    tree=BeautifulSoup(page.read_text(encoding="utf-8"),"html.parser")
    assert tree.html["lang"]==language,name
    assert tree.html.get("data-finish")=="couture-v1",name
    assert tree.select_one(".rc-skip[href='#main']"),name
    assert tree.select_one("main#main"),name
    assert len(tree.select("h1"))==1,name
    is_home=name==language+"/index.html"
    # Respect the owner's approved original homepage visual design.
    assert len(tree.select('link[href*="rose-couture-finish.css"]'))==(0 if is_home else 1),name
    assert tree.select_one('link[rel="canonical"]'),name
    assert tree.select_one('meta[property="og:description"]'),name
    desc=tree.select_one('meta[name="description"]')
    og=tree.select_one('meta[property="og:description"]')
    assert desc and og and desc["content"]==og["content"],(name,"meta mismatch")
    assert len(tree.select("link[hreflang]"))==4,(name,"hreflang")
    assert all(img.get("alt") is not None for img in tree.select("img")),(name,"alt")
    ids=[el["id"] for el in tree.select("[id]")]
    repeats=[key for key,n in Counter(ids).items() if n>1]
    assert not repeats,(name,"duplicate element ids",repeats[:8])
    for el in tree.select("a[href^='/rose-and-co/']"):
        href=urlsplit(el["href"]).path.removeprefix("/rose-and-co/")
        target=root/href
        assert (target/"index.html").is_file() if href.endswith("/") else target.is_file(),(name,"broken link",href)
    structured=[]
    for script in tree.select('script[type="application/ld+json"]'):
        structured.append(json.loads(script.string or script.get_text()))
    assert any(obj.get("@type") in ("Article","WebPage") for obj in structured if isinstance(obj,dict)),name
    is_home=name==language+"/index.html"
    is_catalog=name==language+"/catalog/index.html"
    is_contact=name==language+"/contact/index.html"
    if is_home:
        assert not tree.select(".rc-promise-item"),name
        assert tree.select_one(".hero-copy>p") and len(tree.select_one(".hero-copy>p").get_text(strip=True))>80,name
        assert tree.select_one("img.hero-image[fetchpriority='high']"),name
    else:
        assert tree.select_one(".rc-breadcrumb"),name
        assert any(x.get("@type")=="BreadcrumbList" or any(z.get("@type")=="BreadcrumbList" for z in x.get("@graph",[]) if isinstance(z,dict)) for x in structured if isinstance(x,dict)),name
    if is_catalog:
        assert len(tree.select(".rc-guide-qa"))==3,name
        got={node["id"] for node in tree.select("#catalog-grid .product-card[id]")}
        assert got==expected_ids,(name,"product codes mismatch",len(got),len(expected_ids))
        itm=next(x for x in structured if isinstance(x,dict) and x.get("@type")=="ItemList")
        assert itm.get("numberOfItems")==len(products),name
        assert len(itm["itemListElement"])==len(products),name
        for n,entry in enumerate(itm["itemListElement"],1):
            assert entry["position"]==n,name
            assert (entry["item"]["url"].split("#")[-1] in expected_ids),name
    if is_contact:assert tree.select_one(".rc-buying-help"),name
css=(root/"assets/rose-couture-finish.css").read_text(encoding="utf-8")
assert ".rc-skip:focus" in css and "prefers-reduced-motion" in css
app=(root/"assets/app.js").read_text(encoding="utf-8")
assert "p.price_amd ? Number(p.price_amd)" in app
print("COUTURE QA PASS: 96 pages / 3 languages / canonical and hreflang / schema / product links / images / local guide / admin prices / internal links.")
