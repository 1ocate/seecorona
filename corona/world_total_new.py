import urllib.request
import requests
import sqlite3
import json
from bs4 import BeautifulSoup
from datetime import date, timedelta, datetime

#world_url = requests.get('https://www.worldometers.info/coronavirus/')
#world_data = BeautifulSoup(world_url.content, 'html.parser')
world_data = BeautifulSoup(open("/root/corona/world.html"), "html.parser")
#kemkes = requests.get('https://covid19.disiplin.id')
#kemkes_data = BeautifulSoup(kemkes.content, 'html.parser')

#kemkes_checked = int(kemkes_data.find(text="Kasus dg Spesimen Diperiksa").parent.find_previous('h4').get_text().replace('.',''))
#kemkes_negative = int(kemkes_data.find(text="Kasus dg Spesimen Diperiksa").parent.find_next('h4').get_text().replace('.',''))
now =datetime.now()
today = date.today()
yesterday = date.today() - timedelta(1)
day_b_yesterday = date.today() - timedelta(2)

db = sqlite3.connect("/root/corona/corona.db")
cursor = db.cursor()
nation = []
nation_yes = []
total = []


table = world_data.find(id="main_table_countries_today").find("tbody")
trs = table.find_all("tr")
for tr in trs[8:]:
  tds = tr.find_all("td")
  world= tds[1].get_text().strip()
  positive = tds[2].get_text().replace(",","")
  death = tds[4].get_text().replace(" ","").replace(",","")
  if not death:
     death=0
  cure = tds[6].get_text().replace(",","")
  if not cure:
     cure="0"
  land = tds[13].get_text()
  cursor.execute('SELECT positive,cure,death from world where date =? and world =?',(yesterday,world))
  row= cursor.fetchone()
  if row:
     positive_y = row[0]
     cure_y = row[1]
     death_y = row[2]
     positive_p = int(positive) - positive_y
     if cure=="N/A" or cure_y=="N/A":
       cure_p = 0
     else:
     #  print(cure_y)
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

#yesterday_data

cursor.execute("SELECT world,positive,cure,death from world where date='%s'" % yesterday)
rows= cursor.fetchall()
for row in rows:
  world= row[0]
  positive = row[1]
  death = row[3]
  if not death:
     death=0
  cure = row[2]
  if not cure:
     cure="0"
  cursor.execute('SELECT positive,cure,death from world where date =? and world =?',(day_b_yesterday,world))
  row= cursor.fetchone()
  if row:
     positive_y = row[0]
     cure_y = row[1]
     death_y = row[2]
     positive_p = int(positive) - positive_y
     if cure=="N/A" or cure_y=="N/A":
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
  #cursor.execute('SELECT positive,cure,death from world where date =? and world =?',(today,world))
  #row= cursor.fetchone()
  #if not row:
  #   cursor.execute('INSERT INTO world (world,date) VALUES(?,?)',(world,today))

  #cursor.execute('UPDATE world SET positive=?, cure=?, death=? WHERE Date=? and world=?',(positive, cure, death, today, world))
  #db.commit()

  cursor.execute("SELECT name_ko from world_iso where name ='%s'" % world)
  row_ko= cursor.fetchone()
  if row_ko:
     name_ko= row_ko[0]
  if not row_ko:
     name_ko = world
  #quit()

  nation_yes.append({'World':world, 'World_ko':name_ko, 'Positive': positive, 'Positive_p':positive_p, 'Cure': cure, 'Cure_p':cure_p, 'Death':death, 'Death_p':death_p})
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

id_url = f"https://services5.arcgis.com/VS6HdKS0VfIhv8Ct/arcgis/rest/services/Statistik_Perkembangan_COVID19_Indonesia/FeatureServer/0/query?f=json&where=Tanggal%3Ctimestamp%20%27{today}%2017:00:00%27%20AND%20Jumlah_Kasus_Kumulatif%3E%270%27&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=Tanggal%20desc&resultOffset=0&resultRecordCount=1&resultType=standard&cacheHint=true"

id_request= requests.get(id_url).status_code


if id_request == 200:
    id_data = requests.get(id_url).json()
else:
    print ('error access id data')
    quit()

#i_row = id_data["features"][0]['attributes']
#i_positive= i_row['Jumlah_Kasus_Kumulatif']
#i_cure=i_row['Jumlah_Pasien_Sembuh']
#i_death=i_row['Jumlah_Pasien_Meninggal']
#i_checked=i_row['Jumlah_Kasus_Diperiksa_Spesimen']

url_off = "https://data.covid19.go.id/public/api/update.json"

request_off= requests.get(url_off).status_code

if request_off == 200:
    data_off = requests.get(url_off).json()
else:
    print ('error off data')
    quit()
data_off_total = data_off["update"]["total"]

i_t_checked_off = int(data_off["data"]["total_spesimen"])
i_negative_off = int(data_off["data"]["total_spesimen_negatif"])
i_positive_off = int(data_off_total["jumlah_positif"])
i_cure_off = int(data_off_total["jumlah_sembuh"])
i_death_off = int(data_off_total["jumlah_meninggal"])
i_checked = i_negative_off+i_positive_off
#kemkes_checked = kemkes_negative+i_positive_off
#i_checked = kemkes_checked
#i_checked = i_t_checked_off

#url_kum = "https://spreadsheets.google.com/feeds/cells/1JSf5QUZZzxMHJN8YZn6cz8SCI_2KDt5FqL4inVEh7bk/o8vzu7i/public/values?alt=json"

#request_kum= requests.get(url_kum).status_code

#if request_kum == 200:
#    data_kum = requests.get(url_kum).json()
#else:
#    print ('error kum data')
#    quit()

#rows_kum = data_kum["feed"]["entry"]
#for row in rows_kum[14:-2]:

# cell = row["gs$cell"]["col"]
# row_cell = row["gs$cell"]["row"]
# if cell == "2" and row_cell =="8":
#  i_positive_kum = int(row["content"]["$t"].replace(",",""))

# if cell == "2" and row_cell =="9":
#   i_cure_kum = int(row["content"]["$t"].replace(",",""))

# if cell == "2" and row_cell =="10":
#  i_death_kum = int(row["content"]["$t"].replace(",",""))

#cursor.execute("SELECT positive,cure,death,checked,w_positive,w_cure,w_death from total where date ='%s'" % yesterday)
cursor.execute("SELECT total.positive,total.cure,total.death,total.checked,total.w_positive,total.w_cure,total.w_death,total.checked-total_y.checked as checked_p from total JOIN  total total_y on total.date = date(total_y.date,'+1 days') where total.date ='%s'" % yesterday)
row = cursor.fetchone()
i_positive_y = row[0]
i_cure_y = row[1]
i_death_y = row[2]
i_checked_y = row[3]
w_positive_y = row[4]
w_cure_y = row[5]
w_death_y = row[6]
i_checked_p_y = row[7]

if i_positive_y == int(i_positive):
    i_positive = i_positive_off
   # if i_positive == i_positive_y:
      #i_positive = i_row['Jumlah_Kasus_Kumulatif']
   #   i_positive = i_positive_kum
if i_cure_y == int(i_cure):
    i_cure = i_cure_off
   # if i_cure_y == i_cure:
      #i_cure=i_row['Jumlah_Pasien_Sembuh']
   #   i_cure=i_cure_kum

if i_death_y == int(i_death):
    i_death = i_death_off
   # if i_death_y == i_death:
      #i_death=i_row['Jumlah_Pasien_Meninggal']
   #   i_death=i_death_kum

#if i_checked_y == int(i_checked):
#    i_checked = i_checked_off

i_positive_p = int(i_positive) - i_positive_y
i_cure_p = int(i_cure) - i_cure_y
i_death_p = int(i_death) - i_death_y
i_checked_p = int(i_checked) - i_checked_y

w_positive_p = int(w_positive) - w_positive_y
w_cure_p = int(w_cure) - w_cure_y
w_death_p = int(w_death) - w_death_y

cursor.execute("SELECT positive,cure,death,w_positive,w_cure,w_death from total where date ='%s'" % today)
#cursor.execute("SELECT positive,cure,death from total where date ='%s'" % today)
row= cursor.fetchone()

if not row:
      cursor.execute("INSERT INTO total(date) VALUES('%s')" % today)
      db.commit()

cursor.execute('UPDATE total SET positive=?, positive_p=?, cure=?, cure_p=?, death=?, death_p=?, checked=?, checked_p=?, w_positive=?, w_death=?, w_cure=? WHERE Date=?',(i_positive, i_positive_p, i_cure, i_cure_p, i_death, i_death_p, i_checked, i_checked_p, w_positive, w_death, w_cure, today))
#cursor.execute('UPDATE total SET positive=?, positive_p=?, cure=?, death=?, w_positive=?, w_death=?, w_cure=?, "check"=? WHERE Date=?',(i_positive, i_positive_p, i_cure, i_death, w_positive, w_death, w_cure, id_check, today))
db.commit()

total.append({'name': 'Global','name_ko': '🌐전세계',  'Positive' : w_positive, 'Positive_p' : w_positive_p, 'Cure' : w_cure, 'Cure_p' : w_cure_p, 'Death' : w_death, 'Death_p' : w_death_p, 'Checked':'N/A', 'Checked_p':'0'})
total.append({'name': 'Indonesia','name_ko':'🇮🇩인도네시아' , 'Positive' : i_positive, 'Positive_p' : i_positive_p, 'Cure' : i_cure, 'Cure_p' : i_cure_p, 'Death' : i_death, 'Death_p' : i_death_p, 'Checked':i_checked, 'Checked_p':i_checked_p})

data={ 
    'data':nation,
    'positif' : i_positive,
    'positif_p' : i_positive_p,
    'sembuh' : i_cure,
    'sembuh_p' : i_cure_p,
    'kematian' : i_death,
    'kematian_p' : i_death_p,
    'check_id' : i_checked,
    'check_id_p' : i_checked_p,
    'w_positif' : w_positive,
    'w_positif_p' : w_positive_p,
    'w_kematian' : w_death,
    'w_kematian_p' : w_death_p,
    'w_sembuh' : w_cure,
    'w_sembuh_p' : w_cure_p,
    'check_id_p_y' : i_checked_p_y,
    'date' : now.strftime('%Y-%m-%d %H:%M'),
    'total' : total

}
data_yes={ 
    'data':nation_yes
}

with open('/root/corona/csv/world.json','w') as fp:
    fp.write(json.dumps(data))
with open('/root/corona/csv/world_yes.json','w') as fp:
    fp.write(json.dumps(data_yes))
