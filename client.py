import socket

PASS="TEST";

print "Enter the server address to connect to!"
ip = raw_input()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("0.0.0.0",63541))
s.connect((ip, 8789))
s.send(PASS);
print s.recv(64)
