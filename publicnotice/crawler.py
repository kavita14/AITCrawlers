# importing the requests library
import requests
from parsel import Selector
from HTMLParser import HTMLParser
from selenium import webdriver
from time import sleep
from lxml import html
from selenium.webdriver.common.keys import Keys
import re

base_url = "http://publicnoticeads.com/TN/search/"
urls = []
driver = webdriver.Chrome('/Users/kavitasharma/Downloads/chromedriver')
def process(line):
    mystr = re.sub('\s+',' ',line)
    mystr = mystr.strip()
    if mystr != '' and mystr != None and type(mystr) != None:
        return mystr
class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        for attr in attrs:
            if attr[0] == 'href':
                urls.append(attr[1])

regexps = [
'Address/Description: *?(\d+\s.*?\d{5})',
'address is (.*). Survey',
'Address.*?(\d+\s.*?TN)',
'address: (\S.*?, Tennessee)\.',
'Address/Description: *?(\d+.*?)Current Owner',
'of the property at (\d+.*?, Tennessee)',
'address of the property is believed to be (.*). In the event',
'property is located at.*?(\d+.*?\d{5})',
]

# api-endpoint
URL = "http://publicnoticeads.com/AzureSearchService/Azure/Search"
frmdata = {"appSiteLongDesc":"","headerColor":"#990000","dividerColor":"#dcdcdc","resultAbbrev":"PN","resultType":"Public Notice","resultTypePlural":"Public Notices","sessWebPath":"http://publicnoticeads.com/TN","returnPath":"searchnotices.asp","appStateCD":"TN","appSiteDesc":"Tennessee Newspapers","pageSize":"300","currentPage":"1","searchWordsOr":"","searchWordsAnd":"","searchWordsNot":"","searchWordsExact":"","county":"All","publication":"All","dateRangeFrom":"","dateRangeTo":"","nextRecordNumber":"","endPos":"","numMaxReturned":"250"}


# sending get request and saving the response as response object
r = requests.post(url = URL, data = frmdata)
sel = Selector(text=r.text)
elems = sel.xpath('//small/a').extract()
for elem in elems:
    parser = MyHTMLParser()
    parser.feed(elem)

for url in urls:
    crawl_url = base_url+url
    driver.get(crawl_url)
    sleep(3)
    sel = Selector(text=driver.page_source)
    #print(driver.page_source)
    noticeText = sel.xpath('//div[@id="noticeText"]//text()').extract()
    processedNotice = [process(notice) for notice in noticeText]
    noticeList = [x for x in processedNotice if x is not None]
    notice = " ".join(noticeList)
    #print("notice text====",notice)

    for exp in regexps:
        searchObj = re.search(exp,notice)
        if searchObj:
            print("searched object====found")
            print("expression",exp)
            print(searchObj.group())
            
            break
