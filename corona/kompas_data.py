import json
import sqlite3
import requests
from bs4 import BeautifulSoup
from datetime import date, timedelta, datetime

res = requests.get('https://www.kompas.com/covid-19')

# print(res.content)
kompas = BeautifulSoup(res.content, 'html.parser')


provisi = kompas.find('div','covid__wscroll')
provisi_rows = provisi.find_all('div','covid__row')
#detik =[]

for provisi_row in provisi_rows:
    province= provisi_row.find('div','covid__prov').get_text()
    positive= provisi_row.find('div','covid__total').find('span','-odp').find('strong').get_text()
    #detik.append({'title':title, 'img':img, 'link':link, 'date':date, 'category':category})
    print(province,positive)

#json_data = json.dumps(detik)
#print (json_data)
#with open('./csv/detik.json', 'w', encoding="utf-8") as make_file:
#    json.dump(detik, make_file, ensure_ascii=False)
