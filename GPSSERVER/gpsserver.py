#RUN WITH PYTHON 2.7
import os
import gps
import socket     
import random
import time
import thread

FORMAT="require('update')([null,null]);";
RANDOM_SEED="TEST"
NEXT="NEW"
KILL="KIL"
SERVER_IP="10.3.108.10"
USE_CRYPT= False;

class Data:
	data = "NOTSET"

def connectToServer():	
	global dataObj	
	while True:
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.bind(("0.0.0.0", 63467)) #Bind to all interfaces on port 8787
			s.connect((SERVER_IP, 8787));
			validConnec(s);
		except socket.error:
			s.close();
			time.sleep(5)

def validConnec(s):
	global dataObj;
	while True:
		print dataObj.data;		
		if(USE_CRYPT):
			s.send(Encrypt(dataObj.data))
		else:
			s.send(dataObj.data);
		time.sleep(5)
def Encrypt(data):
	global RANDOM_SEED;
	random.seed(RANDOM_SEED);
	
	crypt = "";

	for x in range(0, len(data)):
		seed = random.randint(0,100);
		crypt += "" + chr(ord(data[x])+ seed)	
	return crypt;

def setLatLong():     
	global dataObj;
	# Listen on port 2947 (gpsd) of localhost
	session = gps.gps("localhost", "2947") #Connect to gpsd on port 2947
        session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE);
	dataObj.data = FORMAT;
	while True:	#Constantly update global var with Lat/Long
   		try:
     			report = session.next(); #Grab the next GPS message, if it has the correct data, write it to a global var
    			if report['class'] == 'TPV':
				if hasattr(report, 'lat') and hasattr(report, 'lon'):
					dataObj.data =  "require('update')([" + repr(report.lat) + ", " + repr(report.lon) + ']};';
		except KeyError: #If no message exisists in queue, wait
    			pass
		
os.system("sudo killall gpsd")	#kill previous instances of gpsd
os.system("sudo gpsd /dev/ttyUSB0 -F /var/run/gpsd.sock") #Start gpsd listening to /var/ttyUSB0

dataObj = Data();
thread.start_new_thread( setLatLong, ())
connectToServer()
