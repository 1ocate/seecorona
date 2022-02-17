import json
import urllib.request
import requests
import sqlite3
from bs4 import BeautifulSoup
from datetime import date, timedelta, datetime

today = date.today()
yesterday = date.today() - timedelta(1)


url_kum = "https://spreadsheets.google.com/feeds/cells/1JSf5QUZZzxMHJN8YZn6cz8SCI_2KDt5FqL4inVEh7bk/o8vzu7i/public/values?alt=json"

request_kum= requests.get(url_kum).status_code

if request_kum == 200:
    data_kum = requests.get(url_kum).json()
else:
    print ('error kum data')
    quit()

rows_kum = data_kum["feed"]["entry"]
for row in rows_kum[14:-2]:

 cell = row["gs$cell"]["col"]
 row_cell = row["gs$cell"]["row"]
 if cell == "2" and row_cell =="8":
  i_positive_kum = int(row["content"]["$t"].replace(",",""))

 if cell == "2" and row_cell =="9":
   i_cure_kum = int(row["content"]["$t"].replace(",",""))

 if cell == "2" and row_cell =="10":
  i_death_kum = int(row["content"]["$t"].replace(",",""))

print(i_cure_kum)
print(i_positive_kum)


