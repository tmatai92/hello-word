1. Check Github automation script

   - Directions:
	+ Run script automate_github.py to clone(if repository not existed) / pull new commit from github
	+ Read config info from 'cfg/config.txt'
	+ Checkout the new config and archive each config folder with format folder_name.tar into source folder
	+ Using cron to run this script continutious
    - Run script:
        + python automate_github.py

2.SSH and deploy from Jenkins to stations

   - Directions:

        + transfer_stations.py script: ssh to server
   	+ Copy folder.tar from local path to station (opt/tmp as default)
   	+ Extract new folder.tar to working path (opt/config as default)
   	+ Archive the existed in working folder with format folder_name_yyyy_mm_dd.tar

    - Run script:
	+ python transfer_staion.py station_ip ssh_username ssh_password ssh_port folder_name
		ex: python transfer_stations.py 172.16.10.2 root root 22 THRPT
	+ Require: Paramiko library

