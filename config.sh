#!/bin/bash			
#passwd *PASSWORD*
rm -r ../python_games
sudo apt-get install gpsd gpsd-clients python-gps
sudo apt-get install python3-pip
pip3 install asyncio	
pip3 install websockets
#Test with "cgps -s"

#Obsolete, onlly use for debugging both on the same computer
