import socket
import time
import _thread
import os


class Data:
	data = "NOTSET"

def collectData():
	global dataObj;	
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Create a TCPIP socket
	s.bind(("0.0.0.0", 8787)) #Bind to all interfaces on port 8787
	s.listen(100) #Accept a maximum of 100 connection simultaneously
	while True:	    	
		c = s.accept()	#Accept a new connection
		_thread.start_new_thread( setDataWithClient, (c,))	    		
		

def setDataWithClient(sock):
	(client,addr) = sock;
	global dataObj	
	while True:
		dataObj.data = client.recv(64);		
		print( dataObj.data);
		time.sleep(5);	

def serveClients():
	global dataObj;	
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Create a TCPIP socket
	s.bind(("0.0.0.0", 8789)) #Bind to all interfaces on port 8787
	s.listen(100) #Accept a maximum of 100 connection simultaneously
	while True: 	
		c = s.accept()	#Accept a new connection
		print( "NEW CLIENT! VALUE OF DATA IS ", dataObj.data);    		
		_thread.start_new_thread( returnLatLong, (c,))		
		

def returnLatLong(sock):	#Handle open socket
	(client,addr)=sock;
	global dataObj;	
	print( dataObj.data)
	client.send(dataObj.data);
	client.close();

dataObj = Data();
_thread.start_new_thread( collectData, ())
serveClients();
