import os
import subprocess
import urllib.request
import datetime
import sys
import shutil


APP_DIR = os.path.dirname(os.path.abspath(__file__))
class Centralize:
	"""docstring for Centralize"""
	def __init__(self):
		super(Centralize, self).__init__()

	def internetOn(self):
		try:
			urllib.request.urlopen('https://www.google.com/')
			return True
		except urllib.request.URLError as err: 
			return False

	def getConfig(self):
		config = {}
		with open(os.path.join(APP_DIR, "cfg", "config.txt")) as f:
			for line in f:
				key, value = line.partition("=")[::2]
				config[key.strip()] = value.strip()
			return config

	def clone(self, repoPath, repository):
		os.chdir(repoPath)
		self.log(">>>>>>> Local repository stored: %s"%repoPath)
		self.log(">>>>>>> Done")
		self.log(">>>>>>> Start to clone the project")
		self.log(">>>>>>>Send the command: git clone %s"%repository)
		os.system("git clone "+repository)
		self.log(">>>>>>> Done")

	def pull(self, project="hello-word"):
		self.log(">>>>>>> Pull Request")
		os.chdir(os.path.join(APP_DIR, "repository", project))
		self.log(">>>>>>> Start to pull the latest commit")
		self.log(">>>>>>> Sending the command: git pull")
		pullProcess = subprocess.Popen("git pull", universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		pullProcess.wait()
		self.log(">>>>>>> Done")
		self.diff()

	def diff(self, cmd = "git log"):
		self.log(">>>>>>> Saving the github history to log.txt")
		logfile = open(os.path.join(APP_DIR, "log", "history.log"), "w")
		diffLog = subprocess.Popen(cmd, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		for line in diffLog.stdout:
			logfile.write(line)
		logfile.close()
		diffLog.wait()
		self.log(">>>>>>> Done")

	def updateLatestVersion(self):
		latestVersion = subprocess.check_output("git log -1 --pretty=%h").decode('utf-8').strip()
		self.log(">>>>>>> Found the latest commit version: %s"%latestVersion)
		self.log(">>>>>>> Updating the latest commit version into _version.txt file")
		with open(os.path.join(APP_DIR, "sources", "_version.txt"), "w") as version:
			print("Git commit version: %s"%latestVersion, file = version)
		self.log(">>>>>>>>>>>>>>>>> End Script >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")	

	def execute(self):
		self.log(">>>>>>>>>>>>>>>>> Start Script >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
		online = self.internetOn()
		if online:
			config = self.getConfig()
			print(config["repository"])
			repoPath = os.path.join(APP_DIR, "repository")
			self.log(">>>>>>> Checking the repository path")
			if not os.path.exists(repoPath):
				self.log(">>>>>>> The repository is not existed")
				self.log(">>>>>>> Creating a repository path")
				os.makedirs(repoPath)
				self.log(">>>>>>> Done")
				self.clone(repoPath, config["repository"])
			else:
				self.log(">>>>>>> The repository is existing")
				self.pull()
			self.zipdir(os.path.join(APP_DIR, "repository", config["project"], "Config"))
			self.updateLatestVersion()
		else:
			self.log(">>>>>>> No internet connection!", isError = true)
			self.log(">>>>>>> Exit!")

	def log(self, msg, err = False):
		logPath = os.path.join(APP_DIR, "log")	
		if not os.path.exists(logPath):
			os.makedirs(logPath)
		with open(os.path.join(logPath, "log.txt"), "a+") as log:
			if err:
				print("{date} [Log Error] {msg}".format(date = datetime.datetime.now(), msg = msg), file = log)
			else:
				print("{date} [Log Info] {msg}".format(date = datetime.datetime.now(), msg = msg), file = log)
	
	def zipdir(self, path):
		os.chdir(path)
		if not os.path.exists(os.path.join(APP_DIR, "sources")):
			self.log(">>>>>>> Sources folder is not existed")
			self.log(">>>>>>> Create the sources folder")
			os.makedirs(os.path.join(APP_DIR, "sources"))
		for folder in os.listdir(path):
			self.log(">>>>>>> Archiving %s folder"%folder)
			shutil.make_archive(folder, 'tar', ".", folder)
			self.log(">>>>>>> Moving %s.tar to sources"%folder)
			shutil.move(os.path.join(path, '%s.tar'%folder), os.path.join(APP_DIR, "sources", '%s.tar'%folder))

if __name__ == "__main__":
	App =  Centralize()
	App.execute()
