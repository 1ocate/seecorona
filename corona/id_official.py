import json
import urllib.request
import requests
import sqlite3
from bs4 import BeautifulSoup
from datetime import date, timedelta, datetime

today = date.today()
yesterday = date.today() - timedelta(1)


url_off = "https://data.covid19.go.id/public/api/update.json"

request_off= requests.get(url_off).status_code

if request_off == 200:
    data_off = requests.get(url_off).json()
else:
    print ('error off data')
    quit()
data_off_total = data_off["update"]["total"]

i_checked = data_off["data"]["total_spesimen"]
i_postive = data_off_total["jumlah_positif"]
i_cure = data_off_total["jumlah_sembuh"]
i_death = data_off_total["jumlah_meninggal"]
print(i_checked,i_postive,i_cure,i_death)


