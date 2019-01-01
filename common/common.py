import mysql.connector
import re

def CreateDBConnection():
    connection = mysql.connector.connect(host='localhost',
                             database='web_extractor',
                             user='root',
                             password='technical')
    return connection

def getSiteConfig():
    connection = CreateDBConnection()
    mycursor = connection.cursor()
    mycursor.execute("SELECT * FROM crawler_config")
    siteConfig = mycursor.fetchall()
    return siteConfig

def getZipcodeData():
    connection = CreateDBConnection()
    mycursor = connection.cursor()
    mycursor.execute("SELECT zip FROM zip_county")
    pincodes = mycursor.fetchall()
    return pincodes

def getStateData():
    connection = CreateDBConnection()
    mycursor = connection.cursor()
    mycursor.execute("SELECT zip FROM zip_county")
    pincodes = mycursor.fetchall()
    return pincodes

def parsePhoneNo(phone):
    print(phone)

def parseName(ownerName):

    print(phone)

def saveOwnerDetail(owner_detail):
    print(owner_detail)

def convertTupletoDict(tup):
    di = {}
    for a, b in tup:
        di.setdefault(b, []).append(a)
    return di

def savePropertyAddress(property):
    connection = CreateDBConnection()
    mycursor = connection.cursor()
    sql = "REPLACE INTO proaddress (listing_id, PStreetNum, PStreetName, PSuiteNum,Pcity,PState,Pzip,owner_name,counties,price,url,beds,baths,proptype,square_feet,PYearBuilt,school_district,garage_size,lot_size,amenities,owner_phone) VALUES (%s,%s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s)"
    values = []
    for pro in property:
        print("adress\n")
        print(pro["propertyAddress"])
        proTuple = ()
        proList = list(proTuple)
        listing_id = pro["propertyDetails"]["listing_id"] if "listing_id" in pro["propertyDetails"] else ''
        proList.append(listing_id)
        PStreetNum = " ".join(pro["propertyAddress"]["AddressNumber"]) if "AddressNumber" in pro["propertyAddress"] else ''
        proList.append(PStreetNum)
        PStreetName = ''
        PStreetName = PStreetName + " ".join(pro["propertyAddress"]["StreetNamePreModifier"]) + " " if "StreetNamePreModifier" in pro["propertyAddress"] else ''
        PStreetName = PStreetName + " ".join(pro["propertyAddress"]["StreetNamePreType"]) + " " if "StreetNamePreType" in pro["propertyAddress"] else ''
        PStreetName = PStreetName + " ".join(pro["propertyAddress"]["StreetName"]) + " " if "StreetName" in pro["propertyAddress"] else ''
        PStreetName = PStreetName + " ".join(pro["propertyAddress"]["StreetNamePostType"]) + " " if "StreetNamePostType" in pro["propertyAddress"] else ''
        PStreetName = PStreetName.replace("  "," ")
        PStreetName = re.sub('\,$', '', PStreetName)
        proList.append(PStreetName)
        OccupancyIdentifier = " ".join(pro["propertyAddress"]["OccupancyIdentifier"]) if "OccupancyIdentifier" in pro["propertyAddress"] else ''
        proList.append(OccupancyIdentifier)
        Pcity = " ".join(pro["propertyAddress"]["PlaceName"]) if "PlaceName" in pro["propertyAddress"] else ''
        Pcity = re.sub('\,$', '', Pcity)
        proList.append(Pcity)
        StateName = " ".join(pro["propertyAddress"]["StateName"]) if "StateName" in pro["propertyAddress"] else ''
        proList.append(StateName)
        ZipCode = " ".join(pro["propertyAddress"]["ZipCode"]) if "ZipCode" in pro["propertyAddress"] else ''
        proList.append(ZipCode)
        owner_name = pro["ownerName"] if "ownerName" in pro else ''
        proList.append(owner_name)
        county = pro["county"] if "county" in pro else ''
        proList.append(county)
        price = pro["price"] if "price" in pro else ''
        proList.append(price)
        url = pro["url"] if "url" in pro else ''
        proList.append(url)
        bedrooms = pro["propertyDetails"]["bedrooms"] if "bedrooms" in pro["propertyDetails"] else ''
        proList.append(bedrooms)
        bathrooms = pro["propertyDetails"]["bathrooms"] if "bathrooms" in pro["propertyDetails"] else ''
        proList.append(bathrooms)
        type = pro["propertyDetails"]["type"] if "type" in pro["propertyDetails"] else ''
        proList.append(type)
        sq_feet = pro["propertyDetails"]["sq_feet"] if "sq_feet" in pro["propertyDetails"] else ''
        proList.append(sq_feet)
        yearBuild = pro["propertyDetails"]["yearBuild"] if "yearBuild" in pro["propertyDetails"] else ''
        proList.append(yearBuild)
        schoolDistrict = pro["propertyDetails"]["schoolDistrict"] if "schoolDistrict" in pro["propertyDetails"] else ''
        proList.append(schoolDistrict)
        garage = pro["propertyDetails"]["garage"] if "garage" in pro["propertyDetails"] else ''
        proList.append(garage)
        lot_size = pro["propertyDetails"]["lot_size"] if "lot_size" in pro["propertyDetails"] else ''
        proList.append(lot_size)
        amenities = pro["amenities"] if "amenities" in pro else ''
        proList.append(amenities)
        ownerPhone = pro["ownerPhone"] if "ownerPhone" in pro else ''
        ownerPhone = ownerPhone.replace("-","")
        ownerPhone = re.sub('\,$', '', ownerPhone)
        proList.append(ownerPhone)
        proTupleConv = tuple(proList)
        values.append(proTupleConv)

    mycursor.executemany(sql, values)
    connection.commit()
