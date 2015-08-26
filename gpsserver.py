import os
import threading
import gps
import socket     
import time

def listen():	
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Create a TCPIP socket
	s.bind(("0.0.0.0", 8787)) #Bind to all interfaces on port 8787
	s.listen(100) #Accept a maximum of 100 connection simultaneously

	while True:
	    	c = s.accept()	#Accept a new connection
    		if os.fork(): #Create child process, if not in child, end
      			c[0].close()
    		else:
      			returnLatLong(c) #Give the new client the Lat/Long pair
      			c[0].close()
			exit(0) #Kill child process
		
def returnLatLong((client, addr)):	#Handle open socket
	client.send(data)
	
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
					data =  "LATITIUDE = " + repr(report.lat) + "\nLONGITUDE = " + repr(report.lon)
					print data
  	   	except KeyError: #If no message exisists in queue, wait
    			pass
		
data = "LAT = 00.00000\nLON = 00.00000" #Global var
os.system("sudo killall gpsd")	#kill previous instances of gpsd
os.system("sudo gpsd /dev/ttyUSB0 -F /var/run/gpsd.sock") #Start gpsd listening to /var/ttyUSB0

thread = threading.Thread(target=setLatLong)	#Run setLatLong in a subthread
thread.daemon = True                            # Daemonize thread
thread.start() 
listen()
