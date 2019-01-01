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
    username = driver.find_element_by_name('state')
    username.send_keys('Tennessee')
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
    fsbo_data = []

    for idx,url in enumerate(urls):
        fsbo_obj = {}
        sleep(2)
        driver.get(url)
        sel = Selector(text=driver.page_source)
        #property_detail_list = []
        property_dict = {}
        property_detail = sel.xpath('//*[starts-with(@class, "listing-data")]//tr').extract()
        for tr in property_detail:

            property = Selector(text=tr).xpath('//td//text()').extract()
            if property[0] == 'Listing ID:':
                property_dict["listing_id"] = property[1]
            elif property[0] == 'Bedrooms:':
                property_dict["bedrooms"] = property[1]
            elif property[0] == 'Bathrooms:':
                property_dict["bathrooms"] = property[1]
            elif property[0] == 'Type:':
                property_dict["type"] = property[1]
            elif property[0] == 'Lot Size:':
                property_dict["lot_size"] = property[1]
            elif property[0] == 'Garage:':
                property_dict["garage"] = property[1]
            elif property[0] == 'Subtype:':
                property_dict["subType"] = property[1]
            elif property[0] == 'Sq. Feet:':
                property_dict["sq_feet"] = property[1]
            elif property[0] == 'Year Built:':
                property_dict["yearBuild"] = property[1]
            elif property[0] == 'School District:':
                property_dict["schoolDistrict"] = property[1]

            #property_detail_list.append(property_dict)
            #print(property)
        property_address = sel.xpath('//*[starts-with(@class, "address-copy")]//span[@class="address"]//text()').extract()
        print("property_address")
        parsed_address = [process(address_line) for address_line in property_address]
        print(parsed_address)
        fsbo_obj["propertyDetails"] = property_dict
        fsbo_obj["propertyAddress"] = " ".join(parsed_address)
        fsbo_obj["url"] = url
        fsbo_obj["price"] = sel.xpath('//*[starts-with(@class, "address-copy")]//span[starts-with(@class, "price")]//text()').extract_first()
        county = sel.xpath('//*[starts-with(@class, "address-copy")]/text()').extract()
        parsed_county = [process(coun) for coun in county]
        [x for x in parsed_county if x is not None]
        county = [x for x in parsed_county if x is not None]
        fsbo_obj["county"] = county[0]
        amentites = sel.xpath('//div[starts-with(@class, "amenities")]//li//text()').extract()
        print("amentites")
        parsed_emnties = [process(amenity_line) for amenity_line in amentites]
        print(parsed_emnties)
        fsbo_obj["amenities"] = ",".join(parsed_emnties)

        owner_detail = sel.xpath('//div[@id="sellerModal"]//text()').extract()

        print("owner detail")

        owner_details = [process(owner) for owner in owner_detail]
        owner = [x for x in owner_details if x is not None]
        for idx,own in enumerate(owner):
            if own=='Contact:':
                fsbo_obj["ownerName"] = owner[idx+1]
            if own=='Phone:':
                fsbo_obj["ownerPhone"] = owner[idx+1]
        #print(owner_details)
        # fsbo_obj["owner_detail"] = ",".join(owner_details)
        fsbo_data.append(fsbo_obj)
    return fsbo_data


    driver.quit()
