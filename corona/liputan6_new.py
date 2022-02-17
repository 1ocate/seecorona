import json
import sqlite3
import requests
from bs4 import BeautifulSoup

#res = requests.get('https://www.liputan6.com/search?order=latest&channel_id=9&from_date=19%2F03%2F2020&to_date=19%2F03%2F2020&type=all&q=corona')
res = requests.get('https://www.liputan6.com/tag/corona?type=text')

# print(res.content)
#google = BeautifulSoup(open("./test.html"), 'html.parser')
liputan6 = BeautifulSoup(res.content, 'html.parser')
newsbox = liputan6.find('div','articles--iridescent-list')
articles = newsbox.find_all('article','articles--iridescent-list--item')
#articles = newsbox.find_all('article')
#articles = newsbox.find('span','articles--iridescent-list--text-item__datetime').find('time').get_text()
liputan6 =[]

for article in articles:
    title= article.find('h4').find('a').get('title')
    img =  article.find('picture').find('img').get('src')
    link = article.find('a').get('href')
    date = article.find('time').get_text()
    #date_w = article.find('span').find('time').get('title')
    category = article.find('a','articles--iridescent-list--text-item__category').get_text()
    liputan6.append({'title':title, 'img':img, 'link':link, 'date':date, 'category':category})

json_data = json.dumps(liputan6)
print (json_data)
