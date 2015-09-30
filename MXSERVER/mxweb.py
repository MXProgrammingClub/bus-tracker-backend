#RUN WITH PYTHON 3 FOR WEBSOCK COMPAT

import socket
import time
import thread
import os
import BaseHTTPServer
import SimpleHTTPServer

class Data:
	data = 'NOTSET'

def collectData():
	global dataObj;	
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Create a TCPIP socket
	s.bind(("0.0.0.0", 8787)) #Bind to all interfaces on port 8787
	s.listen(100) #Accept a maximum of 100 connection simultaneously
	while True:	    	
		c = s.accept()	#Accept a new connection
		thread.start_new_thread( setDataWithClient, (c,))	    		
		

def setDataWithClient(sock):
	(client,addr) = sock;
	global dataObj	
	while True:
		dataObj.data = client.recv(64).decode("utf-8") ;		
		print dataObj.data;
		time.sleep(5);	

class TestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
	def do_POST(self):
		global dataObj
		self.send_response(200)
            	self.send_header('Content-type','text/html')
           	self.end_headers()
		self.wfile.write(dataObj.data)

def returnLatLong(sock):	#Handle open socket
	(client,addr)=sock;
	global dataObj;	
	print dataObj.data
	client.send(dataObj.data);
	client.close();

dataObj = Data();
thread.start_new_thread( collectData, ())

server_address = ("0.0.0.0", 8789)
server = BaseHTTPServer.HTTPServer(server_address, TestHandler)
server.serve_forever()
