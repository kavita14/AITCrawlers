import csv
import json
from parsel import Selector
from time import sleep
from selenium import webdriver
from lxml import html
from selenium.webdriver.common.keys import Keys
import re
import sys
import uuid
import os
from common import parseAddress



parseAddress("H-199 kalibari marg");
exit()

def process(line):
    mystr = re.sub('\s+',' ',line)
    return mystr

#PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
DRIVER_BIN = "/Users/mmt7546/Downloads/chromedriver"
driver = webdriver.Chrome(DRIVER_BIN)
urls=[]

driver.get('https://fsbo.com/listings/search/')
username = driver.find_element_by_name('state')
username.send_keys('Alaska')
sleep(2)

driver.find_element_by_id("advancedSearchForm").submit();
elems = driver.find_elements_by_xpath("//a[text() = 'View Listing Details']")
for elem in elems:
    urls.append(elem.get_attribute("href"))
while(1):
    sleep(2)
    nextpage = driver.find_elements_by_class_name("nextPage")
    if nextpage:
        sleep(2)
        nextpage[0].click()
        elems = driver.find_elements_by_xpath("//a[text() = 'View Listing Details']")
        for elem in elems:
            urls.append(elem.get_attribute("href"))
    else:
        break;

for url in urls:
    sleep(2)
    driver.get(url)
    sel = Selector(text=driver.page_source)
    property_detail = sel.xpath('//*[starts-with(@class, "listing-data")]//tr').extract()
    for tr in property_detail:
        property = Selector(text=tr).xpath('//td//text()').extract()
        print(property)
    property_address = sel.xpath('//*[starts-with(@class, "address-copy")]//span//text()').extract()
    print("property_address")
    parsed_address = [process(address_line) for address_line in property_address]
    print(parsed_address)

    amentites = sel.xpath('//div[starts-with(@class, "amenities")]//li//text()').extract()
    print("amentites")
    parsed_emnties = [process(amenity_line) for amenity_line in amentites]
    print(parsed_emnties)

    owner_detail = experience = sel.xpath('//div[@id="sellerModal"]//text()').extract()

    print("owner detail")
    parsed_emnties = [process(amenity_line) for amenity_line in owner_detail]
    print(parsed_emnties)

    exit()

driver.quit()
