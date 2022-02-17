import json
import sqlite3
import requests
from bs4 import BeautifulSoup

#res = requests.get('https://www.liputan6.com/search?order=latest&channel_id=9&from_date=19%2F03%2F2020&to_date=19%2F03%2F2020&type=all&q=corona')
#res = requests.get('https://www.liputan6.com/tag/corona?type=text')
res = requests.get('https://www.liputan6.com/search?order=latest&channel_id=9&from_date=19%2F03%2F2020&to_date=19%2F03%2F2020&type=text&q=corona+indonesia')

# print(res.content)
google = BeautifulSoup(res.content, 'html.parser')


#newsbox = google.find('article','main')
#search_box = google.find('div','articles--iridescent-list')
#articles = newsbox.find_all('article','articles--iridescent-list--item articles--iridescent-list--text-item')
#articles = search_box.find_all('article')
articles = google.find_all('article')
articles_n = google.find('article')
#title = articles.find_all('h2','title')
#print(title)
liputan6 =[]
date_n = articles_n.find('span').find('time').get_text()
for article in articles:
    title= article.find('h4').find('a').get('title')
    img =  article.find('img').get('src')
    link = article.find('a').get('href')
    date = article.find('span').find('time').get_text()
    #date_w = article.find('span').find('time').get('title')
    category = article.find('a','articles--iridescent-list--text-item__category').get_text()
    liputan6.append({'title':title, 'img':img, 'link':link, 'date':date, 'category':category})

json_data = json.dumps(liputan6)
print (json_data)
