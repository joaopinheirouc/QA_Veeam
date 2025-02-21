import hashlib
import sys
import time



def log_message(message):
	timestamp = time.strftime("[%Y-%m-%d %H:%M:%S]")
	log_entry = f"{timestamp} {message}"

	try:
		log = open(log_file, 'a')  
		log.write(log_entry + "\n")
	except FileNotFoundError:
		log_message(f"Error: File '{log_file}' not found.")
		return None



def read_file(file_path):
	try:
		file = open(file_path, 'r')
		return file.read()
	except FileNotFoundError:
		log_message(f"Error: File '{file_path}' not found.")
		return None

def write_file(file_path,text):
	try:
		file = open(file_path, 'w')
		return file.write(text)
	except FileNotFoundError:
		log_message(f"Error: File '{file_path}' not found.")
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

	

def check_file_sync(source_file, replica_file,sync_time):
	
	last_hash = None

	while True:#It is undesirable to use third-party libraries that implement folder synchronization;
		current_hash = calculate_md5(source_file)
		if current_hash and current_hash != last_hash:# Check if there are any changes in the file compared to the replica.
			text = read_file(source_file)
			write_file(replica_file,text)
			log_message(f"Replica '{replica_file}' updated from '{source_file}'.")
			last_hash = current_hash#update the modified hash
		time.sleep(sync_time)#Synchronization should be performed periodically;



if __name__ == "__main__":
	if len(sys.argv) != 5:
		print("Write:\t source_file_path \t replica_file_path \t sync_time \t log_file")
		sys.exit(1)

	source_file = sys.argv[1]
	replica_file = sys.argv[2]
	sync_time = int(sys.argv[3])
	log_file = sys.argv[4]
 
	check_file_sync(source_file, replica_file,sync_time)