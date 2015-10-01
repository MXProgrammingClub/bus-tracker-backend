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
		thread.start_new_thread( setDataWithGPS, (c,)) #"Bind" to a GPS
		

def setDataWithGPS(sock):
	(client,addr) = sock;
	global dataObj	
	while True:
		dataObj.data = client.recv(64).decode("utf-8");	
		print dataObj.data;
		time.sleep(5);	

class RequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
	def do_GET(self):
		print "CALLED!";
		global dataObj
		self.send_response(200)
            	self.send_header('Content-type','text/html')
           	self.end_headers()
		self.wfile.write(dataObj.data)


dataObj = Data();	#Initiialize global var
thread.start_new_thread( collectData, ())	#Begin accepting data from GPS

server_address = ("0.0.0.0", 8789)
server = BaseHTTPServer.HTTPServer(server_address, RequestHandler)
server.serve_forever()		#Start HTTP server to serve clients
