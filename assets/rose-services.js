(()=>{
"use strict";
const hub=document.getElementById("rose-service-hub");if(!hub)return;
const t=JSON.parse(hub.querySelector("#rs-words").textContent);
const data=JSON.parse(hub.querySelector("#rs-data").textContent);
const lang=hub.dataset.lang;
const number=(window.ROSE_CONTACT&&window.ROSE_CONTACT.whatsapp)||"37433081898";
const value=(form,name)=>String(form.elements.namedItem(name).value||"").trim();
const line=(name,v)=>name+": "+v;
function send(lines){
 const u="https://wa.me/"+number+"?text="+encodeURIComponent(lines.filter(Boolean).join("\n"));
 window.open(u,"_blank","noopener,noreferrer");
}
const letter=hub.querySelector("#rs-letter-form"),env=hub.querySelector("#rs-envelope");
function updateLetter(){
 hub.querySelector("#rs-preview-to").textContent=value(letter,"recipient")||t.recipientPlaceholder;
 hub.querySelector("#rs-preview-letter").textContent=value(letter,"letter")||t.letterEmpty;
 hub.querySelector("#rs-preview-from").textContent=value(letter,"sender");
}
letter.addEventListener("input",updateLetter);updateLetter();
hub.querySelector(".rs-envelope-toggle").addEventListener("click",function(){
 const expanded=env.classList.toggle("open");this.setAttribute("aria-expanded",String(expanded));
});
hub.querySelector("#rs-letter-send").addEventListener("click",()=>{
 if(!letter.reportValidity())return;
 send([t.letterHello,line(t.recipient,value(letter,"recipient")),line(t.letterStyle,t.letterStyles[Number(value(letter,"letterstyle"))]),
 line(t.message,value(letter,"letter")),value(letter,"sender")?line(t.sender,value(letter,"sender")):"",t.contactEnd]);
});
hub.querySelector("#rs-letter-bouquet").addEventListener("click",()=>{
 if(!letter.reportValidity())return;
 const dest=document.querySelector('#rose-bouquet-builder [name="rose-note"]');
 if(dest){dest.value=[value(letter,"recipient"),value(letter,"letter"),value(letter,"sender")].filter(Boolean).join(" — ").slice(0,280);dest.dispatchEvent(new Event("input",{bubbles:true}));dest.scrollIntoView({behavior:"smooth",block:"center"});dest.focus({preventScroll:true});}
});
const sur=hub.querySelector("#rs-surprise-form"),date=sur.elements.namedItem("date");
function today(){const d=new Date();return [d.getFullYear(),String(d.getMonth()+1).padStart(2,"0"),String(d.getDate()).padStart(2,"0")].join("-");}
date.min=today();
date.addEventListener("change",()=>date.setCustomValidity(""));
hub.querySelector("#rs-surprise-send").addEventListener("click",()=>{
 date.min=today();if(!sur.reportValidity())return;
 if(value(sur,"date")<today()){date.setCustomValidity(t.date);date.reportValidity();return;}
 date.setCustomValidity("");
 send([t.surpriseHello,line(t.recipient,value(sur,"recipient")),
 value(sur,"phone")?line(t.phone,value(sur,"phone")):"",
 line(t.address,value(sur,"address")),line(t.date,value(sur,"date")),
 line(t.time,t.times[Number(value(sur,"time"))]),
 value(sur,"instructions")?line(t.instructions,value(sur,"instructions")):"",t.contactEnd]);
});
const quiz=hub.querySelector("#rs-quiz-form");
hub.querySelector("#rs-quiz-send").addEventListener("click",()=>{
 if(!quiz.reportValidity())return;
 const occasion=Number(value(quiz,"occasion")),colour=Number(value(quiz,"colour"));
 let index=occasion===0?0:occasion===1?1:occasion===2?2:3;
 if(occasion===3&&colour===0)index=0;
 const cats=["romance","occasions","wedding","signature"];
 hub.querySelector("#rs-recommend").textContent=t.results[index];
 hub.querySelector("#rs-catalog").href="/rose-and-co/"+lang+"/catalog/?category="+cats[index];
 const r=hub.querySelector("#rs-quiz-result");r.hidden=false;r.scrollIntoView({behavior:"smooth",block:"nearest"});
});
const dl=hub.querySelector("#rs-delivery-form"),zone=dl.elements.namedItem("zone");
function updateFee(){
 const item=data.delivery_zones.find(z=>z.id===zone.value);
 hub.querySelector("#rs-fee").textContent=(item&&typeof item.fee_amd==="number")?
 t.feeKnown+" "+new Intl.NumberFormat(lang==="hy"?"hy-AM":lang==="ru"?"ru-RU":"en-US").format(item.fee_amd)+" ֏":t.feeUnknown;
}
zone.addEventListener("change",updateFee);updateFee();
hub.querySelector("#rs-delivery-send").addEventListener("click",()=>{
 const item=data.delivery_zones.find(z=>z.id===zone.value);
 send([t.feeHello,line(t.zone,item?item.label[lang]:""),value(dl,"address")?line(t.address,value(dl,"address")):"",t.contactEnd]);
});
const sampleRail=hub.querySelector(".rs-sample-grid");
if(sampleRail){
 hub.querySelectorAll(".rs-sample-arrow").forEach(btn=>{
  btn.addEventListener("click",()=>{
   const dir=Number(btn.dataset.rsScroll)||1;
   const card=sampleRail.querySelector(".rs-sample-card");
   const gap=parseFloat(getComputedStyle(sampleRail).columnGap)||14;
   const distance=card?card.getBoundingClientRect().width+gap:290;
   sampleRail.scrollBy({left:dir*distance,behavior:window.matchMedia("(prefers-reduced-motion: reduce)").matches?"auto":"smooth"});
  });
 });
}
const reviews=hub.querySelector("#rs-reviews-list");
const approved=(data.reviews||[]).filter(r=>r.approved===true&&r.quote&&r.name);
if(approved.length){
 reviews.replaceChildren();
 approved.slice(0,12).forEach(r=>{
  const quote=r.quote[lang]||r.quote.hy;if(!quote)return;
  const el=document.createElement("blockquote");el.className="rs-review";
  const stars=document.createElement("span");stars.className="rs-stars";
  const rating=Math.max(1,Math.min(5,Number(r.rating)||5));stars.textContent="★".repeat(rating)+"☆".repeat(5-rating);
  const p=document.createElement("p");p.textContent=quote;
  const name=document.createElement("strong");name.textContent=r.name;
  el.append(stars,p,name);reviews.appendChild(el);
 });
}
const review=hub.querySelector("#rs-review-form");
hub.querySelector("#rs-review-send").addEventListener("click",()=>{
 if(!review.reportValidity())return;
 send([t.reviewHello,line(t.name,value(review,"name")),
 line(t.rating,["5","4","3","2","1"][Number(value(review,"rating"))]),
 line(t.reviewMessage,value(review,"review")),
 line(t.permission,review.elements.namedItem("permission").checked?t.yes:t.no)]);
});
})();
