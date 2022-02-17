import json
import urllib.request
import requests
import sqlite3
from bs4 import BeautifulSoup
from datetime import date, timedelta, datetime

today = date.today()
yesterday = date.today() - timedelta(1)

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
    quit()



