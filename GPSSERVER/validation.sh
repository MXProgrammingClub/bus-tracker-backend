#!/bin/sh

status=""
success="Connected"

# Fetches GPS status
get_status(){
	status="$(curl http://bustracker.mxschool.edu:8080/status)"
	echo $status
}

# Validates GPS status every second. 
# Restart if gps is not connected
validate(){
	sleep 10 # Wait for initial boot
	get_status
	if [ $status == $success ]
	then
		sleep 1
	else
		sleep 5
		get_status
		if [ $status != $success ]
		then
			echo GPS Not Connected
			sudo reboot
		fi
	fi

}

# Executes function validate()
while (true) 
do
	validate
done


