import json
import sqlite3
import requests
from bs4 import BeautifulSoup
from datetime import date, timedelta
 
 
 
res1 = requests.get('https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_Indonesia')
res2 = requests.get('https://kemkes.go.id')

# print(res.content)
wiki = BeautifulSoup(res1.content, 'html.parser')
kemkes = BeautifulSoup(res2.content, 'html.parser')

 

positive = wiki.find(text="Confirmed cases")
positive_n = positive.find_next("td").get_text()

cure = wiki.find(text="Recovered")
cure_n = cure.find_next("td").get_text()

death = wiki.find(text="Deaths")
death_n = death.find_next("td").get_text()

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

today = date.today()
yesterday = date.today() - timedelta(1)

db = sqlite3.connect("corona.db")
cursor =db.cursor()
cursor.execute("SELECT positive,cure,death from total where date ='%s'" % yesterday)
row = cursor.fetchone()
positive_y = row[0]
cure_y = row[1]
death_y = row[2]
print (positive_y)
#positive_p = int(positive_n) - positive_y
#cure_p = int(cure_n) - cure_y
#death_p = int(death_n) - death_y



