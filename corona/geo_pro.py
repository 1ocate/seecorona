import json
import urllib.request
import requests
import sqlite3
from bs4 import BeautifulSoup
from datetime import date, timedelta, datetime

#url = "https://api.kawalcorona.com/indonesia/provinsi" 
#url = "https://services5.arcgis.com/VS6HdKS0VfIhv8Ct/arcgis/rest/services/COVID19_Indonesia_per_Provinsi/FeatureServer/0/query?f=json&where=(Kasus_Posi%20%3C%3E%200)%20AND%20(Provinsi%20%3C%3E%20%27Indonesia%27)&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=Kasus_Posi%20desc&resultOffset=0&resultRecordCount=100&resultType=standard&cacheHint=true"

#request= requests.get(url).status_code
#if request == 200:
#    data = requests.get(url).json()
#else:
#    print ('error')
#    quit()

row_p = []
row_p_ko = []
today = date.today()
yesterday = date.today() - timedelta(1)

db = sqlite3.connect("./corona/corona.db")
cursor =db.cursor()

cursor.execute("SELECT province,positive,death from province where date ='%s'" % today )
rows= cursor.fetchall()
#data_pro = data["features"]
#for rows in data_pro:
for row in rows:
    #row = rows["attributes"]
    #province= row["Provinsi"]
    #if province == "Daerah Istimewa Yogyakarta":
    #  province ="DI Yogyakarta" 
    #positive= row["Kasus_Posi"]
    #death= row["Kasus_Meni"] 
    province= row[0]
    positive= row[1]
    death= row[2] 
    if not death:
     death=0

    cursor.execute("SELECT iso,name_ko from province_id_new where province ='%s'" % province)
    row= cursor.fetchone()
    if not row:
      iso = "no"
    else:
      iso = row[0]
      province_ko = row[1]

    row_p.append({ "c":[{"v":iso,"f":province},{"v":positive},{"v":death}]})
    row_p_ko.append({ "c":[{"v":iso,"f":province_ko},{"v":positive},{"v":death}]})


data={
	"cols": [
        {"id":"Country","label":"Country","pattern":"","type":"string"},
        {"id":"Positif","label":"positif","pattern":"","type":"number"},
        {"id":"Kematian","label":"kematian","pattern":"","type":"number"}
        ],
        "rows": row_p
        
}


data_ko={
        "cols": [
        {"id":"Country","label":"Country","pattern":"","type":"string"},
        {"id":"Positif","label":"확진자","pattern":"","type":"number"},
        {"id":"Kematian","label":"사망자","pattern":"","type":"number"}
        ],
        "rows": row_p_ko

}

with open('./corona/csv/geo_pro.json','w') as fp:
    fp.write(json.dumps(data))
with open('./corona/csv/geo_pro_ko.json','w') as fp:
    fp.write(json.dumps(data_ko))
