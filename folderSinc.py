import hashlib
import sys
import time
import os
import shutil

def log_message(message):
		timestamp = time.strftime("[%Y-%m-%d %H:%M:%S]")
		log_entry = f"{timestamp} {message}"

		try:
			with open(log_file, 'a') as log:
				log.write(log_entry + "\n")
		except Exception as e:
			print(f"Logging Error: {e}")

def calculate_md5(file_path):
	hash_num = hashlib.md5()
	try:
		file = open(file_path, 'rb')
		while text := file.read():
			hash_num.update(text)
		return hash_num.hexdigest()
	except FileNotFoundError:
		log_message(f"Error: File '{file_path}' not found.")
		return None
	except Exception as e:
		log_message(f"Error calculating MD5 {file_path}: {e}")
		return None

def check_folder_sync(source_folder, replica_folder):
	
	if not os.path.exists(replica_folder):  #create replica folder
		os.makedirs(replica_folder)
		log_message(f"Created replica folder: {replica_folder}")

	source_files = {f: os.path.join(source_folder, f) for f in os.listdir(source_folder)}#get all source files
	replica_files = {f: os.path.join(replica_folder, f) for f in os.listdir(replica_folder)}#get all replica files

	# Copy or update files from source to replica
	for file_name, source_path in source_files.items():#iterate over source folders and their files
		replica_path = os.path.join(replica_folder, file_name)#create a replica path for each file

		if os.path.isdir(source_path):
			check_folder_sync(source_path, replica_path)#iterate over source directories
		else:
			source_hash = calculate_md5(source_path)
			replica_hash = calculate_md5(replica_path) if os.path.exists(replica_path) else None

			if not os.path.exists(replica_path):#if there is no replica file
				shutil.copy2(source_path, replica_path)
				log_message(f"New replica file copied: {source_path} -> {replica_path}")
			elif source_hash != replica_hash:#update the replica file
				shutil.copy2(source_path, replica_path)
				log_message(f"Replica file updated: >{source_path} -> {replica_path}")

	# Remove files/folders in replica that no longer exist in source
	for file_name, replica_path in replica_files.items():#iterate over replica files and folders
		source_path = os.path.join(source_folder, file_name)

		if not os.path.exists(source_path):#if there is no source path eliminate
			if os.path.isdir(replica_path):#use source path for checking replicas presence
				shutil.rmtree(replica_path)
				log_message(f"Deleted folder: {replica_path}")
			else:##remove file
				os.remove(replica_path)
				log_message(f"Deleted file: {replica_path}")

def main():
	while True:#It is undesirable to use third-party libraries that implement folder synchronization;
		try:
			check_folder_sync(source_folder, replica_folder)
			time.sleep(sync_time)
		except KeyboardInterrupt:
			print("\nSync process terminated.")
			log_message("Sync process terminated by user.")
			break
		except Exception as e:
			log_message(f"Unexpected error: {e}")

if __name__ == "__main__":
	if len(sys.argv) != 5:
		print("Usage: python script.py <source_folder> <replica_folder> <sync_time> <log_file>")
		sys.exit(1)

	source_folder = sys.argv[1]
	replica_folder = sys.argv[2]
	sync_time = int(sys.argv[3])
	log_file = sys.argv[4]

	main()