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
    return mystr

#PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
def crawl(DRIVER_BIN,site_url,site_config):
    #DRIVER_BIN = "../chromedriver"
    driver = webdriver.Chrome(DRIVER_BIN)
    urls=[]
    driver.get(site_url)
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
    fsbo_data = []

    for url in urls:
        fsbo_obj = {}
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
        fsbo_obj["propertyAddress"] = " ".join(parsed_address)

        amentites = sel.xpath('//div[starts-with(@class, "amenities")]//li//text()').extract()
        print("amentites")
        parsed_emnties = [process(amenity_line) for amenity_line in amentites]
        print(parsed_emnties)
        fsbo_obj["amenities"] = ",".join(parsed_emnties)

        owner_detail = experience = sel.xpath('//div[@id="sellerModal"]//text()').extract()

        print("owner detail")
        owner_details = [process(owner) for owner in owner_detail]
        print(owner_details)
        fsbo_data.append(fsbo_obj)
        return fsbo_data
        exit()

    driver.quit()
