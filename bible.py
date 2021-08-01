from time import sleep
from selenium import webdriver
import os

driver = webdriver.Chrome('./chromedriver')

os.makedirs("./bible", exist_ok=True)

def processVerse(verse):
  return verse.get_attribute('innerText')

def getText(url, book, chapter):
  driver.get(url)
  driver.execute_script('''
  verses = document.querySelectorAll(".verse > .txt")
  for(let v of verses){
    for(let c of Array.from(v.children)){
      c.remove()
    }
  }
  ''')
  children = []
  areChildren = True
  verses =  driver.find_elements_by_css_selector(f".verse > .txt") 
  verses = [processVerse(x)+' ' for x in verses]
  if len(verses) > 0:
    with open(f'./bible/{book}_{chapter}.txt', 'w') as f:
      f.writelines(verses)
    return True
  return False

def getUrl(book, chapter):
  url = f"https://bible.usccb.org/bible/{book}/{chapter}"
  return url

#found manually
books = ["genesis", "exodus", "leviticus", "numbers", "deuteronomy", "joshua", "judges", "ruth", "1samuel", "2samuel", "1kings", "2kings", "1chronicles", "2chronicles", "ezra", "nehemiah", "tobit", "judith", "esther", "1maccabees", "2maccabees", "job", "psalms", "proverbs", "ecclesiastes", "songofsongs", "wisdom", "sirach", "isaiah", "jeremiah", "lamentations", "baruch", "ezekiel", "daniel", "hosea", "joel", "amos", "obadiah", "jonah", "micah", "nahum", "habakkuk", "zephaniah", "haggai", "zechariah", "malachi", "matthew", "mark", "luke", "john", "acts", "romans", "1corinthians", "2corinthians", "galatians", "ephesians", "philippians", "colossians", "1thessalonians", "2thessalonians", "1timothy", "2timothy", "titus", "philemon", "hebrews", "james", "1peter", "2peter", "1john", "2john", "3john", "jude", "revelation"]

if __name__ == "__main__":
  for b in books:
    c = 1
    found = True
    while found:
        found = getText(getUrl(b, c), b, c)
        sleep(1) # be friendly-- take your time :)
        c = c+1
        print(b, c, found)
  driver.close()
