import os
import threading
import gps
import socket     
import time

def listen():
	
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind(("0.0.0.0", 8787))
	s.listen(100)

	while True:
	    	c = s.accept()
    		if os.fork():
      			c[0].close()
    		else:
      			returnLatLong(c)
      			c[0].close()
			exit(0)
		
def returnLatLong((client, addr)):	#Wait for someone to ask for a lat/long pair, then returh getLatLong
	client.send(data)
	
def setLatLong():     
	# Listen on port 2947 (gpsd) of localhost
	session = gps.gps("localhost", "2947")
        session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)
	global data
	while True:
   		try:
     			report = session.next()
    			if report['class'] == 'TPV':
				if hasattr(report, 'lat') and hasattr(report, 'lon'):
					data =  "LATITIUDE = " + repr(report.lat) + "\nLONGITUDE = " + repr(report.lon)
					print data
  	   	except KeyError:
    			pass
		
data = "LAT = 00.00000\nLON = 00.00000"
os.system("sudo killall gpsd")
os.system("sudo gpsd /dev/ttyUSB0 -F /var/run/gpsd.sock")

thread = threading.Thread(target=setLatLong)
thread.daemon = True                            # Daemonize thread
thread.start() 
listen()
