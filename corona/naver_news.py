import urllib.request 
from urllib.parse import * 
import requests from bs4 
import BeautifulSoup 
import json
import re 

client_id = "xxxxxxxxxxxx" 
client_secret = "xxxxxxxxxxxx" 
display = "30"

url = "https://openapi.naver.com/v1/search/news.json?query=" + encText + \ "&display=" + str(display) + "&sort=sim"
request = urllib.request.Request(url) 
request.add_header("X-Naver-Client-Id",client_id)
request.add_header("X-Naver-Client-Secret",client_secret)

response = urllib.request.urlopen(request) 
rescode = response.getcode()
if(rescode==200): 
  #response_body_str = response.read().decode('utf-8') 
  response_body_str = response.read().decode('utf-8') 
  json_acceptable_string = response_body_str.replace("'", "\"") response_body = json.loads(response_body_str) title_link = {} for i in range(0, len(response_body['items'])): title_link[response_body['items'][i]['title']] = \ response_body['items'][i]['link'] return title_link else: print("Error Code:" + rescode)

출처: https://koreanfoodie.me/118 [KoreanFoodie's Study]
