import mysql.connector

def CreateDBConnection():
    connection = mysql.connector.connect(host='localhost',
                             database='web_extractor',
                             user='root',
                             password='technical')
    return connection

def getSiteConfig():
    connection = CreateDBConnection()
    mycursor = connection.cursor()
    mycursor.execute("SELECT * FROM site_config")
    siteConfig = mycursor.fetchall()
    return siteConfig

def getZipcodeData():
    connection = CreateDBConnection()
    mycursor = connection.cursor()
    mycursor.execute("SELECT zip FROM zip_county")
    pincodes = mycursor.fetchall()
    return pincodes

def parseAddress(address):
    print("inside parse addrssss function")
    print(address)

def parsePhoneNo(phone):
    print(phone)

def saveOwnerDetail(owner_detail):
    print(owner_detail)

def savePropertyAdd(propertyAdd):
    print(propertyAdd)
