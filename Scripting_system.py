import urllib.request
import zipfile
import os
import pysftp

# Variables for downloading (from VM1)
server_ip = 'http://192.168.1.45'  # IP of the VM containing the ZIP file (VM1)
file_path = 'test100.sql.zip'
file_url = f'{server_ip}/{file_path}'  # URL for downloading the file

# Get the current project directory
current_dir = os.path.dirname(os.path.abspath(__file__))  # Path of the executed script
local_filename = os.path.join(current_dir, 'test100.sql.telechargement.zip')  # Local file for the ZIP
extraction_directory = os.path.join(current_dir, 'extracted_files')  # Directory for extracted files

# SFTP server details (VM2)
sftp_host = '192.168.1.209'  # IP of the SFTP server (VM2)
sftp_port = 22  # Port of the SFTP server
sftp_username = 'tse'  # Username for SFTP
sftp_password = 'tse'  # Password for SFTP
remote_directory = '/srv/sftp/dossier_partage'  # Remote directory on VM2
remote_filename = 'test100.sql'  # Name of the SQL file to upload

# Function to handle host key verification
def host_key_verification(host, key):
    # Load known host keys from a file or define your own behavior
    known_hosts_file = os.path.expanduser('~/.ssh/known_hosts')
    
    # Check if the host key is already in known_hosts
    if not os.path.exists(known_hosts_file):
        with open(known_hosts_file, 'w') as f:
            pass  # Create an empty known hosts file if it doesn't exist

    with open(known_hosts_file, 'r') as f:
        known_hosts = f.readlines()

    # Check if the host key is already known
    for line in known_hosts:
        if host in line:
            print(f"Host key for {host} is already known.")
            return True  # Host key is already known
    
    # Ask the user if they want to trust the new host key
    print(f"New host key detected for {host}:")
    print(f"Key: {key.get_fingerprint()}")
    response = input("Do you want to trust this host key? (yes/no): ")
    
    if response.lower() == 'yes':
        # Add the new host key to known_hosts
        with open(known_hosts_file, 'a') as f:
            f.write(f"{host} {key.get_name()} {key.get_base64()}\n")
        print(f"Host key for {host} added to known hosts.")
        return True
    else:
        print("Connection refused.")
        return False

# Step 1: Download the ZIP file from VM1
try:
    urllib.request.urlretrieve(file_url, local_filename)
    print(f"File downloaded and saved as {local_filename}")
except Exception as e:
    print(f"An error occurred during downloading: {e}")

# Step 2: Unzip the downloaded file
try:
    if not os.path.exists(extraction_directory):
        os.makedirs(extraction_directory)

    with zipfile.ZipFile(local_filename, 'r') as zip_ref:
        zip_ref.extractall(extraction_directory)
    print(f"Files extracted to: {extraction_directory}")
except Exception as e:
    print(f"An error occurred during extraction: {e}")

# Step 3: Upload the extracted SQL file to SFTP server
# Assuming the extracted SQL file is named test100.sql
local_sql_file_path = os.path.join(extraction_directory, 'test100.sql')  # Path to the SQL file

try:
    # Create connection options with custom host key verification
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = pysftp.HostKeys()

    # Connect to the SFTP server with host key verification
    with pysftp.Connection(host=sftp_host, port=sftp_port, username=sftp_username, password=sftp_password, cnopts=cnopts, hostkey_callback=host_key_verification) as sftp:
        print(f"Connected to SFTP server {sftp_host} on port {sftp_port}")         

        # Change to the remote directory
        sftp.chdir(remote_directory)
        print(f"Changed to remote directory: {remote_directory}")

        # Upload the SQL file
        sftp.put(local_sql_file_path, remote_filename)
        print(f"File {remote_filename} uploaded successfully to SFTP server.")

except Exception as e:
    print(f"An error occurred during the upload: {e}")
