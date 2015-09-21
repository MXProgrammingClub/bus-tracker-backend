import socket
import time
import thread
import os


class Data:
	def setData(newData):
		data = newData;
	def getData():
		return data;
	data = "NOTSET"

def collectData():
	global dataObj;	
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Create a TCPIP socket
	s.bind(("0.0.0.0", 8787)) #Bind to all interfaces on port 8787
	s.listen(100) #Accept a maximum of 100 connection simultaneously
	while True:	    	
		c = s.accept()	#Accept a new connection
		thread.start_new_thread( setDataWithClient, (c,))	    		
		

def setDataWithClient((client,addr)):
	global dataObj	
	while True:
		dataObj.data = client.recv(64);		
		print dataObj.data;
		time.sleep(5);	

def serveClients():
	global dataObj;	
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Create a TCPIP socket
	s.bind(("0.0.0.0", 8789)) #Bind to all interfaces on port 8787
	s.listen(100) #Accept a maximum of 100 connection simultaneously
	while True: 	
		c = s.accept()	#Accept a new connection
		print "NEW CLIENT! VALUE OF DATA IS ", dataObj.data;    		
		thread.start_new_thread( returnLatLong, (c,))		
		

def returnLatLong((client, addr)):	#Handle open socket
	global dataObj;	
	print dataObj.data
	client.send(dataObj.data);

dataObj = Data();
thread.start_new_thread( collectData, ())
thread.start_new_thread( serveClients, ())
while True:
	time.sleep(5);
