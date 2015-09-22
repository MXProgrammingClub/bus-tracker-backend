#!/bin/bash			
#passwd *PASSWORD*
rm -r ../python_games
sudo apt-get install gpsd gpsd-clients python-gps
pip install websockets asyncio	
#Test with "cgps -s"
