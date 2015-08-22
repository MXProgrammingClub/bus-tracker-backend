import os
import time
import gps
import socket     
    # Listen on port 2947 (gpsd) of localhost
def main():
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
		#Wait for someone to ask for a lat/long pair, then returh getLatLong
def returnLatLong((client, addr)):
	client.send(getLatLong())
	time.sleep(5);
def getLatLong():     
	session = gps.gps("localhost", "2947")
        session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)
	while True:
   		try:
     			report = session.next()
    			if report['class'] == 'TPV':
				if hasattr(report, 'lat') and hasattr(report, 'lon'):
					return "LATITIUDE = " + repr(report.lat) + "\nLONGITUDE = " + repr(report.lon)
  	   	except KeyError:
    			pass

main()
