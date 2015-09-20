import socket
import time
import threading
import os

NEXT = "NEW"
KILL = "KIL"

def getData():
	global data;
	global raspIP;
	global NEXT;	
	global KILL

	port = 63542;
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind(("0.0.0.0",port))		
	s.connect((raspIP, 8787))		
	while True:
		data = s.recv(64);
		print data;		
		s.send(NEXT)
		time.sleep(5)
		

def returnLatLong((client, addr)):	#Handle open socket
	global data;
	client.send(data);

data = "LAT = 00.00000NOTSERV\nLON = 00.00000" #Global var
raspIP = "192.168.1.152"


thread = threading.Thread(target=getData)	#Run setLatLong in a subthread
thread.daemon = True                            # Daemonize thread
thread.start()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Create a TCPIP socket
s.bind(("0.0.0.0", 8789)) #Bind to all interfaces on port 8787
s.listen(100) #Accept a maximum of 100 connection simultaneously
while True:
	    	c = s.accept()	#Accept a new connection
    		if os.fork(): #Create child process, if not in child, end
      			c[0].close()
    		else:
      			returnLatLong(c) #Give the new client the Lat/Long pair
      			c[0].close()
			exit(0) #Kill child process


