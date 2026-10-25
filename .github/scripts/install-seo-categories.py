#!/usr/bin/env python3
"""Rose & Co commercial category landing pages — helpful, localized, indexable.

Unlike a generic filtered catalog query string, each category gets an actual
HTML page, a useful buying guide, the real available assortment, self-canonical
and hreflang after final-seo-qa, and normal anchor navigation to the catalog.
Runs AFTER the real-photo/feature installers and BEFORE final-seo-qa.
"""
from pathlib import Path
from bs4 import BeautifulSoup
from html import escape
from urllib.parse import quote
import json
import re
import sys

root=Path(sys.argv[1]).resolve()
repo=Path(__file__).resolve().parents[2]
content=json.loads((repo/'.github/seo-category-content.json').read_text(encoding='utf-8'))
data=json.loads((repo/'.github/admin-data.json').read_text(encoding='utf-8'))
products=[p for p in data['products'] if p.get('enabled',True)]
by_category={k:[p for p in products if p['cat']==k] for k in content}
assert all(len(ps)>=4 for ps in by_category.values()),by_category
langs=('hy','ru','en')
prefix='/rose-and-co/'
host='https://alform-creator.github.io'
phone=data.get('settings',{}).get('phone','+37433081898')
wa=data.get('settings',{}).get('whatsapp','37433081898')
assert re.fullmatch(r'\d{7,15}',wa)
L={
'hy':{
'home':'Գլխավոր','catalog':'Կատալոգ','collection':'Ծաղկեփնջերի հավաքածուներ',
'collectionLead':'Ընտրեք ձեր առիթին համապատասխան ձևավորումը՝ իրական աշխատանքների լուսանկարներով։',
'works':'Ընտրանի մեր կատալոգից','worksIntro':'Լուսանկարներում ներկայացված են Rose & Co-ի աշխատանքները։ Ծաղիկների վերջնական կազմը, գինը և հասանելիությունը ճշտվում են պատվերից առաջ։',
'view':'Դիտել կատալոգում','price':'Հարցնել գինը','faq':'Հաճախ տրվող հարցեր',
'more':'Դիտել այլ հավաքածուներ','consult':'Քննարկել պատվերը','all':'Ամբողջ կատալոգը',
'note':'Հիշեցում․ լուսանկարներն իրական աշխատանքների օրինակներ են, ոչ թե տվյալ պահին առկա ապրանքի երաշխիք։',
'contact':'Հարցերի կամ անհատական պատվերի համար գրեք մեզ կամ զանգահարեք։',
'catNames':{'romance':'Սիրային փնջեր','wedding':'Հարսանեկան ծաղիկներ','occasions':'Տոնական փնջեր','signature':'Հեղինակային կոմպոզիցիաներ','wreaths':'Ծաղկեպսակներ','seasonal':'Սեզոնային ծաղիկներ'},
'waText':'Բարև, հետաքրքրված եմ Rose & Co-ի'},
'priceSuffix':' ֏'},
'ru':{
'home':'Главная','catalog':'Каталог','collection':'Коллекции цветочных композиций',
'collectionLead':'Выберите оформление для вашего повода по реальным фотографиям работ.',
'works':'Работы из нашего каталога','worksIntro':'На фотографиях представлены работы Rose & Co. Состав цветов, текущая цена и наличие согласовываются перед заказом.',
'view':'Посмотреть в каталоге','price':'Уточнить цену','faq':'Частые вопросы',
'more':'Другие коллекции','consult':'Обсудить заказ','all':'Весь каталог',
'note':'Обратите внимание: фотографии показывают примеры выполненных работ и не гарантируют наличие точно такой же композиции.',
'contact':'Для вопросов или индивидуального заказа напишите нам или позвоните.',
'catNames':{'romance':'Романтические букеты','wedding':'Свадебные цветы','occasions':'Праздничные букеты','signature':'Авторские композиции','wreaths':'Траурные венки','seasonal':'Сезонные цветы'},
'waText':'Здравствуйте, меня интересует коллекция Rose & Co'},
'priceSuffix':' AMD'},
'en':{
'home':'Home','catalog':'Catalog','collection':'Flower and Bouquet Collections',
'collectionLead':'Browse real arrangement photographs and discover an option for your occasion.',
'works':'Explore the collection','worksIntro':'These photographs show genuine Rose & Co arrangements. The final flowers, price and availability are confirmed before ordering.',
'view':'View in catalog','price':'Ask for price','faq':'Frequently asked questions',
'more':'Discover more collections','consult':'Enquire about this collection','all':'Full catalog',
'note':'Please note: photographs are examples of completed work and do not guarantee that the exact same flowers are currently available.',
'contact':'For questions or a personalised request, message or call us.',
'catNames':{'romance':'Romantic bouquets','wedding':'Wedding flowers','occasions':'Celebration bouquets','signature':'Signature arrangements','wreaths':'Memorial wreaths','seasonal':'Seasonal flowers'},
'waText':'Hello, I am interested in Rose & Co collection'},
'priceSuffix':' AMD'}
}

css=r'''
/* ROSE-CO-SEO-CATEGORY-COLLECTIONS-20261025 */
.seo-collection{--rose-ink:#562a40;--rose-blush:#f4e7e2;color:var(--rose-ink);}
.seo-collection .container{max-width:1280px}
.seo-collection .seo-cat-hero{padding:clamp(50px,7vw,88px) 0;background:linear-gradient(125deg,#fffaf6 0%,#f3e3e2 100%)}
.seo-cat-hero-grid{display:grid;grid-template-columns:minmax(0,1.08fr) minmax(0,.92fr);gap:clamp(20px,6vw,90px);align-items:center}
.seo-cat-kicker{display:block;font-size:11px;font-weight:700;letter-spacing:.17em;color:#96687b;text-transform:uppercase}
.seo-collection h1{font-family:var(--serif,"Noto Serif Armenian",Georgia,serif);font-size:clamp(33px,4.4vw,61px);line-height:1.24;font-weight:500;margin:16px 0 22px;overflow-wrap:anywhere;text-wrap:balance}
.seo-cat-lead{font-size:clamp(14px,1.5vw,17px);line-height:1.9;max-width:61ch}
.seo-cat-hero-photo{aspect-ratio:5/5.4;border-radius:260px 260px 5px 5px;overflow:hidden;box-shadow:0 26px 55px rgba(79,36,52,.12);background:#ead5d1}
.seo-cat-hero-photo img{display:block;width:100%;height:100%;object-fit:cover}
.seo-cat-actions{display:flex;flex-wrap:wrap;gap:11px;margin-top:22px}
.seo-cat-actions .button{min-width:0}
.seo-cat-section{padding:clamp(56px,7vw,93px) 0}
.seo-cat-section h2{font-family:var(--serif,"Noto Serif Armenian",Georgia,serif);font-size:clamp(29px,3.4vw,45px);line-height:1.35;font-weight:500;margin-bottom:16px;text-wrap:balance}
.seo-cat-intro{color:#73616a;max-width:77ch;font-size:14px;line-height:1.9;margin-bottom:29px}
.seo-cat-products{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:clamp(12px,2.3vw,26px)}
.seo-product-card{display:flex;flex-direction:column;min-width:0;text-decoration:none!important;color:inherit;background:#fff;border:1px solid #eee3df;padding:8px 8px 16px;transition:transform .24s ease,box-shadow .24s ease;border-radius:5px}
.seo-product-card:hover{transform:translateY(-3px);box-shadow:0 14px 34px rgba(90,46,63,.1)}
.seo-product-photo{aspect-ratio:4/5;display:block;overflow:hidden;background:#f3e8e4;border-radius:3px}
.seo-product-photo img{width:100%;height:100%;object-fit:cover;display:block;transition:transform .5s ease}
.seo-product-card:hover img{transform:scale(1.035)}
.seo-product-name{font-size:14px;line-height:1.52;font-weight:600;padding:14px 8px 5px;overflow-wrap:anywhere}
.seo-product-ref{font-size:11px;letter-spacing:.08em;color:#927481;padding:0 8px}
.seo-product-price{font-size:12px;color:#753e58;padding:8px 8px 0}
.seo-cat-help{background:#fbf6f2}
.seo-cat-guides{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px;margin-top:27px}
.seo-cat-guide{padding:clamp(21px,3vw,32px);background:#fff;border:1px solid #ede2df;border-radius:5px}
.seo-cat-guide h3{font:500 clamp(20px,2vw,25px)/1.35 var(--serif,Georgia,serif);margin-bottom:14px}
.seo-cat-guide p{font-size:13px;line-height:1.95;color:#796975}
.seo-cat-faq{display:grid;grid-template-columns:1fr 1fr;gap:19px}
.seo-cat-faq article{border-top:1px solid #d3bbc2;padding-top:17px;min-width:0}
.seo-cat-faq h3{font-size:17px;line-height:1.5;margin-bottom:9px}
.seo-cat-faq p{font-size:14px;line-height:1.85;color:#75646d}
.seo-cat-more{display:flex;flex-wrap:wrap;gap:10px;margin-top:20px}
.seo-cat-more a,.seo-catalog-categories a,.seo-home-categories a{display:inline-flex;align-items:center;justify-content:center;padding:10px 15px;border:1px solid #d8bec6;color:#6b3d52;border-radius:3px;text-decoration:none;line-height:1.45;font-size:13px;transition:background .2s ease}
.seo-cat-more a:hover,.seo-catalog-categories a:hover,.seo-home-categories a:hover{background:#f1e4e7}
.seo-catalog-categories,.seo-home-categories{padding:19px 0 26px}
.seo-catalog-categories h2,.seo-home-categories h2{font-family:var(--serif,Georgia,serif);font-size:clamp(22px,2.5vw,32px);line-height:1.35;margin:0 0 11px}
.seo-catalog-categories p,.seo-home-categories p{font-size:13px;line-height:1.7;color:#796773;margin-bottom:16px}
.seo-catalog-categories div,.seo-home-categories div{display:flex;flex-wrap:wrap;gap:9px}
.seo-collection .rc-breadcrumb-shell{border-bottom:1px solid #efe5df}
.seo-product-card:focus-visible,.seo-cat-more a:focus-visible,.seo-catalog-categories a:focus-visible,.seo-home-categories a:focus-visible{outline:2px solid #9b6079;outline-offset:4px}
@media(max-width:980px){.seo-cat-products{grid-template-columns:repeat(3,minmax(0,1fr))}.seo-cat-hero-grid{gap:30px}}
@media(max-width:720px){.seo-cat-hero-grid{grid-template-columns:1fr}.seo-cat-hero-photo{max-height:410px;aspect-ratio:1.45/1;border-radius:180px 180px 3px 3px}.seo-cat-guides{grid-template-columns:1fr}.seo-cat-products{grid-template-columns:repeat(2,minmax(0,1fr))}.seo-cat-faq{grid-template-columns:1fr}.seo-cat-section{padding:52px 0}.seo-collection h1{font-size:clamp(30px,8vw,43px);line-height:1.4}.seo-cat-hero-photo img{object-position:center 45%}}
@media(max-width:390px){.seo-product-name{font-size:12px}.seo-product-price{font-size:11px}.seo-product-card{padding:5px 5px 13px}.seo-cat-more a,.seo-catalog-categories a,.seo-home-categories a{font-size:12px;padding:10px 12px}}
@media(prefers-reduced-motion:reduce){.seo-product-card,.seo-product-photo img{transition:none!important;transform:none!important}}
'''
cssfile=root/'assets/seo-collections.css'
cssfile.write_text(css,encoding='utf-8')
assert (root/'assets/styles.css').is_file()
def E(s):return escape(str(s),quote=True)
def href(lang,slug):return prefix+lang+'/collections/'+slug+'/'
def tags(lang,current=None):
    return ''.join('<a href="'+href(lang,k)+'"'+(' aria-current="page"' if k==current else '')+'>'+E(L[lang]['catNames'][k])+'</a>' for k in content)
def listing(p,lang):
    img=prefix+'assets/images/'+p['img']+'.webp'
    name=p['name'][lang];label=L[lang]
    price=(format(p['price_amd'],',').replace(',',' ')+label['priceSuffix']) if p.get('price_amd') else label['price']
    dest=prefix+lang+'/catalog/?category='+p['cat']+'#product-'+p['id']
    return ('<a class="seo-product-card" href="'+E(dest)+'">'
        '<span class="seo-product-photo"><img loading="lazy" decoding="async" width="960" height="1200" src="'+E(img)+'" alt="'+E(name+' — Rose & Co')+'"></span>'
        '<strong class="seo-product-name">'+E(name)+'</strong><span class="seo-product-ref">Rose &amp; Co · '+E(p['id'])+'</span>'
        '<span class="seo-product-price">'+E(price)+'</span></a>')
for lang in langs:
    locale=L[lang]
    source=(root/lang/'catalog/index.html')
    assert source.is_file()
    for cat,localized in content.items():
        details=localized[lang]
        items=by_category[cat]
        image=prefix+'assets/images/'+items[0]['img']+'.webp'
        dest=root/lang/'collections'/cat/'index.html'
        dest.parent.mkdir(parents=True,exist_ok=True)
        base=BeautifulSoup(source.read_text(encoding='utf-8'),'html.parser')
        base.html['data-page']='category'
        base.html['data-collection']=cat
        base.title.string=details['title']
        for key,value in (('description',details['desc']),('robots','index,follow,max-image-preview:large')):
            node=base.select_one('meta[name="'+key+'"]')
            if not node:
                node=base.new_tag('meta',attrs={'name':key})
                base.head.append(node)
            node['content']=value
        for prop,value in (('og:title',details['title']),('og:description',details['desc']),('og:image',host+image),('og:type','website')):
            node=base.select_one('meta[property="'+prop+'"]')
            if not node:
                node=base.new_tag('meta',attrs={'property':prop})
                base.head.append(node)
            node['content']=value
        for node in base.select('script[type="application/ld+json"]'):
            # Catalog's item-list descriptions are not applicable to this new
            # category and would misrepresent products shown.
            try:j=json.loads(node.string or node.get_text())
            except (ValueError,TypeError):continue
            if (j.get('@type') in ('ItemList','BreadcrumbList')):node.decompose()
        # final-seo-qa refreshes canonical & reciprocal hreflangs.
        for node in base.select('link[rel="canonical"],link[hreflang]'):node.decompose()
        for node in base.select('.language-switcher a'):
            langbutton=node.get_text(' ',strip=True).lower()
            if langbutton in langs:
                node['href']=href(langbutton,cat)
                node['class']=['current'] if langbutton==lang else []
                if langbutton==lang:node['aria-current']='page'
                else:node.attrs.pop('aria-current',None)
        for node in base.select('nav .nav-link'):
            if node.get('href','').rstrip('/')==prefix+lang+'/catalog':
                node['class']=list(set(node.get('class',[])+['active']))
        cssnode=base.new_tag('link',rel='stylesheet',href=prefix+'assets/seo-collections.css?v=1')
        base.head.append(cssnode)
        main=base.select_one('main#main')
        assert main
        guides=''.join('<article class="seo-cat-guide"><h3>'+E(head)+'</h3><p>'+E(body)+'</p></article>' for head,body in details['advice'])
        faqs=''.join('<article><h3>'+E(q)+'</h3><p>'+E(a)+'</p></article>' for q,a in details['faq'])
        message=quote(locale['waText']+' '+locale['catNames'][cat],safe='')
        btn='https://wa.me/'+wa+'?text='+message
        home=prefix+lang+'/'
        catalog=home+'catalog/'
        markup=(
        '<main id="main" class="seo-collection">'
        '<div class="rc-breadcrumb-shell"><div class="container"><nav class="rc-breadcrumb" aria-label="Breadcrumb"><ol>'
        '<li><a href="'+home+'">'+E(locale['home'])+'</a></li>'
        '<li><a href="'+catalog+'">'+E(locale['catalog'])+'</a></li>'
        '<li aria-current="page">'+E(locale['catNames'][cat])+'</li></ol></nav></div></div>'
        '<section class="seo-cat-hero"><div class="container seo-cat-hero-grid"><div>'
        '<span class="seo-cat-kicker">ROSE &amp; CO · THE COLLECTION</span>'
        '<h1>'+E(details['heading'])+'</h1><p class="seo-cat-lead">'+E(details['lead'])+'</p>'
        '<div class="seo-cat-actions"><a class="button btn-burgundy" href="'+E(btn)+'" target="_blank" rel="noopener noreferrer">'+E(locale['consult'])+' ↗</a>'
        '<a class="button btn-outline" href="'+catalog+'">'+E(locale['all'])+'</a></div>'
        '</div><div class="seo-cat-hero-photo"><img src="'+image+'" alt="'+E(items[0]['name'][lang])+'" width="960" height="1200" loading="eager" fetchpriority="high" decoding="async"></div></div></section>'
        '<section class="seo-cat-section"><div class="container"><h2>'+E(locale['works'])+'</h2><p class="seo-cat-intro">'+E(locale['worksIntro'])+'</p>'
        '<div class="seo-cat-products">'+''.join(listing(p,lang) for p in items)+'</div>'
        '<p class="seo-cat-intro" style="margin-top:22px">'+E(locale['note'])+'</p></div></section>'
        '<section class="seo-cat-section seo-cat-help"><div class="container"><h2>'+E(details['adviceTitle'])+'</h2>'
        '<div class="seo-cat-guides">'+guides+'</div></div></section>'
        '<section class="seo-cat-section"><div class="container"><h2>'+E(locale['faq'])+'</h2><div class="seo-cat-faq">'+faqs+'</div></div></section>'
        '<section class="seo-cat-section seo-cat-help"><div class="container"><h2>'+E(locale['more'])+'</h2><p class="seo-cat-intro">'+E(locale['contact'])+'</p>'
        '<nav class="seo-cat-more" aria-label="'+E(locale['more'])+'">'+tags(lang,current=cat)+'</nav></div></section>'
        '</main>')
        new_main=BeautifulSoup(markup,'html.parser').main
        main.replace_with(new_main)
        # Explicit ItemList, not merchant Product offers: no confirmed prices.
        canonical=host+href(lang,cat)
        li=[{"@type":"ListItem","position":i+1,"url":host+catalog+"?category="+cat+"#product-"+p['id'],
             "name":p['name'][lang]} for i,p in enumerate(items)]
        schema={"@context":"https://schema.org","@graph":[
            {"@type":"CollectionPage","@id":canonical+"#collection","url":canonical,
             "name":details['heading'],"description":details['desc'],"inLanguage":lang,
             "primaryImageOfPage":host+image,
             "mainEntity":{"@type":"ItemList","numberOfItems":len(items),"itemListElement":li}},
            {"@type":"BreadcrumbList","itemListElement":[
                {"@type":"ListItem","position":1,"name":locale['home'],"item":host+home},
                {"@type":"ListItem","position":2,"name":locale['catalog'],"item":host+catalog},
                {"@type":"ListItem","position":3,"name":locale['catNames'][cat],"item":canonical}
            ]}
        ]}
        node=base.new_tag('script',type='application/ld+json')
        node.string=json.dumps(schema,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')
        base.head.append(node)
        dest.write_text(str(base),encoding='utf-8')
    # Cross-link collections from the existing catalog and homepage with a
    # clearly visible, responsive set of human-written labels.
    for rel in ('catalog/index.html','index.html'):
        file=root/lang/rel
        doc=BeautifulSoup(file.read_text(encoding='utf-8'),'html.parser')
        secid='seo-categories-'+('home' if rel=='index.html' else 'catalog')
        assert not doc.select_one('#'+secid)
        section='<section class="'+('seo-home-categories section container' if rel=='index.html' else 'seo-catalog-categories container')+'" id="'+secid+'">'
        section+='<h2>'+E(locale['collection'])+'</h2><p>'+E(locale['collectionLead'])+'</p><div>'+tags(lang)+'</div></section>'
        sec=BeautifulSoup(section,'html.parser').section
        if rel=='catalog/index.html':
            target=doc.select_one('section.catalog-section')
            assert target
            target.insert_before(sec)
        else:
            target=doc.select_one('#featured') or doc.select_one('.categories-section')
            assert target
            target.insert_after(sec)
        link=doc.new_tag('link',rel='stylesheet',href=prefix+'assets/seo-collections.css?v=1')
        doc.head.append(link)
        file.write_text(str(doc),encoding='utf-8')
    # Replace footer links that previously navigated to filter query strings
    # with the canonical category pages throughout the actual site.
    for file in (root/lang).rglob('index.html'):
        doc=BeautifulSoup(file.read_text(encoding='utf-8'),'html.parser')
        changed=False
        for a in doc.select('footer a[href]'):
            old=a['href']
            for cat in content:
                if old==prefix+lang+'/catalog/?category='+cat:
                    a['href']=href(lang,cat)
                    changed=True
                    break
        if changed:file.write_text(str(doc),encoding='utf-8')
print('Rose & Co SEO category pages generated:',len(content)*len(langs),
      '| products on collection cards:',sum(len(v) for v in by_category.values())*3,
      '| bilingual/canonical-ready, honest descriptions, accessible links.')
