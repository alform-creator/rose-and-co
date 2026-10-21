(()=>{'use strict';
const data=window.ROSE_DATA||{products:[],flowers:[],cats:[]};const locale=document.documentElement.lang||'hy';const i18n=window.ROSE_I18N||{};const t=i18n[locale]||i18n.hy;const contact=window.ROSE_CONTACT||{};
const $=s=>document.querySelector(s);const $$=s=>[...document.querySelectorAll(s)];
const norm=s=>(s||'').toString().toLocaleLowerCase().normalize('NFKD');
const esc=s=>(s||'').toString().replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
let toastTimer;
function toast(msg){let node=$('#toast');if(!node)return;node.textContent=msg;node.classList.add('visible');clearTimeout(toastTimer);toastTimer=setTimeout(()=>node.classList.remove('visible'),4200)}
function phone(){return (contact.phone||'').toString().replace(/[^\d+]/g,'')}
function wa(){return (contact.whatsapp||contact.phone||'').toString().replace(/[^\d]/g,'')}
function contactClick(event,kind,p){const number=kind==='phone'?phone():wa();if(!number){event.preventDefault();toast(t.clickContact);return false}
if(kind==='phone'){event.currentTarget.href='tel:'+number;}else{const message=p?`Rose & Co · ${p.name[locale]} (${p.id}). ${t.price}`:'Rose & Co · '+t.price;event.currentTarget.href=`https://wa.me/${number}?text=${encodeURIComponent(message)}`;event.currentTarget.target='_blank';event.currentTarget.rel='noopener noreferrer';}return true}
function connectButtons(root=document,product){root.querySelectorAll('[data-requires-contact]').forEach(b=>b.addEventListener('click',e=>contactClick(e,b.dataset.requiresContact,product)))}
connectButtons();
const menuToggle=$('#menu-toggle');const menu=$('#mobile-menu');if(menuToggle&&menu){menuToggle.addEventListener('click',()=>{let opened=menu.classList.toggle('open');menuToggle.setAttribute('aria-expanded',String(opened))});menu.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>{menu.classList.remove('open');menuToggle.setAttribute('aria-expanded','false')}))}
function openItem(id){const p=data.products.find(x=>x.id===id);const dlg=$('#product-dialog');if(!p||!dlg)return;
const cats=t.categories||[];const catName=cats[data.cats.indexOf(p.cat)]||'';
$('#modal-content').innerHTML=`<div class="modal-inner"><div class="modal-photo"><img src="/rose-and-co/assets/images/${esc(p.img)}.webp" alt="${esc(p.name[locale])}" width="820" height="950"></div><div class="modal-info"><span class="eyebrow">ROSE & CO · ${esc(p.id)}</span><div class="category-label" style="margin-top:20px">${esc(catName)}</div><h2>${esc(p.name[locale])}</h2><p>${esc(p.desc[locale])}</p><div class="modal-price">${esc(t.price)}</div><div class="modal-actions"><a class="button btn-burgundy" href="#contact" data-requires-contact="phone">☎ ${esc(t.call)}</a><a class="button btn-outline" href="#contact" data-requires-contact="whatsapp">WhatsApp ↗</a><a class="button btn-instagram" href="${esc(contact.instagram||'https://www.instagram.com/rose___co/')}" target="_blank" rel="noopener noreferrer"><span aria-hidden="true">◎</span> ${esc(t.instagram)}</a></div><p class="modal-note">${esc(t.imageNote)} ${esc(t.seasonNote)}</p></div></div>`;
connectButtons(dlg,p);dlg.showModal();$('#modal-close')?.focus();}
$$('.product-card').forEach(card=>{card.addEventListener('click',()=>openItem(card.dataset.item));card.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();openItem(card.dataset.item)}})});
$('#modal-close')?.addEventListener('click',()=>$('#product-dialog')?.close());$('#product-dialog')?.addEventListener('click',e=>{if(e.target.id==='product-dialog')e.target.close()});
// local filtering with URL category deep linking
if($('#filter-row')){let current='all',query='';const param=new URLSearchParams(location.search).get('category');if(data.cats.includes(param))current=param;function filter(){let shown=0;$$('#catalog-grid .product-card').forEach(card=>{const visible=(current==='all'||card.dataset.category===current)&&norm(card.dataset.name).includes(norm(query));card.hidden=!visible;if(visible)shown++});$('#result-count').textContent=shown+' '+t.found;$('#no-results').hidden=!!shown;$$('.filter-chip').forEach(btn=>{const selected=btn.dataset.filter===current;btn.classList.toggle('active',selected);btn.setAttribute('aria-pressed',String(selected))})}$$('.filter-chip').forEach(btn=>btn.addEventListener('click',()=>{current=btn.dataset.filter;let url=new URL(location.href);if(current==='all')url.searchParams.delete('category');else url.searchParams.set('category',current);history.replaceState({},'',url.pathname+url.search);filter()}));$('#catalog-search')?.addEventListener('input',e=>{query=e.target.value;filter()});filter()}
if($('#type-filter')){const typeButtons=$$('.type-chip');typeButtons.forEach(btn=>btn.addEventListener('click',()=>{let filter=btn.dataset.type;typeButtons.forEach(b=>b.classList.toggle('active',b===btn));$$('.flower-type').forEach(tile=>{tile.hidden=filter!=='all'&&tile.dataset.kind!==filter})}))}
// visible phone buttons only when proper number exists
if(phone()){const el=$('.contact-phone');if(el){el.href='tel:'+phone();el.removeAttribute('data-requires-contact')}}
if(wa()){const el=$('.contact-whatsapp');if(el){el.href='https://wa.me/'+wa();el.target='_blank';el.rel='noopener noreferrer';el.removeAttribute('data-requires-contact')}}
})();
