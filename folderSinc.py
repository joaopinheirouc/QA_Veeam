import hashlib
import sys
import time
import os
import shutil

def log_message(message):
	timestamp = time.strftime("[%Y-%m-%d %H:%M:%S]")
	log_entry = f"{timestamp} {message}"

	try:
		log = open(log_file, 'a')  
		log.write(log_entry + "\n")
	except FileNotFoundError:
		log_message(f"Error: File '{log_file}' not found.")
		return None



def calculate_md5(file_path):
	hash_num = hashlib.md5()
	try:
		file = open(file_path, 'rb')
		while text := file.read():
			hash_num.update(text)
	except FileNotFoundError:
		log_message(f"Error: File '{file_path}' not found.")
		return None
	return hash_num.hexdigest()

	

def check_folder_sync():

	while True:#It is undesirable to use third-party libraries that implement folder synchronization;
		
		if not os.path.exists(replica_folder):#create replica folder
			os.makedirs(replica_folder)
			log_message(f"Replica folder created : {replica_folder}")


		source_files = {f: os.path.join(source_folder, f) for f in os.listdir(source_folder)}#get all source files
		replica_files = {f: os.path.join(replica_folder, f) for f in os.listdir(replica_folder)}#get all replica files


		for files,source_path  in source_files.items(): 
			replica_path = os.path.join(replica_folder,files)

			if os.path.isdir(source_path):
				check_folder_sync(source_path,replica_path)#enter a directory
			else:#if its file 
				source_hash = calculate_md5(source_path)
				replica_hash = calculate_md5(replica_path)
				
				if not os.path.exists(replica_path):#if there is no replica file
					shutil.copy2(source_path, replica_path)
					log_message(f"New file copied: {source_path} -> {replica_path}")
				elif source_hash != replica_hash:#update the replica file
					shutil.copy2(source_path, replica_path)
					log_message(f"Replica file updated: {source_path} -> {replica_path}")

		for files, replica_path in replica_files.items():
			source_path = os.path.join(source_folder, files)

			if not os.path.exists(source_path):
				if os.path.isdir(replica_path):
					shutil.rmtree(replica_path)
					log_message(f"Deleted folder: {replica_path}")
				else:
					os.remove(replica_path)##remove file
					log_message(f"Deleted file: {replica_path}")

		time.sleep(sync_time)

if __name__ == "__main__":
	if len(sys.argv) != 5:
		print("Write:\t source_folder \t replica_foulder_path \t sync_time \t log_file")
		sys.exit(1)

	source_folder = sys.argv[1]
	replica_folder = sys.argv[2]
	sync_time = int(sys.argv[3])
	log_file = sys.argv[4]
 
	check_folder_sync()
