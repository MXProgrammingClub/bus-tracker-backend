import socket
import threading
import os

def getData():
	global data;
	global raspIP;
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind(("0.0.0.0",63542))
	s.connect((raspIP, 8787))
	while True:
		data = s.recv(64);


def returnLatLong((client, addr)):	#Handle open socket
	global data;
	#if(verifyEncryption((client, addr))): 
	client.send(data);
	
def verifyEncryption((client, addr)):
	global PASS;
	passWd = client.recv(16);	
	if(passWd == PASS): 
		return True;




data = "LAT = 00.00000\nLON = 00.00000" #Global var
raspIP = "127.0.0.1"
PASS = "TEST"

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


