#!/usr/bin/python

import serial 
import MySQLdb

#establish connection to MySQL. You'll have to change this for your database.
dbConn = MySQLdb.connect("localhost","root","1111","od") or die ("could not connect to database")
#open a cursor to the database
cursor = dbConn.cursor()

device = '/dev/ttyACM0' #this will have to be changed to the serial port you are using
try:
  print "Trying...",device 
  arduino = serial.Serial(device, 9600) 
except: 
  print "Failed to connect on",device    
 
try:
  while True:
    data = arduino.readline()  #read the data from the arduino
    pieces = data.split("\t")  #split the data by the tab
    #Here we are going to insert the data into the Database
    print pieces;
    pieces[2] = pieces[2].split("\r")[0]
    try:
      cursor.execute("INSERT INTO od_mk (temp,hum,ldr) VALUES ('{}','{}','{}')".format(pieces[0],pieces[1],pieces[2]))
      dbConn.commit() #commit the insert
    except MySQLdb.IntegrityError:
      print "failed to insert data"
    finally:
      #cursor.close()  close just incase it failed
      pass
except:
  print "Failed to get data from Arduino!"