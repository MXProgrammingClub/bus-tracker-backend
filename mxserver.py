import socket
import time
import threading
import os


def getData():
	global data;
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Create a TCPIP socket
	s.bind(("0.0.0.0", 8787)) #Bind to all interfaces on port 8787
	s.listen(100) #Accept a maximum of 100 connection simultaneously
	while True:
	    	c = s.accept()	#Accept a new connection
    		if os.fork(): #Create child process, if not in child, end
      			print "New GPS!"
    		else:
      			setDataWithClient(c) #Give the new client the Lat/Long pair
      			c[0].close()
			exit(0) #Kill child process

def setDataWithClient((client,addr)):
	global data;
	data = client.recv(64);
	while True:
		print data;
		time.sleep(5);
		data = client.recv(64)		

def serveClients():
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

def returnLatLong((client, addr)):	#Handle open socket
	global data;
	print data;
	client.send(data);


data = "LAT0000";

thread = threading.Thread(target=getData)	#Run setLatLong in a subthread
thread.daemon = True                            # Daemonize thread
thread.start()

serveClients();




