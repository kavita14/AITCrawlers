# importing the requests library
import requests
from parsel import Selector
from HTMLParser import HTMLParser
from selenium import webdriver
from time import sleep
from lxml import html
from datetime import datetime
from selenium.webdriver.common.keys import Keys
import re

base_url = "https://www.auctionzip.com/cgi-bin/auctionlist.cgi?txtSearchZip=37205&txtSearchRadius=30&idxSearchCategory=30736&gid=0&year=2019&month=1&day=19&txtSearchKeywords=&showlive=1"
urls = []
driver = webdriver.Chrome('/Users/kavitasharma/Downloads/chromedriver')
def process(line):
    mystr = re.sub('\s+',' ',line)
    mystr = mystr.strip()
    if mystr != '' and mystr != None and type(mystr) != None:
        return mystr

currentDay = datetime.now().day
currentMonth = datetime.now().month
currentYear = datetime.now().year

driver.get(base_url)
sleep(2)
sel = Selector(text=driver.page_source)
auctionList = driver.find_elements_by_xpath('//a[@class="az_title_href"]')
for auc in auctionList:
    listhref = auc.get_attribute("href")
    if 'Listings' in listhref:
        urls.append(listhref)

print(urls)

for url in urls:
    driver.get(url)
    sleep(2)
    sel = Selector(text=driver.page_source)
    
