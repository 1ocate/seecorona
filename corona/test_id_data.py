import json
import urllib.request
import requests
import sqlite3
from bs4 import BeautifulSoup
from datetime import date, timedelta, datetime

#url = "https://api.kawalcorona.com/indonesia/provinsi"
url = "https://services5.arcgis.com/VS6HdKS0VfIhv8Ct/arcgis/rest/services/Statistik_Perkembangan_COVID19_Indonesia/FeatureServer/0/query?f=json&where=Tanggal%3Ctimestamp%20%272020-05-02%2017:00:00%27%20&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=Tanggal%20asc&resultOffset=0&resultRecordCount=100&resultType=standard&cacheHint=true"

request= requests.get(url).status_code
if request == 200:
    data = requests.get(url).json()
else:
    print ('error')
    quit()

ID = []
today = date.today()
yesterday = date.today() - timedelta(1)

db = sqlite3.connect("corona.db")
cursor =db.cursor()

data_pro = data["features"]

for rows in data_pro:
    row = rows["attributes"]
    hari = row["Hari_ke"]
    test = row["Jumlah_Kasus_Diperiksa_Spesimen"]
    test_total = row["Jumlah_Spesimen_Diperiksa"]
    
    negative = row ["Jumlah_Negatif"]
    #print(hari,test,negative)
    print(test_total)
