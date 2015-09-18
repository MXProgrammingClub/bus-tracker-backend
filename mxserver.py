import socket
import threading
import os

def getData():
	global data;
	global raspIP;
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind(("0.0.0.0",63542))
	
	while True:
		s.connect((raspIP, 8787))		
		data = s.recv(64);
		s.close();		


def returnLatLong((client, addr)):	#Handle open socket
	global data;
	client.send(data);

data = "LAT = 00.00000NOTSERV\nLON = 00.00000" #Global var
raspIP = "127.0.0.1"


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


