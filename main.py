import common.common as commModule
import fsbo.crawler as fsbo
import forsalebyowner.crawler as salebyowner
import publicnotice.crawler as publicnotice
import usaddress
from nameparser import HumanName

DRIVER_BIN = "/Users/kavitasharma/Downloads/chromedriver"

site_id = input("Please Select Crawler for Exceution:\n Enter 1 for FSBO.com \n Enter 2 for PDCTN.com \n Enter 3 for Publicnotice.com \n Enter 0 to run All\n")
if site_id == 1:
    site_url = "https://fsbo.com/listings/search/"
    site_config = commModule.getSiteConfig();
    data_from_fsbo = fsbo.crawl(DRIVER_BIN,site_url,site_config)
    for fsbo in data_from_fsbo:
        fsbo["propertyAddress"] = usaddress.parse(fsbo["propertyAddress"])
        fsbo["propertyAddress"] = commModule.convertTupletoDict(fsbo["propertyAddress"])
        #fsbo["ownerName"] = HumanName(fsbo["ownerName"])
    commModule.savePropertyAddress(data_from_fsbo)

elif site_id == 2:
    site_url = "https://www.forsalebyowner.com/search/list/tennessee/proximity,desc-sort"
    site_config = commModule.getSiteConfig();
    data_from_salebyowner = salebyowner.crawl(DRIVER_BIN,site_url,site_config)
    for salebyowner in data_from_salebyowner:
        salebyowner["propertyAddress"] = usaddress.parse(salebyowner["propertyAddress"])
        salebyowner["propertyAddress"] = commModule.convertTupletoDict(salebyowner["propertyAddress"])
        #fsbo["ownerName"] = HumanName(fsbo["ownerName"])
    commModule.savePropertyAddress(data_from_salebyowner)

elif site_id == 3:
    site_url = "http://publicnoticeads.com/TN/search/searchnotices.asp"
    site_config = commModule.getSiteConfig();
    data_from_publicnotice = publicnotice.crawl(DRIVER_BIN,site_url,site_config)
    for publicnotice in data_from_publicnotice:
        publicnotice["propertyAddress"] = usaddress.parse(salebyowner["propertyAddress"])
        publicnotice["propertyAddress"] = commModule.convertTupletoDict(salebyowner["propertyAddress"])
        #fsbo["ownerName"] = HumanName(fsbo["ownerName"])
    commModule.savePropertyAddress(data_from_publicnotice)
