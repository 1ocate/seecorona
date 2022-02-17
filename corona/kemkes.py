import json
import sqlite3
import requests
from bs4 import BeautifulSoup
from datetime import date, timedelta, datetime

kemkes = requests.get('https://covid19.disiplin.id')
kemkes_data = BeautifulSoup(res.content, 'html.parser')
checked = int(kemkes.find(text="Kasus dg Spesimen Diperiksa").parent.find_previous('h4').get_text().replace('.',''))


