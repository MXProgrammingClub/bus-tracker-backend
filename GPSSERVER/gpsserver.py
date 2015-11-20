# RUN WITH PYTHON 2.7
import os
import gps
import socket
import time
import thread

DEFAULT = "require('update')([null,null]);" # Default format for data
SERVER = "bustracker.mxschool.edu" # Server address for connection

# --------------------------
# Data class for output data
class Data:
	data = DEFAULT

# -----------------------------------
# Connects to the server via a socket
def connect_to_server():	
	global dataObj	
	while True:
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Creates a socket
			s.bind(("0.0.0.0", 63467)) # Binds to all interfaces on port 63467

			print "Connecting to server " + (SERVER or "'undefined'")
			s.connect((SERVER, 8787)) # Connects to server on port 8787
			send_data(s)
		except socket.error as e:
			print e
			s.close()
			time.sleep(5)

# -------------------------------------
# Sends data to the server via a socket
# @param s The socket for data sending
def send_data(s):
	global dataObj
	while True:
		print dataObj.data
		s.send(dataObj.data)
		time.sleep(2) # Pauses for 2 seconds

# ------------------------------------------
# Determines latitude and longetude from gps
def set_lat_lon():	 
	global dataObj

	# Listens on port 2947 (gpsd) of localhost
	session = gps.gps("localhost", "2947") # Connect to gpsd on port 2947
	session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)
	dataObj.data = DEFAULT
	while True:	# Constantly updates global var with Lat/Lon
   		try:
	 		report = session.next() # Grabs the next GPS message; if it has the correct data, write it to a global var
			if report['class'] == 'TPV':
				dataObj.data =  "require('update')([" + repr(report.lat) + "," + repr(report.lon) + "]);"
		except KeyError: # If no message exists in queue, wait
			pass

os.system("sudo killall gpsd")	# Kills previous instances of gpsd
os.system("sudo gpsd /dev/ttyUSB0 -F /var/run/gpsd.sock") # Starts gpsd listening to /dev/ttyUSB0

dataObj = Data() # New instance of Data object
thread.start_new_thread(set_lat_lon, ())
connect_to_server()
