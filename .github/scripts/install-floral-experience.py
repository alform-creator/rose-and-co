#!/usr/bin/env python3
"""Add rose petals, scroll-bloom ornaments, and localized bouquet builder to Rose & Co."""
from pathlib import Path
from html import escape
import re
import sys

root=Path(sys.argv[1]).resolve()
assets=root/"assets"
assert (root/"hy"/"index.html").is_file()

ROSE_SVG = '''<svg class="rose-bloom-flower" viewBox="0 0 80 80" aria-hidden="true" focusable="false" xmlns="http://www.w3.org/2000/svg">
<g class="rbe-leaves"><path d="M40 58 Q21 65 14 48 Q31 43 40 58Z" fill="#89a58b"/><path d="M42 57 Q62 62 68 45 Q49 45 42 57Z" fill="#79957f"/></g>
<path d="M40 73 Q42 58 40 48" fill="none" stroke="#719375" stroke-width="3" stroke-linecap="round"/>
<g class="rbe-petals" fill="#d994a5" stroke="#a95f78" stroke-width=".75">
<ellipse cx="40" cy="29" rx="12" ry="20" transform="rotate(0 40 40)"/>
<ellipse cx="40" cy="29" rx="12" ry="20" transform="rotate(60 40 40)"/>
<ellipse cx="40" cy="29" rx="12" ry="20" transform="rotate(120 40 40)"/>
<ellipse cx="40" cy="29" rx="12" ry="20" transform="rotate(180 40 40)"/>
<ellipse cx="40" cy="29" rx="12" ry="20" transform="rotate(240 40 40)"/>
<ellipse cx="40" cy="29" rx="12" ry="20" transform="rotate(300 40 40)"/>
</g>
<circle class="rbe-core" cx="40" cy="40" r="12" fill="#f8d7d1"/>
<path class="rbe-core" d="M35 37 Q43 31 47 40 Q47 49 38 48 Q32 44 39 40" fill="none" stroke="#ab667c" stroke-width="2.1" stroke-linecap="round"/>
</svg>'''

LANG = {
"hy": {
"nav":"Ստեղծիր փունջ","eyebrow":"YOUR OWN BOUQUET","title":"Ստեղծիր քո ծաղկեփունջը",
"intro":"Ընտրիր քո սիրելի ծաղիկներն ու գույները։ Մենք կքննարկենք կոմպոզիցիան, առկայությունն ու գինը անհատապես։",
"flower":"Ծաղիկների տեսակ","color":"Գունապնակ","count":"Ծաղիկների քանակ","wrap":"Փաթեթավորում",
"note":"Բացիկի խոսքեր (ըստ ցանկության)","placeholder":"Գրի՛ր քո փոքրիկ ուղերձը…",
"flowerchoices":["Վարդեր","Պիոններ","Կակաչներ","Խառը ծաղիկներ"],
"colorchoices":["Նուրբ վարդագույն","Կարմիր","Սպիտակ / կրեմագույն","Յասամանագույն"],
"wrapchoices":["Նուրբ ժապավեն","Կրաֆտ թուղթ","Նվերային տուփ"],
"preview":"Քո ծաղկեփնջի նախնական տեսքը","previewnote":"Նկարազարդումը խորհրդանշական է․ իրական ծաղիկների կազմը և երանգը կհաստատվեն մեզ հետ։",
"summary":"Քո ընտրությունը","units":"հատ",
"button":"Ուղարկել հարցում WhatsApp-ով ↗","disclaimer":"Հարցում ուղարկելը դեռ պատվերի կամ գնի հաստատում չէ։",
"subject":"Բարև, ուզում եմ պատվիրել իմ ընտրած ծաղկեփունջը Rose & Co-ից։",
"orderFlower":"Ծաղիկներ","orderColor":"Գույն","orderCount":"Քանակ","orderWrap":"Փաթեթավորում","orderMessage":"Բացիկ",
"orderEnding":"Խնդրում եմ ճշտել առկայությունը և գինը։"
},
"ru": {
"nav":"Собрать букет","eyebrow":"YOUR OWN BOUQUET","title":"Создайте свой букет",
"intro":"Выберите цветы, оттенок и упаковку. Мы уточним состав, наличие и стоимость индивидуально.",
"flower":"Какие цветы","color":"Палитра","count":"Количество цветов","wrap":"Упаковка",
"note":"Текст открытки (необязательно)","placeholder":"Напишите небольшое послание…",
"flowerchoices":["Розы","Пионы","Тюльпаны","Смешанные цветы"],
"colorchoices":["Нежно-розовый","Красный","Белый / кремовый","Сиреневый"],
"wrapchoices":["Атласная лента","Крафт-бумага","Подарочная коробка"],
"preview":"Эскиз вашего букета","previewnote":"Иллюстрация условная: точные цветы и оттенки обсуждаются с флористом.",
"summary":"Ваш выбор","units":"шт.",
"button":"Уточнить в WhatsApp ↗","disclaimer":"Отправка запроса не подтверждает цену или заказ.",
"subject":"Здравствуйте! Хочу заказать букет собственной композиции от Rose & Co.",
"orderFlower":"Цветы","orderColor":"Цвет","orderCount":"Количество","orderWrap":"Упаковка","orderMessage":"Открытка",
"orderEnding":"Подскажите, пожалуйста, наличие и стоимость."
},
"en": {
"nav":"Build a bouquet","eyebrow":"YOUR OWN BOUQUET","title":"Create your own bouquet",
"intro":"Choose your flowers, palette and finishing touches. We'll confirm composition, availability and pricing personally.",
"flower":"Flower variety","color":"Colour palette","count":"Number of stems","wrap":"Wrapping",
"note":"Gift card message (optional)","placeholder":"Write a little note…",
"flowerchoices":["Roses","Peonies","Tulips","Mixed flowers"],
"colorchoices":["Blush pink","Classic red","Ivory / cream","Lilac"],
"wrapchoices":["Silk ribbon","Kraft paper","Gift box"],
"preview":"Your bouquet concept","previewnote":"Illustrative preview only. Actual varieties and colours are confirmed with our florist.",
"summary":"Your selection","units":"stems",
"button":"Enquire on WhatsApp ↗","disclaimer":"An enquiry does not confirm an order or its price.",
"subject":"Hello! I'd love a custom bouquet from Rose & Co.",
"orderFlower":"Flowers","orderColor":"Colour","orderCount":"Stems","orderWrap":"Wrapping","orderMessage":"Card",
"orderEnding":"Please confirm availability and price."
}
}

CSS = r'''
/* ROSE-CO-FLORAL-EXPERIENCE-20261025 */
/* Rose-petal flourish: light DOM, pointer-events none, never intercepts clicks. */
.rose-petal-field {position:fixed;inset:0;overflow:hidden;pointer-events:none;z-index:21;}
.rose-petal {
  position:absolute;top:-48px;left:0;
  width:var(--petal-size,15px);height:calc(var(--petal-size,15px)*1.35);
  border-radius:74% 18% 73% 26%;transform-origin:50% 50%;
  background:linear-gradient(125deg,rgba(255,239,231,.95),rgba(228,158,176,.78) 50%,rgba(190,103,128,.55));
  box-shadow:inset 1px 1px 2px rgba(255,255,255,.65),0 1px 3px rgba(120,67,82,.08);
  opacity:0;will-change:transform;
  animation:rose-petal-fall var(--petal-duration,7s) var(--petal-delay,0s) linear forwards;
}
.rose-petal:nth-child(3n) {background:linear-gradient(145deg,#fff1e9,#edd0ca 67%,#d8a1aa);}
.rose-petal:nth-child(5n) {background:linear-gradient(120deg,#fee6e4,#e6b0bb 70%,#bd7d95);}
@keyframes rose-petal-fall {
  0%{opacity:0;transform:translate3d(0,-10px,0) rotate(0deg)}
  8%{opacity:.84}
  83%{opacity:.77}
  100%{opacity:0;transform:translate3d(var(--petal-drift,80px),105vh,0) rotate(var(--petal-turn,620deg))}
}

/* Animated rose ornaments bloom as each heading enters the viewport. */
.rose-bloom-ornament {display:block;width:64px;height:66px;margin:-8px 0 12px;pointer-events:none;}
.section-head.centered .rose-bloom-ornament,
.page-intro .rose-bloom-ornament,.article-hero .rose-bloom-ornament {margin:-6px auto 12px;}
.rose-bloom-flower {display:block;width:100%;height:100%;overflow:visible;}
.rose-bloom-ornament .rbe-petals,
.rose-bloom-ornament .rbe-core {transform:scale(.12) rotate(-35deg);transform-origin:40px 40px;opacity:.2;}
.rose-bloom-ornament .rbe-leaves {opacity:.25;transform:translateY(12px);transform-origin:40px 55px;}
.rose-bloom-ornament.is-bloomed .rbe-petals {
  animation:rose-open-petals 1.15s cubic-bezier(.14,.8,.2,1) both;
}
.rose-bloom-ornament.is-bloomed .rbe-core {
  animation:rose-open-petals 1.02s .20s cubic-bezier(.14,.8,.2,1) both;
}
.rose-bloom-ornament.is-bloomed .rbe-leaves {
  animation:rose-open-leaves .85s .08s ease-out both;
}
@keyframes rose-open-petals {
  0% {transform:scale(.12) rotate(-35deg);opacity:.22}
  68%{transform:scale(1.08) rotate(8deg);opacity:1}
  100%{transform:scale(1) rotate(0);opacity:1}
}
@keyframes rose-open-leaves{
  0%{opacity:.25;transform:translateY(12px) scale(.78)}
  100%{opacity:1;transform:translateY(0) scale(1)}
}

/* Responsive luxury bouquet configurator, matching existing story section. */
.rose-builder-section {
  position:relative;overflow:hidden;isolation:isolate;
  background:
    radial-gradient(circle at 80% 20%,rgba(239,192,200,.40),transparent 35%),
    linear-gradient(135deg,#fffaf6 0%,#f5e7e3 58%,#f8eee9 100%);
  padding:clamp(66px,8vw,108px) 0;
  border-block:1px solid rgba(156,95,113,.12);
  scroll-margin-top:30px;
}
.rose-builder-section::before,.rose-builder-section::after {
  content:"";position:absolute;z-index:-1;pointer-events:none;
  background:url('/rose-and-co/assets/rose-atelier-soft-floral.svg?v=luxe1') center/contain no-repeat;
  opacity:.34;width:330px;height:430px;
}
.rose-builder-section::before{top:-190px;left:-140px;}
.rose-builder-section::after{right:-140px;bottom:-190px;transform:rotate(170deg);}
.rose-builder-header{text-align:center;max-width:770px;margin:0 auto 37px;}
.rose-builder-header .rose-bloom-ornament{margin:0 auto 7px;}
.rose-builder-header h2{
  font:500 clamp(32px,4.2vw,53px)/1.3 var(--serif);
  color:var(--wine);letter-spacing:-.03em;margin:12px 0 14px;
}
.rose-builder-header p{color:#786660;font-size:14px;line-height:1.85;}
.rose-builder-layout{
  display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,.9fr);
  align-items:start;gap:clamp(22px,4vw,52px);
}
.rose-builder-form{
  padding:clamp(22px,3vw,35px);
  background:rgba(255,252,249,.87);
  border:1px solid rgba(149,84,106,.17);
  box-shadow:0 15px 55px rgba(99,53,65,.09);
}
.rose-builder-fieldset{border:0;padding:0;margin:0 0 24px;min-width:0;}
.rose-builder-fieldset legend,.rose-builder-label{
  color:#632940;font-weight:700;font-size:12px;
  letter-spacing:.015em;margin-bottom:12px;display:block;
}
.rose-builder-options{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:9px;}
.rose-builder-options.rose-builder-colours{grid-template-columns:repeat(4,minmax(0,1fr));}
.rose-builder-choice{position:relative;cursor:pointer;min-width:0;}
.rose-builder-choice input{
  position:absolute;opacity:0;width:1px;height:1px;inset:50%;
}
.rose-builder-choice span{
  display:flex;align-items:center;justify-content:center;text-align:center;
  gap:8px;padding:12px 9px;min-height:53px;
  border:1px solid #e4d2cb;background:#fff9f5;
  font-size:12px;line-height:1.45;color:#67565a;
  transition:border-color .2s,background .2s,box-shadow .2s;
}
.rose-builder-choice input:checked+span{
  border-color:#83435a;background:#f8e9e8;
  color:#542039;box-shadow:inset 0 0 0 1px #83435a;
  font-weight:700;
}
.rose-builder-choice input:focus-visible+span{outline:3px solid #b67b88;outline-offset:2px;}
.rose-builder-swatch{
  display:inline-block;flex:0 0 18px;width:18px;height:18px;
  border:1px solid rgba(97,50,58,.15);border-radius:50%;
  background:var(--swatch,#ecb2be);
}
.rose-builder-count{
  display:block;width:100%;max-width:220px;
  padding:12px 15px;background:#fffaf7;color:#542439;
  border:1px solid #d8b7bb;border-radius:2px;font:inherit;font-size:14px;
}
.rose-builder-note {
  width:100%;min-height:80px;resize:vertical;
  border:1px solid #e0c7c6;background:#fffdfa;color:#542b3b;
  padding:14px;font:inherit;font-size:13px;line-height:1.5;border-radius:2px;
}
.rose-builder-note:focus-visible,.rose-builder-count:focus-visible {
  outline:2px solid #b67b88;outline-offset:2px;
}
.rose-builder-preview{
  position:sticky;top:24px;padding:25px clamp(16px,2.4vw,30px) 29px;
  border:1px solid rgba(157,100,113,.15);
  background:linear-gradient(145deg,rgba(255,252,249,.96),rgba(244,227,225,.98));
  box-shadow:0 20px 55px rgba(94,44,64,.09);
}
.rose-builder-preview h3{
  font:500 clamp(22px,2.4vw,29px)/1.3 var(--serif);
  color:var(--wine);margin:0 0 10px;text-align:center;
}
.rose-builder-stage {
  display:grid;place-items:center;min-height:300px;
  border-radius:220px 220px 7px 7px;
  background:radial-gradient(ellipse at 50% 45%,#fffaf6,#f3dedb 78%,#ead2d0 100%);
  overflow:hidden;
}
.rose-builder-stage svg{width:100%;max-width:335px;max-height:315px;height:auto;}
.rose-builder-previewnote {font-size:11px;color:#85716d;line-height:1.75;margin:12px 0;}
.rose-builder-preview h4 {
  font-size:12px;text-transform:uppercase;letter-spacing:.13em;
  margin:18px 0 9px;color:#87465f;
}
.rose-builder-summary{font-size:13px;line-height:1.75;color:#52484a;margin:0 0 20px;overflow-wrap:anywhere;}
.rose-builder-order{display:flex!important;width:100%;white-space:normal;text-align:center;gap:9px;justify-content:center;}
.rose-builder-disclaimer{font-size:11px;line-height:1.65;color:#856d70;margin:11px 0 0;}
.rose-builder-footer,.rose-builder-nav{color:#8f4c63!important;}
.rose-builder-footer{display:inline-block!important;margin-top:9px;font-size:12px!important;font-weight:700;}
.hero-buttons .rose-builder-hero-link{font-weight:700;}
@media(max-width:1100px) {
  .desktop-nav {gap:clamp(8px,1vw,15px);}
  .desktop-nav .nav-link {font-size:11px;}
}
@media(max-width:850px) {
  .rose-builder-layout {grid-template-columns:minmax(0,1fr);}
  .rose-builder-preview{position:static;max-width:700px;margin:auto;width:100%;}
  .rose-builder-header{margin-bottom:22px;}
}
@media(max-width:640px) {
  .rose-builder-options.rose-builder-colours{grid-template-columns:repeat(2,minmax(0,1fr));}
  .rose-builder-form{padding:18px 15px;}
  .rose-builder-section{padding:65px 0;}
  .rose-builder-stage{min-height:245px;}
  .rose-builder-stage svg{max-height:270px;}
  .rose-bloom-ornament{width:53px;height:56px;}
  .rose-builder-section::before,.rose-builder-section::after{width:205px;height:290px;opacity:.2;}
}
@media(prefers-reduced-motion:reduce) {
  .rose-petal-field{display:none!important;}
  .rose-bloom-ornament .rbe-petals,.rose-bloom-ornament .rbe-core,.rose-bloom-ornament .rbe-leaves{
    animation:none!important;opacity:1!important;transform:none!important;
  }
}
'''

JS = r'''(() => {
  "use strict";
  const reduced=window.matchMedia("(prefers-reduced-motion: reduce)");
  const opening=()=>document.documentElement.classList.contains("rose-bloom-on");

  // Visually subtle falling petals. Max 16 elements per burst, removed on finish.
  const petalLayer=document.createElement("div");
  petalLayer.className="rose-petal-field";
  petalLayer.setAttribute("aria-hidden","true");
  document.body.appendChild(petalLayer);
  let lastBurst=0;
  function petals(count=14){
    if(reduced.matches||document.hidden||opening())return;
    const now=Date.now();
    if(now-lastBurst<18000)return;
    lastBurst=now;
    const max=window.innerWidth<640?9:count;
    for(let i=0;i<max;i++){
      const el=document.createElement("span");
      el.className="rose-petal";
      el.style.left=(4+(i*89/max)%92)+"%";
      el.style.setProperty("--petal-size",(9+(i*7)%13)+"px");
      el.style.setProperty("--petal-duration",(5.5+(i%5)*.7)+"s");
      el.style.setProperty("--petal-delay",(i%6)*.32+"s");
      el.style.setProperty("--petal-drift",(-80+(i*37)%160)+"px");
      el.style.setProperty("--petal-turn",((i%2?-1:1)*(320+i*59))+"deg");
      petalLayer.appendChild(el);
      el.addEventListener("animationend",()=>el.remove(),{once:true});
    }
  }
  // Give the first entrance animation time to finish before petals are shown.
  window.setTimeout(()=>petals(16),opening()?5500:900);
  // Gentle repeat for an active visible tab, not an unbroken barrage.
  const petalInterval=window.setInterval(()=>petals(8),70000);

  // Scroll-triggered 3D-style SVG rose opening beside section headings.
  const ornaments=[...document.querySelectorAll(".rose-bloom-ornament")];
  if(reduced.matches||!("IntersectionObserver" in window)){
    ornaments.forEach(x=>x.classList.add("is-bloomed"));
  }else{
    const observer=new IntersectionObserver(entries=>{
      entries.forEach(e=>{
        if(e.isIntersecting){
          e.target.classList.add("is-bloomed");
          observer.unobserve(e.target);
        }
      });
    },{threshold:.24,rootMargin:"0px 0px -25px 0px"});
    ornaments.forEach(x=>observer.observe(x));
  }

  // Live bouquet concept and WhatsApp enquiry; not a checkout or a price quote.
  const builder=document.querySelector("#rose-bouquet-builder");
  if(builder){
    const form=builder.querySelector(".rose-builder-form");
    const image=builder.querySelector(".rose-builder-stage");
    const summary=builder.querySelector(".rose-builder-summary");
    const enquire=builder.querySelector(".rose-builder-order");
    const lang=builder.getAttribute("data-lang")||"hy";
    const words=JSON.parse(builder.querySelector(".rose-builder-words").textContent);
    const flowerNames=words.flowerchoices,colorNames=words.colorchoices,wrapNames=words.wrapchoices;
    const palette=[
      ["#f8d7dc","#df9bad","#b96888"],
      ["#e8a2ad","#c1506a","#8c2748"],
      ["#fff8eb","#f0e4d9","#d0b9ae"],
      ["#dfc9e9","#c0a6d5","#9078b2"]
    ];
    function selected(group){
      const node=form.querySelector('[name="'+group+'"]:checked');
      return node?Number(node.value):0;
    }
    function flower(cx,cy,scale,col,type){
      // Four distinct floral silhouettes, all inline SVG.
      const radius=type===1?17:type===2?10:13;
      const layers=type===2?5:7;
      let s='<g transform="translate('+cx+' '+cy+') scale('+scale+')">';
      for(let n=0;n<layers;n++){
        const angle=n*360/layers;
        s+='<ellipse cx="0" cy="-'+(type===2?11:12)+'" rx="'+(type===2?7:10)+'" ry="'+(type===2?17:15)+'" transform="rotate('+angle+')" fill="'+col[(n+1)%3]+'" opacity=".96"/>';
      }
      s+='<circle r="'+radius+'" fill="'+col[0]+'" opacity=".78"/>';
      s+='<path d="M-6 -2 Q-2 -13 7 -5 Q15 5 1 10 Q-11 9 -6 0 Q0 -4 3 2" stroke="'+col[2]+'" stroke-width="2.3" fill="none" stroke-linecap="round"/>';
      return s+'</g>';
    }
    function preview(type,tint,qty,wrap){
      const col=palette[tint],total=Math.max(9,Math.min(23,Math.ceil(Math.sqrt(qty)*3.0)));
      const blooms=[];
      for(let n=0;n<total;n++){
        const ring=Math.sqrt((n+.6)/total),angle=n*2.39996;
        const x=155+Math.cos(angle)*ring*91, y=123+Math.sin(angle)*ring*77;
        const c=type===3?palette[n%4]:col;
        blooms.push({x,y,markup:flower(x.toFixed(1),y.toFixed(1),(0.65+0.12*(n%3)).toFixed(2),c,type)});
      }
      blooms.sort((a,b)=>a.y-b.y);
      const paper=wrap===1?"#d4c0a8":wrap===2?"#eed4d7":"#fbebe6";
      const bouquet=wrap===2
        ?'<path d="M97 188 L211 188 L198 282 L108 282Z" fill="'+paper+'" stroke="#c49baa" stroke-width="2"/><path d="M106 200H202" stroke="#b98598" stroke-width="2"/>'
        :'<path d="M57 163 Q160 185 253 165 L181 286 L132 286Z" fill="'+paper+'" stroke="#d3b2ab" stroke-width="2"/><path d="M77 169 L154 260 L233 173" stroke="#d7b2ba" opacity=".8" fill="none" stroke-width="3"/>';
      return '<svg viewBox="0 0 310 310" role="img" aria-label="'+words.preview+'" xmlns="http://www.w3.org/2000/svg">'+
        '<ellipse cx="155" cy="293" rx="72" ry="9" fill="#b47b8f" opacity=".16"/>'+
        '<g stroke="#698670" stroke-width="3.5" stroke-linecap="round" opacity=".85">'+
        '<path d="M155 265Q110 170 102 99 M155 265Q174 140 215 90 M155 265Q165 158 154 74 M155 265Q145 155 81 120"/></g>'+
        '<path d="M150 260 Q123 211 107 230 Q125 257 150 260Z M157 251 Q199 212 225 220 Q207 242 157 251Z" fill="#8fab91"/>'+
        bouquet+
        blooms.map(b=>b.markup).join("")+
        '<path d="M132 263 Q153 258 177 265 L177 275 Q156 282 133 275Z" fill="#c27a92"/>'+
        '<path d="M155 271 Q143 258 128 267 Q134 280 155 273 Q168 261 185 267 Q180 280 155 273Z" fill="#e6b5bf"/>'+
        '</svg>';
    }
    function update(){
      const f=selected("rose-flower"),c=selected("rose-color"),w=selected("rose-wrap");
      const count=Number(form.querySelector('[name="rose-count"]').value)||15;
      const note=form.querySelector('[name="rose-note"]').value.trim().slice(0,280);
      image.innerHTML=preview(f,c,count,w);
      const parts=[flowerNames[f],colorNames[c],count+" "+words.units,wrapNames[w]];
      summary.textContent=parts.join(" · ");
      const message=[
        words.subject,
        words.orderFlower+": "+flowerNames[f],
        words.orderColor+": "+colorNames[c],
        words.orderCount+": "+count,
        words.orderWrap+": "+wrapNames[w]
      ];
      if(note) message.push(words.orderMessage+": "+note);
      message.push(words.orderEnding);
      const phone=(window.ROSE_CONTACT&&window.ROSE_CONTACT.whatsapp)||"37433081898";
      enquire.href="https://wa.me/"+phone+"?text="+encodeURIComponent(message.join("\n"));
    }
    form.addEventListener("change",update);
    form.addEventListener("input",e=>{if(e.target.name==="rose-note")update();});
    update();
  }

  window.addEventListener("pagehide",()=>{
    window.clearInterval(petalInterval);
    petalLayer.replaceChildren();
  },{once:true});
})();'''

def choices(name, labels, css_extra=None):
    out=[]
    colours=["#e8adbc","#b34261","#f6e6df","#b49bcd"]
    for i,label in enumerate(labels):
        swatch=(f'<i class="rose-builder-swatch" style="--swatch:{colours[i]}" aria-hidden="true"></i>'
                if css_extra=="swatches" else "")
        out.append(f'<label class="rose-builder-choice"><input type="radio" name="{name}" value="{i}"'
                   +(' checked' if i==0 else '')+'>'
                   +f'<span>{swatch}{escape(label)}</span></label>')
    return "".join(out)

def make_builder(lang):
    w=LANG[lang]
    counts="".join(f'<option value="{n}"'+(" selected" if n==15 else "")+f'>{n}</option>'
                   for n in [9,15,25,35,51,75,101])
    import json
    data=json.dumps({
       "flowerchoices":w["flowerchoices"],"colorchoices":w["colorchoices"],
       "wrapchoices":w["wrapchoices"],"preview":w["preview"],"units":w["units"],
       "subject":w["subject"],"orderFlower":w["orderFlower"],"orderColor":w["orderColor"],
       "orderCount":w["orderCount"],"orderWrap":w["orderWrap"],
       "orderMessage":w["orderMessage"],"orderEnding":w["orderEnding"],
    },ensure_ascii=False).replace("<","\\u003c")
    return f'''<section class="rose-builder-section" id="rose-bouquet-builder" data-lang="{lang}">
<div class="container"><div class="rose-builder-header">
<span class="rose-bloom-ornament" aria-hidden="true">{ROSE_SVG}</span>
<span class="eyebrow">{escape(w["eyebrow"])}</span>
<h2>{escape(w["title"])}</h2><p>{escape(w["intro"])}</p></div>
<div class="rose-builder-layout">
<form class="rose-builder-form" autocomplete="off">
<fieldset class="rose-builder-fieldset"><legend>{escape(w["flower"])}</legend>
<div class="rose-builder-options">{choices("rose-flower",w["flowerchoices"])}</div></fieldset>
<fieldset class="rose-builder-fieldset"><legend>{escape(w["color"])}</legend>
<div class="rose-builder-options rose-builder-colours">{choices("rose-color",w["colorchoices"],"swatches")}</div></fieldset>
<div class="rose-builder-fieldset"><label class="rose-builder-label" for="rose-count">{escape(w["count"])}</label>
<select class="rose-builder-count" id="rose-count" name="rose-count">{counts}</select></div>
<fieldset class="rose-builder-fieldset"><legend>{escape(w["wrap"])}</legend>
<div class="rose-builder-options">{choices("rose-wrap",w["wrapchoices"])}</div></fieldset>
<div><label class="rose-builder-label" for="rose-note">{escape(w["note"])}</label>
<textarea class="rose-builder-note" name="rose-note" id="rose-note" maxlength="280" placeholder="{escape(w["placeholder"],quote=True)}"></textarea></div>
</form><aside class="rose-builder-preview" aria-live="off">
<h3>{escape(w["preview"])}</h3><div class="rose-builder-stage" aria-label="{escape(w["preview"],quote=True)}"></div>
<p class="rose-builder-previewnote">{escape(w["previewnote"])}</p>
<h4>{escape(w["summary"])}</h4><p class="rose-builder-summary" aria-live="polite"></p>
<a class="button btn-burgundy rose-builder-order" href="https://wa.me/37433081898" target="_blank" rel="noopener noreferrer">{escape(w["button"])}</a>
<p class="rose-builder-disclaimer">{escape(w["disclaimer"])}</p></aside>
</div><script class="rose-builder-words" type="application/json">{data}</script>
</div></section>'''

def add_bloom_marks(html):
    # Titles in the main sections, story, about and article pages; decor is aria-hidden.
    def decorate(m):
        opening=m.group(1)
        if 'rose-bloom-ornament' in opening:
            return opening
        return opening+'<span class="rose-bloom-ornament" aria-hidden="true">'+ROSE_SVG+'</span>'
    html=re.sub(r'(<div class="section-head(?: [^"]*)?">)',decorate,html)
    html=re.sub(r'(<div class="spotlight-copy">)',decorate,html)
    html=re.sub(r'(<section class="page-intro"><div class="container">)',decorate,html)
    html=re.sub(r'(<section class="article-hero container">)',decorate,html)
    return html

(assets/"rose-experience.css").write_text(CSS+"\n",encoding="utf-8")
(assets/"rose-experience.js").write_text(JS+"\n",encoding="utf-8")
counts={}
for lang,w in LANG.items():
    files=list((root/lang).rglob("*.html"))
    assert files, f"No {lang} pages"
    changed=0
    for file in files:
        html=file.read_text(encoding="utf-8")
        assert "rose-experience.js" not in html, f"Duplicate install: {file}"
        assert "</head>" in html and "</body>" in html, file
        html=add_bloom_marks(html)
        builderlink=f"/rose-and-co/{lang}/#rose-bouquet-builder"
        menu=f'<a class="nav-link rose-builder-nav" href="{builderlink}">{escape(w["nav"])}</a>'
        # Add an accessible entry point on all translated pages.
        for cls in ("desktop-nav","mobile-menu"):
            pattern=r'(<nav\b[^>]*class="'+cls+r'"[^>]*>.*?)(</nav>)'
            html,n=re.subn(pattern,lambda m:m.group(1)+menu+m.group(2),html,count=1,flags=re.S)
            assert n==1, f"Missing {cls} in {file}"
        # Homepage: real builder section + discovery link in opening hero.
        if file == root/lang/"index.html":
            assert '<section class="about-spotlight">' in html
            html=html.replace('<section class="about-spotlight">',
                make_builder(lang)+'<section class="about-spotlight">',1)
            hero_pattern=r'(<div class="hero-buttons">.*?)(</div>)'
            hero_a=f'<a class="text-link rose-builder-hero-link" href="#rose-bouquet-builder">{escape(w["nav"])} <span>↗</span></a>'
            html,n=re.subn(hero_pattern,lambda m:m.group(1)+hero_a+m.group(2),html,count=1,flags=re.S)
            assert n==1, f"Missing hero buttons {lang}"
        foot=f'<a class="rose-builder-footer" href="{builderlink}">{escape(w["nav"])} ↗</a>'
        html,n=re.subn(r'(<p class="footer-quote">.*?</p>)',lambda m:m.group(1)+foot,html,count=1,flags=re.S)
        assert n==1, f"Missing footer quote in {file}"
        html=html.replace("</head>",
            '<link rel="stylesheet" href="/rose-and-co/assets/rose-experience.css?v=atelier3"/>'
            '<script defer src="/rose-and-co/assets/rose-experience.js?v=atelier3"></script>'
            "</head>",1)
        file.write_text(html,encoding="utf-8")
        changed+=1
    counts[lang]=changed

assert all(v>=6 for v in counts.values())
assert all('id="rose-bouquet-builder"' in (root/lang/"index.html").read_text(encoding="utf-8") for lang in LANG)
print("Rose & Co luxury interactive floral experience:",counts,
      "petals, scroll-opening rose and localized WhatsApp bouquet builder.")
