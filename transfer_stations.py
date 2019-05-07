import paramiko
import os
import sys
import datetime
from re import sub

class Centralize:
	"""docstring for Centralize"""
	def __init__(self):
		super(Centralize, self).__init__()

	def main(self, server, username, password, port, folder):
		source_path = 'D:/service_328/sources'
		remote_tmp_path = '/opt/its3/TSLIB/tmp'
		working_path = '/opt/its3/TSLIB'
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		try:
			ssh.connect(server, username=username, password=password, port=port, timeout=30)
			print ("Connection Passed")
		except paramiko.SSHException:
			print ("Connection Failed")
			quit()
		ftp_client=ssh.open_sftp()
		try:
			ftp_client.stat(remote_tmp_path)
		except FileNotFoundError:
			ftp_client.mkdir(remote_tmp_path)
			ftp_client.mkdir(working_path)
		ftp_client.put(os.path.join(source_path,'%s.tar'%folder), '{tmp_path}/{folder}.tar'.format(tmp_path = remote_tmp_path, folder = folder))
		ftp_client.close()
		try:
			command = 'tar -cvf {path}/{folder}_{date}.tar {path}/config'.format(date = datetime.datetime.now().strftime("%Y%m%d%H%M%S"), folder = folder, path= working_path)
			(stdin, stdout, stderr) = ssh.exec_command(command)
			stdout.read()
			print ("Executing commands {command}".format(command=command))
			command_rm = 'rm -rf {path}/config'.format(path=working_path)
			(stdin, stdout, stderr) = ssh.exec_command(command_rm)
			stdout.read()
			print ("Executing commands {command}".format(command=command_rm))
		except:
			pass
		command = 'tar -xvf {tmp_path}/{folder}.tar -C {path}'.format(tmp_path = remote_tmp_path, folder = folder, path= working_path)
		(stdin, stdout, stderr) = ssh.exec_command(command)
		stdout.read()
		print ("Executing commands {command}".format(command=command))
		command_re = 'mv {path}/{folder} {path}/config'.format(folder = folder, path= working_path)
		(stdin, stdout, stderr) = ssh.exec_command(command_re)
		stdout.read()
		print ("Executing commands {command}".format(command=command_re))
		command_get = 'hostname'
		(stdin, stdout, stderr) = ssh.exec_command(command_get)
		strout = stdout.readline()
		print ("Executing commands {command}".format(command=command_get))
		strout_rm = strout.replace("-LX","")
		print (strout_rm)
		try:
			command_read = 'cat {path}/config/TS/ts_profile.xml'.format(path= working_path)
			(stdin, stdout, stderr) = ssh.exec_command(command_read)
			print ("Executing commands {command}".format(command=command_read))
			for line in stdout.readlines():
				if '<TS_NAME>' in line:
					print ('found: ' + line)
					line_fix_1 = line.replace('<TS_NAME>','')
					line_fix_2 = line_fix_1.replace('</TS_NAME>','')
					command_write = "sed -i -E 's/{line}/{hostname}/g' {path}/config/TS/ts_profile.xml".format(hostname=strout_rm.strip(),line=line_fix_2.strip(), path=working_path)
					(stdin, stdout, stderr) = ssh.exec_command(command_write)
					print ("Executing commands {command}".format(command=command_write))
					break
		except:
			print ("Executing command %s...Fail - No output" % (command_read))
		ssh.close()
if __name__ == '__main__':
	App =  Centralize()
	server = sys.argv[1]
	username = sys.argv[2]
	password = sys.argv[3]
	port = sys.argv[4]
	folder = sys.argv[5]
	App.main(server, username, password, port, folder)