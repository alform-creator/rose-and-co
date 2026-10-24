#!/usr/bin/env python3
"""Rose & Co: five honest, interactive gift tools on the three-language static shop."""
from pathlib import Path
from html import escape
import json, re, sys

root=Path(sys.argv[1]).resolve()
assets=root/"assets"
data=json.loads(Path(".github/rose-services-data.json").read_text(encoding="utf-8"))
assert data["version"]==1
assert data["delivery_zones"]
assert all(z["fee_amd"] is None or (isinstance(z["fee_amd"],int) and z["fee_amd"]>=0) for z in data["delivery_zones"])
assert all(r.get("approved") is True for r in data["reviews"])

COPY={
"hy":{
"nav":"Նվերներ և առաքում","title":"Մի փոքր ավելի շատ սեր","intro":"Սիրային նամակ, անակնկալ առաքում և անհատական ծաղկեփունջ․ ամեն բան մեկ վայրում։",
"tabs":["Սիրային նամակ","Անակնկալ առաքում","Օգնիր ընտրել","Առաքման հաշվիչ","Կարծիքներ"],
"titles":["Գաղտնի սիրային նամակ","Անակնկալ առաքում","Օգնիր ինձ ընտրել","Առաքման հաշվիչ","Հաճախորդների կարծիքներ"],
"descs":["Ստեղծիր նամակ, ընտրիր ձևավորումը և կցիր ծաղկեփնջի պատվերին։","Նշիր ցանկալի օրը, ժամը և հասցեն․ առաքման հնարավորությունը կհաստատենք անձամբ։","Պատասխանիր 3 հարցի՝ ծաղկեփնջի համապատասխան ուղղությունը գտնելու համար։","Ընտրիր բնակավայրը․ եթե հաստատված սակագին կա, այն կցուցադրվի։","Կարծիքները հրապարակվում են միայն ստուգումից և հեղինակի համաձայնությունից հետո։"],
"recipient":"Ստացողի անուն","recipientPlaceholder":"Ում ես նվիրում","sender":"Քո անունը (ըստ ցանկության)","message":"Նամակի տեքստ","msgPlaceholder":"Գրիր քո սիրելի խոսքերը…","letterStyle":"Նամակի ձևը","letterStyles":["Դասական","Ռոմանտիկ","Նուրբ"],
"letterPreview":"Քո նամակի նախադիտումը","letterEmpty":"Քո նամակը կհայտնվի այստեղ…","envelope":"Բացել / փակել նամակը","letterSend":"Ուղարկել նամակը ↗","letterBouquet":"Ավելացնել ծաղկեփնջին ↗",
"phone":"Ստացողի հեռախոս (ըստ ցանկության)","address":"Առաքման հասցե","addressPlaceholder":"Բնակավայր, փողոց, տուն","date":"Նախընտրելի ամսաթիվ","time":"Նախընտրելի ժամային հատված","times":["Առավոտ","Ցերեկ","Երեկո"],"instructions":"Անակնկալի մանրամասներ (ըստ ցանկության)","surpriseSend":"Ուղարկել անակնկալի հարցումը ↗",
"occasion":"Ի՞նչ առիթով","occasions":["Սիրելիիս համար","Ծննդյան օր / տոն","Հարսանիք","Ուղղակի ուրախացնելու համար"],"colour":"Գունապնակ","colours":["Կարմիր","Վարդագույն","Սպիտակ","Գունավոր"],"style":"Ոճ","styles":["Դասական","Շքեղ","Նուրբ"],"quizSend":"Ընտրել ծաղկեփունջը","recommend":"Քեզ խորհուրդ ենք տալիս","results":["Ռոմանտիկ վարդեր","Տոնական ծաղկեփունջ","Հարսանեկան սպիտակ փունջ","Հեղինակային ծաղկեփունջ"],"catalog":"Դիտել կատալոգում ↗","builder":"Ստեղծել անհատական փունջ ↗",
"zone":"Առաքման տարածք","fee":"Առաքման մոտավոր արժեք","feeUnknown":"Գինը ճշտվում է անհատապես","feeKnown":"Սահմանված արժեք՝","feeNote":"Միայն հաստատված սակագներն են ցուցադրվում։ Հասանելիությունը և վերջնական գինը հաստատվում են պատվերի ժամանակ։","feeSend":"Ճշտել առաքման արժեքը ↗",
"reviewsEmpty":"Դեռ հրապարակված, հաստատված կարծիքներ չկան։ Կարող ես առաջիններից լինել։","name":"Քո անունը","rating":"Գնահատական","reviewMessage":"Քո կարծիքը","reviewPlaceholder":"Պատմիր քո փորձից…","permission":"Թույլ եմ տալիս ստուգումից հետո հրապարակել իմ կարծիքն ու անունը։","reviewSend":"Ուղարկել կարծիք WhatsApp-ով ↗","reviewNote":"Կարծիքներն ավտոմատ չեն հրապարակվում, և տվյալները կայքում չեն պահպանվում։",
"disclaimer":"Հարցումը չի հաստատում պատվերը, գինը կամ առաքման ժամը։","contactEnd":"Խնդրում եմ ճշտել հնարավորությունը և վերջնական արժեքը։",
"letterHello":"Բարև, ուզում եմ ծաղկեփնջին ավելացնել նամակ։","surpriseHello":"Բարև, ուզում եմ պատվիրել անակնկալ առաքում։","feeHello":"Բարև, ուզում եմ ճշտել ծաղիկների առաքման արժեքը։","reviewHello":"Բարև, ուզում եմ թողնել կարծիք Rose & Co-ի մասին։","yes":"այո","no":"ոչ"
},
"ru":{
"nav":"Подарки и доставка","title":"Чуть больше любви","intro":"Письмо, сюрприз и индивидуальный букет — всё для особенного момента.",
"tabs":["Любовное письмо","Сюрприз","Помочь выбрать","Доставка","Отзывы"],"titles":["Тайное любовное письмо","Доставка-сюрприз","Помогите мне выбрать","Расчёт доставки","Отзывы покупателей"],
"descs":["Составьте письмо и обсудите его оформление вместе с букетом.","Укажите желаемую дату, время и адрес — возможность доставки подтвердим лично.","Ответьте на три вопроса, чтобы подобрать направление.","Выберите район, чтобы увидеть подтверждённую стоимость или запросить расчёт.","Публикуем лишь реальные отзывы с разрешения автора."],
"recipient":"Имя получателя","recipientPlaceholder":"Кому букет","sender":"Ваше имя (необязательно)","message":"Текст письма","msgPlaceholder":"Напишите от сердца…","letterStyle":"Оформление","letterStyles":["Классика","Романтика","Нежное"],
"letterPreview":"Предпросмотр письма","letterEmpty":"Ваше письмо появится здесь…","envelope":"Открыть / закрыть письмо","letterSend":"Отправить письмо ↗","letterBouquet":"Добавить к букету ↗",
"phone":"Телефон получателя (необязательно)","address":"Адрес доставки","addressPlaceholder":"Город, улица, дом","date":"Желаемая дата","time":"Часть дня","times":["Утро","День","Вечер"],"instructions":"Пожелания к сюрпризу (необязательно)","surpriseSend":"Отправить запрос ↗",
"occasion":"Повод","occasions":["Любимому человеку","День рождения / праздник","Свадьба","Просто порадовать"],"colour":"Палитра","colours":["Красный","Розовый","Белый","Разноцветный"],"style":"Стиль","styles":["Классика","Роскошный","Нежный"],"quizSend":"Подобрать букет","recommend":"Мы рекомендуем","results":["Романтичные розы","Праздничный букет","Белый свадебный букет","Авторская композиция"],"catalog":"Смотреть в каталоге ↗","builder":"Создать свой букет ↗",
"zone":"Зона доставки","fee":"Ориентировочная доставка","feeUnknown":"Стоимость уточняется индивидуально","feeKnown":"Установленная стоимость:","feeNote":"Отображаем только подтверждённые тарифы. Окончательная цена и возможность доставки согласуются с вами.","feeSend":"Уточнить стоимость ↗",
"reviewsEmpty":"Пока нет опубликованных подтверждённых отзывов. Вы можете оставить первый.","name":"Ваше имя","rating":"Оценка","reviewMessage":"Ваш отзыв","reviewPlaceholder":"Расскажите о своём опыте…","permission":"Разрешаю опубликовать отзыв и моё имя после проверки.","reviewSend":"Отправить отзыв в WhatsApp ↗","reviewNote":"Отзывы не публикуются автоматически; данные на сайте не хранятся.",
"disclaimer":"Запрос не является подтверждением заказа, цены или времени доставки.","contactEnd":"Пожалуйста, уточните возможность и окончательную цену.",
"letterHello":"Здравствуйте! Хочу добавить письмо к букету.","surpriseHello":"Здравствуйте! Хочу доставку-сюрприз.","feeHello":"Здравствуйте! Хочу узнать стоимость доставки.","reviewHello":"Здравствуйте! Хочу оставить отзыв для Rose & Co.","yes":"да","no":"нет"
},
"en":{
"nav":"Gifts & delivery","title":"A little more love","intro":"A heartfelt letter, a surprise and a custom bouquet — make their day.",
"tabs":["Love letter","Surprise delivery","Help me choose","Delivery quote","Reviews"],"titles":["Secret love letter","Surprise delivery","Help me choose","Delivery estimate","Customer reviews"],
"descs":["Write a message to include with your flower enquiry.","Request a preferred date, time of day and address. We'll confirm availability personally.","Answer three questions for a bouquet suggestion.","Select your area to view a confirmed fee or request a quote.","Only genuine, approved feedback is displayed."],
"recipient":"Recipient's name","recipientPlaceholder":"Their name","sender":"Your name (optional)","message":"Your letter","msgPlaceholder":"Write from the heart…","letterStyle":"Letter style","letterStyles":["Classic","Romantic","Delicate"],
"letterPreview":"Letter preview","letterEmpty":"Your letter will appear here…","envelope":"Open / close envelope","letterSend":"Send letter enquiry ↗","letterBouquet":"Add to bouquet ↗",
"phone":"Recipient's phone (optional)","address":"Delivery address","addressPlaceholder":"Town, street, building","date":"Preferred date","time":"Time of day","times":["Morning","Afternoon","Evening"],"instructions":"Surprise instructions (optional)","surpriseSend":"Send surprise enquiry ↗",
"occasion":"Occasion","occasions":["For someone special","Birthday / celebration","Wedding","Just because"],"colour":"Palette","colours":["Red","Pink","White","Colourful"],"style":"Style","styles":["Classic","Lush","Delicate"],"quizSend":"Find my bouquet","recommend":"Our suggestion","results":["Romantic roses","Celebration bouquet","White wedding bouquet","Signature arrangement"],"catalog":"Browse this collection ↗","builder":"Build a custom bouquet ↗",
"zone":"Delivery area","fee":"Estimated delivery fee","feeUnknown":"Please enquire for a quote","feeKnown":"Listed rate:","feeNote":"Only confirmed fees are displayed. Availability and the final price require confirmation.","feeSend":"Request a delivery quote ↗",
"reviewsEmpty":"No verified customer reviews have been published yet. You could be the first.","name":"Your name","rating":"Rating","reviewMessage":"Your feedback","reviewPlaceholder":"Tell us about your experience…","permission":"I consent to my review and name being published after moderation.","reviewSend":"Send review on WhatsApp ↗","reviewNote":"Reviews are not published automatically. This site does not store submissions.",
"disclaimer":"An enquiry does not confirm an order, price or delivery time.","contactEnd":"Please confirm availability and final pricing.",
"letterHello":"Hello! I'd like to add a letter to my bouquet.","surpriseHello":"Hello! I'd like a surprise delivery.","feeHello":"Hello! I'd like a delivery quote.","reviewHello":"Hello! I'd like to leave feedback for Rose & Co.","yes":"yes","no":"no"
}
}

# ROSE-CO-INSPIRATIONAL-COPY-V1: editorial sample wording. Never misrepresent as real testimonials.
EDITORIAL_LINES = {
  "hy": [
    "Ծաղիկները պարզապես հիասքանչ էին։ Ամեն մանրուք այնքան նուրբ էր։",
    "Այսպիսի գեղեցիկ ծաղկեփունջ վաղուց չէի տեսել։",
    "Այնքան գեղեցիկ էր, որ ափսոսում էի բացել փաթեթավորումը։",
    "Ստացողի ժպիտն ամեն ինչ արժեր։",
    "Շատ ճաշակով ու սիրով պատրաստված կոմպոզիցիա։",
    "Ծաղիկներն իսկապես խոսում էին իմ փոխարեն։",
    "Գեղեցկություն՝ ամեն մի թերթիկի մեջ։",
    "Պարզապես աննկարագրելի նուրբ ու էլեգանտ։",
    "Իմ պատկերացրածից էլ գեղեցիկ ստացվեց։",
    "Ծաղկեփունջ, որը երկար կմնա հիշողության մեջ։",
    "Շատ գեղեցիկ գույների համադրություն ու յուրահատուկ ոճ։",
    "Ամեն ինչ այնքան խնամքով ու նրբությամբ էր արված։",
    "Սիրով ընտրված ծաղիկներ՝ սիրելի մարդու համար։",
    "Այս ծաղկեփունջն իսկական փոքրիկ արվեստի գործ էր։",
    "Այնպիսի ծաղիկներ, որոնք առանց խոսքերի ուրախացնում են։",
    "Յուրաքանչյուր դետալ իր տեղում էր։",
    "Գեղեցիկ փաթեթավորում, նուրբ գույներ, հիանալի արդյունք։",
    "Անակնկալը ստացվեց հենց այնպես, ինչպես երազում էի։",
    "Շքեղություն, որը երբեք չափազանցված չի թվում։",
    "Rose & Co-ն պարզապես ծաղիկներ չէ, այլ գեղեցիկ զգացմունք։"
  ],
  "ru": [
    "Цветы были невероятно красивыми, а каждая деталь — нежной.",
    "Давно не встречала настолько красивый букет.",
    "Так красиво, что даже жалко было разворачивать упаковку.",
    "Улыбка получателя стоила всего.",
    "Композиция создана с любовью и безупречным вкусом.",
    "Цветы сказали всё за меня.",
    "Красота в каждом лепестке.",
    "Невероятно нежно и элегантно.",
    "Получилось даже прекраснее, чем я представляла.",
    "Букет, который надолго останется в памяти.",
    "Прекрасные сочетания оттенков и особый стиль.",
    "В каждой детали чувствуется забота.",
    "Цветы, выбранные с любовью для самого дорогого человека.",
    "Этот букет похож на маленькое произведение искусства.",
    "Цветы, которые дарят радость без лишних слов.",
    "Каждая деталь на своём месте.",
    "Красивая упаковка, мягкие оттенки, прекрасный результат.",
    "Сюрприз получился именно таким, о каком я мечтала.",
    "Роскошь без лишней вычурности.",
    "Rose & Co — это не просто цветы, а красивые эмоции."
  ],
  "en": [
    "The flowers were breathtaking, with care in every detail.",
    "I hadn't seen a bouquet this beautiful in ages.",
    "So lovely I almost didn't want to unwrap it.",
    "The recipient's smile made it all worthwhile.",
    "A composition created with love and exquisite taste.",
    "The flowers said everything I couldn't put into words.",
    "Beauty in every petal.",
    "Delicate, elegant and truly unforgettable.",
    "Even prettier than I had imagined.",
    "A bouquet that will stay in my memory.",
    "Beautiful colours brought together with a unique touch.",
    "Every detail felt thoughtful and tender.",
    "Flowers chosen with love for someone special.",
    "Such a bouquet is a little work of art.",
    "Flowers that bring joy without a single word.",
    "Every little detail belongs exactly where it is.",
    "Beautiful wrapping, gentle shades, a lovely result.",
    "The surprise turned out just as I had dreamed.",
    "Luxury that feels effortless and never excessive.",
    "Rose & Co is more than flowers — it's a beautiful feeling."
  ]
}
EDITORIAL_LABELS = {
  "hy": ("20 ստեղծագործական տող՝ ծաղիկների մասին", "Սրանք հորինված օրինակային տեքստեր են, ոչ թե հաճախորդների իրական կարծիքներ։"),
  "ru": ("20 красивых фраз о цветах", "Это вымышленные примеры текста, а не реальные отзывы покупателей."),
  "en": ("20 lovely lines about flowers", "These are fictional example lines, not genuine customer testimonials.")
}
assert all(len(lines)==20 for lines in EDITORIAL_LINES.values())

def h(s):return escape(str(s),quote=True)
def inputfield(label,name,placeholder="",required=False,kind="text",length=160):
 return '<div><label for="rs-'+name+'">'+h(label)+'</label><input id="rs-'+name+'" name="'+name+'" type="'+kind+'" maxlength="'+str(length)+'" placeholder="'+h(placeholder)+'"'+(" required" if required else "")+'></div>'
def textarea(label,name,placeholder,required=False,length=800):
 return '<div><label for="rs-'+name+'">'+h(label)+'</label><textarea id="rs-'+name+'" name="'+name+'" maxlength="'+str(length)+'" placeholder="'+h(placeholder)+'"'+(" required" if required else "")+'></textarea></div>'
def selectfield(label,name,options):
 return '<div><label for="rs-'+name+'">'+h(label)+'</label><select id="rs-'+name+'" name="'+name+'">'+''.join('<option value="'+str(i)+'">'+h(item)+'</option>' for i,item in enumerate(options))+'</select></div>'
def button(label,id):
 return '<button type="button" class="button btn-burgundy" id="'+id+'">'+h(label)+'</button>'
def panel(id,title,desc,content,extra=""):
 return '<section class="rs-card" id="rs-'+id+'"><div class="rs-cardhead"><span class="eyebrow">ROSE &amp; CO</span><h3>'+h(title)+'</h3><p>'+h(desc)+'</p></div>'+content+extra+'</section>'
def make_service(lang):
 w=COPY[lang]
 letter='<div class="rs-grid"><form class="rs-form" id="rs-letter-form">'+inputfield(w["recipient"],"recipient",w["recipientPlaceholder"],True)+inputfield(w["sender"],"sender")
 letter+=selectfield(w["letterStyle"],"letterstyle",w["letterStyles"])+textarea(w["message"],"letter",w["msgPlaceholder"],True,650)
 letter+='<div class="rs-actions">'+button(w["letterSend"],"rs-letter-send")+'<button type="button" class="rs-textbtn" id="rs-letter-bouquet">'+h(w["letterBouquet"])+'</button></div></form>'
 letter+='<div class="rs-envelopebox"><h4>'+h(w["letterPreview"])+'</h4><div class="rs-envelope" id="rs-envelope"><div class="rs-paper"><strong id="rs-preview-to"></strong><p id="rs-preview-letter">'+h(w["letterEmpty"])+'</p><em id="rs-preview-from"></em></div></div><button type="button" class="rs-envelope-toggle" aria-expanded="false">'+h(w["envelope"])+'</button></div></div>'
 surprise='<form id="rs-surprise-form" class="rs-form"><div class="rs-two">'+inputfield(w["recipient"],"recipient",w["recipientPlaceholder"],True)+inputfield(w["phone"],"phone","",False,"tel",36)+'</div>'
 surprise+=inputfield(w["address"],"address",w["addressPlaceholder"],True,"text",250)
 surprise+='<div class="rs-two">'+inputfield(w["date"],"date","",True,"date",30)+selectfield(w["time"],"time",w["times"])+'</div>'
 surprise+=textarea(w["instructions"],"instructions","",False,350)+'<div class="rs-actions">'+button(w["surpriseSend"],"rs-surprise-send")+'</div><p class="rs-note">'+h(w["disclaimer"])+'</p></form>'
 quiz='<form id="rs-quiz-form" class="rs-form rs-three">'+selectfield(w["occasion"],"occasion",w["occasions"])+selectfield(w["colour"],"colour",w["colours"])+selectfield(w["style"],"style",w["styles"])+'<div class="rs-actions">'+button(w["quizSend"],"rs-quiz-send")+'</div></form>'
 quiz+='<div id="rs-quiz-result" class="rs-result" hidden><p>'+h(w["recommend"])+'</p><strong id="rs-recommend"></strong><div class="rs-actions"><a id="rs-catalog" class="button btn-burgundy" href="/rose-and-co/'+lang+'/catalog/">'+h(w["catalog"])+'</a><a class="rs-textbtn" href="/rose-and-co/'+lang+'/#rose-bouquet-builder">'+h(w["builder"])+'</a></div></div>'
 zones=''.join('<option value="'+h(z["id"])+'">'+h(z["label"][lang])+'</option>' for z in data["delivery_zones"])
 delivery='<div class="rs-grid"><form id="rs-delivery-form" class="rs-form"><div><label for="rs-zone">'+h(w["zone"])+'</label><select id="rs-zone" name="zone">'+zones+'</select></div>'+inputfield(w["address"],"address",w["addressPlaceholder"],False,"text",250)
 delivery+='<div class="rs-actions">'+button(w["feeSend"],"rs-delivery-send")+'</div></form><div class="rs-feebox"><span class="eyebrow">'+h(w["fee"])+'</span><strong id="rs-fee">'+h(w["feeUnknown"])+'</strong><p>'+h(w["feeNote"])+'</p></div></div>'
 review='<div class="rs-grid"><div id="rs-reviews-list" class="rs-reviews"><p class="rs-empty">'+h(w["reviewsEmpty"])+'</p></div>'
 label,notice=EDITORIAL_LABELS[lang]
 editorial='<details class="rs-editorial"><summary>'+h(label)+'</summary><p class="rs-editorial-notice">'+h(notice)+'</p><ol class="rs-editorial-list">'+''.join('<li>'+h(line)+'</li>' for line in EDITORIAL_LINES[lang])+'</ol></details>'
 review+='<div class="rs-editorial-wrap">'+editorial+'</div>'
 review+='<form id="rs-review-form" class="rs-form">'+inputfield(w["name"],"name","",True)+selectfield(w["rating"],"rating",["5","4","3","2","1"])+textarea(w["reviewMessage"],"review",w["reviewPlaceholder"],True,700)
 review+='<label class="rs-check"><input type="checkbox" name="permission">'+h(w["permission"])+'</label><div class="rs-actions">'+button(w["reviewSend"],"rs-review-send")+'</div><p class="rs-note">'+h(w["reviewNote"])+'</p></form></div>'
 all_cards=[panel("letter",w["titles"][0],w["descs"][0],letter),panel("surprise",w["titles"][1],w["descs"][1],surprise),panel("quiz",w["titles"][2],w["descs"][2],quiz),panel("delivery",w["titles"][3],w["descs"][3],delivery),panel("reviews",w["titles"][4],w["descs"][4],review)]
 jump=''.join('<a href="#rs-'+id+'">'+h(t)+'</a>' for id,t in zip(("letter","surprise","quiz","delivery","reviews"),w["tabs"]))
 def script_data(id,obj):
  safe=json.dumps(obj,ensure_ascii=False,separators=(",",":")).replace("<","\\u003c").replace("&","\\u0026")
  return '<script id="'+id+'" type="application/json">'+safe+'</script>'
 return '<section id="rose-service-hub" class="rose-services" data-lang="'+lang+'"><div class="container"><header class="rs-header"><span class="eyebrow">FLOWERS WITH FEELING</span><h2>'+h(w["title"])+'</h2><p>'+h(w["intro"])+'</p></header><nav class="rs-links" aria-label="'+h(w["nav"])+'">'+jump+'</nav>'+''.join(all_cards)+'</div>'+script_data("rs-words",w)+script_data("rs-data",data)+'</section>'

CSS=r'''
/* ROSE-CO-NEW-SERVICES-20261025 */
.rose-services{background:linear-gradient(150deg,#fff9f5,#f2e2df 50%,#fff9f4);padding:clamp(65px,8vw,110px) 0;scroll-margin-top:16px}
.rs-header{text-align:center;max-width:760px;margin:0 auto 30px}
.rs-header h2{font:500 clamp(32px,4.1vw,54px)/1.27 var(--serif);color:#642c42;margin:14px 0}
.rs-header p,.rs-cardhead p,.rs-note{font-size:13px;line-height:1.85;color:#79646b}
.rs-links{display:flex;justify-content:center;gap:9px;flex-wrap:wrap;margin:0 auto 35px}
.rs-links a{font-size:12px;color:#713b50;border:1px solid #ddbbc5;background:#fffaf6;border-radius:25px;padding:9px 13px;white-space:nowrap}
.rs-links a:hover,.rs-links a:focus-visible{background:#f3dee3}
.rs-card{background:rgba(255,252,249,.94);border:1px solid #e4ccd0;box-shadow:0 18px 54px rgba(75,30,49,.07);padding:clamp(20px,3vw,42px);margin:25px 0 35px;scroll-margin-top:22px}
.rs-cardhead{max-width:800px;margin-bottom:21px}
.rs-cardhead h3{font:500 clamp(26px,3.2vw,40px)/1.3 var(--serif);color:#63293e;margin:10px 0}
.rs-grid{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,.95fr);gap:clamp(20px,4vw,48px);align-items:start}
.rs-form{display:grid;gap:14px;min-width:0}
.rs-two{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}
.rs-three{grid-template-columns:repeat(3,minmax(0,1fr));align-items:end}
.rs-form label{display:block;color:#6d384b;font-size:12px;font-weight:700;margin-bottom:7px;line-height:1.5}
.rs-form input:not([type=checkbox]),.rs-form select,.rs-form textarea{display:block;width:100%;min-width:0;border:1px solid #dcc3c3;border-radius:2px;background:#fffaf7;color:#51343f;font:400 13px var(--sans);padding:12px;min-height:45px}
.rs-form textarea{min-height:116px;resize:vertical;line-height:1.7}
.rs-form input:focus-visible,.rs-form select:focus-visible,.rs-form textarea:focus-visible{outline:2px solid #a56f82;outline-offset:2px}
.rs-actions{display:flex;gap:12px;flex-wrap:wrap;align-items:center;margin:6px 0}
.rs-actions .button{white-space:normal;text-align:center;gap:8px}
.rs-textbtn{display:inline-flex;align-items:center;background:transparent;color:#71324c;border:0;text-decoration:underline;text-underline-offset:5px;cursor:pointer;font-size:13px;padding:10px}
.rs-envelopebox{background:linear-gradient(145deg,#edd2d6,#f9ece7);padding:25px;text-align:center;min-width:0}
.rs-envelopebox h4{font:500 20px var(--serif);color:#693147}
.rs-envelope{position:relative;background:#fff9f4;border:1px solid #deb7c3;box-shadow:0 12px 40px rgba(88,40,61,.13);min-height:280px;max-width:400px;margin:auto;overflow:hidden}
.rs-envelope::before{content:"";position:absolute;z-index:2;top:0;left:0;right:0;height:100px;clip-path:polygon(0 0,100% 0,50% 100%);background:#e9beca;transform-origin:top;transition:transform .65s ease}
.rs-envelope.open::before{transform:rotateX(175deg)}
.rs-paper{padding:110px 19px 18px}
.rs-paper strong,.rs-paper em{font:italic 17px var(--serif);color:#89465f;overflow-wrap:anywhere}
.rs-paper p{font:400 14px/1.8 var(--serif);color:#643649;max-height:165px;overflow:auto;white-space:pre-wrap;overflow-wrap:anywhere}
.rs-envelope-toggle{margin:15px 0 0;border:1px solid #b98498;color:#613147;background:#fffaf6;padding:10px 14px;font-size:12px;cursor:pointer}
.rs-result{padding:21px;background:#f8e9e7;border:1px solid #cda9b5;margin-top:20px}
.rs-result[hidden]{display:none}
.rs-result strong{display:block;font:500 26px var(--serif);color:#672940;margin:10px 0}
.rs-feebox{padding:32px;background:linear-gradient(150deg,#f8e6e7,#fff8f3);border:1px solid #e3c6ce}
.rs-feebox strong{display:block;margin:15px 0;font:500 clamp(22px,3vw,31px)/1.35 var(--serif);color:#713b50}
.rs-feebox p{font-size:12px;color:#826c73}
.rs-reviews{display:grid;gap:12px}
.rs-empty{background:#f9eeed;border:1px dashed #c9a4b0;color:#795765;font-size:13px;line-height:1.7;padding:25px}
.rs-review{padding:18px;border:1px solid #e0c7cd;background:#fff9f5;margin:0}
.rs-review p{font-size:13px;line-height:1.8;white-space:pre-wrap;overflow-wrap:anywhere}
.rs-review strong{font-size:12px;color:#6e344b}
.rs-stars{color:#a86177;letter-spacing:2px}
.rs-check{display:flex!important;align-items:flex-start;gap:10px;font-weight:400!important}
.rs-check input{width:18px;height:18px;flex:none;accent-color:#8b4963}
.rs-editorial-wrap{grid-column:1/-1;margin-top:2px}
.rs-editorial{background:#fffaf7;border:1px solid #e4c9d1;padding:19px 20px}
.rs-editorial summary{color:#733b52;font-size:14px;font-weight:700;cursor:pointer}
.rs-editorial-notice{font-size:12px;color:#846b74;line-height:1.8;margin:12px 0}
.rs-editorial-list{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:9px 29px;padding-left:22px;margin:0}
.rs-editorial-list li{padding:8px 3px;font-size:13px;line-height:1.7;color:#5e4650}
@media(max-width:700px){.rs-editorial-list{grid-template-columns:1fr}}

@media(max-width:900px){.rs-grid,.rs-three{grid-template-columns:1fr}.rs-links{justify-content:flex-start}.rs-card{margin:20px 0}}
@media(max-width:640px){.rs-card{padding:18px 15px}.rs-two{grid-template-columns:1fr}.rs-links{overflow-x:auto;flex-wrap:nowrap;padding-bottom:10px}.rs-actions{flex-direction:column;align-items:stretch}.rs-actions .button{width:100%}.rs-envelopebox{padding:15px}.rs-envelope{min-height:250px}.rs-cardhead h3{font-size:27px}}
@media(prefers-reduced-motion:reduce){.rs-envelope::before{transition:none}}
'''

JS=r'''(()=>{
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
})();'''

(assets/"rose-services.css").write_text(CSS+"\n",encoding="utf-8")
(assets/"rose-services.js").write_text(JS+"\n",encoding="utf-8")
counts={}
for lang,w in COPY.items():
 files=list((root/lang).rglob("*.html"))
 for page in files:
  html=page.read_text(encoding="utf-8")
  assert "rose-services.js" not in html
  link="/rose-and-co/"+lang+"/#rose-service-hub"
  menu='<a class="nav-link" href="'+link+'">'+h(w["nav"])+'</a>'
  m=re.search(r'(<nav[^>]*class="mobile-menu"[^>]*>.*?)(</nav>)',html,re.S)
  assert m,page
  html=html[:m.start()]+m.group(1)+menu+m.group(2)+html[m.end():]
  if page==root/lang/"index.html":
   assert '<section class="about-spotlight">' in html
   html=html.replace('<section class="about-spotlight">',make_service(lang)+'<section class="about-spotlight">',1)
   m=re.search(r'(<div class="hero-buttons">.*?)(</div>)',html,re.S)
   assert m,page
   call='<a class="text-link" href="#rose-service-hub">'+h(w["nav"])+' <span>↗</span></a>'
   html=html[:m.start()]+m.group(1)+call+m.group(2)+html[m.end():]
  m=re.search(r'(<p class="footer-quote">.*?</p>)',html,re.S)
  assert m,page
  foot='<a class="rose-builder-footer" href="'+link+'">'+h(w["nav"])+' ↗</a>'
  html=html[:m.end()]+foot+html[m.end():]
  assert "</head>" in html
  html=html.replace("</head>",'<link rel="stylesheet" href="/rose-and-co/assets/rose-services.css?v=services1"/><script defer src="/rose-and-co/assets/rose-services.js?v=services1"></script></head>',1)
  page.write_text(html,encoding="utf-8")
 counts[lang]=len(files)
for lang in COPY:
 html=(root/lang/"index.html").read_text(encoding="utf-8")
 assert all('id="rs-'+id+'"' in html for id in ("letter","surprise","quiz","delivery","reviews"))
assert all(n>6 for n in counts.values())
print("Five rose services installed for HY/RU/EN:",counts," verified customer reviews:",len(data["reviews"]))
