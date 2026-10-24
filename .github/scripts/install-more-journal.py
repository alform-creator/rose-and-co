#!/usr/bin/env python3
"""Publish ten extra illustrated florist journal posts in Armenian, Russian, English.

Applied after the six-feature journal expansion and final-site-polish.
It preserves the existing 10 articles per language. Pictures come from
existing Rose & Co customer photographs, never generic placeholders.
"""
from pathlib import Path
from bs4 import BeautifulSoup
from html import escape
from xml.etree.ElementTree import Element, SubElement, ElementTree
import json
import re
import sys

root=Path(sys.argv[1]).resolve()
repo=Path(__file__).resolve().parents[2]
input_dir=repo/'.github'/'journal-extra-2026'
source='/rose-and-co/assets/images/real-2026/'
site_root='https://alform-creator.github.io/rose-and-co/'
langs=('hy','ru','en')
paths=sorted(input_dir.glob('part-*.json'))
assert len(paths)==2, f'Expected two article data parts, found {len(paths)}'
articles=[]
for path in paths:
    data=json.loads(path.read_text(encoding='utf-8'))
    assert len(data)==5, f'Expected 5 articles in {path}'
    articles.extend(data)
assert len(articles)==10
slugs=[row['slug'] for row in articles]
assert len(set(slugs))==10
for row in articles:
    assert re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',row['slug'])
    assert (root/'assets'/'images'/'real-2026'/row['image']).is_file(),f'Unavailable photo: {row["image"]}'
    for lang in langs:
        parts=row['langs'][lang]
        assert len(parts)==11,f'{row["slug"]}: expected 11 {lang} text fields, got {len(parts)}'
        assert all(isinstance(s,str) and s.strip() for s in parts)
        assert len(parts[1])<200,'Keep summaries suitable for search descriptions'

translations={
 'hy':{
    'back':'← Վերադառնալ բլոգ',
    'read':'Կարդալ հոդվածը ↗',
    'intro':'Իրական ծաղիկների լուսանկարներ և խորհուրդներ Rose & Co-ից։',
    'cta':'Դիտել ծաղկեփնջերի կատալոգը ↗',
 },
 'ru':{
    'back':'← Вернуться в блог',
    'read':'Читать статью ↗',
    'intro':'Реальные фотографии цветочных работ и советы от Rose & Co.',
    'cta':'Посмотреть каталог букетов ↗',
 },
 'en':{
    'back':'← Back to journal',
    'read':'Read story ↗',
    'intro':'Real floral photography and practical advice from Rose & Co.',
    'cta':'Explore the flower catalog ↗',
 },
}
today='2026-10-25'

def make_card(item,lang,index):
    title,summary=item['langs'][lang][:2]
    url=f'/rose-and-co/{lang}/journal/{item["slug"]}/'
    photo=source+item['image']+'?v=journal20-20261025'
    markup=(f'<a class="journal-card" href="{url}">'
        f'<div class="journal-photo"><img src="{photo}" loading="lazy" '
        f'decoding="async" width="820" height="950" '
        f'alt="{escape(title,quote=True)}"/>'
        f'<span class="journal-index">{index:02d}</span></div>'
        f'<span class="eyebrow">ROSE &amp; CO JOURNAL</span>'
        f'<h3>{escape(title)}</h3><p>{escape(summary)}</p>'
        f'<span class="journal-read">{translations[lang]["read"]}</span></a>')
    card=BeautifulSoup(markup,'html.parser').select_one('a.journal-card')
    assert card is not None
    return card

def replace_metadata(soup,selector,key,value):
    tag=soup.select_one(selector)
    if tag:tag[key]=value

for lang in langs:
    journal_path=root/lang/'journal'/'index.html'
    soup=BeautifulSoup(journal_path.read_text(encoding='utf-8'),'html.parser')
    grid=soup.select_one('.journal-grid')
    assert grid is not None, 'Journal grid missing'
    count=len(grid.select(':scope > .journal-card'))
    assert count==10, f'Expected existing ten articles, got {count} in {lang}'
    template=(root/lang/'journal'/'flower-care'/'index.html').read_text(encoding='utf-8')
    for n,item in enumerate(articles,11):
        title,summary,h2a,p1,p2,h3,p3,p4,h2b,p5,p6=item['langs'][lang]
        photo=source+item['image']+'?v=journal20-20261025'
        canonical=f'{site_root}{lang}/journal/{item["slug"]}/'
        grid.append(make_card(item,lang,n))
        page=BeautifulSoup(template,'html.parser')
        main=page.select_one('main')
        assert main is not None
        body=(f'<section class="article-hero container">'
              f'<a class="article-back" href="/rose-and-co/{lang}/journal/">{translations[lang]["back"]}</a>'
              f'<span class="eyebrow">ROSE &amp; CO · THE JOURNAL</span>'
              f'<h1>{escape(title)}</h1><p>{escape(summary)}</p>'
              f'<div class="article-photo"><img src="{photo}" '
              f'alt="{escape(title,quote=True)}" width="820" height="950" '
              f'loading="eager" decoding="async"/></div></section>'
              f'<article class="container article-body">'
              f'<h2 class="seo-article-h2">{escape(h2a)}</h2>'
              f'<p>{escape(p1)}</p><p>{escape(p2)}</p>'
              f'<h3 class="seo-article-h3">{escape(h3)}</h3>'
              f'<p>{escape(p3)}</p><p>{escape(p4)}</p>'
              f'<h2 class="seo-article-h2">{escape(h2b)}</h2>'
              f'<p>{escape(p5)}</p><p>{escape(p6)}</p>'
              f'<div class="journal-article-cta"><span class="eyebrow">ROSE &amp; CO</span>'
              f'<p>{escape(translations[lang]["intro"])}</p>'
              f'<a class="button btn-burgundy" href="/rose-and-co/{lang}/catalog/">'
              f'{translations[lang]["cta"]}</a></div></article>'
              f'<div class="container article-return"><a class="button btn-outline" '
              f'href="/rose-and-co/{lang}/journal/">{translations[lang]["back"]}</a></div>')
        main.clear()
        for element in list(BeautifulSoup(body,'html.parser').contents):
            main.append(element)
        assert len(page.select('main h1'))==1
        page.title.string=title+' | Rose & Co'
        for selector,value in (
            ('meta[name="description"]',summary),
            ('meta[property="og:description"]',summary),
            ('meta[property="og:title"]',title+' — Rose & Co'),
            ('meta[property="og:image"]',site_root+'assets/images/real-2026/'+item['image']),
        ):
            replace_metadata(page,selector,'content',value)
        for alt in page.select('link[rel="alternate"]'):
            hl=alt.get('hreflang')
            if hl in langs:alt['href']=f'/rose-and-co/{hl}/journal/{item["slug"]}/'
            elif hl=='x-default':alt['href']=f'/rose-and-co/hy/journal/{item["slug"]}/'
        oldcanon=page.select_one('link[rel="canonical"]')
        if oldcanon:oldcanon['href']=canonical
        else:page.head.append(page.new_tag('link',rel='canonical',href=canonical))
        ld=page.new_tag('script',type='application/ld+json')
        ld.string=json.dumps({
            '@context':'https://schema.org',
            '@type':'BlogPosting','headline':title,'description':summary,
            'image':site_root+'assets/images/real-2026/'+item['image'],
            'datePublished':today,'dateModified':today,'inLanguage':lang,
            'mainEntityOfPage':canonical,
            'publisher':{'@type':'Organization','name':'Rose & Co'},
        },ensure_ascii=False)
        page.head.append(ld)
        folder=root/lang/'journal'/item['slug']
        assert not folder.exists(),f'New journal path already exists: {folder}'
        folder.mkdir(parents=True)
        (folder/'index.html').write_text(str(page),encoding='utf-8')
    assert len(grid.select(':scope > .journal-card'))==20
    journal_path.write_text(str(soup),encoding='utf-8')

    # Surface three additional articles on the homepage; the 6-card,
    # 3-column gallery has no incomplete row on desktop.
    home=root/lang/'index.html'
    hs=BeautifulSoup(home.read_text(encoding='utf-8'),'html.parser')
    highlights=hs.select_one('.journal-grid')
    assert highlights is not None
    assert len(highlights.select(':scope > .journal-card'))==3
    for i in (0,3,9):  # roses, birthday flowers, flower boxes
        highlights.append(make_card(articles[i],lang,11+i))
    assert len(highlights.select(':scope > .journal-card'))==6
    home.write_text(str(hs),encoding='utf-8')

# Cover the image frame edge to edge for every journal image (old and new).
# The product catalog retains its separate full-photo object-fit:contain rules.
style=root/'assets'/'styles.css'
css=style.read_text(encoding='utf-8')
marker='/* ROSE-CO-JOURNAL-20-NO-GAPS-20261025 */'
assert marker not in css,'Journal expansion should run once in a clean deployment'
css+=r'''

/* ROSE-CO-JOURNAL-20-NO-GAPS-20261025
   All editorial thumbnails use the exact same cropping window without
   letterboxing; only article photography is affected, never product photos. */
.journal-grid {display:grid;align-items:stretch;row-gap:34px;column-gap:22px;}
.journal-grid .journal-card {display:flex;flex-direction:column;min-width:0;height:100%;margin:0;}
.journal-grid .journal-photo {
  display:block;position:relative;aspect-ratio:4/3;
  width:100%;height:auto;min-height:0;max-height:none;overflow:hidden;
  padding:0;margin:0 0 15px;border-radius:3px;background:#eee5e1;
}
.journal-grid .journal-photo img,
.journal-grid .journal-photo img[src*="wreaths-"] {
  position:absolute;inset:0;width:100%;height:100%;
  object-fit:cover;object-position:center center;
  display:block;background:transparent;
}
.journal-grid .journal-photo .journal-index {position:absolute;z-index:2;}
.journal-card > h3 {line-height:1.37;margin:11px 0 10px;overflow-wrap:break-word;}
.journal-card > p {
  margin:0 0 18px;
  line-height:1.8;
  display:-webkit-box;-webkit-box-orient:vertical;
  -webkit-line-clamp:3;line-clamp:3;overflow:hidden;
}
.journal-card > .journal-read {margin-top:auto;align-self:flex-start;}
/* Twenty journal posts make five full rows on desktop, ten on tablet,
   and twenty on phone. The homepage has six: two complete desktop rows. */
@media (min-width:1101px) {
 html[data-page="journal"] .journal-grid {grid-template-columns:repeat(4,minmax(0,1fr));}
 html[data-page="home"] .journal-grid {grid-template-columns:repeat(3,minmax(0,1fr));}
 html[data-page="journal"] .journal-card > h3 {font-size:clamp(18px,1.62vw,23px);}
 html[lang="hy"][data-page="journal"] .journal-card > h3 {font-size:clamp(17px,1.52vw,22px);}
}
@media (min-width:641px) and (max-width:1100px) {
 html[data-page="journal"] .journal-grid,
 html[data-page="home"] .journal-grid {grid-template-columns:repeat(2,minmax(0,1fr));}
}
@media (max-width:640px) {
 html[data-page="journal"] .journal-grid,
 html[data-page="home"] .journal-grid {grid-template-columns:minmax(0,1fr);row-gap:30px;}
 .journal-grid .journal-photo {aspect-ratio:4/3;}
 .journal-card > h3,html[lang="hy"] .journal-card > h3 {
   min-height:0;font-size:22px;line-height:1.39;
 }
}
/* Uniform article photography, without wide empty borders on tall photos. */
.article-photo {position:relative;display:block;aspect-ratio:16/9;height:auto;overflow:hidden;background:#ede3df;}
.article-photo img,
.article-photo img[src*="wreaths-"] {
  width:100%;height:100%;object-fit:cover;object-position:center;
  background:transparent;
}
@media (max-width:640px) {.article-photo {aspect-ratio:4/3;}}
'''
style.write_text(css,encoding='utf-8')

# Force a fresh stylesheet on all pages, including the original 10 articles.
for htmlfile in root.rglob('*.html'):
    html=htmlfile.read_text(encoding='utf-8')
    html=re.sub(r'(/rose-and-co/assets/styles\.css)(?:\?v=[\w-]+)?',
        r'\1?v=journal20-20261025',html)
    htmlfile.write_text(html,encoding='utf-8')

# Rebuild sitemap after all 30 newly localized pages have been created.
urls=[site_root]
for lang in langs:
    for p in sorted((root/lang).rglob('index.html')):
        urls.append(site_root+p.parent.relative_to(root).as_posix()+'/')
urlset=Element('urlset',{'xmlns':'http://www.sitemaps.org/schemas/sitemap/0.9'})
for url in sorted(set(urls)):
    row=SubElement(urlset,'url')
    SubElement(row,'loc').text=url
ElementTree(urlset).write(root/'sitemap.xml',encoding='utf-8',xml_declaration=True)

# Deployment check: exactly 20 articles + journal listing for each language.
for lang in langs:
    pages=list((root/lang/'journal').rglob('index.html'))
    assert len(pages)==21,(lang,len(pages))
    listing=BeautifulSoup((root/lang/'journal'/'index.html').read_text(encoding='utf-8'),'html.parser')
    cards=listing.select('.journal-grid > .journal-card')
    assert len(cards)==20,(lang,len(cards))
    for card in cards:
        img=card.select_one('.journal-photo img')
        assert img is not None
        assert img.get('src','').startswith(source)
print('Rose & Co: added 10 new posts per language (30 pages), total 20 posts each, equal-size filled photos, updated sitemap.')
