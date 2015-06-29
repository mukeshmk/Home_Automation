#!/usr/bin/python

import serial 
import MySQLdb

def create_table():
  cursor.execute("""SELECT TABLE_NAME 
                    FROM INFORMATION_SCHEMA.TABLES
                    WHERE TABLE_TYPE = 'BASE TABLE' AND TABLE_SCHEMA="""+"\'"+str(d)+"\'")
  result = cursor.fetchall()
  for i in range(0,len(result)):
    print str(i+1)+" "+str(result[i][0])
  print "Make sure the new table name doesn't exists."
  t=raw_input("enter the new table name:")
  # Create table as per requirement
  sql = """CREATE TABLE """+str(t)+""" 
        (
          SNo INT AUTO_INCREMENT,
          Temp FLOAT(10,2),
          Hum FLOAT(6,2),
          LDR FLOAT(10,2),
          Time TIMESTAMP,
          PRIMARY KEY (SNo)
        )"""
  cursor.execute(sql)
  return t

def reuse_table():
  # Drop table if it already exist using execute() method.
  cursor.execute("""SELECT TABLE_NAME 
                    FROM INFORMATION_SCHEMA.TABLES
                    WHERE TABLE_TYPE = 'BASE TABLE' AND TABLE_SCHEMA="""+"\'"+str(d)+"\'")
  result = cursor.fetchall()
  for i in range(0,len(result)):
    print str(i+1)+" "+str(result[i][0])
  return result[input("Enter Table No:")-1][0]

def choose():
  print "\nWhat do you want to do?\n"
  print "1. Create new Table\n"
  print "2. Re-Use existing Table\n"
  ch = input("Enter your Choice:")

  if ch == 1:
    return create_table()
  elif ch == 2:
    return reuse_table()
  else:
    print "wrong choice enter again:"
	choose()
    

#establish connection to MySQL. You'll have to change this for your database.
dbConn = MySQLdb.connect("localhost","root","1111") or die ("could not connect to database")
#open a cursor to the database
cursor = dbConn.cursor()

d="od"

# Create New Database
sql = """CREATE DATABASE IF NOT EXISTS """+str(d)
cursor.execute(sql)
#Use the newly created Database
sql = """USE """+str(d)
cursor.execute(sql)

t=choose()
print t
device = '/dev/ttyACM0' #this will have to be changed to the serial port you are using
try:
  print "Trying...",device 
  arduino = serial.Serial(device, 9600) 
except: 
  print "Failed to connect on",device    
sno = 1
try:
  while True:
    data = arduino.readline()  #read the data from the arduino
    print str(sno)+" "+str(data)
    sno=sno+1
    pieces = data.split("\t")  #split the data by the tab
    #Here we are going to insert the data into the Database
    pieces[2] = pieces[2].split("\r")[0]
    try:
      cursor.execute("INSERT INTO "+str(t)+" (temp,hum,ldr,Time) VALUES ('{}','{}','{}',CURRENT_TIMESTAMP)".format(pieces[0],pieces[1],pieces[2]))
      dbConn.commit() #commit the insert
    except MySQLdb.IntegrityError:
      print "failed to insert data"
    finally:
      #cursor.close()  close just incase it failed
      pass
except:
  print "Failed to get data from Arduino!"