#!/usr/bin/env python3
"""Improve Rose & Co heading keywords without altering product names or images."""
from pathlib import Path
import sys, re
root=Path(sys.argv[1])
mapping={
"hy":{
"home":[("h1","Ծաղիկներ՝ զգացմունքների լեզվով","Ծաղիկներ և ծաղկեփնջեր Հայաստանում՝ Rose & Co"),
("h2","Ստեղծված ամեն առիթի համար","Ծաղիկներ և ծաղկեփնջեր՝ յուրաքանչյուր առիթի համար"),
("h2","Հատուկ ընտրված ծաղկեփնջեր","Գեղեցիկ ծաղկեփնջեր և վարդեր Հայաստանում"),
("h2","Ծաղիկների տեսակների ուղեցույց","Ծաղիկների տեսակներ՝ վարդեր, քրիզանթեմներ և այլ ծաղիկներ"),
("h2","Մեր ծաղկային օրագիրը","Ծաղիկների և ծաղկեփնջերի խնամքի խորհուրդներ")],
"catalog":[("h1","Կատալոգ","Ծաղիկների և ծաղկեփնջերի կատալոգ Հայաստանում")],
"flowers":[("h1","Ծաղիկների տեսակներ","Ծաղիկների տեսակներ Հայաստանում՝ վարդեր և այլ ծաղիկներ")],
"about":[("h1","Մեր մասին","Rose & Co՝ ծաղիկներ և ծաղկեփնջեր Հայաստանում")],
"contact":[("h1","Կապ","Ծաղիկների և ծաղկեփնջերի պատվեր՝ կապ Rose & Co-ի հետ")],
"journal":[("h1","Բլոգ","Բլոգ՝ ծաղիկներ, ծաղկեփնջեր և խնամքի խորհուրդներ")]},
"ru":{
"home":[("h1","Цветы — язык чувств","Цветы и букеты в Армении — Rose & Co"),
("h2","Цветы на любой случай","Цветы и букеты для любого повода"),
("h2","Избранные букеты","Красивые букеты и розы в Армении"),
("h2","Путеводитель по цветам","Виды цветов: розы, хризантемы и другие"),
("h2","Наш цветочный журнал","Советы по уходу за цветами и букетами")],
"catalog":[("h1","Каталог","Каталог цветов и букетов в Армении")],
"flowers":[("h1","Виды цветов","Виды цветов в Армении: розы и другие цветы")],
"about":[("h1","О нас","Rose & Co — цветы и букеты в Армении")],
"contact":[("h1","Контакты","Заказать цветы и букеты — контакты Rose & Co")],
"journal":[("h1","Блог","Блог о цветах, букетах и уходе за ними")]},
"en":{
"home":[("h1","Flowers speak the language of feeling","Flowers and bouquets in Armenia — Rose & Co"),
("h2","Made for every occasion","Flowers and bouquets for every occasion"),
("h2","Curated bouquets","Beautiful bouquets and roses in Armenia"),
("h2","A guide to flower varieties","Flower varieties: roses, chrysanthemums and more"),
("h2","The floral journal","Flower and bouquet care tips")],
"catalog":[("h1","Collection","Flowers and bouquets catalog in Armenia")],
"flowers":[("h1","Flower varieties","Flower varieties in Armenia: roses and more")],
"about":[("h1","Our story","Rose & Co — flowers and bouquets in Armenia")],
"contact":[("h1","Contact","Order flowers and bouquets — contact Rose & Co")],
"journal":[("h1","Journal","Flower and bouquet journal: care and inspiration")]}}
changed=0
for lang, pages in mapping.items():
 for page, rules in pages.items():
  file=root/lang/("index.html" if page=="home" else f"{page}/index.html")
  if not file.exists():raise FileNotFoundError(file)
  text=file.read_text(encoding="utf-8")
  for tag, old, new in rules:
   oldhtml=f"<{tag}>{old}</{tag}>"
   newhtml=f"<{tag}>{new}</{tag}>"
   if oldhtml in text:
    text=text.replace(oldhtml,newhtml,1)
   elif newhtml not in text:
    raise ValueError(f"Expected heading not found: {file}: {old}")
  file.write_text(text,encoding="utf-8")
  changed+=1
print(f"Updated natural SEO headings on {changed} Rose & Co pages.")
