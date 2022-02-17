import json
import sqlite3
import requests
from bs4 import BeautifulSoup
from datetime import date, timedelta, datetime

res = requests.get('https://news.google.com/search?q=%EC%BD%94%EB%A1%9C%EB%82%98%20%22%EC%9D%B8%EB%8F%84%EB%84%A4%EC%8B%9C%EC%95%84%22%20when%3A1d&hl=ko&gl=KR&ceid=KR%3Ako')

google = BeautifulSoup(res.content, 'html.parser')

news =[]

#articles= google.find(id="nav-tabContent").find(text="Indonesia").parent
articles= google.find("figure").parent.parent.parent.parent.find_all("figure")
#id_check= indonesia.parent.find_next_siblings()[9].text.replace(",","")
for article in articles:
       data = article.find("img")
       if not data is None:       	
         img = data.get("src")
         img_s = data.get("srcset")
         link = data.parent.parent.get("href").replace("./","")
         link = "https://news.google.com/"+link
         in_article = data.parent.parent.find_next_sibling()
         title = in_article.find("h3").get_text()
         title_f = title.find(" - ")
         if title_f != -1:
           title = title[0:title_f]
         date = in_article.find("time").get("datetime")
         site = in_article.find("time").findPrevious('a').get_text()
         news.append({'img':img, 'img_s':img_s,'link': link, 'title':title, 'date': date, 'site':site})

with open('./corona/csv/google_news_ko.json','w') as fp:
    fp.write(json.dumps(news))
