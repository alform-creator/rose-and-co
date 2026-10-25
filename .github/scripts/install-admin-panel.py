#!/usr/bin/env python3
"""Build a simple GitHub-backed dashboard and apply its approved data changes."""
from pathlib import Path
from bs4 import BeautifulSoup
from html import escape
import json,re,shutil,sys
site=Path(sys.argv[1]).resolve()
repo=Path(__file__).resolve().parents[2]
data=json.loads((repo/'.github/admin-data.json').read_text(encoding='utf-8'))
assert data['schema']==1
langs=('hy','ru','en')
cats=('romance','wedding','occasions','signature','wreaths','seasonal','teddies','plush','sweets')
all_products=data['products']
assert all_products and len({p['id'] for p in all_products})==len(all_products)
for p in all_products:
    assert re.fullmatch(r'[A-Za-z0-9_-]{2,20}',p['id'])
    assert p['cat'] in cats
    assert re.fullmatch(r'(real-2026|rose50|admin)/[A-Za-z0-9_-]+',p['img'])
    assert all(0<len(str(p['name'].get(l,'')))<=160 for l in langs)
    assert all(len(str(p['desc'].get(l,'')))<=800 for l in langs)
    assert p.get('price_amd') is None or (type(p['price_amd'])==int and 0<p['price_amd']<=100000000)
media=repo/'.github/admin-media'
target=site/'assets/images/admin'
target.mkdir(parents=True,exist_ok=True)
if media.exists():
    for file in media.iterdir():
        if file.is_file() and re.fullmatch(r'[A-Za-z0-9_-]+\.webp',file.name):
            shutil.copy2(file,target/file.name)
for p in all_products:
    assert (site/'assets/images'/(p['img']+'.webp')).is_file(),('missing image',p['img'])
products=[p for p in all_products if p.get('enabled',True)]
assert products
settings=data.get('settings',{})
phone=settings.get('phone','+37433081898')
whatsapp=settings.get('whatsapp','37433081898')
instagram=settings.get('instagram','https://www.instagram.com/rose___co/')
assert re.fullmatch(r'\+?\d{7,15}',phone)
assert re.fullmatch(r'\d{7,15}',whatsapp)
assert instagram.startswith('https://www.instagram.com/')
(site/'assets/contact-config.js').write_text('window.ROSE_CONTACT = '+json.dumps(
 dict(phone=phone,whatsapp=whatsapp,instagram=instagram),ensure_ascii=False)+';\n',encoding='utf-8')
catalog=site/'assets/catalog.json'
catalog_data=json.loads(catalog.read_text(encoding='utf-8'))
catalog_data['products']=[{k:v for k,v in p.items() if k in ('id','img','cat','name','desc','price_amd')} for p in products]
raw=json.dumps(catalog_data,ensure_ascii=False,separators=(',',':'))
catalog.write_text(raw+'\n',encoding='utf-8')
(site/'assets/catalog.js').write_text('window.ROSE_DATA='+raw+';\n',encoding='utf-8')
category_labels={
'hy':('Սիրո փնջեր','Հարսանեկան','Տոնական','Հեղինակային','Ծաղկեպսակներ','Սեզոնային','Արջուկներ','Փափուկ խաղալիքներ','Քաղցրավենիք'),
'ru':('Для любимых','Свадебные','Для праздников','Авторские','Венки','Сезонные','Мишки','Мягкие игрушки','Сладости'),
'en':('Romantic Bouquets','Wedding','Occasions','Signature','Wreaths','Seasonal','Teddy Bears','Plush Toys','Sweets')
}
phrases={
'hy':('Դիտել կոմպոզիցիան: ','Հարցնել գինը','Գինը՝ ',' ցուցադրված աշխատանք'),
'ru':('Посмотреть композицию: ','Узнать цену','Цена: ',' товаров'),
'en':('View arrangement: ','Ask for price','Price: ',' items')
}
def card(p,lang):
    title=p['name'][lang];view,ask,cost,unit=phrases[lang]
    img='/rose-and-co/assets/images/'+p['img']+'.webp?v=adm2'
    amount=(format(p['price_amd'],',').replace(',',' ')+' ֏') if p.get('price_amd') else None
    category=category_labels[lang][cats.index(p['cat'])]
    names=' '.join(p['name'].values()).lower()
    brand='' if p['cat']=='wreaths' else '<span aria-hidden="true" class="photo-brand-tag">Rose <small>&amp; Co</small></span>'
    html=f'''<article class="product-card" role="button" tabindex="0" data-item="{escape(p['id'],quote=True)}" data-category="{escape(p['cat'],quote=True)}" data-name="{escape(names,quote=True)}" aria-label="{escape(view+title,quote=True)}"><div class="card-image"><img src="{escape(img,quote=True)}" alt="{escape(title+' — Rose & Co',quote=True)}" width="960" height="1200" loading="lazy" decoding="async"/>{brand}<span class="card-id">{escape(p['id'])}</span><span class="corner-arrow">↗</span></div><div class="product-meta"><span class="category-label">{escape(category)}</span><h3>{escape(title)}</h3><p>{escape(amount or ask)}</p><span class="card-action">{escape(cost+amount if amount else ask)}<span>→</span></span></div></article>'''
    return BeautifulSoup(html,'html.parser').article
reviews=data.get('reviews',[])
for x in reviews:
    assert 0<len(x.get('name',''))<=90
    assert 1<=int(x.get('rating',5))<=5
    assert all(len(x.get('text',{}).get(l,''))<=700 for l in langs)
delivery=settings.get('delivery',{})
for lang in langs:
    for file in (site/lang).rglob('*.html'):
        soup=BeautifulSoup(file.read_text(encoding='utf-8'),'html.parser')
        for grid in soup.select('#catalog-grid'):
            grid.clear()
            for p in products:grid.append(card(p,lang))
        for grid in soup.select('#featured .product-grid'):
            grid.clear()
            features=[p for p in products if p.get('featured')]
            for p in (features or products[:8])[:8]:grid.append(card(p,lang))
        for span in soup.select('#result-count'):
            span.string=str(len(products))+phrases[lang][3]
        setting=soup.select_one('#rs-data')
        if setting:
            ctx=json.loads(setting.string or setting.get_text())
            for zone in ctx.get('delivery_zones',[]):zone['fee_amd']=delivery.get(zone['id'])
            ctx['reviews']=[dict(name=r['name'],rating=int(r.get('rating',5)),text=r.get('text',{}))
                            for r in reviews if r.get('approved')]
            setting.string=json.dumps(ctx,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')
        for a in soup.select('a[href]'):
            href=a.get('href','')
            if href.startswith('tel:+37433081898'):
                a['href']=href.replace('tel:+37433081898','tel:'+phone,1)
            if href.startswith('https://wa.me/37433081898'):
                a['href']=href.replace('https://wa.me/37433081898','https://wa.me/'+whatsapp,1)
        override=data.get('pages',{}).get(file.relative_to(site).as_posix(),{})
        if override:
            for key,selector in (('h1','main h1'),('title','title'),('intro','.hero-copy>p,.page-intro p,.article-hero>p')):
                if override.get(key):
                    x=soup.select_one(selector)
                    if x:x.clear();x.append(override[key])
            if override.get('description'):
                for selector in ('meta[name=description]','meta[property="og:description"]'):
                    x=soup.select_one(selector)
                    if x:x['content']=override['description']
            if override.get('title'):
                x=soup.select_one('meta[property="og:title"]')
                if x:x['content']=override['title']
        file.write_text(str(soup),encoding='utf-8')

# Use owner-set prices in product dialog as well as catalog cards.
app=site/'assets/app.js'
appsrc=app.read_text(encoding='utf-8')
assert 'esc(t.price)' in appsrc
appsrc=appsrc.replace('esc(t.price)',"esc(p.price_amd ? Number(p.price_amd).toLocaleString('en-US')+' ֏' : t.price)")
appsrc=appsrc.replace('data.products.find(x=>x.id===id)',"data.products.find(x=>x.id===id)")
app.write_text(appsrc,encoding='utf-8')
dash=site/'admin'
dash.mkdir(exist_ok=True)
for name in ('index.html','admin.css','admin.js'):
    shutil.copy2(repo/'.github/admin-panel'/name,dash/name)
robots=site/'robots.txt'
robots.write_text(robots.read_text(encoding='utf-8')+'\nDisallow: /rose-and-co/admin/\n',encoding='utf-8')
print('Rose & Co Admin published:',len(products),'visible /',len(all_products),'products;',
      sum(bool(r.get('approved')) for r in reviews),'approved genuine reviews.')
