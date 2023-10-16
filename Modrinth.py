import os
import zipfile
import json
import urllib.request
import hashlib

dir = os.getcwd()
modpacks_count = 0
all_mods = 0
downloaded_mods = 0
extract_file = "modrinth.index.json"

def get_sha1_hash(mod_path):
	hash_sha1 = hashlib.sha1()
	with open(mod_path, "rb") as f:
		for chunk in iter(lambda: f.read(4096), b""):
			hash_sha1.update(chunk)
	return hash_sha1.hexdigest()

def check_file_valid(index, mod_path):
	if os.path.exists(mod_path) and str(get_sha1_hash(mod_path)) == index["hashes"]["sha1"]:
		return True
	else:
		return False

for file in os.listdir(dir):
	if file.endswith(".mrpack"):
		modpacks_count += 1
		with zipfile.ZipFile(dir + "/" + file, 'r') as zip:
			zip.extract(extract_file)
		with open(extract_file) as index:
			index = json.load(index)
		folder_name = index["name"] + " " + index["dependencies"]["minecraft"]
		try:
			os.mkdir(folder_name)
		except: pass
		finally:
			print("Старт скачивания...")
			all_mods = len(index["files"])
			for index in index["files"]:
				mod_path = f"{dir}/{folder_name}/{index['path'].split('/')[1]}"
				if check_file_valid(index, mod_path):
					continue
				else:
					print(f"Скачивается [{str(downloaded_mods)}/{str(all_mods)}]")
					urllib.request.urlretrieve(index["downloads"][0], mod_path)
					downloaded_mods += 1
			print(f"Все моды успешно скачаны в {dir}/{folder_name}")
			all_mods = 0
			downloaded_mods = 0
			os.remove(extract_file)

if modpacks_count == 0:
	print("Модпаки не найдены! Пожауйста переместите файлы .mrpack в текущую папку!")