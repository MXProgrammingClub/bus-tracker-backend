import socket
import random

RANDOM_SEED="TEST"
def Decrypt(data):
	global RANDOM_SEED;
	random.seed(RANDOM_SEED);
	crypt = "";
	for x in range(0, len(data)):
		seed = random.randint(0,100);
		val = ord(data[x])
		crypt += "" + chr(val- seed)	
	return crypt;

print "Enter the server address to connect to!"
ip = raw_input()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("0.0.0.0",63540))
s.connect((ip, 8789))
print Decrypt(s.recv(64))
