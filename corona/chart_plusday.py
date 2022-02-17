import json
import sqlite3
from datetime import date, timedelta, datetime
import telegram

#Telegram

TELEGRAM_TOKEN = 'secret'

bot = telegram.Bot(token=TELEGRAM_TOKEN)
chat_id = 'secret'

#Date

today = date.today()
yesterday = date.today() - timedelta(1)


date =[]
positive=[]
process=[]
positive_p =[]
death =[]
death_p =[]
cure =[]
cure_p =[]
checked =[]
checked_p =[]
negative =[]
negative_p =[]
positive_per =[]
positive_per_d =[]

#Set database

db = sqlite3.connect("/root/corona/corona.db")
cursor =db.cursor()

#Update check
update_file ='positive_day.json'
cursor.execute('SELECT date from update_file where date =? and name =?',(today,update_file))
row= cursor.fetchone()
if row:
   quit()
  

cursor.execute('SELECT positive,positive_p,death,death_p,cure,cure_p,checked,checked_p,date from total')
#cursor.execute('SELECT positive,positive_p,death,death_p,cure,cure_p,checked,checked_p,date from total where date < "2020-08-25"')
rows = cursor.fetchall() 
for row in rows:
  #print(row) 
  positive.append(row[0])
  positive_p.append(row[1])
  death.append(row[2])
  death_p.append(row[3])
  cure.append(row[4])
  cure_p.append(row[5])
  checked.append(row[6])
  checked_p.append(row[7])
  date.append(row[8])
  process_r = row[0] - row[2] - row[4]
  process.append(process_r)
  negative_r = row[6] - row[0]
  negative.append(negative_r)
  negative_p_r = row[7] - row[1]
  negative_p.append(negative_p_r)
  positive_per_r= (row[0]/row[6])*100
  positive_per_r=round(positive_per_r,2)
  positive_per.append(positive_per_r)
  if row[7] == 0:
     positive_per_p_r= 0
  else:
     positive_per_p_r= (row[1]/row[7])*100
     positive_per_p_r=round(positive_per_p_r,2)
  positive_per_d.append(positive_per_p_r)

data={"positive":positive,"positive_p":positive_p,"process":process,"death":death,"death_p":death_p,"cure":cure,"cure_p":cure_p,"checked":checked,"checked_p":checked_p,"negative":negative,"negative_p":negative_p,"positive_per":positive_per,"positive_per_p":positive_per_d,"date":date}

# if update write json file

cursor.execute("SELECT checked_p from total where date ='%s'" % today)
row = cursor.fetchone() 


if row[0] > 0:
    with open(f'/root/corona/csv/{update_file}','w') as fp:
     fp.write(json.dumps(data))

    cursor.execute('INSERT INTO update_file (name,date) VALUES(?,?)',(update_file,today))
    db.commit()
    bot.sendMessage(chat_id=chat_id, text='데이터 업데이트 완료')

