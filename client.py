import socket
import random

RANDOM_SEED="TEST"
PASS="TEST";
def Decrypt(data):
	global RANDOM_SEED;
	random.seed(RANDOM_SEED);
	crypt = "";
	for x in range(0, len(data)):
		crypt += "" + chr(ord(data[x])- random.randint(0,100))	
	return crypt;

print "Enter the server address to connect to!"
ip = raw_input()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("0.0.0.0",63541))
s.connect((ip, 8787))
#s.send(PASS);
print Decrypt(s.recv(64))
