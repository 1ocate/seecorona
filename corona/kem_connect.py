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


headers1 = { 'User-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0','Accept-Language': 'en-us','Accept-Encoding': 'html', 'X-Requested-With': 'XMLHttpRequest'}
url1 = "https://covid19.disiplin.id"

res = requests.get(url1, headers=headers1)

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
   #if province == "Di Yogyakarta":
   #1   province ="DI Yogyakarta"
   #if province == "Dki Jakarta":
   #   province ="DKI Jakarta"
   positive = int(row["properties"]["total_case"])
   death = int(row["properties"]["total_died"])
   cure = int(row["properties"]["total_recover"])
   print(province,positive,death,cure)

    
   cursor.execute("SELECT site,name_ko from province_id_new where province ='%s'" % province)
   row= cursor.fetchone()
   if not row:
      link = "no"
      name_ko = "no"
   else:
      link = row[0]
      name_ko = row[1]



#with open('/root/corona/csv/province.json','w') as fp:
#    fp.write(json.dumps(data))

#Update check


