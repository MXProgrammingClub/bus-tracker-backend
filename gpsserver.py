import os
import threading
import gps
import socket     
import random

RANDOM_SEED="TEST"
NEXT="NEW"
KILL="KIL"
SERVER_IP="192.168.1.187"

def connectToServer():	
	global NEXT
	global KILL	
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Create a TCPIP socket
	s.bind(("0.0.0.0", 63469)) #Bind to all interfaces on port 8787
	s.connect((SERVER_IP, 8787));
	
	s.send(Encrypt(data));
	while True:
		s.send(Encrypt(data))
def Encrypt(data):
	global RANDOM_SEED;
	random.seed(RANDOM_SEED);
	
	crypt = "";

	for x in range(0, len(data)):
		seed = random.randint(0,100);
		crypt += "" + chr(ord(data[x])+ seed)	
	return crypt;

def setLatLong():     
	# Listen on port 2947 (gpsd) of localhost
	session = gps.gps("localhost", "2947") #Connect to gpsd on port 2947
        session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)	#Stream the gps data
	global data
	while True:	#Constantly update global var with Lat/Long
   		try:
     			report = session.next() #Grab the next GPS message, if it has the correct data, write it to a global var
    			if report['class'] == 'TPV':
				if hasattr(report, 'lat') and hasattr(report, 'lon'):
					data =  "LAT " + repr(report.lat) + " LON " + repr(report.lon)
					print data
  	   	except KeyError: #If no message exisists in queue, wait
    			pass
		
data = "LAT = 00.00000\nLON = 00.00000" #Global var
os.system("sudo killall gpsd")	#kill previous instances of gpsd
os.system("sudo gpsd /dev/ttyUSB0 -F /var/run/gpsd.sock") #Start gpsd listening to /var/ttyUSB0

thread = threading.Thread(target=setLatLong)	#Run setLatLong in a subthread
thread.daemon = True                            # Daemonize thread
thread.start() 
connectToServer()
