(()=>{
'use strict';
const REPO='alform-creator/rose-and-co';
const BASE='https://api.github.com/repos/'+REPO+'/contents/';
const LANGS=['hy','ru','en'];
const CATS={romance:'Սիրո փնջեր',wedding:'Հարսանեկան',occasions:'Տոնական',signature:'Հեղինակային',wreaths:'Ծաղկեպսակներ',seasonal:'Սեզոնային',teddies:'Արջուկներ',plush:'Փափուկ խաղալիքներ',sweets:'Քաղցրավենիք'};
const $=id=>document.getElementById(id);
let token='',data=null,configSha='',selectedId=null,selectedReview=null,currentPage='',pendingPhotos=new Map(),loading=false,dirty=false,currentUsername='';
const imgUrl=p=>p&&p.img?'/rose-and-co/assets/images/'+p.img+'.webp?v=adm2':'';
function notice(message,error=false){
 const el=$('banner');el.hidden=false;el.textContent=message;el.classList.toggle('error',error);
 if(!error)setTimeout(()=>{if(el.textContent===message)el.hidden=true},8000);
}
function status(d){
 dirty=d;const p=$('publish');p.disabled=!data||loading||!d;
 p.textContent=loading?'Հրապարակվում է…':d?'Հրապարակել փոփոխությունները':'Փոփոխություններ չկան';
 renderOverview();
}
function renderOverview(){
 if(!data)return;
 $('stat-all').textContent=data.products.length.toLocaleString('en-US');
 $('stat-visible').textContent=data.products.filter(p=>p.enabled!==false).length.toLocaleString('en-US');
 $('stat-priced').textContent=data.products.filter(p=>Number.isInteger(p.price_amd)&&p.price_amd>0).length.toLocaleString('en-US');
 $('stat-reviews').textContent=(data.reviews||[]).filter(r=>r.approved===true).length.toLocaleString('en-US');
}
function text(id,value){const el=$(id);if(el)el.value=value??'';}
function value(id){return ($(id)?.value||'').trim();}
function esc(s){return String(s||'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;','\'':'&#39;'}[c]));}
function bytesOf(str){return new TextEncoder().encode(str);}
function base64(bytes){let s='';for(let i=0;i<bytes.length;i+=8000)s+=String.fromCharCode(...bytes.subarray(i,i+8000));return btoa(s);}
function utf8(base){const raw=atob(base.replace(/\s/g,''));return new TextDecoder().decode(Uint8Array.from(raw,c=>c.charCodeAt(0)));}
async function api(path,opts={}){
 if(!token)throw Error('Անհրաժեշտ է GitHub-ի բանալին։');
 const r=await fetch(BASE+path+(opts.method?'':'?ref=main'),{
  method:opts.method||'GET',
  headers:{Accept:'application/vnd.github+json',Authorization:'Bearer '+token,'X-GitHub-Api-Version':'2022-11-28',
   ...(opts.body?{'Content-Type':'application/json'}:{})},
  body:opts.body?JSON.stringify(opts.body):undefined,
  cache:'no-store'
 });
 if(!r.ok){
  const res=await r.json().catch(()=>({}));
  if(r.status===401||r.status===403)throw Error('GitHub մուտքը մերժվել է։ Ստուգիր token-ի իրավունքը (Contents: Read and write)։');
  if(r.status===409)throw Error('Տվյալները փոխվել են այլ սարքից։ Թարմացրու էջը և կրկին փորձիր։');
  throw Error('GitHub '+r.status+': '+(res.message||'խնդիր առաջացավ'));
 }
 return r.json();
}
function getProduct(){return data?.products.find(p=>p.id===selectedId);}
function genid(){
 let n=1;while(data.products.some(p=>p.id==='RA'+String(n).padStart(3,'0')))n++;
 return 'RA'+String(n).padStart(3,'0');
}
function nav(tab){
 for(const b of document.querySelectorAll('[data-tab]'))b.classList.toggle('current',b.dataset.tab===tab);
 for(const el of document.querySelectorAll('.tab'))el.hidden=el.id!=='tab-'+tab;
 $('page-heading').textContent=({
 overview:'Կառավարման գլխավոր էջ',products:'Ապրանքների կառավարում',settings:'Կայքի կարգավորումներ',
 reviews:'Հաճախորդների կարծիքներ',pages:'Էջերի տեքստեր',help:'Օգնություն'
 })[tab]||'Rose & Co';
}
function renderList(){
 const q=value('product-search').toLocaleLowerCase();
 const list=$('product-items');list.replaceChildren();
 const all=data.products.filter(p=>(p.id+' '+Object.values(p.name||{}).join(' ')).toLocaleLowerCase().includes(q));
 $('product-count').textContent='Գտնվեց '+all.length+' ապրանք · Ընդամենը '+data.products.length;
 for(const p of all){
  const b=document.createElement('button');b.type='button';b.className='item'+(p.id===selectedId?' active':'');
  const i=document.createElement('img');i.alt='';i.loading='lazy';i.src=pendingPhotos.get(p.id)?.url||imgUrl(p);
  const d=document.createElement('div');const title=document.createElement('b'),subtitle=document.createElement('small');
  title.textContent=p.name.hy||p.id;
  subtitle.textContent=p.id+' · '+(p.enabled===false?'Թաքցված · ':'')+(p.price_amd?Number(p.price_amd).toLocaleString('en-US')+' ֏':'Գին չկա');
  d.append(title,subtitle);b.append(i,d);b.addEventListener('click',()=>selectProduct(p.id));
  list.append(b);
 }
}
function selectProduct(id){
 selectedId=id;
 const p=getProduct();
 $('product-fields').hidden=!p;
 $('product-title').textContent=p?'Խմբագրում · '+p.id:'Ընտրիր ապրանք';
 if(!p){renderList();return;}
 const src=pendingPhotos.get(id)?.url||imgUrl(p);
 $('photo-preview').src=src;
 text('product-id',p.id);text('product-cat',p.cat);text('product-price',p.price_amd??'');
 $('product-enabled').checked=p.enabled!==false;
 $('product-featured').checked=!!p.featured;
 for(const l of LANGS){text('name-'+l,p.name[l]);text('desc-'+l,p.desc[l]);}
 renderList();
}
function setFieldsFromProduct(){
 const p=getProduct();if(!p)return;
 p.cat=value('product-cat');
 const raw=value('product-price');
 p.price_amd=raw===''?null:Number(raw);
 p.enabled=$('product-enabled').checked;
 p.featured=$('product-featured').checked;
 for(const l of LANGS){p.name[l]=value('name-'+l);p.desc[l]=value('desc-'+l);}
 status(true);
 renderList();
}
function renderSettings(){
 const s=data.settings||{};
 text('setting-phone',s.phone);text('setting-wa',s.whatsapp);text('setting-instagram',s.instagram);
 text('setting-google-verify',s.google_site_verification||'');
 for(const z of ['zovuni','yerevan','kotayk','other'])text('fee-'+z,s.delivery?.[z]??'');
}
function readSettings(){
 const s=data.settings||(data.settings={});
 s.phone=value('setting-phone');s.whatsapp=value('setting-wa');
 s.instagram=value('setting-instagram');s.google_site_verification=value('setting-google-verify').trim();s.delivery=s.delivery||{};
 for(const z of ['zovuni','yerevan','kotayk','other']){
  const n=value('fee-'+z);s.delivery[z]=n===''?null:Number(n);
 }
 status(true);
}
function renderReviews(){
 const list=$('review-list');list.replaceChildren();
 if(!data.reviews.length){const p=document.createElement('p');p.className='hint';p.textContent='Իրական կարծիքներ դեռ չկան։';list.append(p);}
 data.reviews.forEach((r,i)=>{
  const line=document.createElement('div');line.className='review-row';
  const name=document.createElement('div'),btn=document.createElement('button');
  const strong=document.createElement('strong');strong.textContent=r.name;
  const state=document.createElement('span');state.textContent=r.approved?' · Հաստատված':' · Չհրապարակված';
  name.append(strong,state);btn.type='button';btn.textContent='Խմբագրել';
  btn.addEventListener('click',()=>selectReview(i));line.append(name,btn);list.append(line);
 });
}
function selectReview(i){
 selectedReview=i;
 const r=data.reviews[i];$('review-editor').hidden=!r;if(!r)return;
 text('review-name',r.name);text('review-rating',r.rating||5);
 for(const l of LANGS)text('review-'+l,r.text?.[l]||'');
 $('review-approved').checked=!!r.approved;
}
function updateReview(){
 const r=data.reviews[selectedReview];if(!r)return;
 r.name=value('review-name');r.rating=Number(value('review-rating'))||5;
 r.text=r.text||{};for(const l of LANGS)r.text[l]=value('review-'+l);
 r.approved=$('review-approved').checked;status(true);renderReviews();
}
function pageKeyFromUrl(url){
 try{
  const path=new URL(url).pathname.replace(/^\/rose-and-co\//,'');
  if(!/^(hy|ru|en)\//.test(path))return '';
  return path.endsWith('/')?path+'index.html':path;
 }catch{return '';}
}
async function loadPages(){
 let paths=[];
 try{
  const r=await fetch('/rose-and-co/sitemap.xml?v=admin', {cache:'no-store'});
  if(r.ok){
    const xml=new DOMParser().parseFromString(await r.text(),'text/xml');
    paths=Array.from(xml.getElementsByTagName('loc'),x=>pageKeyFromUrl(x.textContent)).filter(Boolean);
  }
 }catch{}
 if(paths.length===0)paths=['hy/index.html','ru/index.html','en/index.html'];
 for(const x of Object.keys(data.pages||{}))if(!paths.includes(x))paths.push(x);
 const sel=$('page-select');sel.replaceChildren();
 for(const path of paths){const option=document.createElement('option');option.value=path;option.textContent=path.replace('/index.html','/');sel.append(option);}
 currentPage=sel.value||paths[0];renderPage();
}
function renderPage(){
 currentPage=$('page-select').value;
 const x=data.pages?.[currentPage]||{};
 for(const k of ['h1','title','description','intro'])text('page-'+k,x[k]||'');
}
function updatePage(){
 const obj={};for(const k of ['h1','title','description','intro']){const v=value('page-'+k);if(v)obj[k]=v;}
 if(!data.pages)data.pages={};
 if(Object.keys(obj).length)data.pages[currentPage]=obj;
 else delete data.pages[currentPage];
 status(true);
}
async function processImage(file,id){
 if(!file||!file.type.startsWith('image/'))throw Error('Ընտրիր նկար՝ JPG, PNG կամ WEBP։');
 if(file.size>10*1024*1024)throw Error('Նկարի չափը չի կարող գերազանցել 10 ՄԲ։');
 const image=await createImageBitmap(file);
 let width=image.width,height=image.height;
 const ratio=Math.min(1,1200/width,1500/height);
 width=Math.max(1,Math.round(width*ratio));height=Math.max(1,Math.round(height*ratio));
 const canvas=document.createElement('canvas');canvas.width=width;canvas.height=height;
 const ctx=canvas.getContext('2d');ctx.drawImage(image,0,0,width,height);
 image.close?.();
 const blob=await new Promise((resolve,reject)=>canvas.toBlob(b=>b?resolve(b):reject(Error('Նկարը մշակել չհաջողվեց')),'image/webp',.84));
 const array=new Uint8Array(await blob.arrayBuffer());
 if(array.byteLength>1.9*1024*1024)throw Error('Նկարը չափազանց մեծ է նույնիսկ սեղմելուց հետո։');
 const fileBase=id+'-'+Date.now();
 const name='admin/'+fileBase;
 const existing=pendingPhotos.get(id);
 if(existing)URL.revokeObjectURL(existing.url);
 const url=URL.createObjectURL(blob);
 pendingPhotos.set(id,{name,content:base64(array),url});
 const p=data.products.find(x=>x.id===id);if(p)p.img=name;
 if(selectedId===id)$('photo-preview').src=url;
 status(true);renderList();notice('Նկարը պատրաստ է։ Հրապարակելիս այն կտեղադրվի GitHub-ում։');
}
const VAULT_KEY='rose_co_admin_encrypted_v1';
const encoder=new TextEncoder();
const decoder=new TextDecoder();
function renderAuth(){
 const stored=localStorage.getItem(VAULT_KEY);
 $('vault-login').hidden=!stored;
 $('vault-setup').hidden=!!stored;
 $('login-error').hidden=true;
}
function validateVault(raw){
 if(typeof raw!=='string'||raw.length>20000)throw Error('Մուտքի ֆայլը չափազանց մեծ է։');
 const v=JSON.parse(raw);
 if(v.v!==1||!['salt','iv','data'].every(k=>typeof v[k]==='string'&&/^[A-Za-z0-9+/]+={0,2}$/.test(v[k])))throw Error('Սա Rose & Co-ի մուտքի ֆայլ չէ։');
 if(atob(v.salt).length!==16||atob(v.iv).length!==12||atob(v.data).length<32)throw Error('Մուտքի ֆայլը վնասված է։');
 return JSON.stringify({v:1,salt:v.salt,iv:v.iv,data:v.data});
}
function exportVault(){
 try{
  const raw=validateVault(localStorage.getItem(VAULT_KEY));
  const blob=new Blob([raw],{type:'application/json'}),url=URL.createObjectURL(blob);
  const a=document.createElement('a');a.href=url;a.download='RoseCo-encrypted-access.json';a.click();
  setTimeout(()=>URL.revokeObjectURL(url),1000);
  notice('Մուտքի գաղտնագրված ֆայլը պատրաստ է։ Նոր սարքում այն բացելու համար պետք է քո լոգինն ու գաղտնաբառը։');
 }catch(e){notice(e.message,true);}
}
async function importVault(event){
 const file=event.target.files?.[0];if(!file)return;
 try{
  if(file.size>20000)throw Error('Մուտքի ֆայլը չափազանց մեծ է։');
  const raw=validateVault(await file.text());
  if(dirty&&!confirm('Չհրապարակված փոփոխությունները կկորչեն։ Շարունակե՞լ։'))return;
  if(localStorage.getItem(VAULT_KEY)&&!confirm('Փոխարինե՞լ այս սարքում պահված մուտքը ներմուծվող ֆայլով։'))return;
  localStorage.setItem(VAULT_KEY,raw);dirty=false;disconnect();renderAuth();
  notice('Մուտքը ներմուծված է։ Օգտագործիր նույն լոգինն ու գաղտնաբառը։');
  $('login-user').focus();
 }catch(e){notice('Ֆայլը ներմուծել չհաջողվեց․ '+e.message,true);}
 finally{event.target.value='';}
}
async function derivePasswordKey(password,salt){
 const keyMaterial=await crypto.subtle.importKey('raw',encoder.encode(password),'PBKDF2',false,['deriveKey']);
 return crypto.subtle.deriveKey({name:'PBKDF2',hash:'SHA-256',iterations:480000,salt},
  keyMaterial,{name:'AES-GCM',length:256},false,['encrypt','decrypt']);
}
async function makeVault(username,password,secret){
 const salt=crypto.getRandomValues(new Uint8Array(16));
 const iv=crypto.getRandomValues(new Uint8Array(12));
 const key=await derivePasswordKey(password,salt);
 const plaintext=encoder.encode(JSON.stringify({username,token:secret,version:1}));
 const encrypted=new Uint8Array(await crypto.subtle.encrypt({name:'AES-GCM',iv},key,plaintext));
 return JSON.stringify({v:1,salt:base64(salt),iv:base64(iv),data:base64(encrypted)});
}
async function readVault(username,password){
 const raw=localStorage.getItem(VAULT_KEY);if(!raw)throw Error('Այս սարքում հաշիվ դեռ կարգավորված չէ։');
 const stored=JSON.parse(raw);
 if(stored.v!==1||!stored.salt||!stored.iv||!stored.data)throw Error('Անվավեր մուտքի տվյալներ։');
 const salt=Uint8Array.from(atob(stored.salt),c=>c.charCodeAt(0));
 const iv=Uint8Array.from(atob(stored.iv),c=>c.charCodeAt(0));
 const encrypted=Uint8Array.from(atob(stored.data),c=>c.charCodeAt(0));
 const key=await derivePasswordKey(password,salt);
 const bytes=await crypto.subtle.decrypt({name:'AES-GCM',iv},key,encrypted);
 const result=JSON.parse(decoder.decode(bytes));
 if(result.username!==username||typeof result.token!=='string'||result.version!==1)
  throw Error('Սխալ լոգին կամ գաղտնաբառ։');
 return result.token;
}
async function connectWithToken(candidate){
 token=candidate;
 try{
  const doc=await api('.github/admin-data.json');
  data=JSON.parse(utf8(doc.content));configSha=doc.sha;
  if(data.schema!==1||!Array.isArray(data.products))throw Error('Ադմին տվյալների ֆայլի ձևաչափը սխալ է։');
  data.reviews=data.reviews||[];data.pages=data.pages||{};
  $('auth').hidden=true;$('workspace').hidden=false;
  $('connection').textContent='Միացված է';$('connection').classList.remove('offline');
  renderList();selectProduct(data.products[0]?.id);
  renderSettings();renderReviews();await loadPages();
  status(false);notice('Մուտքն հաջողվեց։ Կարող ես խմբագրել կայքը։');
 }catch(e){token='';data=null;throw e;}
}
async function setupAccount(event){
 event.preventDefault();
 const username=value('setup-user');
 const password=$('setup-password').value;
 const confirmPassword=$('setup-confirm').value;
 const candidate=value('setup-token');
 const button=$('setup-save');
 if(username.length<3||username.length>60||!(/^[\p{L}\p{N}_.-]+$/u.test(username))){notice('Լոգինը պետք է լինի 3–60 նիշ՝ տառեր, թվեր, կետ, գծիկ կամ ներքևի գծիկ։',true);return;}
 if(password.length<12||password.length>128){notice('Ընտրիր առնվազն 12 նիշից բաղկացած գաղտնաբառ։',true);return;}
 if(password!==confirmPassword){notice('Գաղտնաբառերը չեն համընկնում։',true);return;}
 if(!candidate){notice('Առաջին անգամ անհրաժեշտ է GitHub-ի բանալին։',true);return;}
 button.disabled=true;
 try{
   await connectWithToken(candidate);
   const vault=await makeVault(username,password,candidate);
   localStorage.setItem(VAULT_KEY,vault);
   $('setup-token').value='';$('setup-password').value='';$('setup-confirm').value='';
   currentUsername=username;
   renderAuth();
   notice('Մուտքը կարգավորված է։ Օգնություն բաժնից ներբեռնիր գաղտնագրված մուտքի ֆայլը՝ նոր սարքում նույն գաղտնաբառով աշխատելու համար։');
 }catch(e){notice('Կարգավորումը չհաջողվեց․ '+e.message,true);}
 finally{button.disabled=false;}
}
async function signIn(event){
 event.preventDefault();
 const username=value('login-user');
 const password=$('login-password').value;
 const button=$('login-submit');button.disabled=true;
 try{
   const candidate=await readVault(username,password);
   await connectWithToken(candidate);
   currentUsername=username;
   $('login-password').value='';
 }catch(e){
   notice('Մուտքը չհաջողվեց։ Ստուգիր լոգինը, գաղտնաբառը կամ GitHub-ի բանալու գործողությունը։',true);
 }finally{button.disabled=false;}
}
function validate(){
 if(data.products.length===0)throw Error('Կատալոգը չի կարող դատարկ լինել։');
 const ids=new Set();
 for(const p of data.products){
  if(!/^[A-Za-z0-9_-]{2,20}$/.test(p.id)||ids.has(p.id))throw Error('Սխալ կամ կրկնվող ապրանքի համար՝ '+p.id);
  ids.add(p.id);
  if(!CATS[p.cat])throw Error('Անհայտ կատեգորիա՝ '+p.id);
  if(!/^(real-2026|rose50|admin)\/[A-Za-z0-9_-]+$/.test(p.img))throw Error('Նկար չի ընտրված՝ '+p.id);
  if(p.price_amd!==null&&(!Number.isInteger(p.price_amd)||p.price_amd<=0||p.price_amd>100000000))throw Error('Սխալ գին՝ '+p.id);
  for(const l of LANGS)if(!(p.name?.[l]||'').trim())throw Error('Բացակայում է ապրանքի անվանումը՝ '+p.id+' / '+l);
 }
 if(data.products.every(p=>p.enabled===false))throw Error('Առնվազն մեկ ապրանք պետք է տեսանելի լինի։');
 if(!/^\+?\d{7,15}$/.test(data.settings.phone))throw Error('Հեռախոսահամարը սխալ է։');
 if(!/^\d{7,15}$/.test(data.settings.whatsapp))throw Error('WhatsApp համարը սխալ է։');
 if(!data.settings.instagram.startsWith('https://www.instagram.com/'))throw Error('Instagram հղումը սխալ է։');
 if(data.settings.google_site_verification&&!/^[A-Za-z0-9_-]{10,160}$/.test(data.settings.google_site_verification))throw Error('Google verification կոդը սխալ է։ Պետք է տեղադրել միայն content-ի արժեքը։');
 for(const z of Object.values(data.settings.delivery||{}))if(z!==null&&(!Number.isInteger(z)||z<0))throw Error('Առաքման գինը սխալ է։');
 for(const r of data.reviews)if(r.approved&&(!r.name||LANGS.some(l=>!r.text?.[l])))throw Error('Հաստատված կարծիքն անվանում և երեք լեզվի տեքստ պետք է ունենա։');
}
async function publish(){
 if(!data||loading)return;
 try{validate();}catch(e){notice(e.message,true);return;}
 if(!confirm('Հրապարակե՞լ բոլոր փոփոխությունները Rose & Co կայքում։'))return;
 loading=true;status(true);
 try{
  for(const [id,photo] of pendingPhotos){
   if(photo.uploaded)continue;
   $('publish').textContent='Նկարի ներբեռնում՝ '+id+'…';
   await api('.github/admin-media/'+photo.name.slice('admin/'.length)+'.webp',{
    method:'PUT',
    body:{message:'Rose & Co admin: upload '+id+' product photo',content:photo.content,branch:'main'}
   });
   photo.uploaded=true;
  }
  $('publish').textContent='Տվյալների պահպանում…';
  const updated=await api('.github/admin-data.json',{method:'PUT',
   body:{message:'Rose & Co admin: update catalog and storefront settings',
   content:base64(bytesOf(JSON.stringify(data,null,2)+'\n')),
   sha:configSha,branch:'main'}
  });
  configSha=updated.content?.sha||configSha;
  for(const photo of pendingPhotos.values())URL.revokeObjectURL(photo.url);
  pendingPhotos.clear();
  loading=false;status(false);selectProduct(selectedId);notice('Պահպանվեց GitHub-ում։ Կայքը թարմացվում է GitHub Actions-ի միջոցով։');
 }catch(e){loading=false;status(true);notice('Պահպանել չհաջողվեց․ '+e.message,true);}
}
function disconnect(){
 token='';data=null;configSha='';selectedId=null;loading=false;currentUsername='';
 for(const v of pendingPhotos.values())URL.revokeObjectURL(v.url);
 pendingPhotos.clear();$('workspace').hidden=true;$('auth').hidden=false;
 $('connection').textContent='Չմիացված';$('connection').classList.add('offline');
 $('banner').hidden=true;text('login-password','');renderAuth();status(false);
}
async function changeDevicePassword(event){
 event.preventDefault();
 if(!token||!currentUsername){notice('Կրկին մուտք գործիր և փորձիր փոխել գաղտնաբառը։',true);return;}
 const oldPassword=$('old-password').value;
 const nextPassword=$('new-password').value;
 const confirmed=$('confirm-new-password').value;
 if(nextPassword.length<12||nextPassword.length>128){notice('Նոր գաղտնաբառը պետք է լինի առնվազն 12 նիշ։',true);return;}
 if(nextPassword!==confirmed){notice('Նոր գաղտնաբառերը չեն համընկնում։',true);return;}
 const form=$('change-password-form');
 const button=form.querySelector('button[type=submit]');button.disabled=true;
 try{
  const unlocked=await readVault(currentUsername,oldPassword);
  if(unlocked!==token)throw Error('Այս սարքի հաշիվը չի համապատասխանում ընթացիկ մուտքին։');
  localStorage.setItem(VAULT_KEY,await makeVault(currentUsername,nextPassword,unlocked));
  form.reset();
  notice('Նոր գաղտնաբառը պահպանվեց այս սարքի համար։');
 }catch(e){notice('Գործող գաղտնաբառը սխալ է կամ տվյալները վնասվել են։',true);}
 finally{button.disabled=false;}
}
for(const btn of document.querySelectorAll('[data-tab]'))btn.addEventListener('click',()=>nav(btn.dataset.tab));
$('vault-import').addEventListener('change',importVault);
$('vault-export').addEventListener('click',exportVault);
$('setup-form').addEventListener('submit',setupAccount);
$('login-form').addEventListener('submit',signIn);
$('reset-vault').addEventListener('click',()=>{
 if(confirm('Այս սարքի գաղտնագրված մուտքի տվյալները մաքրե՞լ։ Դրանք վերականգնելու համար կրկին պետք կլինի GitHub-ի բանալին։')){
  localStorage.removeItem(VAULT_KEY);
  disconnect();
  renderAuth();
 }
});
$('publish').addEventListener('click',publish);
$('disconnect').addEventListener('click',disconnect);
$('change-password-form').addEventListener('submit',changeDevicePassword);
for(const link of document.querySelectorAll('[data-goto]'))link.addEventListener('click',()=>nav(link.dataset.goto));
$('quick-new-product').addEventListener('click',()=>{
 nav('products');$('add-product').click();
});
$('product-search').addEventListener('input',renderList);
const cat=$('product-cat');for(const [id,name] of Object.entries(CATS)){const opt=document.createElement('option');opt.value=id;opt.textContent=name;cat.append(opt);}
$('product-form').addEventListener('submit',e=>e.preventDefault());
for(const id of ['product-cat','product-price','product-enabled','product-featured',...LANGS.flatMap(l=>['name-'+l,'desc-'+l])]){
 $(id).addEventListener('input',setFieldsFromProduct);$(id).addEventListener('change',setFieldsFromProduct);
}
$('add-product').addEventListener('click',()=>{
 const id=genid();data.products.unshift({id,img:'',cat:'romance',
  name:{hy:'Նոր ծաղկեփունջ',ru:'Новый букет',en:'New bouquet'},
  desc:{hy:'',ru:'',en:''},price_amd:null,enabled:false,featured:false
 });selectedId=id;selectProduct(id);status(true);
 notice('Նոր ապրանքն ավելացվել է։ Ընտրիր նկար և լրացրու անունները։');
});
$('remove-product').addEventListener('click',()=>{
 const p=getProduct();if(!p||!confirm('Հեռացնե՞լ '+p.id+' ապրանքը։'))return;
 data.products=data.products.filter(x=>x.id!==p.id);
 const pending=pendingPhotos.get(p.id);if(pending)URL.revokeObjectURL(pending.url);
 pendingPhotos.delete(p.id);selectProduct(data.products[0]?.id);status(true);
});
$('photo-input').addEventListener('change',async e=>{
 const file=e.target.files?.[0],p=getProduct();if(!file||!p)return;
 try{await processImage(file,p.id);}catch(err){notice(err.message,true);}
 e.target.value='';
});
$('settings-form').addEventListener('input',readSettings);
$('settings-form').addEventListener('change',readSettings);
$('add-review').addEventListener('click',()=>{
 data.reviews.push({name:'',rating:5,text:{hy:'',ru:'',en:''},approved:false});
 selectReview(data.reviews.length-1);renderReviews();status(true);
});
for(const id of ['review-name','review-rating','review-approved',...LANGS.map(l=>'review-'+l)]){
 $(id).addEventListener('input',updateReview);$(id).addEventListener('change',updateReview);
}
$('review-delete').addEventListener('click',()=>{
 if(selectedReview===null||!confirm('Ջնջե՞լ այս կարծիքը։'))return;
 data.reviews.splice(selectedReview,1);selectedReview=null;$('review-editor').hidden=true;renderReviews();status(true);
});
$('page-select').addEventListener('change',renderPage);
for(const id of ['page-h1','page-title','page-description','page-intro'])$(id).addEventListener('input',updatePage);
window.addEventListener('beforeunload',e=>{if(dirty){e.preventDefault();e.returnValue='';}});
renderAuth();nav('overview');status(false);
})();