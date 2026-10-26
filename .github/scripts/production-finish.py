#!/usr/bin/env python3
"""Production fixes applied after all source-archive and admin generators."""
from pathlib import Path
from bs4 import BeautifulSoup
import json,re,sys
from urllib.parse import quote
root=Path(sys.argv[1]).resolve()
repo=Path(__file__).resolve().parents[2]
settings=json.loads((repo/'.github/admin-data.json').read_text())['settings']
css='''/* ROSE PRODUCTION RELEASE 2026-10-26 */
:root{--muted:#6b5b59}
.language-switcher a{color:#76535d;min-width:30px;min-height:36px;display:inline-flex;align-items:center;justify-content:center}
.category-label,.disclaimer,.modal-note{color:#79535e}
.modal-info h2{font-size:clamp(26px,3vw,40px);line-height:1.4;overflow-wrap:break-word}
.modal-actions{flex-wrap:wrap;gap:10px}
.modal-actions .button{min-height:48px;white-space:normal;text-align:center}
.product-card[hidden]{display:none!important}
.product-card{scroll-margin-top:110px}
.product-meta>p:has(+.card-action){display:none!important}
.hero h1{font-size:clamp(40px,4.5vw,66px)}
html[lang=hy] .hero h1{font-size:clamp(36px,3.7vw,54px);line-height:1.38}
.rose-runner{width:220px!important;height:107px!important;left:auto!important;right:18px;bottom:12px;transform:translateY(14px);z-index:30!important}
.rose-runner::before{inset:15px 4px 3px;border-radius:60px 60px 18px 18px}
.rose-runner-close{top:0!important;right:0!important;min-width:32px;min-height:32px}
@keyframes rr-scene-cycle{0%{opacity:0;transform:translateY(16px)}7%,86%{opacity:1;transform:translateY(0)}100%{opacity:0;transform:translateY(13px)}}
@media(max-width:760px){
 .rose-runner{display:block!important;width:220px!important;height:107px!important;right:8px;bottom:max(8px,env(safe-area-inset-bottom,0px))}
 .rose-runner-close{min-width:44px;min-height:44px}
 input,select,textarea{font-size:16px!important}
 .hero h1{font-size:clamp(32px,7.5vw,44px)}
 html[lang=hy] .hero h1{font-size:clamp(30px,7.4vw,39px);line-height:1.42}
 .language-switcher a,.menu-toggle{min-height:44px;min-width:36px}
 .modal-info{padding:24px 20px}
 .modal-info h2{font-size:28px}
 .modal-actions .button{flex:1 1 130px}
 .filter-chip,.type-chip{min-height:44px}
}
@media(prefers-reduced-motion:reduce){
 html{scroll-behavior:auto!important}
 .rose-runner,.rose-runner.rose-runner-active,.rose-petal{display:none!important}
 .marquee-track{animation:none!important}
}
'''
(root/'assets/production.css').write_text(css)
# Initial, inspectable links: do not rely on a click to set their destinations.
app=root/'assets/app.js'
js=app.read_text()
start=js.index('function contactClick(')
end=js.index('connectButtons();',start)
replacement=r'''function productMessage(p){return p?`Rose & Co · ${p.name[locale]||p.name.hy} (${p.id}). ${p.price_amd ? Number(p.price_amd).toLocaleString('en-US')+' AMD' : t.price}`:'Rose & Co · '+t.price}
function connectButtons(root=document,product){
 root.querySelectorAll('[data-requires-contact]').forEach(b=>{
  const number=b.dataset.requiresContact==='phone'?phone():wa();
  if(!number){b.addEventListener('click',e=>{e.preventDefault();toast(t.clickContact)});return}
  if(b.dataset.requiresContact==='phone')b.href='tel:'+number;
  else{b.href='https://wa.me/'+number+'?text='+encodeURIComponent(productMessage(product));b.target='_blank';b.rel='noopener noreferrer'}
 });
}
'''
js=js[:start]+replacement+js[end:]
js=js.replace('dlg.showModal();',"if(!dlg.open)dlg.showModal();dlg.setAttribute('aria-labelledby','product-modal-title');history.replaceState(null,'',location.pathname+location.search+'#product-'+encodeURIComponent(p.id));")
js=js.replace('<h2>${esc(p.name[locale])}</h2>','<h2 id="product-modal-title">${esc(p.name[locale])}</h2>')
js=js.replace('${esc(t.imageNote)} ${esc(t.seasonNote)}','${esc(t.seasonNote)}')
# Product URLs from category pages and shared links must actually open the item.
js=js.replace('// local filtering with URL category deep linking',r'''
function openHashProduct(){
 const match=location.hash.match(/^#product-([A-Za-z0-9_-]{2,20})$/);
 if(match)openItem(match[1]);
}
window.addEventListener('hashchange',openHashProduct);
$('#product-dialog')?.addEventListener('close',()=>{
 if(location.hash.startsWith('#product-'))history.replaceState(null,'',location.pathname+location.search);
});
openHashProduct();
// local filtering with URL category deep linking''')
# Escape closes mobile navigation and returns focus to its control.
js=js.replace('// visible phone buttons only when proper number exists',r'''
document.addEventListener('keydown',event=>{
 if(event.key==='Escape'&&menu?.classList.contains('open')){
  menu.classList.remove('open');menuToggle.setAttribute('aria-expanded','false');menuToggle.focus();
 }
});
// visible phone buttons only when proper number exists''')
app.write_text(js)
count=0
for lang in ('hy','ru','en'):
 for p in (root/lang).rglob('index.html'):
  doc=BeautifulSoup(p.read_text(),'html.parser')
  doc.head.append(doc.new_tag('link',rel='stylesheet',href='/rose-and-co/assets/production.css?v=20261026-intro3'))
  for script in doc.select('script[src]'):
   src=script['src']
   if '/assets/' in src:script['src']=src.split('?')[0]+'?v=release20261026-intro3'
  # Honor no-JS, copy-link and open-in-new-tab behavior throughout public pages.
  for a in doc.select('[data-requires-contact]'):
   kind=a.get('data-requires-contact')
   a['href']='tel:'+settings['phone'] if kind=='phone' else 'https://wa.me/'+settings['whatsapp']
   if kind!='phone':a['target']='_blank';a['rel']='noopener noreferrer'
  # Correct the skip target to the real main element on every localized page.
  for a in doc.select('.rc-skip'):a['href']='#main'
  if lang=='hy':
   for image in doc.select('img.hero-image'):image['alt']='Rose & Co-ի վարդագույն ծաղկային կոմպոզիցիա'
  if lang=='ru':
   for image in doc.select('img.hero-image'):image['alt']='Розовая цветочная композиция Rose & Co'
  # A small, dismissible ornament should not restart on each route change.
  # Form and keyboard access remain independent of decorative motion.
  p.write_text(str(doc));count+=1
# Avoid broad generated-image claims for the catalog's real work photographs.
notes={
 'hy':'Լուսանկարներն օգնում են ընտրել կոմպոզիցիան։ Վերջնական կազմը, տեսքը, գինը և առկայությունը ճշտվում են պատվերից առաջ։',
 'ru':'Фотографии помогают выбрать композицию. Окончательный состав, вид, стоимость и наличие согласуем перед заказом.',
 'en':'Use the photographs as a guide. We confirm the final composition, appearance, price and availability before ordering.'}
for lang in notes:
 p=root/lang/'catalog/index.html';d=BeautifulSoup(p.read_text(),'html.parser')
 for n in d.select('.disclaimer'):n.string=notes[lang]
 p.write_text(str(d))
# Deployment identity allows an unambiguous production check without cache guesses.
(root/'release.json').write_text(json.dumps({'release':'2026-10-26-production','pages':count,'languages':['hy','ru','en']}))
print('PRODUCTION FINISH:',count,'pages; eager contact URLs, product deep links, readable controls, restrained mobile motion.')
