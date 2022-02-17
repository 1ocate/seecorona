import json
import sqlite3
import requests
from bs4 import BeautifulSoup
from datetime import date, timedelta, datetime
import telegram

TELEGRAM_TOKEN = '1250942763:AAFGD3fpY5zovpooXGQZ8ESBHHchhy2R0SY'

bot = telegram.Bot(token=TELEGRAM_TOKEN)
updates = bot.getUpdates()
chat_id = '129061235'


ID = []
ID_Y = []
today = date.today()
yesterday = date.today() - timedelta(1)
day_b_yesterday = date.today() - timedelta(2)

db = sqlite3.connect("/root/corona/corona.db")
cursor =db.cursor()

url1 = "https://covid19.disiplin.id"
res = requests.get(url1)

if res.status_code == 200:
   url1_data  = BeautifulSoup(res.content, 'html.parser')
else:
   print ('error_url1')
   print (res.status_code)

   quit()

cookies = res.cookies.get_dict()
meta = url1_data.find("meta", {"name":"csrf-token"})
csrfToken= meta["content"]


headers = { 'User-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0','Accept-Language': 'en-us','Accept-Encoding': 'html', 'X-Requested-With': 'XMLHttpRequest'}
headers['X-CSRF-TOKEN'] = csrfToken

post_data= { 'emerging': 'COVID-19' }


url2 ="https://covid19.disiplin.id/emerging/data_provinces"
res2 = requests.post(url2, data=post_data, headers=headers, cookies=cookies)


if res2.status_code == 200:
    data_kem = res2.json()

else:
    print ('error kem data')
    print (res2.status_code)
    bot.sendMessage(chat_id=chat_id, text='error kem data')
    bot.sendMessage(chat_id=chat_id, text='res2.status_code')
    quit()

#print (data_kem);
#quit()
for row in data_kem["features"]:
   province = row["properties"]["provinsi"].title()
   if province == "Di Yogyakarta":
      province ="DI Yogyakarta"
   if province == "Dki Jakarta":
      province ="DKI Jakarta"
   positive = int(row["properties"]["total_case"])
   death = int(row["properties"]["total_died"])
   cure = int(row["properties"]["total_recover"])
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

#   cursor.execute('UPDATE province SET positive=?, cure=?, death=? WHERE Date=? and province=?',(positive, cure, death, today, province))
   cursor.execute('UPDATE province SET positive=?, cure=?, death=? WHERE Date=? and province=?',(positive, cure, death, yesterday, province))
   db.commit()

   #cursor.execute("SELECT site,name_ko from province_id_new where province ='%s'" % province)
   #row= cursor.fetchone()
   #if not row:
   #   link = "no"
   #   name_ko = "no"
   #else:
   #   link = row[0]
   #   name_ko = row[1]


#   ID.append({'Province':province, 'Positive': positive, 'Positive_p':positive_p, 'Cure': cure, 'Cure_p':cure_p, 'Death':death, 'Death_p':death_p, 'link':link, 'Province_ko':name_ko})
    #ID.append({'Id':id, 'Province':province, 'Positive': positive, 'Positive_p':str(positive_p), 'Cure': cure, 'Cure_p':str(cure_p), 'Death':death, 'Death_p':str(death_p), 'link':link 'Province_ko':name_ko})

cursor.execute("SELECT province,positive,cure,death from province where date ='%s'" % today )
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
    cursor.execute('SELECT positive,cure,death from province where date =? and province =?',(yesterday,province))
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

    cursor.execute("SELECT site,name_ko from province_id_new where province ='%s'" % province)
    row= cursor.fetchone()
    if not row:
      link = "no"
      name_ko = "no"
    else:
      link = row[0]
      name_ko = row[1]

    ID.append({'Province':province, 'Positive': positive, 'Positive_p':positive_p, 'Cure': cure, 'Cure_p':cure_p, 'Death':death, 'Death_p':death_p, 'link':link, 'Province_ko':name_ko})


data={'data':ID}

with open('/root/corona/csv/province.json','w') as fp:
    fp.write(json.dumps(data))

#Update check
update_file ='province_y.json'
#cursor.execute('SELECT date from update_file where date =? and name =?',(today,update_file))
#row= cursor.fetchone()
#if row:
#   quit()

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

cursor.execute('INSERT INTO update_file (name,date) VALUES(?,?)',(update_file,today))
db.commit()

with open(f'/root/corona/csv/{update_file}','w') as fp:
    fp.write(json.dumps(data_y))


