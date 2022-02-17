import json
import sqlite3
import requests
from bs4 import BeautifulSoup
from datetime import date, timedelta, datetime

#url = "https://www.tokopedia.com/seecorona"
#headers = {'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0'}
#headers = {'User-agent': 'Mozilla/5.0'}
headers = { 'User-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0','Accept-Language': 'en-us','Accept-Encoding': 'html'}
#headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


res = requests.get('https://m.tokopedia.com/seecorona?source=universe&st=product',headers=headers)

toko = BeautifulSoup(res.content, 'html.parser')

list = toko.find(text="Semua Produk").find_next("div","css-yxh0dp")
list = toko.find(id="masonry-column-0")
#print(list)
products = list.find_all('div','css-lczlz3')
#products = list.find_all('div','css-9djufs')
print(products)
info =[]

for product in products:
    title= product.find('span','css-1bjwylw').get_text()
    #img =  product.find('img')
    img =  product.find('img').get('src')
    link = product.find('a').get('href')
    price = product.find('span','css-o5uqvq').get_text()
    #dates = article.find('span','date')
    #span = article.find('span','category').extract()
    #date = dates.get_text()
    #detik.append({'title':title, 'img':img, 'link':link, 'date':date, 'category':category})
    print(link,title,price,img)

#json_data = json.dumps(detik)
#print (json_data)
#with open('./csv/detik.json', 'w', encoding="utf-8") as make_file:
#    json.dump(detik, make_file, ensure_ascii=False)
