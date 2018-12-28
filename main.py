import common.common as commModule
import fsbo.crawler as fsbo

site_id = input("Please Select Crawler for Exceution:\n 1. Enter 1 for FSBO.com \n 2. Enter 2 for PDCTN.com \n Enter 0 to run All\n")
#site_id=int(site_id)
print(site_id)
print(type(site_id))
if site_id == 1:
    DRIVER_BIN = "/Users/kavitasharma/Downloads/chromedriver"
    site_url = "https://fsbo.com/listings/search/"
    site_config = commModule.getSiteConfig();
    fsbo.crawl(DRIVER_BIN,site_url,site_config)

elif site_id == 2:
    print("Crawler is not ready yet!")
