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
w_positive = w_positive.replace(" ", "").replace(",",".")
w_death= world.find(text="Deaths:").find_next("div","maincounter-number").find('span').get_text().replace(",",".")
w_cure= world.find(text="Recovered:").find_next("div","maincounter-number").find('span').get_text().replace(",",".")

positive = wiki.find(text="Confirmed cases")
positive_n = positive.find_next("td").get_text().replace(",","")
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
yesterday = date.today() - timedelta(1)

db = sqlite3.connect("corona.db")
cursor =db.cursor()

cursor.execute("SELECT positive,cure,death,w_positive,w_cure,w_death from total where date ='%s'" % yesterday)
row = cursor.fetchone()
positive_y = row[0]
cure_y = row[1]
death_y = row[2]
w_positive_y = row[3]
w_cure_y = row[4]
w_death_y = row[5]

positive_p = int(positive_n) - positive_y
cure_p = int(cure_n) - cure_y
death_p = int(death_n) - death_y

w_positive = w_positive.replace(".", "")
w_death= w_death.replace(".","")
w_cure= w_cure.replace(".","")
w_positive_p = int(w_positive) - w_positive_y
w_cure_p = int(w_cure) - w_cure_y
w_death_p = int(w_death) - w_death_y

cursor.execute("SELECT positive,cure,death,w_positive,w_cure,w_death from total where date ='%s'" % today)
row= cursor.fetchone()

if not row:
      cursor.execute("INSERT INTO total(date) VALUES('%s')" % today)
      db.commit()

cursor.execute('UPDATE total SET positive=?, positive_p=?, cure=?, death=?, w_positive=?, w_death=?, w_cure=? WHERE Date=?',(positive_n, positive_p, cure_n, death_n, w_positive, w_death, w_cure, today))
db.commit()

data = {
   'positif' : positive_n,
   'positif_p' : positive_p,
   'sembuh' : cure_n,
   'sembuh_p' : cure_p,
   'kematian' : death_n,
   'kematian_p' : death_p,
   'w_positif' : w_positive,
   'w_positif_p' : w_positive_p,
   'w_kematian' : w_death,
   'w_kematian_p' : w_death_p,
   'w_sembuh' : w_cure,
   'w_sembuh_p' : w_cure_p,
   'date' : now.strftime('%Y-%m-%d %H:%M')+' WIB'
}

with open('./csv/api_world_id.json', 'w', encoding="utf-8") as make_file:
    json.dump(data, make_file, ensure_ascii=False)

#json_data =json.dumps(data)
#print(json_data)

