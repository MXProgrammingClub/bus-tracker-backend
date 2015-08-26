Small GPS server using gpsd, sockets and python to allow TCP requests of an RPi's location. Run config.sh to install the needed dependencies, then gpsserver.py in a screen to accept connections; by default the server will listen on port 8787 of all interfaces. Client.py can be pointed at an IP and will attempt to connect to a GPSServer, the port is assumed to be 8787. All code written by Ted Pyne, licensed under the BSD 3 clause license.