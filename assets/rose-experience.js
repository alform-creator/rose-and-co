(() => {
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
})();
