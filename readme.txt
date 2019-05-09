1. Push configuration to github Netgear
2. SSH and deploy from Jenkins to stations

   - Directions:
	+ Checkout the new config and archive each config folder with format folder_name.tar into source folder
        + transfer_stations.py script: ssh to server
   	+ Copy folder.tar from local path to station (path/tmp as default)
   	+ Extract new folder.tar to working path (path/config as default)
   	+ Archive the existed in working folder with format folder_name_yyyy_mm_dd.tar

    - Run script:
	+ python transfer_staion.py station_ip ssh_username ssh_password ssh_port folder_name
		ex: python transfer_stations.py 172.16.10.2 root root 22 THRPT
	+ Require: Paramiko library

