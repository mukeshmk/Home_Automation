#!/usr/bin/python

import serial 
import MySQLdb

def choose():
	print "in progress"

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
device = '/dev/ttyACM1' #this will have to be changed to the serial port you are using
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
      cursor.execute("INSERT INTO "+str(t)+" (temp,hum,ldr) VALUES ('{}','{}','{}')".format(pieces[0],pieces[1],pieces[2]))
      dbConn.commit() #commit the insert
    except MySQLdb.IntegrityError:
      print "failed to insert data"
    finally:
      #cursor.close()  close just incase it failed
      pass
except:
  print "Failed to get data from Arduino!"