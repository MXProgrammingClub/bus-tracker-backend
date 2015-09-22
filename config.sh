#!/bin/bash			
#passwd *PASSWORD*
rm -r ../python_games
sudo apt-get install gpsd gpsd-clients python-gps
sudo apt-get install python3-pip
pip install asyncio	
pip install websockets
#Test with "cgps -s"
