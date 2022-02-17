import json
import urllib.request
import requests
import sqlite3
from bs4 import BeautifulSoup
from datetime import date, timedelta, datetime

ID = []
ID_Y = []
today = date.today()
yesterday = date.today() - timedelta(1)
day_b_yesterday = date.today() - timedelta(2)


url = "https://news.google.com/covid19/map?hl=id&mid=%2Fm%2F03ryn&gl=ID&ceid=ID%3Aid"
res = requests.get(url)
request= res.status_code

if request == 200:
   #data = requests.get(url)
    data = BeautifulSoup(res.content, 'html.parser')
else:
    print ('error google data')
    quit()

db = sqlite3.connect("/root/corona/corona.db")
cursor =db.cursor()

province = data.find('table').find('tbody')
rows = province.find_all('tr')
sum = 0

for row in rows[1:]:
   province= row.find('th').get_text()
   if province == "Daerah Istimewa Yogyakarta":
      province ="DI Yogyakarta"
   if province == "Jakarta":
      province ="DKI Jakarta"
   if province == "Kepulauan Bangka Belitung":
      province ="Kepulauan Bangka Belitung"   
   province_td = row.find_all('td')
   positive = int(province_td[0].get_text().replace(".",""))
   cure = int(province_td[3].get_text().replace(".",""))
   death = int(province_td[4].get_text().replace(".",""))
   perjt = province_td[2].get_text()

   if (province == "Indonesia"):
       total = positive


   
   if (perjt!= "Tidak ada data" and province != "Indonesia"):
      sum=sum+positive
      cursor.execute('SELECT positive,cure,death from province where date =? and province =?',(yesterday,province))
      row= cursor.fetchone()
      if row:
         positive_y = row[0]
         cure_y = row[1]
         death_y = row[2]
         positive_p = int(positive) - positive_y
         cure_p = int(cure) - cure_y
         death_p = int(death) - death_y
         #print(province,positive_p,cure_p,death_p)
      else:
         positive_p = positive
         cure_p = cure
         death_p = death
      cursor.execute('SELECT positive,cure,death from province where date =? and province =?',(today,province))
      row= cursor.fetchone()
      if not row:
         cursor.execute('INSERT INTO province (province,date) VALUES(?,?)',(province,today))
   
      cursor.execute("SELECT site,name_ko from province_id_new where province ='%s'" % province)
      row= cursor.fetchone()
      if not row:
         link = "no"
         name_ko = "no"
      else:
         link = row[0]
         name_ko = row[1]
   
      cursor.execute('UPDATE province SET positive=?, cure=?, death=? WHERE Date=? and province=?',(positive, cure, death, today, province))
      db.commit()
      ID.append({'Province':province, 'Positive': positive, 'Positive_p':positive_p, 'Cure': cure, 'Cure_p':cure_p, 'Death':death, 'Death_p':death_p, 'link':link, 'Province_ko':name_ko})

#####belum diketahui######

positive = total-sum
cure = 0
death = 0
province = "Lokasi belum diketahui"
cursor.execute('SELECT positive,cure,death from province where date =? and province =?',(yesterday,province))
row= cursor.fetchone()
if row:
      positive_y = row[0]
      cure_y = row[1]
      death_y = row[2]
      positive_p = int(positive) - positive_y
      cure_p = int(cure) - cure_y
      death_p = int(death) - death_y
      #print(province,positive_p,cure_p,death_p)
else:
      positive_p = positive
      cure_p = cure
      death_p = death
 
ID.append({'Province':province, 'Positive': positive, 'Positive_p':positive_p, 'Cure': cure, 'Cure_p':cure_p, 'Death':death, 'Death_p':death_p, 'link':link, 'Province_ko':"조사중"})


#####belum diketahui######
data={'data':ID}

cursor.execute("SELECT province,positive,cure,death from province where date ='%s'" % yesterday )
rows= cursor.fetchall()
for row in rows:
    province= row[0]
    positive= row[1]
    cure= row[2]
    if not cure:
     cure=0
    death= row[3]
    if not death:
     death=0
    cursor.execute('SELECT positive,cure,death from province where date =? and province =?',(day_b_yesterday,province))
    row= cursor.fetchone()
    if row:
      positive_y = row[0]
      cure_y = row[1]
      death_y = row[2]
      positive_p = int(positive) - positive_y
      cure_p = int(cure) - cure_y
      death_p = int(death) - death_y
    else:
      positive_p = positive
      cure_p = cure
      death_p = death
    #cursor.execute('SELECT positive,cure,death from province where date =? and province =?',(today,province))
    #row= cursor.fetchone()
    #if not row:
    #  cursor.execute('INSERT INTO province (province,date) VALUES(?,?)',(province,today))

    #cursor.execute('UPDATE province SET positive=?, cure=?, death=? WHERE Date=? and province=?',(positive, cure, death, today, province))
    #db.commit()

    cursor.execute("SELECT site,name_ko from province_id_new where province ='%s'" % province)
    row= cursor.fetchone()
    if not row:
      link = "no"
      name_ko = "no"
    else:
      link = row[0]
      name_ko = row[1]

    ID_Y.append({'Province':province, 'Positive': positive, 'Positive_p':positive_p, 'Cure': cure, 'Cure_p':cure_p, 'Death':death, 'Death_p':death_p, 'link':link, 'Province_ko':name_ko})

data_y={'data':ID_Y}


with open('/root/corona/csv/province.json','w') as fp:
    fp.write(json.dumps(data))
with open('/root/corona/csv/province_y.json','w') as fp:
    fp.write(json.dumps(data_y))
