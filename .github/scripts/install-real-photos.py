#!/usr/bin/env python3
"""Publish Rose & Co's user-supplied, non-repeating catalog and editorial photographs.

Usage: python3 rose_install_2026.py <unpacked-site> [source-images-zip]
If no zip argument, reassemble repository .rose-customer-2026/part-*.b64.
"""
from pathlib import Path
from bs4 import BeautifulSoup
from zipfile import ZipFile
from html import escape
import base64
import json
import os
import re
import sys

root=Path(sys.argv[1]).resolve()
photo_dir=root/'assets'/'images'/'real-2026'
photo_dir.mkdir(parents=True,exist_ok=True)
if len(sys.argv)>2:
    bundle_path=Path(sys.argv[2])
    archive=ZipFile(bundle_path,'r')
else:
    parts=sorted(Path(__file__).resolve().parents[2].glob('.rose-customer-2026/part-*.b64'))
    if len(parts)<40:raise RuntimeError(f'Missing upload chunks: {len(parts)}')
    zipped=base64.b64decode(''.join(p.read_text(encoding='ascii') for p in parts),validate=True)
    import io
    archive=ZipFile(io.BytesIO(zipped),'r')
expected={f'{group}-{i:02d}.webp' for group,count in [('flowers',41),('wreaths',16),('toys',5),('sweets',3),('editorial',7)] for i in range(1,count+1)}
files=set(archive.namelist())
if files!=expected:raise RuntimeError(f'Invalid image collection: missing={expected-files} extra={files-expected}')
for name in sorted(files):
    target=photo_dir/name
    target.write_bytes(archive.read(name))
archive.close()

# Product names are descriptive rather than fanciful, translated in all three languages.
FLOWERS=[
 ('Վարդագույն և սպիտակ ծաղկեփունջ','Розово-белый букет','Pink and White Bouquet','occasions'),
 ('Սպիտակ և վարդագույն վարդեր','Белые и розовые розы','White and Pink Roses','romance'),
 ('Վարդագույն ծաղիկներով փունջ','Букет с розовыми цветами','Pink Flower Bouquet','occasions'),
 ('Վարդագույն փունջ','Розовый букет','Pink Bouquet','romance'),
 ('Սպիտակ և կանաչ ծաղկեփունջ','Бело-зелёный букет','White and Green Bouquet','wedding'),
 ('Գունավոր ծաղիկներ տուփում','Цветы в коробке','Mixed Flowers in a Box','signature'),
 ('Դեղին և կապույտ ծաղիկներ','Жёлтые и синие цветы','Yellow and Blue Flowers','occasions'),
 ('Վարդագույն վարդերի փունջ','Букет розовых роз','Pink Rose Bouquet','romance'),
 ('Կապույտ և սպիտակ քրիզանթեմներ','Синие и белые хризантемы','Blue and White Chrysanthemums','occasions'),
 ('Կրեմագույն և մանուշակագույն ծաղիկներ','Кремово-сиреневые цветы','Cream and Lilac Flowers','signature'),
 ('Վարդագույն վարդերի փոքր փունջ','Небольшой букет розовых роз','Small Pink Rose Bouquet','romance'),
 ('Վարդագույն վարդեր զամբյուղում','Розовые розы в корзине','Pink Roses in a Basket','signature'),
 ('Դեղձագույն վարդերով ծաղկեփունջ','Букет с персиковыми розами','Peach Rose Bouquet','occasions'),
 ('Դեղձագույն խառը ծաղկեփունջ','Смешанный персиковый букет','Peach Mixed Bouquet','signature'),
 ('Վարդագույն և կանաչ ծաղիկներ','Розово-зелёные цветы','Pink and Green Flowers','occasions'),
 ('Վարդագույն վարդեր և քրիզանթեմներ','Розовые розы и хризантемы','Pink Roses and Chrysanthemums','romance'),
 ('Սպիտակ ծաղկեփունջ','Белый букет','White Flower Bouquet','wedding'),
 ('Վարդագույն խառը փունջ','Смешанный розовый букет','Pink Mixed Bouquet','occasions'),
 ('Արևածաղիկների փունջ','Букет подсолнухов','Sunflower Bouquet','seasonal'),
 ('Մանուշակագույն ծաղիկներ զամբյուղում','Сиреневые цветы в корзине','Lilac Flowers in a Basket','signature'),
 ('Մանուշակագույն և կրեմագույն փունջ','Сиренево-кремовый букет','Lilac and Cream Bouquet','signature'),
 ('Կապույտ և սպիտակ ծաղիկներ','Синие и белые цветы','Blue and White Flowers','occasions'),
 ('Վարդագույն վարդերով ծաղկեփունջ','Букет с розовыми розами','Bouquet with Pink Roses','romance'),
 ('Հարսանեկան սպիտակ փունջ','Белый свадебный букет','White Bridal Bouquet','wedding'),
 ('51 սպիտակ վարդ','51 белая роза','51 White Roses','romance'),
 ('101 կարմիր վարդ','101 красная роза','101 Red Roses','romance'),
 ('Կապույտ վարդերի փունջ','Букет синих роз','Blue Rose Bouquet','signature'),
 ('Վարդեր զամբյուղում','Розы в корзине','Roses in a Basket','signature'),
 ('Սպիտակ վարդերի փոքր փունջ','Небольшой букет белых роз','Small White Rose Bouquet','wedding'),
 ('Վարդագույն հորտենզիաներով փունջ','Букет с розовой гортензией','Pink Hydrangea Bouquet','signature'),
 ('Սպիտակ ծաղիկներով նվերային զամբյուղ','Подарочная корзина с белыми цветами','White Flower Gift Basket','occasions'),
 ('Կարմիր վարդեր տուփում','Красные розы в коробке','Red Roses in a Box','romance'),
 ('Մուգ վարդագույն վարդերի փունջ','Букет ярко-розовых роз','Deep Pink Rose Bouquet','romance'),
 ('Մանր վարդագույն վարդերի փունջ','Букет мелких розовых роз','Pink Spray Rose Bouquet','romance'),
 ('Վարդագույն գիպսոֆիլա զամբյուղում','Розовая гипсофила в корзине','Pink Baby’s Breath Basket','seasonal'),
 ('Սպիտակ և վարդագույն մանր վարդեր','Бело-розовые кустовые розы','White and Pink Spray Roses','romance'),
 ('Գունավոր քրիզանթեմների փունջ','Букет разноцветных хризантем','Colorful Chrysanthemum Bouquet','seasonal'),
 ('Կարմիր վարդերով կլոր տուփ','Круглая коробка с красными розами','Round Box of Red Roses','romance'),
 ('Դեղձագույն վարդեր զամբյուղում','Персиковые розы в корзине','Peach Roses in a Basket','signature'),
 ('Բաց վարդագույն և սպիտակ վարդեր','Светло-розовые и белые розы','Pale Pink and White Roses','wedding'),
 ('Արևածաղիկների փոքր փունջ','Небольшой букет подсолнухов','Small Sunflower Bouquet','seasonal')]
assert len(FLOWERS)==41
TOYS=[
 ('Փափուկ նապաստակ','Плюшевый зайчик','Plush Bunny','plush'),
 ('Մոխրագույն արջուկ','Серый мишка','Grey Teddy Bear','teddies'),
 ('Վարդագույն արջուկ','Розовый мишка','Pink Teddy Bear','plush'),
 ('Բեժ արջուկ','Бежевый мишка','Beige Teddy Bear','teddies'),
 ('Սպիտակ արջուկ','Белый мишка','White Teddy Bear','teddies')]
SWEETS=[
 ('Շոկոլադ և արջուկ','Шоколад и мишка','Chocolate and Teddy Bear'),
 ('Շոկոլադե նվերային հավաքածու','Подарочный набор шоколада','Chocolate Gift Set'),
 ('Վարդեր և քաղցրավենիք տուփում','Розы и сладости в коробке','Roses and Sweets in a Box')]

products=[]
def add(id, name, cat, img, desc=None):
    names=dict(zip(('hy','ru','en'),name))
    if desc is None:
      desc={'hy':'Պատվիրելու համար կապ հաստատեք մեզ հետ։ Ծաղիկների առկայությունը և փնջի կազմը կարող են փոխվել։',
            'ru':'Свяжитесь с нами, чтобы оформить заказ. Наличие цветов и состав букета уточняются.',
            'en':'Contact us to order. Flower availability and bouquet composition are confirmed on request.'}
    products.append({'id':id,'img':img,'cat':cat,'name':names,'desc':desc,'illustration':False})
for n,(hy,ru,en,cat) in enumerate(FLOWERS,1):
    desc=None
    if n in (25,26):
      desc={'hy':'Կարող եք ընտրել սովորական կամ երկար ցողուններով տարբերակը։ Հասանելիությունը ճշտեք պատվիրելիս։',
            'ru':'Можно выбрать стандартные или длинные стебли. Наличие уточняйте при заказе.',
            'en':'Choose standard or long stems. Please confirm availability before ordering.'}
    add(f'RF{n:02d}',(hy,ru,en),cat,f'real-2026/flowers-{n:02d}',desc)
for n in range(1,17):
    add(f'RW{n:02d}',('Պսակ','Венок','Wreath'),'wreaths',f'real-2026/wreaths-{n:02d}',{
       'hy':'Պսակի տեսքը, ծաղիկների ընտրությունն ու առկայությունը ճշտեք պատվիրելիս։',
       'ru':'Внешний вид, состав и наличие венка уточняйте при заказе.',
       'en':'Confirm wreath composition and availability when ordering.'})
for n,(hy,ru,en,cat) in enumerate(TOYS,1):
    add(f'RT{n:02d}',(hy,ru,en),cat,f'real-2026/toys-{n:02d}',{
       'hy':'Գույնը, չափսը և առկայությունը ճշտեք պատվիրելիս։',
       'ru':'Уточните цвет, размер и наличие перед заказом.',
       'en':'Please confirm color, size and availability before ordering.'})

# Preserve each of the existing six sweets with its original photo.
p= root/'assets'/'catalog.json'
old=json.loads(p.read_text(encoding='utf-8'))
old_sweets=[x for x in old['products'] if x.get('cat')=='sweets' and x.get('id','').startswith('RG')]
assert len(old_sweets)==6,(len(old_sweets),[x['id'] for x in old_sweets])
products.extend(old_sweets)
for n,(hy,ru,en) in enumerate(SWEETS,1):
    add(f'RS{n:02d}',(hy,ru,en),'sweets',f'real-2026/sweets-{n:02d}',{
       'hy':'Քաղցրավենիքի տեսականին և կազմը կարող են տարբերվել՝ ճշտեք պատվիրելիս։',
       'ru':'Состав подарка и ассортимент сладостей уточняйте при заказе.',
       'en':'Confirm the gift contents and sweet selection before ordering.'})
assert len(products)==71,len(products)
assert len({a['img'] for a in products})==71,'Duplicate catalog images'
newdata={**old,'products':products}
for filename in ('catalog.json','catalog.js'):
    dst=root/'assets'/filename
    raw=json.dumps(newdata,ensure_ascii=False,separators=(',',':'))
    dst.write_text(('window.ROSE_DATA='+raw+';' if filename.endswith('.js') else raw)+'\n',encoding='utf-8')

prefix='/rose-and-co/assets/images/'
editorial={'pink-peonies.webp':'editorial-01.webp',
 'blush-ceremony.webp':'editorial-02.webp',
 'atelier-peony.webp':'editorial-03.webp',
 'atelier-detail.webp':'editorial-05.webp',
 'atelier-elegance.webp':'editorial-07.webp',
 'studio-birthday.webp':'editorial-06.webp',
 'white-wreath.webp':'editorial-07.webp',
 'blush-wreath.webp':'editorial-01.webp',
 'crimson-wreath.webp':'editorial-05.webp'}
categories=['romance','wedding','occasions','signature','wreaths','seasonal','teddies','plush']
category_img={'romance':'editorial-05','wedding':'editorial-03','occasions':'editorial-07','signature':'editorial-02',
              'wreaths':'wreaths-12','seasonal':'editorial-01','teddies':'editorial-06','plush':'editorial-04'}
category_names={
 'hy':{'romance':'Սիրո փնջեր','wedding':'Հարսանեկան','occasions':'Տոնական','signature':'Հեղինակային','wreaths':'Ծաղկեպսակներ','seasonal':'Սեզոնային','teddies':'Արջուկներ','plush':'Փափուկ խաղալիքներ','sweets':'Քաղցրավենիք'},
 'ru':{'romance':'Для любимых','wedding':'Свадебные','occasions':'Для праздников','signature':'Авторские','wreaths':'Венки','seasonal':'Сезонные','teddies':'Мишки','plush':'Мягкие игрушки','sweets':'Сладости'},
 'en':{'romance':'Romantic Bouquets','wedding':'Wedding','occasions':'Occasions','signature':'Signature','wreaths':'Wreaths','seasonal':'Seasonal','teddies':'Teddy Bears','plush':'Plush Toys','sweets':'Sweets'}}
terms={
 'hy':{'call':'Դիտել կոմպոզիցիան: ','price':'Գինը ճշտելու համար կապ հաստատել','question':'Հարցնել գինը','found':' ցուցադրված աշխատանք'},
 'ru':{'call':'Посмотреть композицию: ','price':'Уточните цену при обращении','question':'Узнать цену','found':' товаров'},
 'en':{'call':'View arrangement: ','price':'Contact us to confirm the price','question':'Ask for price','found':' items'}}

def card(p,lang):
    l=terms[lang]
    title=p['name'][lang]
    cat=category_names[lang].get(p['cat'],p['cat'])
    name_str=' '.join(p['name'].values()).lower()
    tag = '' if p['cat']=='wreaths' else '<span class="photo-brand-tag" aria-hidden="true">Rose <small>&amp; Co</small></span>'
    # Product title will also be used inside the existing modal via assets/catalog.js.
    markup=f'''<article class="product-card" role="button" tabindex="0" data-item="{escape(p['id'],quote=True)}" data-category="{escape(p['cat'],quote=True)}" data-name="{escape(name_str,quote=True)}" aria-label="{escape(l['call']+title,quote=True)}"><div class="card-image"><img src="{prefix}{escape(p['img'],quote=True)}.webp?v=real4" alt="{escape(title+' — Rose & Co',quote=True)}" width="960" height="1200" loading="lazy" decoding="async"/>{tag}<span class="card-id">{escape(p['id'])}</span><span class="corner-arrow">↗</span></div><div class="product-meta"><span class="category-label">{escape(cat)}</span><h3>{escape(title)}</h3><p>{escape(l['price'])}</p><span class="card-action">{escape(l['question'])}<span>→</span></span></div></article>'''
    return BeautifulSoup(markup,'html.parser').article

pages=0
for page in root.rglob('*.html'):
    lang=next((x for x in ('hy','ru','en') if x in page.parts),None)
    if not lang:continue
    soup=BeautifulSoup(page.read_text(encoding='utf-8'),'html.parser')
    for notice in soup.select('.notice-strip'):notice.decompose()
    # Do not alter the first prominent hero photo or the splash/intro image.
    for node in soup.select('img[src]'):
        src=node.get('src','')
        original=src.split('/')[-1].split('?')[0]
        if original in editorial:
           node['src']=prefix+'real-2026/'+editorial[original]+'?v=real4'
        elif '/rose50/' in src and node.find_parent('article',class_='product-card') is None:
           # Use the premium sharp Rose & Co + Raffaello photograph for the
           # Sweets section cover on all HY/RU/EN homepages. Do not affect
           # original sweets products or the introductory hero photograph.
           if original=='category-sweets.webp':
               node['src']=prefix+'rose50/sweets-05.webp?v=sweets-cover-20261024'
               continue
           if original.startswith('category-'):
               group=original[len('category-'):-len('.webp')]
               if group in category_img:
                   node['src']=prefix+'real-2026/'+category_img[group]+'.webp?v=real4'
           elif original.startswith('wreaths-'):
               node['src']=prefix+'real-2026/wreaths-12.webp?v=real4'
    for catalog in soup.select('#catalog-grid'):
        catalog.clear()
        for entry in products:catalog.append(card(entry,lang))
    for count in soup.select('#result-count'):
        count.string=str(len(products))+terms[lang]['found']
    featured=soup.select_one('#featured .product-grid')
    if featured:
        featured.clear()
        featured_items=[products[i] for i in (25,24,7,20,18,23,39,41)]
        for item in featured_items:featured.append(card(item,lang))
    # Homepage messages now describe actual photographed work, not design mockups.
    substitutions={
      'hy':{'Նկարներն օրինակային են, իսկ վերջնական կազմը և առկայությունը հաստատվում են կապ հաստատելիս։':'Ներկայացված են իրական ծաղկային աշխատանքների լուսանկարներ։ Պատվերի առկայությունն ու կազմը ճշտեք մեզ հետ։'},
      'ru':{'Изображения представлены для вдохновения.':'В каталоге представлены фотографии цветочных работ.'},
      'en':{'Images are for inspiration.':'Explore photographs of floral arrangements.'}}
    html=str(soup)
    for before,after in substitutions[lang].items():html=html.replace(before,after)
    page.write_text(html,encoding='utf-8')
    pages+=1

# Correct thumbnail and modal photo presentation: NEVER crop a customer's actual product.
css=root/'assets'/'styles.css'
css.write_text(css.read_text(encoding='utf-8')+'''
/* Rose & Co 2026: one consistent portrait frame, whole product always visible. */
.card-image {aspect-ratio:4/5 !important; background:#eae7e5 !important; display:grid; place-items:center;}
.card-image img {width:100% !important; height:100% !important; object-fit:contain !important; object-position:center center !important; display:block !important;}
.product-card:hover .card-image img {transform:scale(1.015) !important;}
.modal-photo {background:#eae7e5; display:grid; place-items:center;}
.modal-photo img {width:100%; height:100%; object-fit:contain !important; object-position:center center !important;}
.card-image .photo-brand-tag {position:absolute;bottom:15px;right:16px;z-index:3;min-width:58px;padding:9px 8px 8px;text-align:center;background:rgba(255,250,243,.94);border:1px solid #d3c4b7;color:#5b3d43;font-family:Georgia,serif;font-style:italic;font-size:13px;line-height:.93;letter-spacing:-.01em;box-shadow:0 3px 12px rgba(0,0,0,.10);transform:rotate(6deg);pointer-events:none;}
.card-image .photo-brand-tag small {display:block;font-size:9px;letter-spacing:.09em;font-style:normal;margin-top:3px;}
.card-image .photo-brand-tag:before {content:'';position:absolute;top:-11px;left:48%;height:11px;width:1px;background:rgba(93,77,70,.65);transform:rotate(-8deg);}
@media (max-width:768px) {.card-image{aspect-ratio:4/5 !important;}.card-image .photo-brand-tag{font-size:11px;bottom:10px;right:9px;padding:7px 6px;min-width:48px;}}

/* Consistent product card heights: every Ask for price stays on the same
   baseline within its grid row, even when names wrap to extra lines. */
.product-grid {align-items:stretch;}
.product-grid .product-card {display:flex;flex-direction:column;height:100%;min-width:0;}
.product-grid .product-card .card-image {flex:0 0 auto;width:100%;}
.product-grid .product-card .product-meta {display:flex;flex-direction:column;flex:1 1 auto;min-width:0;}
/* Keep the price note on one baseline across each row, despite multi-line names. */
.product-grid .product-card .product-meta p {margin-top:auto;display:flex;align-items:flex-end;min-width:0;}
.product-grid .product-card .card-action {margin-top:0;}
''',encoding='utf-8')
# Bust CSS cache on GitHub Pages devices.
for page in root.rglob('*.html'):
    html=page.read_text(encoding='utf-8')
    html=html.replace('/rose-and-co/assets/styles.css"','/rose-and-co/assets/styles.css?v=align6"')
    html=html.replace('/rose-and-co/assets/catalog.js"','/rose-and-co/assets/catalog.js?v=real4"')
    html=html.replace('/rose-and-co/assets/app.js"','/rose-and-co/assets/app.js?v=real4"')
    page.write_text(html,encoding='utf-8')
# Reuse existing modal; clear old cache hints from its source.
js=root/'assets'/'app.js'
s=js.read_text(encoding='utf-8')
s=s.replace('${esc(p.img)}.webp?v=photo2','${esc(p.img)}.webp?v=real4')
s=s.replace('${esc(p.img)}.webp"','${esc(p.img)}.webp?v=real4"')
js.write_text(s,encoding='utf-8')
# Delete old catalog-only assets, not the user's favorite landing hero or any original sweet photos.
old_photos=root/'assets'/'images'/'rose50'
for pat in ('flowers-*.webp','wreaths-*.webp','teddy-bears-*.webp'):
  for path in old_photos.glob(pat):path.unlink()
for name in ['category-romance.webp','category-wedding.webp','category-occasions.webp','category-signature.webp','category-wreaths.webp','category-seasonal.webp','category-teddies.webp','category-plush.webp']:
   (old_photos/name).unlink(missing_ok=True)
(old_photos/'manifest.json').unlink(missing_ok=True)
# Removing unused artist-montage assets prevents future confusion; don't touch hero or sweet categories.
for name in ['pink-peonies.webp','blush-ceremony.webp','atelier-peony.webp','atelier-elegance.webp','atelier-detail.webp','studio-birthday.webp','white-wreath.webp','crimson-wreath.webp','blush-wreath.webp']:
    (root/'assets'/'images'/name).unlink(missing_ok=True)
# Track correct customer-image inventory for sanity checking.
(root/'assets'/'images'/'real-2026'/'inventory.json').write_text(json.dumps({'flowers':41,'wreaths':16,'toys':5,'new_sweets':3,'editorial':7,'catalog_products':len(products),'old_sweets_preserved':len(old_sweets)},ensure_ascii=False,indent=2),encoding='utf-8')
print('Rose & Co: 72 user photographs installed, 71 uniquely pictured catalog items, 6 original sweets preserved, hero untouched; edited',pages,'locale pages.')