import os
import gps
import socket     

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
	os.system("sudo killall gpsd")
	os.system("sudo gpsd /dev/ttyUSB0 -F /var/run/gpsd.sock")	
	# Listen on port 2947 (gpsd) of localhost
	session = gps.gps("localhost", "2947")
        session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)
	while True:
   		try:
     			report = session.next()
    			if report['class'] == 'TPV':
				if hasattr(report, 'lat') and hasattr(report, 'lon'):
					data = "LATITIUDE = " + repr(report.lat) + "\nLONGITUDE = " + repr(report.lon)
  	   	except KeyError:
    			pass

str data
if os.fork():
	setLatLong()
else:
	listen()
