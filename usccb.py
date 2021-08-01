import time
from time import sleep
import json
from selenium import webdriver
import datetime
import os

driver = webdriver.Chrome('./chromedriver')

os.makedirs("./bible", exist_ok=True)

def getText(url, y, m, d):
  driver.get(url)
  children = []
  areChildren = True
  i=1
  while areChildren: 
    try:
      x = driver.find_element_by_css_selector(f".wr-block:nth-child({i})") 
      children.append(x.get_attribute("innerText")) 
      i = i+1
    except:
      areChildren = False
  with open(f'./text/{y}-{m}-{d}.txt', 'w') as f:
    f.writelines(children)

def getYMD(daysAgo):
  dt = datetime.datetime.now() - datetime.timedelta(days=daysAgo)
  y,m,d = dt.year, dt.month, dt.day
  return y,m,d

def getUrl(y,m,d):
  url = f"https://bible.usccb.org/bible/readings/{m:02d}{d:02d}{str(y)[2:]}.cfm"
  return url

if __name__ == "__main__":
  for i in range(365*3):
    y,m,d = getYMD(i)
    url = getUrl(y,m,d)
    getText(url,y,m,d)
    sleep(1) # be friendly-- take your time :)
  driver.close()
