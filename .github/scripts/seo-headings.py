#!/usr/bin/env python3
"""Improve Rose & Co heading keywords without altering product names or images."""
from pathlib import Path
import sys, re
root=Path(sys.argv[1])
mapping={
"hy":{
"home":[("h1","Ծաղիկներ՝ զգացմունքների լեզվով","Ծաղիկներ և ծաղկեփնջեր Հայաստանում՝ Rose & Co"),
("h2","Ստեղծված ամեն առիթի համար","Ծաղիկներ և ծաղկեփնջեր՝ յուրաքանչյուր առիթի համար"),
("h2","Հատուկ ընտրված ծաղկեփնջեր","Գեղեցիկ ծաղկեփնջեր և վարդեր Հայաստանում"),
("h2","Ծաղիկների տեսակների ուղեցույց","Ծաղիկների տեսակներ՝ վարդեր, քրիզանթեմներ և այլ ծաղիկներ"),
("h2","Մեր ծաղկային օրագիրը","Ծաղիկների և ծաղկեփնջերի խնամքի խորհուրդներ")],
"catalog":[("h1","Կատալոգ","Ծաղիկների և ծաղկեփնջերի կատալոգ Հայաստանում")],
"flowers":[("h1","Ծաղիկների տեսակներ","Ծաղիկների տեսակներ Հայաստանում՝ վարդեր և այլ ծաղիկներ")],
"about":[("h1","Մեր մասին","Rose & Co՝ ծաղիկներ և ծաղկեփնջեր Հայաստանում")],
"contact":[("h1","Կապ","Ծաղիկների և ծաղկեփնջերի պատվեր՝ կապ Rose & Co-ի հետ")],
"journal":[("h1","Բլոգ","Բլոգ՝ ծաղիկներ, ծաղկեփնջեր և խնամքի խորհուրդներ")]},
"ru":{
"home":[("h1","Цветы — язык чувств","Цветы и букеты в Армении — Rose & Co"),
("h2","Цветы на любой случай","Цветы и букеты для любого повода"),
("h2","Избранные букеты","Красивые букеты и розы в Армении"),
("h2","Путеводитель по цветам","Виды цветов: розы, хризантемы и другие"),
("h2","Наш цветочный журнал","Советы по уходу за цветами и букетами")],
"catalog":[("h1","Каталог","Каталог цветов и букетов в Армении")],
"flowers":[("h1","Виды цветов","Виды цветов в Армении: розы и другие цветы")],
"about":[("h1","О нас","Rose & Co — цветы и букеты в Армении")],
"contact":[("h1","Контакты","Заказать цветы и букеты — контакты Rose & Co")],
"journal":[("h1","Блог","Блог о цветах, букетах и уходе за ними")]},
"en":{
"home":[("h1","Flowers speak the language of feeling","Flowers and bouquets in Armenia — Rose & Co"),
("h2","Made for every occasion","Flowers and bouquets for every occasion"),
("h2","Curated bouquets","Beautiful bouquets and roses in Armenia"),
("h2","A guide to flower varieties","Flower varieties: roses, chrysanthemums and more"),
("h2","The floral journal","Flower and bouquet care tips")],
"catalog":[("h1","Collection","Flowers and bouquets catalog in Armenia")],
"flowers":[("h1","Flower varieties","Flower varieties in Armenia: roses and more")],
"about":[("h1","Our story","Rose & Co — flowers and bouquets in Armenia")],
"contact":[("h1","Contact","Order flowers and bouquets — contact Rose & Co")],
"journal":[("h1","Journal","Flower and bouquet journal: care and inspiration")]}}
changed=0
for lang, pages in mapping.items():
 for page, rules in pages.items():
  file=root/lang/("index.html" if page=="home" else f"{page}/index.html")
  if not file.exists():raise FileNotFoundError(file)
  text=file.read_text(encoding="utf-8")
  for tag, old, new in rules:
   oldhtml=f"<{tag}>{old}</{tag}>"
   newhtml=f"<{tag}>{new}</{tag}>"
   if oldhtml in text:
    text=text.replace(oldhtml,newhtml,1)
   elif newhtml not in text:
    raise ValueError(f"Expected heading not found: {file}: {old}")
  file.write_text(text,encoding="utf-8")
  changed+=1
print(f"Updated natural SEO headings on {changed} Rose & Co pages.")


# Further meaningful H2/H3 hierarchy for catalog, flower guide and articles.
# Keep all product-card H3 labels short (especially "Պսակ").
from bs4 import BeautifulSoup

CONTENT={
"hy":{
 "h2":{
  "catalog":"Ծաղկեփնջեր, վարդեր և նվերներ Հայաստանում",
  "flowers":"Վարդեր, պիոններ, հորտենզիաներ և այլ ծաղիկներ",
  "journal":"Ծաղկեփնջերի խնամք, հարսանեկան ծաղիկներ և խորհուրդներ",
  "about":"Ծաղիկներ և ծաղկեփնջեր՝ Rose & Co-ի պատմությունը",
  "contact":"Ծաղիկների պատվեր՝ զանգահարեք կամ գրեք մեզ",
  "home_about":"Rose & Co՝ մեր ծաղիկների խանութի պատմությունը",
  "home_contact":"Ծաղկեփնջերի պատվեր՝ կապ հաստատեք մեզ հետ"
 },
 "article":{
  "flower-care":["Ծաղկեփնջերի խնամք․ ինչպես պահպանել ծաղիկները","Ծաղկեփնջերի խնամքի առաջին քայլերը","Ինչպես երկար պահել ծաղիկների թարմությունը"],
  "wedding-guide":["Հարսանեկան ծաղիկներ և ծաղկեփնջեր․ ընտրության ուղեցույց","Հարսանեկան ծաղկեփնջի ոճի ընտրություն","Հարսանեկան ծաղիկների գույներն ու սեզոնը"],
  "seasonal-flowers":["Սեզոնային ծաղիկներ Հայաստանում․ երբ ինչ ընտրել","Գարնանային ծաղիկներ և ծաղկեփնջեր","Ամառային և աշնանային ծաղիկներ"],
  "memorial-wreaths":["Ծաղկեպսակների ընտրություն Հայաստանում","Ծաղկեպսակի ծաղիկների և գույների ընտրություն","Ծաղկեպսակների չափերն ու ձևերը"]},
 "desc":{
  "home":"Rose & Co՝ ծաղիկներ և ծաղկեփնջեր Հայաստանում։ Դիտեք իրական ծաղկեփնջեր, վարդեր և նվերներ, գինն ու առկայությունը ճշտեք մեզ հետ։",
  "catalog":"Իրական ծաղկեփնջերի, վարդերի, ծաղկեպսակների և նվերների կատալոգ Հայաստանում։ Պատվերի գինն ու առկայությունը ճշտեք մեզ հետ։",
  "flowers":"Ծաղիկների տեսակների ուղեցույց՝ վարդեր, պիոններ, հորտենզիաներ և այլ ծաղիկներ Հայաստանում։",
  "journal":"Բլոգ ծաղիկների և ծաղկեփնջերի մասին․ խնամք, սեզոնային ընտրություն, հարսանեկան ծաղիկներ։",
  "about":"Rose & Co՝ ծաղիկների խանութ Հայաստանում։ Ծանոթացեք մեր ծաղկեփնջերին ու աշխատանքներին։",
  "contact":"Rose & Co-ի ծաղիկների և ծաղկեփնջերի պատվերի հարցերով կապ՝ Զովունի, 033 081 898։"
 }},
"ru":{
 "h2":{
  "catalog":"Букеты, розы и подарки в Армении",
  "flowers":"Розы, пионы, гортензии и другие цветы",
  "journal":"Уход за букетами, свадебные цветы и советы",
  "about":"Цветы и букеты — история Rose & Co",
  "contact":"Заказ цветов — позвоните или напишите нам",
  "home_about":"История цветочного магазина Rose & Co",
  "home_contact":"Закажите букет — свяжитесь с нами"
 },
 "article":{
  "flower-care":["Уход за букетом: как сохранить цветы свежими","Как подготовить букет к вазе","Как дольше сохранить свежесть цветов"],
  "wedding-guide":["Свадебные цветы и букеты: советы по выбору","Как выбрать стиль свадебного букета","Цветовая палитра и сезонные цветы"],
  "seasonal-flowers":["Сезонные цветы в Армении: что выбрать","Весенние цветы и букеты","Летние и осенние цветы"],
  "memorial-wreaths":["Как выбрать траурный венок в Армении","Цветы и оттенки для траурного венка","Размеры и формы цветочных венков"]},
 "desc":{
  "home":"Rose & Co: цветы и букеты в Армении. Настоящие фотографии роз, букетов и подарков. Уточняйте цену и наличие.",
  "catalog":"Каталог цветов, букетов, роз, венков и подарков в Армении. Уточняйте состав, наличие и цену.",
  "flowers":"Гид по видам цветов в Армении: розы, пионы, гортензии и сезонные цветы.",
  "journal":"Блог о цветах и букетах: уход, свадебные цветы и сезонный выбор.",
  "about":"Rose & Co: цветочный магазин в Армении, букеты и цветочные композиции.",
  "contact":"Как связаться с Rose & Co для заказа цветов и букетов: Зовуни, 033 081 898."
 }},
"en":{
 "h2":{
  "catalog":"Bouquets, Roses and Gifts in Armenia",
  "flowers":"Roses, Peonies, Hydrangeas and More",
  "journal":"Bouquet Care, Wedding Flowers and Seasonal Tips",
  "about":"Flowers and Bouquets — Our Story",
  "contact":"Flower Orders — Call or Message Us",
  "home_about":"The Rose & Co Flower Shop Story",
  "home_contact":"Enquire About Flower Bouquets"
 },
 "article":{
  "flower-care":["Bouquet Care: How to Keep Flowers Fresh","Preparing Your Bouquet for a Vase","How to Keep Cut Flowers Fresh Longer"],
  "wedding-guide":["Wedding Flowers and Bouquets: A Selection Guide","Choosing a Wedding Bouquet Style","Wedding Flower Colors and Seasonality"],
  "seasonal-flowers":["Seasonal Flowers in Armenia: What to Choose","Spring Flowers and Bouquets","Summer and Autumn Flowers"],
  "memorial-wreaths":["Choosing Memorial Flower Wreaths in Armenia","Flower and Color Choices for Wreaths","Wreath Shapes and Sizes"]},
 "desc":{
  "home":"Rose & Co flowers and bouquets in Armenia. Browse real photos of roses, floral gifts and bouquets, and enquire about availability.",
  "catalog":"Catalog of real bouquets, roses, floral wreaths and gifts in Armenia. Enquire about availability and price.",
  "flowers":"A guide to flower varieties in Armenia: roses, peonies, hydrangeas and seasonal flowers.",
  "journal":"Flower and bouquet journal: care, wedding flowers and seasonal inspiration.",
  "about":"Rose & Co is a flower shop in Armenia with bouquets and floral gifts.",
  "contact":"Contact Rose & Co in Zovuni, Armenia, to enquire about bouquets: 033 081 898."
 }}
}

def change_heading(node, value):
    if node is None: raise ValueError(f"Missing heading for {value}")
    node.clear()
    node.append(value)

def insert_h(section, title):
    assert section is not None, f"No section for heading {title}"
    if section.select_one(".seo-section-title"): return
    h=section._root.new_tag("h2") if hasattr(section,"_root") else None
    # Use BeautifulSoup.new_tag through the document in the caller instead.

extended=0
for lang, settings in CONTENT.items():
  for section_name in ("home","catalog","flowers","journal","about","contact",
                       "flower-care","wedding-guide","seasonal-flowers","memorial-wreaths"):
    page=root/lang/(
       "index.html" if section_name=="home" else
       f"journal/{section_name}/index.html" if section_name in settings["article"]
       else f"{section_name}/index.html"
    )
    if not page.is_file(): raise FileNotFoundError(page)
    soup=BeautifulSoup(page.read_text(encoding="utf-8"), "html.parser")
    h2=settings["h2"]
    if section_name=="home":
        change_heading(soup.select_one(".about-spotlight .spotlight-copy h2"),h2["home_about"])
        change_heading(soup.select_one(".contact-section h2"),h2["home_contact"])
    elif section_name in ("about","contact"):
        if section_name=="about":
            change_heading(soup.select_one(".about-spotlight .spotlight-copy h2"),h2["about"])
        change_heading(soup.select_one(".contact-section h2"),h2["contact"])
    elif section_name in ("catalog","flowers","journal"):
        target=soup.select_one({"catalog":".catalog-section","flowers":".types-section",
                                "journal":".journal-grid"}[section_name])
        if target is None:raise ValueError(f"No target on {page}")
        wrapper=target.find_parent("section") if section_name=="journal" else target
        if wrapper is None:raise ValueError(f"No section on {page}")
        if not wrapper.select_one(".seo-section-title"):
            heading=soup.new_tag("h2")
            heading["class"]="seo-section-title"
            heading.string=h2[section_name]
            wrapper.insert(0, heading)
    else:
        title,main_h2,sub_h3=settings["article"][section_name]
        change_heading(soup.select_one(".article-hero h1"),title)
        body=soup.select_one(".article-body")
        if body is None:raise ValueError(f"No body on {page}")
        ps=body.find_all("p",recursive=False)
        if len(ps)<2:raise ValueError(f"Not enough article paragraphs: {page}")
        if not body.find("h2",recursive=False):
            h=soup.new_tag("h2");h["class"]="seo-article-h2";h.string=main_h2
            ps[0].insert_before(h)
        if not body.find("h3",recursive=False):
            h=soup.new_tag("h3");h["class"]="seo-article-h3";h.string=sub_h3
            ps[1].insert_before(h)
    # The editorial H3 previews align with the article H1, while product
    # names remain as simple and descriptive as previously agreed.
    if section_name in ("home","journal"):
        for card in soup.select(".journal-card"):
            url=card.get("href","")
            slug=next((key for key in settings["article"] if f"/{key}/" in url),None)
            if slug:change_heading(card.find("h3"),settings["article"][slug][0])
    h1=soup.select_one("main h1")
    if h1 is None or len(soup.select("main h1"))!=1:
        raise ValueError(f"Page must have exactly one H1: {page}")
    title=h1.get_text(" ",strip=True)
    if soup.title:
        soup.title.string=title if "Rose & Co" in title else title+" | Rose & Co"
    og=soup.select_one('meta[property="og:title"]')
    if og:og["content"]=title+" — Rose & Co"
    if section_name in settings["desc"]:
        description=settings["desc"][section_name]
        for selector in ('meta[name="description"]','meta[property="og:description"]'):
            node=soup.select_one(selector)
            if node:node["content"]=description
    for product in soup.select(".product-card"):
        if product.find("h3") is None:raise ValueError(f"Missing product title: {page}")
    page.write_text(str(soup),encoding="utf-8")
    extended+=1

style=root/"assets"/"styles.css"
css=style.read_text(encoding="utf-8")
if "/* ROSE-CO-SEO-HEADINGS-2026 */" not in css:
    style.write_text(css+"""
/* ROSE-CO-SEO-HEADINGS-2026: semantic hierarchy, gentle typography. */
.seo-section-title{color:var(--wine);font-family:var(--serif);font-weight:500;font-size:clamp(23px,2.5vw,32px);line-height:1.28;letter-spacing:-.025em;margin:0 0 26px;max-width:850px}
.article-body>.seo-article-h2{font-family:var(--serif);font-weight:500;font-size:clamp(27px,3vw,35px);line-height:1.3;color:var(--wine);margin:12px 0 23px;letter-spacing:-.025em}
.article-body>.seo-article-h3{font-family:var(--serif);font-weight:500;font-size:clamp(21px,2.2vw,27px);line-height:1.35;color:var(--wine);margin:33px 0 16px;letter-spacing:-.01em}
@media(max-width:640px){.seo-section-title{font-size:25px;margin-bottom:20px}.article-body>.seo-article-h2{font-size:27px}.article-body>.seo-article-h3{font-size:22px}}
""",encoding="utf-8")

# Distinct cache version after the new typography is present. The animation
# installer can add its own JS independently without changing this CSS URL.
for file in root.rglob("*.html"):
    s=file.read_text(encoding="utf-8")
    if "styles.css?v=align6" in s:
        file.write_text(s.replace("styles.css?v=align6","styles.css?v=seo20261024"),encoding="utf-8")

assert extended==30, f"Expected 30 locale pages, found {extended}"
print(f"Rose & Co semantic SEO additions: {extended} pages; H2/H3 articles and catalog headings.")
