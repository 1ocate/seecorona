import urllib.request
import requests
import sqlite3
import json
from bs4 import BeautifulSoup
from datetime import date, timedelta, datetime

#world_url = requests.get('https://www.worldometers.info/coronavirus/')
#world_data = BeautifulSoup(world_url.content, 'html.parser')
world_data = BeautifulSoup(open("world.html"), "html.parser")
now =datetime.now()
today = date.today()
yesterday = date.today() - timedelta(1)

db = sqlite3.connect("corona.db")
cursor = db.cursor()
nation = []


table = world_data.find(id="main_table_countries_today").find("tbody")
trs = table.find_all("tr")
for tr in trs[8:]:
  tds = tr.find_all("td")
  world= tds[0].get_text().strip()
  positive = tds[1].get_text().replace(",","")
  death = tds[3].get_text().replace(" ","").replace(",","")
  if not death:
     death=0
  cure = tds[5].get_text().replace(",","")
  if not cure:
     cure="0"
  land = tds[12].get_text()
  cursor.execute('SELECT positive,cure,death from world where date =? and world =?',(yesterday,world))
  row= cursor.fetchone()
  if row:
     positive_y = row[0]
     cure_y = row[1]
     death_y = row[2]
     positive_p = int(positive) - positive_y
     if cure=="N/A":
       cure_p = 0
     else:
       cure_p = int(cure) - cure_y

     death_p = int(death) - death_y
  else:
     #positive_p = positive
     positive_p = 0
     #cure_p = cure
     cure_p = 0
     #death_p = death
     death_p = 0
  cursor.execute('SELECT positive,cure,death from world where date =? and world =?',(today,world))
  row= cursor.fetchone()
  if not row:
     cursor.execute('INSERT INTO world (world,date) VALUES(?,?)',(world,today))

  cursor.execute('UPDATE world SET positive=?, cure=?, death=? WHERE Date=? and world=?',(positive, cure, death, today, world))
  db.commit()

  cursor.execute("SELECT name_ko from world_iso where name ='%s'" % world)
  row_ko= cursor.fetchone()
  if row_ko:
     name_ko= row_ko[0]
  if not row_ko:
     name_ko = world
  #quit()

  nation.append({'World':world, 'World_ko':name_ko, 'Positive': positive, 'Positive_p':positive_p, 'Cure': cure, 'Cure_p':cure_p, 'Death':death, 'Death_p':death_p})
    #ID.append({'Id':id, 'Province':province, 'Positive': positive, 'Positive_p':str(positive_p), 'Cure': cure, 'Cure_p':str(cure_p), 'Death':death, 'Death_p':str(death_p)})

w_positive= world_data.find(text="Coronavirus Cases:").find_next("div","maincounter-number").find('span').get_text()
w_positive = w_positive.replace(" ", "").replace(",","")
w_death= world_data.find(text="Deaths:").find_next("div","maincounter-number").find('span').get_text().replace(",","")
w_cure= world_data.find(text="Recovered:").find_next("div","maincounter-number").find('span').get_text().replace(",","")
indonesia= world_data.find(id="nav-tabContent").find(text="Indonesia").parent
#id_check= indonesia.parent.find_next_siblings()[9].text.replace(",","")
i_positive= indonesia.parent.find_next_siblings()[0].text.replace(",","")
i_death= indonesia.parent.find_next_siblings()[2].text.replace(",","")
i_cure= indonesia.parent.find_next_siblings()[4].text.replace(",","")

cursor.execute("SELECT positive,cure,death,w_positive,w_cure,w_death from total where date ='%s'" % yesterday)
row = cursor.fetchone()
i_positive_y = row[0]
i_cure_y = row[1]
i_death_y = row[2]
w_positive_y = row[3]
w_cure_y = row[4]
w_death_y = row[5]

i_positive_p = int(i_positive) - i_positive_y
i_cure_p = int(i_cure) - i_cure_y
i_death_p = int(i_death) - i_death_y

w_positive_p = int(w_positive) - w_positive_y
w_cure_p = int(w_cure) - w_cure_y
w_death_p = int(w_death) - w_death_y

cursor.execute("SELECT positive,cure,death,w_positive,w_cure,w_death from total where date ='%s'" % today)
#cursor.execute("SELECT positive,cure,death from total where date ='%s'" % today)
row= cursor.fetchone()

if not row:
      cursor.execute("INSERT INTO total(date) VALUES('%s')" % today)
      db.commit()

cursor.execute('UPDATE total SET positive=?, positive_p=?, cure=?, cure_p=?, death=?, death_p=?, w_positive=?, w_death=?, w_cure=?  WHERE Date=?',(i_positive, i_positive_p, i_cure, i_cure_p, i_death, i_death_p, w_positive, w_death, w_cure, today))
#cursor.execute('UPDATE total SET positive=?, positive_p=?, cure=?, cure_p=?, death=?, death_p=?, w_positive=?, w_death=?, w_cure=?, "check"=? WHERE Date=?',(i_positive, i_positive_p, i_cure, i_cure_p, i_death, i_death_p, w_positive, w_death, w_cure, id_check, today))
db.commit()

data={ 
    'data':nation,
    'positif' : i_positive,
    'positif_p' : i_positive_p,
    'sembuh' : i_cure,
    'sembuh_p' : i_cure_p,
    'kematian' : i_death,
    'kematian_p' : i_death_p,
    'w_positif' : w_positive,
    'w_positif_p' : w_positive_p,
    'w_kematian' : w_death,
    'w_kematian_p' : w_death_p,
    'w_sembuh' : w_cure,
    'w_sembuh_p' : w_cure_p,
    'date' : now.strftime('%Y-%m-%d %H:%M')

}

with open('./csv/world.json','w') as fp:
    fp.write(json.dumps(data))
