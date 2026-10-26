#!/usr/bin/env python3
"""Final Rose & Co design + SEO, after admin edits. Only 3 approved locales."""
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urlsplit
from html import escape
import json,re,shutil,sys
site=Path(sys.argv[1]).resolve()
repo=Path(__file__).resolve().parents[2]
base="https://alform-creator.github.io"
prefix="/rose-and-co/"
settings=json.loads((repo/".github/admin-data.json").read_text(encoding="utf-8"))
items=[p for p in settings["products"] if p.get("enabled",True)]
opts=settings["settings"]
has_prices=any(p.get("price_amd") for p in items)
overrides=settings.get("pages",{})
shutil.copy2(repo/".github/scripts/rose-couture-finish.css",site/"assets/rose-couture-finish.css")
words={
"hy":{
"home":"Գլխավոր","names":{"catalog":"Կատալոգ","flowers":"Ծաղիկների տեսակներ","about":"Մեր մասին","contact":"Կապ","journal":"Բլոգ"},
"nav":"Էջի տեղադրությունը","skip":"Անցնել հիմնական բովանդակությանը",
"hero":"Ծաղկեփունջ՝ սիրելիին նվիրելու, կարևոր օրը նշելու կամ պարզապես ժպիտ պարգևելու համար։ Դիտեք ծաղկային աշխատանքների լուսանկարները, ընտրեք ձեր սիրելի տարբերակը և մեզ հետ ճշտեք կազմը, գինն ու պատվերի պայմանները։",
"alt":"Վարդագույն ծաղիկների նուրբ կոմպոզիցիա — Rose & Co",
"meta_home":"Rose & Co՝ վարդեր, ծաղկեփնջեր, հարսանեկան ծաղիկներ ու նվերներ Հայաստանում։ Դիտեք ծաղկային աշխատանքները և ճշտեք գինն ու առաքման պայմանները։",
"meta_catalog":"Rose & Co-ի ծաղկեփնջերի կատալոգ՝ վարդեր, տոնական ու հարսանեկան փնջեր, ծաղկեպսակներ և նվերներ։ Ընտրեք ըստ առիթի և ճշտեք գինն ու առկայությունը։",
"price_none":"Գինը և առկայությունը հաստատվում են պատվերից առաջ։","price_yes":"Նշված գները հաստատվում են վերջնական կազմն ու առկայությունը ճշտելուց հետո։",
"promise":[("Ծաղկային լուսանկարներ","Դիտեք կատալոգում ներկայացված փնջերն ու կոմպոզիցիաները։"),("Յուրաքանչյուր առիթի համար","Վարդեր, տոնական փնջեր, հարսանեկան ծաղիկներ և ծաղկեպսակներ։"),("Հստակ պայմանավորվածություն","Պատվերից առաջ միասին ճշտում ենք գինը, կազմը և առաքման պայմանները։")],
"kicker":"ՕԳՆՈՒԹՅՈՒՆ ԸՆՏՐՈՒԹՅԱՆ ՀԱՄԱՐ","guide_title":"Ինչպե՞ս ընտրել և պատվիրել ծաղկեփունջ",
"guide_intro":"Ընտրեք ձեր սիրելի կոմպոզիցիան կամ պատմեք՝ ում համար և ինչ առիթով եք փունջ պատվիրում։ Մեզ հետ կարող եք ճշտել ծաղիկների կազմը, գույները և հասանելի տարբերակները։",
"qa":[("Կարելի՞ է պատվիրել նկարում եղած փունջը։","Նկարը ընտրության հիմք է։ Ծաղիկների առկայությունն ու վերջնական տեսքը հաստատում ենք պատվերից առաջ։"),("Ինչպե՞ս իմանալ ծաղկեփնջի գինը։","Ընտրեք կոմպոզիցիան կամ նշեք նախընտրած չափսը։ Կճշտենք տվյալ պահին հնարավոր տարբերակի արժեքը։"),("Կարո՞ղ եք առաքել իմ նշած օրը։","Գրեք նախընտրած օրը, ժամը և հասցեն։ Առաքման հնարավորությունն ու վճարը կհաստատենք առանձին։")],
"whatsapp":"Հարցնել WhatsApp-ով","contact":"Կապ հաստատել","contact_copy":"Յուրաքանչյուր պատվերից առաջ ճշտում ենք ծաղիկների առկայությունը, վերջնական կազմը և առաքման պայմանները։",
"contact_h":"Արդեն ընտրե՞լ եք ծաղկեփունջ","contact_note":"Ուղարկեք կոմպոզիցիայի համարը կամ անունը և ցանկալի օրը։ Կպատասխանենք գնի, առկայության և առաքման հարցերին։","go_catalog":"Դիտել կատալոգը"},
"ru":{
"home":"Главная","names":{"catalog":"Каталог","flowers":"Виды цветов","about":"О нас","contact":"Контакты","journal":"Журнал"},
"nav":"Путь к странице","skip":"Перейти к содержимому",
"hero":"Букет для близкого человека, особого события или простого знака внимания. Посмотрите цветочные композиции, выберите понравившуюся работу — а состав, стоимость и условия заказа мы уточним вместе.",
"alt":"Нежная цветочная композиция в розовых оттенках — Rose & Co",
"meta_home":"Rose & Co — розы, букеты, свадебные цветы и подарки в Армении. Фото композиций; стоимость, наличие и условия доставки уточняйте перед заказом.",
"meta_catalog":"Каталог Rose & Co: розы, праздничные и свадебные букеты, венки и подарки в Армении. Выберите композицию и уточните стоимость и наличие.",
"price_none":"Стоимость и наличие подтверждаем перед заказом.","price_yes":"Указанные цены подтверждаем после согласования состава и наличия цветов.",
"promise":[("Фотографии композиций","В каталоге представлены фотографии цветочных работ."),("Для разных поводов","Розы, праздничные и свадебные букеты, композиции и венки."),("Условия до заказа","Согласуем стоимость, состав и условия доставки заранее.")],
"kicker":"ПОМОЖЕМ С ВЫБОРОМ","guide_title":"Как выбрать и заказать букет",
"guide_intro":"Выберите понравившуюся композицию или расскажите, кому и к какому событию нужны цветы. Мы уточним состав, оттенки и доступные варианты.",
"qa":[("Можно заказать букет точно как на фото?","Фото служит ориентиром. Наличие цветов и окончательный вид согласуем перед заказом."),("Как узнать стоимость?","Укажите композицию или размер, а мы сообщим стоимость доступного варианта."),("Как согласовать доставку?","Напишите дату, время и адрес. Возможность доставки и стоимость уточним отдельно.")],
"whatsapp":"Спросить в WhatsApp","contact":"Связаться","contact_copy":"Перед заказом уточняем наличие цветов, окончательный состав и условия доставки.",
"contact_h":"Уже выбрали букет?","contact_note":"Пришлите название или номер композиции и желаемую дату. Уточним стоимость, наличие и доставку.","go_catalog":"Открыть каталог"},
"en":{
"home":"Home","names":{"catalog":"Collection","flowers":"Flower varieties","about":"About us","contact":"Contact","journal":"Journal"},
"nav":"You are here","skip":"Skip to main content",
"hero":"A bouquet for someone special, an important occasion or a thoughtful everyday gesture. Explore our floral arrangements, choose a favourite and contact us to confirm the composition, price and order details.",
"alt":"Delicate pink floral arrangement — Rose & Co",
"meta_home":"Rose & Co bouquets, roses, wedding flowers and gifts in Armenia. Explore floral arrangements and enquire about prices, availability and delivery details.",
"meta_catalog":"Explore the Rose & Co flower collection in Armenia: roses, celebration and bridal bouquets, wreaths and gifts. Ask about prices and availability.",
"price_none":"Prices and availability are confirmed before ordering.","price_yes":"Displayed prices are confirmed once the composition and availability are agreed.",
"promise":[("Floral photography","Explore photographs of bouquets and arrangements in our collection."),("For every occasion","Roses, celebration bouquets, bridal flowers and remembrance wreaths."),("Clear order details","We confirm the price, composition and delivery details in advance.")],
"kicker":"A LITTLE GUIDANCE","guide_title":"How to choose and order a bouquet",
"guide_intro":"Choose a floral arrangement you love, or tell us who the flowers are for and what you have in mind. We can confirm the composition, colours and available options.",
"qa":[("Can I order exactly what is pictured?","Use the photo as a reference. We confirm available flowers and the final look before ordering."),("How can I find out the price?","Choose an arrangement or size and contact us for the price of an available option."),("How can I arrange delivery?","Share the preferred date, time and address. We'll confirm if delivery is possible and its cost.")],
"whatsapp":"Enquire on WhatsApp","contact":"Contact us","contact_copy":"We confirm the flower availability, final composition and delivery details before every order.",
"contact_h":"Already found a bouquet?","contact_note":"Send the arrangement name or reference number and preferred date. We'll confirm prices, availability and delivery options.","go_catalog":"View collection"}
}
# The original Rose & Co hero copy was approved before the couture refresh.
# Preserve it on HY/RU/EN; the newer SEO/collection enhancements remain elsewhere.
CLASSIC_HERO={
"hy":"Արտիստիկ ծաղկեփնջեր, նրբագեղ հարսանեկան ձևավորումներ և հիշատակի ծաղկեպսակներ։ Ընտրեք ձեր ոճը, իսկ գինն ու հասանելիությունը ճշտեք մեզ հետ։",
"ru":"Авторские букеты, утончённая свадебная флористика и памятные венки. Выбирайте вдохновение, а цену и наличие уточняйте лично.",
"en":"Artfully styled bouquets, elegant wedding flowers and thoughtful remembrance wreaths. Find your inspiration and enquire for availability and pricing."
}
def soupof(source):return BeautifulSoup(source,"html.parser")
def settext(node,val):node.clear();node.append(val)
def setmeta(doc,attr,val):
 node=doc.select_one(attr)
 if node:node["content"]=val
def jsonld(doc,obj):
 node=doc.new_tag("script",type="application/ld+json")
 node.string=json.dumps(obj,ensure_ascii=False,separators=(",",":")).replace("<","\\u003c")
 doc.head.append(node)
seen=0
for lang in ("hy","ru","en"):
 w=words[lang]
 for path in sorted((site/lang).rglob("index.html")):
  rel=path.relative_to(site).as_posix()
  route=rel[:-len("index.html")]
  canonical=base+prefix+route
  group=rel.split("/")[1] if len(rel.split("/"))>2 else ""
  home=(route==lang+"/")
  catalog=(route==lang+"/catalog/")
  contact=(route==lang+"/contact/")
  article="/journal/" in route and not route.endswith("/journal/")
  edit=overrides.get(rel,{})
  doc=soupof(path.read_text(encoding="utf-8"))
  assert doc.head and doc.main and doc.h1,rel
  doc.html["data-finish"]="couture-v1"
  # The homepage keeps the previously approved rose atelier design.
  # Other 95 localized pages retain the refinements and SEO rules.
  if not home:
   doc.head.append(doc.new_tag("link",rel="stylesheet",href=prefix+"assets/rose-couture-finish.css?v=1"))
  for origin in ("https://fonts.googleapis.com","https://fonts.gstatic.com"):
   if not doc.head.select_one('link[rel="preconnect"][href="'+origin+'"]'):
    link=doc.new_tag("link",rel="preconnect",href=origin)
    if origin.endswith("gstatic.com"):link["crossorigin"]=""
    doc.head.append(link)
  for node in doc.select("nav.desktop-nav"):
   node["aria-label"]={"hy":"Հիմնական նավարկում","ru":"Основная навигация","en":"Main navigation"}[lang]
  for node in doc.select("a.brand[aria-label]"):node["aria-label"]="Rose & Co · "+w["home"]
  for switch in doc.select(".language-switcher"):
   switch["aria-label"]={"hy":"Ընտրել լեզուն","ru":"Выбрать язык","en":"Select language"}[lang]
   for a in switch.select("a"):
    if "current" in a.get("class",[]):a["aria-current"]="page"
  skip=doc.new_tag("a",href="#main")
  skip["class"]="rc-skip"
  skip.string=w["skip"]
  doc.body.insert(0,skip)

  if home:
   intro=doc.select_one(".hero-copy>p")
   if intro and not edit.get("intro"):settext(intro,CLASSIC_HERO[lang])
   hero=doc.select_one("img.hero-image")
   if hero:
    hero["alt"]="Luxurious pink floral arrangement";hero["loading"]="eager";hero["fetchpriority"]="high";hero["decoding"]="async"
   if not edit.get("description"):
    setmeta(doc,'meta[name="description"]',w["meta_home"])
    setmeta(doc,'meta[property="og:description"]',w["meta_home"])
   # Do not insert the later three-column promise strip on the original homepage.
  if catalog:
   if not edit.get("description"):
    setmeta(doc,'meta[name="description"]',w["meta_catalog"])
    setmeta(doc,'meta[property="og:description"]',w["meta_catalog"])
   count=doc.select_one(".catalog-count")
   if count:
    spans=count.find_all("span",recursive=False)
    if len(spans)>=2:settext(spans[1],w["price_yes" if has_prices else "price_none"])
   faq=''.join('<div class="rc-guide-qa"><h3>'+escape(q)+'</h3><p>'+escape(a)+'</p></div>' for q,a in w["qa"])
   markup='<section class="rc-guide" aria-labelledby="rc-guide-title"><div class="container rc-guide-grid"><div><span class="rc-guide-kicker">'+escape(w["kicker"])+'</span><h2 id="rc-guide-title">'+escape(w["guide_title"])+'</h2><p class="rc-guide-intro">'+escape(w["guide_intro"])+'</p><div class="rc-guide-actions"><a class="button btn-burgundy" href="https://wa.me/'+opts["whatsapp"]+'" target="_blank" rel="noopener noreferrer">'+escape(w["whatsapp"])+' ↗</a><a class="text-link" href="'+prefix+lang+'/contact/">'+escape(w["contact"])+' →</a></div></div><div>'+faq+'</div></div></section>'
   csec=doc.select_one(".catalog-section")
   if csec:csec.insert_after(soupof(markup).section)
   else:doc.main.append(soupof(markup).section)
   products=[{"@type":"ListItem","position":n,
     "item":{"@type":"Thing","name":p["name"][lang],"url":canonical+"#product-"+p["id"],
       "image":base+prefix+"assets/images/"+p["img"]+".webp"}}
      for n,p in enumerate(items,1)]
   jsonld(doc,{"@context":"https://schema.org","@type":"ItemList",
      "name":w["names"]["catalog"],"numberOfItems":len(products),"itemListElement":products})
  for p in doc.select(".contact-section .contact-grid > div:first-child > p"):
   if len(p.get_text(" ",strip=True))<170:settext(p,w["contact_copy"])
  if contact:
   section=doc.select_one(".contact-section")
   if section:
    markup='<section class="rc-buying-help"><div class="container rc-buying-help-inner"><div><h2>'+escape(w["contact_h"])+'</h2><p>'+escape(w["contact_note"])+'</p></div><a class="button btn-outline" href="'+prefix+lang+'/catalog/">'+escape(w["go_catalog"])+' ↗</a></div></section>'
    section.insert_before(soupof(markup).section)
  for card in doc.select(".product-card[data-item]"):
   if re.fullmatch(r"[A-Za-z0-9_-]{2,20}",card["data-item"]):card["id"]="product-"+card["data-item"]
  if not home and not doc.main.select_one('.rc-breadcrumb'):
   is_top=group in w["names"] and not article
   title=w["names"][group] if is_top else doc.h1.get_text(" ",strip=True)
   crumbs=[(w["home"],prefix+lang+"/")]
   if article:crumbs.append((w["names"]["journal"],prefix+lang+"/journal/"))
   crumbs.append((title,None))
   mark='<ol>'+''.join('<li><a href="'+escape(target,quote=True)+'">'+escape(name)+'</a></li>' if target else '<li aria-current="page">'+escape(name)+'</li>' for name,target in crumbs)+'</ol>'
   nav=soupof('<div class="rc-breadcrumb-shell"><div class="container"><nav class="rc-breadcrumb" aria-label="'+escape(w["nav"],quote=True)+'">'+mark+'</nav></div></div>').div
   first=doc.main.find(recursive=False)
   if first:first.insert_before(nav)
   else:doc.main.append(nav)
   jsonld(doc,{"@context":"https://schema.org","@type":"BreadcrumbList",
     "itemListElement":[{"@type":"ListItem","position":i+1,"name":name,"item":base+(target or prefix+route)} for i,(name,target) in enumerate(crumbs)]})

  # Preserve true administrator contact details, including structured data.
  old="+37433081898";new=opts["phone"]
  for a in doc.select("a[href]"):
   href=a["href"]
   if href.startswith("tel:"+old):a["href"]="tel:"+new+href[len("tel:"+old):]
   if href.startswith("https://wa.me/37433081898"):a["href"]=href.replace("https://wa.me/37433081898","https://wa.me/"+opts["whatsapp"],1)
   if href.startswith("https://www.instagram.com/rose___co/"):a["href"]=opts["instagram"]
  if new!=old:
   digits=re.sub(r"\D","",new)
   shown=("0"+digits[3:5]+" "+digits[5:8]+" "+digits[8:11]) if len(digits)==11 and digits.startswith("374") else new
   for el in doc.find_all(string=lambda v:v and "033 081 898" in str(v)):
    el.replace_with(str(el).replace("033 081 898",shown))
  for node in doc.select('script[type="application/ld+json"]'):
   try:structured=json.loads(node.string or node.get_text())
   except (ValueError,TypeError):continue
   if not isinstance(structured,dict):continue
   typ=structured.get("@type")
   if typ in ("Florist","LocalBusiness"):
    structured["telephone"]=opts["phone"]
    structured["sameAs"]=[opts["instagram"]]
   if typ in ("WebPage","Article","CollectionPage"):
    m=doc.select_one('meta[name="description"]')
    if m:structured["description"]=m.get("content","")
    structured["name"]=doc.title.get_text(strip=True)
    if typ=="Article":
     structured["headline"]=doc.h1.get_text(" ",strip=True)
     photo=next((p for p in doc.select("main img[src]")
       if urlsplit(p.get("src","")).path.startswith(prefix+"assets/images/")),None)
     if photo:
      img=urlsplit(photo["src"]).path
      if (site/img[len(prefix):]).is_file():
       structured["image"]=base+img
       setmeta(doc,'meta[property="og:image"]',base+img)
     structured["mainEntityOfPage"]={"@type":"WebPage","@id":canonical}
   node.string=json.dumps(structured,ensure_ascii=False,separators=(",",":")).replace("<","\\u003c")
  path.write_text(str(doc),encoding="utf-8")
  seen+=1
# The displayed amount must match WhatsApp product enquiries when admin sets a price.
app=site/"assets/app.js"
js=app.read_text(encoding="utf-8")
old="("+ "$"+"{p.id}). "+"$"+"{t.price}"
new="("+ "$"+"{p.id}). "+"$"+"{p.price_amd ? Number(p.price_amd).toLocaleString('en-US')+' AMD' : t.price}"
assert old in js or new in js
app.write_text(js.replace(old,new),encoding="utf-8")
css=site/"assets/rose-couture-finish.css"
css.write_text(css.read_text(encoding="utf-8")+'''
.rc-skip{position:fixed;left:12px;top:-120px;z-index:150;background:#542036;color:#fff;
 padding:10px 18px;border-radius:4px;font-size:13px;box-shadow:0 8px 22px rgba(0,0,0,.2)}
.rc-skip:focus{top:12px}
''',encoding="utf-8")
# Keep keyboard-accessible skip navigation without applying the later couture
# stylesheet that changed the approved homepage hero composition and spacing.
base_css=site/"assets/styles.css"
base_text=base_css.read_text(encoding="utf-8")
marker="/* ROSE HOME CLASSIC SKIP NAV */"
if marker not in base_text:
 base_css.write_text(base_text+"""
/* ROSE HOME CLASSIC SKIP NAV */
.rc-skip{position:fixed;left:12px;top:-120px;z-index:150;background:#542036;color:#fff;padding:10px 18px;border-radius:4px;font-size:13px;box-shadow:0 8px 22px rgba(0,0,0,.2)}
.rc-skip:focus{top:12px}
""",encoding="utf-8")
assert seen==96,seen
print("Rose & Co couture: 96 localized pages; consistent design, admin pricing, accessible paths, ItemList & BreadcrumbList.")
