#!/usr/bin/env python3
"""Reproducible Rose & Co extensions applied after ZIP extraction."""
from pathlib import Path
import json,html,re,sys
root=Path(sys.argv[1])
assert (root/"hy/index.html").exists()
CALL="033 081 898"
WA="095 806 009"
NUM="+37433081898"
WA_NUM="37495806009"
CATS={"hy":["Արջուկներ","Փափուկ խաղալիքներ","Քաղցրավենիք"],
      "ru":["Мишки","Мягкие игрушки","Сладости"],
      "en":["Teddy bears","Soft toys","Sweets"]}
IDS=["teddies","plush","sweets"]
GIFT_NAMES=[
 ("RG01",0,"gift-bear.svg",["Դասական փափուկ արջուկ","Классический плюшевый мишка","Classic teddy bear"]),
 ("RG02",0,"gift-bear.svg",["Արջուկ՝ սիրելիին","Мишка для любимого человека","A bear for someone special"]),
 ("RG03",1,"gift-bunny.svg",["Փափուկ նապաստակ","Плюшевый зайчик","Plush bunny"]),
 ("RG04",1,"gift-bunny.svg",["Քնքուշ փափուկ խաղալիք","Нежная мягкая игрушка","Sweet soft toy"]),
 ("RG05",2,"gift-chocolate.svg",["Շոկոլադե նվեր","Шоколадный подарок","Chocolate gift"]),
 ("RG06",2,"gift-chocolate.svg",["Քաղցր անակնկալ","Сладкий сюрприз","Sweet surprise"])]
DESCS={
 "hy":["Ցուցադրական տարբերակ։ Գույնը, չափը և առկայությունը ճշտեք զանգով կամ WhatsApp-ով։",
       "Նվերի օրինակային տարբերակ։ Առկա տեսականին և գինը ճշտեք մեզ հետ։",
       "Քաղցր նվերի ցուցադրական օրինակ։ Տեսականին, առկայությունն ու գինը ճշտեք մեզ հետ։"],
 "ru":["Иллюстративный вариант. Цвет, размер и наличие уточняйте по телефону или WhatsApp.",
       "Пример подарка. Ассортимент и цену уточняйте при обращении.",
       "Иллюстрация сладкого подарка. Ассортимент, наличие и цену уточняйте."],
 "en":["Illustrative design. Ask about size, color and availability by phone or WhatsApp.",
       "Gift idea for illustration. Please enquire about options and price.",
       "Illustrative sweet gift. Enquire about selection, availability and price."]}
LANGS=["hy","ru","en"]
def read(path): return (root/path).read_text(encoding="utf-8")
def write(path,data):
 p=root/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(data,encoding="utf-8")
def jd(obj):return json.dumps(obj,ensure_ascii=False,separators=(",",":"))
items=[]
for code,idx,pic,names in GIFT_NAMES:
 items.append({"id":code,"img":pic,"cat":IDS[idx],
  "name":dict(zip(LANGS,names)),
  "desc":{l:DESCS[l][idx] for l in LANGS},"illustration":True})
catalog=json.loads(read("assets/catalog.js").removeprefix("window.ROSE_DATA=").strip().removesuffix(";"))
catalog["products"]=[x for x in catalog["products"] if not x["id"].startswith("RG")]+items
for key in IDS:
 if key not in catalog["cats"]:catalog["cats"].append(key)
write("assets/catalog.js","window.ROSE_DATA="+jd(catalog)+";\n")
write("assets/catalog.json",json.dumps(catalog,ensure_ascii=False,indent=2)+"\n")
translations=json.loads(read("assets/ui-translations.js").removeprefix("window.ROSE_I18N=").strip().removesuffix(";"))
for lang in LANGS:
 o=translations[lang];o["categories"]=o["categories"][:6]+CATS[lang]
 o["phonePending"]=CALL
 if lang=="hy":
  o.update(noPhone="Զանգ՝ "+CALL+" · WhatsApp՝ "+WA+"։",follow="Զանգ՝ "+CALL+" · WhatsApp՝ "+WA+"։",clickContact="Զանգահարեք "+CALL+" կամ գրեք WhatsApp՝ "+WA+"։",
    catIntro="Ծաղկեփնջեր, արջուկներ, փափուկ խաղալիքներ և քաղցրավենիք։ Նկարները ցուցադրական են․ գինն ու առկայությունը ճշտեք մեզ հետ։")
 elif lang=="ru":
  o.update(noPhone="Звонки: "+CALL+" · WhatsApp: "+WA+".",follow="Звонки: "+CALL+" · WhatsApp: "+WA+".",clickContact="Позвоните "+CALL+" или напишите в WhatsApp: "+WA+".",
    catIntro="Цветы, мишки, мягкие игрушки и сладости. Иллюстрации условные, наличие и цену уточняйте.")
 else:
  o.update(noPhone="Calls: "+CALL+" · WhatsApp: "+WA+".",follow="Calls: "+CALL+" · WhatsApp: "+WA+".",clickContact="Call "+CALL+" or WhatsApp "+WA+".",
    catIntro="Flowers, teddy bears, soft toys and sweets. Images are illustrative; ask about price and availability.")
write("assets/ui-translations.js","window.ROSE_I18N="+jd(translations)+";\n")
write("assets/contact-config.js","window.ROSE_CONTACT = { phone: '"+NUM+"', whatsapp: '"+WA_NUM+"', instagram: 'https://www.instagram.com/rose___co/' };\n")
app=read("assets/app.js")
# Only the modal image URL needs SVG awareness; original floral images remain WebP.
old="/rose-and-co/assets/images/"+chr(36)+"{esc(p.img)}.webp"
new="/rose-and-co/assets/images/"+chr(36)+"{esc(p.img)}"+chr(36)+"{p.img.endsWith('.svg')?'':'.webp'}"
assert old in app,"Modal image pattern changed"
write("assets/app.js",app.replace(old,new))

# Elegant original sample drawings; deliberately illustrative, not product photos.
top='''<svg xmlns="http://www.w3.org/2000/svg" width="820" height="950" viewBox="0 0 820 950"><defs><linearGradient id="a" x1="0" x2="1" y1="0" y2="1"><stop stop-color="#faefe8"/><stop offset="1" stop-color="#dec7c0"/></linearGradient><filter id="s"><feDropShadow dx="0" dy="18" stdDeviation="25" flood-color="#4f3040" flood-opacity=".18"/></filter></defs><rect width="820" height="950" fill="url(#a)"/><circle cx="700" cy="135" r="290" fill="#fff7ef" opacity=".35"/><ellipse cx="410" cy="872" rx="360" ry="60" fill="#ba9394" opacity=".14"/><text x="410" y="100" font-family="Georgia" font-size="19" letter-spacing="6" text-anchor="middle" fill="#744453">ROSE &amp; CO</text>'''
bottom='''<text x="410" y="918" font-family="Georgia" font-size="16" text-anchor="middle" letter-spacing="3" fill="#855462">A LITTLE GIFT WITH LOVE</text></svg>'''
bear='''<g filter="url(#s)" fill="#be9079"><circle cx="261" cy="310" r="89"/><circle cx="559" cy="310" r="89"/><ellipse cx="410" cy="682" rx="202" ry="213"/><circle cx="410" cy="417" r="199"/><ellipse cx="274" cy="796" rx="80" ry="94"/><ellipse cx="546" cy="796" rx="80" ry="94"/></g><g fill="#e4bfaa"><circle cx="261" cy="310" r="44"/><circle cx="559" cy="310" r="44"/><ellipse cx="410" cy="674" rx="116" ry="134"/><ellipse cx="410" cy="480" rx="99" ry="70"/><ellipse cx="274" cy="796" rx="50" ry="53"/><ellipse cx="546" cy="796" rx="50" ry="53"/></g><g fill="#543c36"><circle cx="344" cy="411" r="13"/><circle cx="476" cy="411" r="13"/><ellipse cx="410" cy="470" rx="26" ry="21"/></g><path d="M410 491v20q-25 20-47-2m47 2q25 20 47-2" fill="none" stroke="#695049" stroke-width="7" stroke-linecap="round"/><g fill="#752841"><path d="M410 574Q316 493 321 575Q338 641 410 593Z"/><path d="M410 574Q506 491 500 576Q477 637 410 593Z"/><circle cx="410" cy="585" r="29"/></g>'''
bunny='''<g filter="url(#s)"><ellipse cx="314" cy="276" rx="86" ry="219" transform="rotate(-13 314 276)" fill="#dcc0b9"/><ellipse cx="506" cy="276" rx="86" ry="219" transform="rotate(13 506 276)" fill="#dcc0b9"/><ellipse cx="314" cy="276" rx="44" ry="170" transform="rotate(-13 314 276)" fill="#c899a0"/><ellipse cx="506" cy="276" rx="44" ry="170" transform="rotate(13 506 276)" fill="#c899a0"/><ellipse cx="410" cy="683" rx="200" ry="205" fill="#e9d7ce"/><ellipse cx="410" cy="475" rx="186" ry="192" fill="#f5e8dc"/><ellipse cx="276" cy="791" rx="78" ry="98" fill="#f5e8dc"/><ellipse cx="544" cy="791" rx="78" ry="98" fill="#f5e8dc"/></g><g fill="#5d4650"><circle cx="350" cy="461" r="13"/><circle cx="470" cy="461" r="13"/></g><path d="M392 520q18-20 36 0q-7 21-18 21q-10 0-18-21" fill="#c58b95"/><path d="M410 537v18m0 0q-20 12-40-5m40 5q20 12 40-5" stroke="#8c6f73" stroke-width="6" fill="none" stroke-linecap="round"/><g fill="#9e6174"><path d="M410 655Q320 584 323 661Q346 709 410 679Z"/><path d="M410 655Q500 584 497 661Q474 709 410 679Z"/></g><circle cx="410" cy="663" r="29" fill="#72354e"/>'''
sweets='''<g filter="url(#s)"><rect x="130" y="282" width="560" height="500" rx="29" fill="#633947"/><rect x="150" y="307" width="520" height="448" rx="17" fill="#d6b092"/><rect x="171" y="331" width="478" height="397" rx="12" fill="#503139"/></g><g fill="#ac7258" stroke="#e2c39d" stroke-width="5"><circle cx="257" cy="425" r="59"/><circle cx="410" cy="425" r="59"/><circle cx="563" cy="425" r="59"/><circle cx="257" cy="604" r="59"/><circle cx="410" cy="604" r="59"/><circle cx="563" cy="604" r="59"/></g><g fill="#ead0b1"><path d="M214 426q43-72 87 0q-45-19-87 0M367 426q44-72 87 0q-45-19-87 0M520 426q44-72 87 0q-45-19-87 0"/><circle cx="257" cy="604" r="23"/><circle cx="410" cy="604" r="23"/><circle cx="563" cy="604" r="23"/></g><path d="M153 768h514" stroke="#ecd6b5" stroke-width="14"/>'''
for name,shape in [("gift-bear.svg",bear),("gift-bunny.svg",bunny),("gift-chocolate.svg",sweets)]:
 write("assets/images/"+name,top+shape+bottom)

PRICE={"hy":"Գինը ճշտելու համար կապ հաստատել","ru":"Стоимость уточняйте у нас","en":"Contact us for price"}
ASK={"hy":"Հարցնել գինը","ru":"Узнать цену","en":"Enquire about price"}
VIEW={"hy":"Դիտել նվերը","ru":"Посмотреть подарок","en":"View gift"}
def card(p,lang):
 n=html.escape(p["name"][lang],quote=True)
 allnames=html.escape(" ".join(p["name"].values()).lower(),quote=True)
 c=html.escape(CATS[lang][IDS.index(p["cat"])])
 return ('<article class="product-card gift-product" data-category="'+p["cat"]+'" data-name="'+allnames+'" data-item="'+p["id"]+
  '" tabindex="0" role="button" aria-label="'+VIEW[lang]+': '+n+'"><div class="card-image"><img src="/rose-and-co/assets/images/'+p["img"]+
  '" alt="'+n+'" loading="lazy" width="820" height="950"><span class="card-id">'+p["id"]+'</span><span class="corner-arrow">↗</span></div>'+
  '<div class="product-meta"><span class="category-label">'+c+'</span><h3>'+n+'</h3><p>'+PRICE[lang]+'</p>'+
  '<span class="card-action">'+ASK[lang]+'<span>→</span></span></div></article>')
for file in root.rglob("*.html"):
 lang=file.relative_to(root).parts[0]
 if lang not in LANGS:continue
 s=file.read_text(encoding="utf-8")
 s=s.replace('"telephone":"+37495806009"','"telephone":"'+NUM+'"')
 s=s.replace("tel:+37495806009","tel:"+NUM)
 s=s.replace("095 806 009",CALL)
 # Give the existing footer both routes instead of replacing WhatsApp.
 anchor='<a class="footer-phone" href="tel:'+NUM+'">'+CALL+'</a>'
 if anchor in s:
  s=s.replace(anchor,anchor+'<a class="footer-whatsapp" href="https://wa.me/'+WA_NUM+'" target="_blank" rel="noopener noreferrer">WhatsApp · '+WA+' ↗</a>')
 l={"hy":"Զանգահարել","ru":"Позвонить","en":"Call"}[lang]
 s=re.sub(r'(<a[^>]*class="[^"]*\bcontact-phone\b[^"]*"[^>]*>).*?(</a>)',
          lambda m:m.group(1)+l+" · "+CALL+" ↗"+m.group(2),s,flags=re.S)
 s=re.sub(r'(<a[^>]*class="[^"]*\bcontact-whatsapp\b[^"]*"[^>]*>).*?(</a>)',
          lambda m:m.group(1)+"WhatsApp · "+WA+" ↗"+m.group(2),s,flags=re.S)
 if 'id="contact-pending"' in s:
  s=s.replace('</a> · ','</a> · <a href="https://wa.me/'+WA_NUM+'" target="_blank" rel="noopener noreferrer">WhatsApp: '+WA+'</a> · ')
 parts=file.relative_to(root).parts
 if len(parts)==3 and parts[1]=="catalog" and parts[2]=="index.html":
  buttons="".join('<button class="filter-chip" data-filter="'+key+'" aria-pressed="false">'+html.escape(CATS[lang][idx])+'</button>' for idx,key in enumerate(IDS))
  s,n=re.subn(r'(<div class="filter-row" id="filter-row">.*?)(</div>)',
               lambda m:m.group(1)+buttons+m.group(2),s,count=1,flags=re.S)
  assert n==1,"Catalog filters missing"
  marker='<div class="product-grid" id="catalog-grid">'
  assert marker in s
  s=s.replace(marker,marker+"".join(card(p,lang) for p in items),1)
  s=re.sub(r'(<span id="result-count">)\d+',lambda m:m.group(1)+str(len(catalog["products"])),s,count=1)
  d=html.escape(translations[lang]["catIntro"],quote=True)
  s=re.sub(r'(<meta name="description" content=")[^"]+',lambda m:m.group(1)+d,s,count=1)
 if len(parts)==2 and parts[1]=="index.html":
  links="".join('<a href="/rose-and-co/'+lang+'/catalog/?category='+key+'" class="occasion-card"><img src="/rose-and-co/assets/images/'+pic+
   '" alt="'+html.escape(CATS[lang][idx])+'" loading="lazy" width="820" height="950"><span class="occasion-caption"><span>'+
   html.escape(CATS[lang][idx])+'</span><b>↗</b></span></a>'
   for idx,(key,pic) in enumerate(zip(IDS,["gift-bear.svg","gift-bunny.svg","gift-chocolate.svg"])))
  s,n=re.subn(r'(<div class="occasion-grid">.*?)(</div>)',lambda m:m.group(1)+links+m.group(2),s,count=1,flags=re.S)
  assert n==1,"Home occasions missing"
 file.write_text(s,encoding="utf-8")
css=read("assets/styles.css")
css+="""
.footer-whatsapp{display:block;margin-top:10px;color:#e6c9c6;font-size:13px}
.footer-whatsapp:hover{text-decoration:underline}
.gift-product .card-image{background:#f7e9e3}
@media(min-width:900px){.occasion-grid{grid-template-columns:repeat(3,minmax(0,1fr))}}
@media(max-width:460px){.contact-buttons .button{white-space:normal;text-align:center}}
"""
write("assets/styles.css",css)
print("Rose & Co extended:",len(catalog["products"]),"products, 3 gift categories, separate contact numbers")
