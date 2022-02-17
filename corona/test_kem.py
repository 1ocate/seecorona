import json
import sqlite3
import requests
from bs4 import BeautifulSoup
from datetime import date, timedelta, datetime

res = requests.get('https://kemkes.go.id')

# print(res.content)
kemkes = BeautifulSoup(res.content, 'html.parser')

 



t_diperiksa = kemkes.find(text="Jumlah orang yang diperiksa")
t_diperiksa_n = t_diperiksa.find_next("td").find_next("td").get_text()

negatif = kemkes.find(text="Negatif COVID-19")
negatif_n = negatif.find_next("td").find_next("td").get_text()

s_diperiksa = kemkes.find(text="Proses Pemeriksaan")
s_diperiksa_n = s_diperiksa.find_next("td").find_next("td").get_text()

now = datetime.now()

today = date.today()
yesterday = date.today() - timedelta(1)

#db = sqlite3.connect("corona.db")
#cursor =db.cursor()
#
#cursor.execute("SELECT positive,cure,death from total where date ='%s'" % yesterday)
#row = cursor.fetchone()
#positive_y = row[0]
#cure_y = row[1]
#death_y = row[2]
#positive_p = int(positive_n) - positive_y
#cure_p = int(cure_n) - cure_y
#death_p = int(death_n) - death_y

data = {
   't_diperiksa' : t_diperiksa_n,
   'negatif' : negatif_n,
   's_diperiksa' : s_diperiksa_n,
   'date' : now.strftime('%Y-%m-%d %H:%M')+' WIB'
}

json_data =json.dumps(data)
print(json_data)

#t_diperiksa_n = t_diperiksa_n.replace(".","")
negatif_n = negatif_n.replace(".","")
s_diperiksa_n = s_diperiksa_n.replace(".","")

db = sqlite3.connect("corona.db")
cursor = db.cursor()
cursor.execute('UPDATE total SET "check"=?, negative=?, process=?, WHERE Date=?',(t_diperiksa_n, negatif_n, s_diperiksa_n, today))
db.commit()
