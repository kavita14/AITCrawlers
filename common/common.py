import mysql.connector

def CreateDBConnection():
    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      passwd="technical",
      database="web_extractor",
      auth_plugin='mysql_native_password'
    )
    return mydb
    #cur = conn.cursor()

def getPincodeData():
    connection = CreateDBConnection()
    mycursor = connection.cursor()
    mycursor.execute("SELECT zip FROM zip_county")
    myresult = mycursor.fetchall()
    print("my result===")
    print(myresult)

def parseAddress(address):
    print("inside parse addrssss function")
    print(address)

def parsePhone(phone):
    print(phone)

def saveOwnerDetail(owner_detail):
    print(owner_detail)

def savePropertyAdd(propertyAdd):
    print(propertyAdd)
