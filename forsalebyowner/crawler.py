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

def process(line):
    mystr = re.sub('\s+',' ',line)
    mystr = mystr.strip()
    if mystr != '' and mystr != None and type(mystr) != None:
        return mystr

#PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
def crawl(DRIVER_BIN,site_url,site_config):
    #DRIVER_BIN = "../chromedriver"
    driver = webdriver.Chrome(DRIVER_BIN)
    urls=[]
    driver.get(site_url)
    elems = driver.find_elements_by_xpath("//div[@class='estate-info']//a")
    for elem in elems:
        if not 'newConstructionListing' in elem.get_attribute("href") and not 'foreclosureListing' in elem.get_attribute("href"):
            urls.append(elem.get_attribute("href"))
    while(1):
        #
        nextpage = driver.find_elements_by_class_name("pager-nav_next")
        if nextpage:
            #
            nextpage[0].click()
            elems = driver.find_elements_by_xpath("//div[@class='estate-info']//a")
            for elem in elems:
                if not 'newConstructionListing' in elem.get_attribute("href") and not 'foreclosureListing' in elem.get_attribute("href"):
                    urls.append(elem.get_attribute("href"))
        else:
            break;

    fsbo_data = []

    for idx,url in enumerate(urls):
        
        fsbo_obj = {}

        driver.get(url)
        sel = Selector(text=driver.page_source)
        propertyAddress = ''
        propertyAddress = propertyAddress + " " + sel.xpath('//span[@itemprop="streetAddress"]//text()').extract_first()
        propertyAddress = propertyAddress + " " + sel.xpath('//span[@itemprop="addressLocality"]//text()').extract_first()
        propertyAddress = propertyAddress + " " + sel.xpath('//span[@itemprop="addressRegion"]//text()').extract_first()
        propertyAddress = propertyAddress + " " +sel.xpath('//span[@itemprop="postalCode"]//text()').extract_first()
        fsbo_obj["propertyAddress"] = propertyAddress.strip()

        propertyDetail = county = sel.xpath('//*[contains(@class, "list-inline--with-delimiters")]//text()').extract()
        propertyDetails = [process(prodetail) for prodetail in propertyDetail]
        property_dict = {}
        property_dict["bedrooms"] = propertyDetails[6]
        property_dict["bathrooms"] = propertyDetails[11]
        property_dict["bathrooms"] = property_dict["bathrooms"].replace('baths','').strip()
        fsbo_obj["price"] = propertyDetails[2]
        fsbo_obj["url"] = url


        listing = sel.xpath('//ul[@class="list-inline"]//text()').extract()
        list = [process(list) for list in listing]
        listing_id = [x for x in list if x is not None]
        property_dict["listing_id"] = listing_id[5]

        listingFact = sel.xpath('//div[@id="listing-facts"]//text()').extract()
        listingFacts = [process(listFact) for listFact in listingFact]
        listFacts = [x for x in listingFacts if x is not None]
        for list in listFacts:
            if 'Square Feet:' in list:
                property_dict["sq_feet"] = list.split(':')[1].strip()
            elif 'Built in:' in list:
                property_dict["yearBuild"] = list.split(':')[1].strip()
            elif 'Structure Type:' in list:
                property_dict["type"] = list.split(':')[1].strip()
            elif 'Lot Size:' in list:
                property_dict["lot_size"] = list.split(':')[1].strip()
            elif 'Bathrooms:' in list:
                property_dict["bathrooms"] = list.split(':')[1].strip()
            elif 'Square Feet:' in list:
                property_dict["sq_feet"] = list.split(':')[1].strip()

        fsbo_obj["propertyDetails"] = property_dict


        ownerPhone = sel.xpath('//div[@id="contact"]//span//text()').extract()
        fsbo_obj["ownerPhone"] = ownerPhone[1] if len(ownerPhone)>1 else ''
        fsbo_data.append(fsbo_obj)
    return fsbo_data


    driver.quit()
