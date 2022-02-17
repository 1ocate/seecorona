import json
import urllib.request
import requests
import sqlite3
from bs4 import BeautifulSoup
from datetime import date, timedelta, datetime

#url = "https://api.kawalcorona.com/indonesia/provinsi" 
url = "https://services5.arcgis.com/VS6HdKS0VfIhv8Ct/arcgis/rest/services/COVID19_Indonesia_per_Provinsi/FeatureServer/0/query?f=json&where=(Kasus_Posi%20%3C%3E%200)%20AND%20(Provinsi%20%3C%3E%20%27Indonesia%27)&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=Kasus_Posi%20desc&resultOffset=0&resultRecordCount=100&resultType=standard&cacheHint=true"

request= requests.get(url).status_code
if request == 200:
    data = requests.get(url).json()
else:
    print ('error')
    quit()

ID = []
ID_Y = []
today = date.today()
yesterday = date.today() - timedelta(1)
day_b_yesterday = date.today() - timedelta(2)
#yesterday = date.today() - timedelta(2)

db = sqlite3.connect("/root/corona/corona.db")
cursor =db.cursor()

data_pro = data["features"]

for rows in data_pro:
    row = rows["attributes"]
    province= row["Provinsi"]
    if province == "Daerah Istimewa Yogyakarta":
      province ="DI Yogyakarta" 
    positive= row["Kasus_Posi"]
    cure= row["Kasus_Semb"]
    if not cure:
     cure=0
    death= row["Kasus_Meni"] 
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
    cursor.execute('SELECT positive,cure,death from province where date =? and province =?',(today,province))
    row= cursor.fetchone()
    if not row:
      cursor.execute('INSERT INTO province (province,date) VALUES(?,?)',(province,today))

    cursor.execute('UPDATE province SET positive=?, cure=?, death=? WHERE Date=? and province=?',(positive, cure, death, today, province))
    db.commit()

    cursor.execute("SELECT site,name_ko from province_id_new where province ='%s'" % province)
    row= cursor.fetchone()
    if not row:
      link = "#"
      name_ko = "조사중"
    else:
      link = row[0]
      name_ko = row[1]
	

    ID.append({'Province':province, 'Positive': positive, 'Positive_p':positive_p, 'Cure': cure, 'Cure_p':cure_p, 'Death':death, 'Death_p':death_p, 'link':link, 'Province_ko':name_ko})
    #ID.append({'Id':id, 'Province':province, 'Positive': positive, 'Positive_p':str(positive_p), 'Cure': cure, 'Cure_p':str(cure_p), 'Death':death, 'Death_p':str(death_p), 'link':link 'Province_ko':name_ko})

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
