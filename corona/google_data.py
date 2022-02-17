import json
import sqlite3
import requests
from bs4 import BeautifulSoup
from datetime import date, timedelta, datetime

res = requests.get('https://news.google.com/covid19/map?hl=id&mid=%2Fm%2F03ryn&gl=ID&ceid=ID%3Aid')

# print(res.content)
google = BeautifulSoup(res.content, 'html.parser')
province_table = google.find('table').find('tbody')
province_table_rows = province_table.find_all('tr')
google =[]
i = 1 
sum =0 
for province_table_row in province_table_rows[1:]:
 
    province = province_table_row.find('th').get_text()

    province_td = province_table_row.find_all('td')
    positive = int(province_td[0].get_text().replace(".",""))
    cure = province_td[3].get_text()
    death = province_td[4].get_text()
    perjt = province_td[2].get_text()
        
    if (province == "Indonesia"):      
       total = positive

    if (perjt!= "Tidak ada data" and province != "Indonesia"):
        print (i,province,positive,cure,death)
        i=i+1
        sum=sum+positive
        google.append({'Province':province, 'Positive': positive,  'Cure': cure, 'Death': death })

positive = total-sum
province = "Lokasi belum diketahui"
google.append({'Province':province, 'Positive': positive,  'Cure': 0, 'Death': 0 })

print(google)


#json_data = json.dumps(detik)
#print (json_data)
#with open('./csv/detik.json', 'w', encoding="utf-8") as make_file:
#    json.dump(detik, make_file, ensure_ascii=False)
