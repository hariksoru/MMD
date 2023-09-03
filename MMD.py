#ModrinthDownloader.py v.2
import os
import zipfile
import json
import urllib.request

class MDM:
	dir = os.getcwd()
	modpacks_count = 0
	all_mods = 0
	downloaded_mods = 0
	extract_file = "modrinth.index.json"
	
	def downloader(self, index, folder_name):
		print("Start downloading mods...")
		for url in index["files"]:
			print("Downloading... [" + str(self.downloaded_mods) + "/" + str(self.all_mods) + "]")
			urllib.request.urlretrieve(url["downloads"][0], self.dir + "/" + folder_name + "/" + url["path"].split("/")[1])
			self.downloaded_mods += 1
		print("All mods are downloaded successfully to " + self.dir + "/" + folder_name)
		self.all_mods = 0
		self.downloaded_mods = 0
	
	def __init__(self):
		for file in os.listdir(self.dir):
			if file.endswith(".mrpack"):
				self.modpacks_count += 1
				with zipfile.ZipFile(self.dir + "/" + file, 'r') as zip:
					with zip.open(self.extract_file) as index:
						index = json.load(index)
				folder_name = index["name"] + " " + index["dependencies"]["minecraft"]
				self.all_mods = len(index["files"])
				try:
					os.mkdir(folder_name)
				except FileExistsError:
					answer = input(f"{folder_name} is already exists and contains {len(os.listdir(self.dir + '/' + folder_name))} out of {self.all_mods}. Start downloading mods? (Y/N) ").lower()
					if answer == "yes" or answer == "y":
						self.downloader(index, folder_name)
					else:
						pass
				else:
					self.downloader(index, folder_name)
		if self.modpacks_count == 0:
			print("Modpacks not found! Please move .mrpack files to this folder!")

MDM()