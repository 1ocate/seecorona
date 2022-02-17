import json
import sqlite3
import requests
from bs4 import BeautifulSoup
from datetime import date, timedelta, datetime

#res = requests.get('https://news.google.com/search?q=corona%20indoensia&hl=id&gl=ID&ceid=ID%3Aid')
res = requests.get('https://www.detik.com/search/searchall?query=corona&page=1&sortby=&sorttime=0&siteid=2&fromdatex=&todatex=&hitperpages=9&siteid=3')

# print(res.content)
google = BeautifulSoup(res.content, 'html.parser')


newsbox = google.find('div','media_rows')
articles = newsbox.find_all('article')
#title = articles.find_all('h2','title')
#print(title)
detik =[]

for article in articles:
    title= article.find('h2','title').get_text()
    img =  article.find('img').get('src')
    link = article.find('a').get('href')
    category = article.find('span','category').get_text()
    dates = article.find('span','date')
    span = article.find('span','category').extract()
    date = dates.get_text()
    detik.append({'title':title, 'img':img, 'link':link, 'date':date, 'category':category})

#json_data = json.dumps(detik)
#print (json_data)
with open('./csv/detik.json', 'w', encoding="utf-8") as make_file:
    json.dump(detik, make_file, ensure_ascii=False)
