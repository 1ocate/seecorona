import json
import sqlite3
import requests
from bs4 import BeautifulSoup
from datetime import date, timedelta, datetime

res1 = requests.get('https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_Indonesia')
res2 = requests.get('https://www.worldometers.info/coronavirus/')

# print(res.content)
wiki = BeautifulSoup(res1.content, 'html.parser')
world = BeautifulSoup(res2.content, 'html.parser')

w_positive= world.find(text="Coronavirus Cases:").find_next("div","maincounter-number").find('span').get_text()
w_positive = w_positive.replace(" ", "").replace(",","")
w_death= world.find(text="Deaths:").find_next("div","maincounter-number").find('span').get_text().replace(",","")
w_cure= world.find(text="Recovered:").find_next("div","maincounter-number").find('span').get_text().replace(",","")

positive = wiki.find(text="Confirmed cases")
positive_n = positive.find_next("td").get_text()
positive_f = positive_n.find("[")

if positive_f != -1:
 positive_n = positive_n[0:positive_f]

cure = wiki.find(text="Recovered")
cure_n = cure.find_next("td").get_text()
cure_f = cure_n.find("[")

if cure_f != -1:
 cure_n = cure_n[0:cure_f]

death = wiki.find(text="Deaths")
death_n = death.find_next("td").get_text()

death_f = death_n.find("[")

if death_f != -1:
  death_n = death_n[0:death_f]

#process_n = int(positif_n) - int(cure_n) - int(death_n)

#diperiksa = kemkes.find(text="Jumlah orang yang diperiksa")
#diperiksa_n = diperiksa.find_next("td").find_next("td").get_text()

#negatif = kemkes.find(text="Negatif COVID-19")
#negatif_n = negatif.find_next("td").find_next("td").get_text()

#testing = kemkes.find(text="Proses Pemeriksaan")
#testing_n = testing.find_next("td").find_next("td").get_text()

#print(positif,positif_n )
#print(cure,cure_n )
#print(death,death_n )
#print("Mati,Pulih,Perawatan")
#print( "{},{},{}".format(death_n,cure_n,process_n) )
#print(diperiksa_n,negatif_n,testing_n)
now =datetime.now()

today = date.today()
nextday = date.today() + timedelta(1)
yesterday = date.today() - timedelta(1)

db = sqlite3.connect("corona.db")
cursor =db.cursor()

cursor.execute("SELECT positive from total where date ='%s'" % yesterday)
row = cursor.fetchone()
positive_y = row[0]

positive_p = int(positive_n) - positive_y

#cursor.execute("update  set positive=positive_n where date ='%s'" % today)
cursor.execute('UPDATE total SET positive=?, positive_p=?, cure=?, death=?, w_positive=?, w_death=?, w_cure=? WHERE Date=?',(positive_n, positive_p, cure_n, death_n, w_positive, w_death, w_cure, today))
db.commit()

cursor.execute("INSERT INTO total(date) VALUES('%s')" % nextday)
db.commit()
