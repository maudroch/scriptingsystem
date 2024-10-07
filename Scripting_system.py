import urllib.request
import zipfile
import os
import pysftp

# Variables for downloading (from VM1)
server_ip = 'http://161.3.49.126'  # IP of the VM containing the ZIP file (VM1)
file_path = 'test100.sql.zip'
file_url = f'{server_ip}/{file_path}'  # URL for downloading the file

# Get the current project directory
current_dir = os.path.dirname(os.path.abspath(__file__))  # Path of the executed script
local_filename = os.path.join(current_dir, 'test100.sql.telechargement.zip')  # Local file for the ZIP
extraction_directory = os.path.join(current_dir, 'extracted_files')  # Directory for extracted files

# SFTP server details (VM2)
sftp_host = '161.3.40.10'  # IP of the SFTP server (VM2)
sftp_port = 22  # Port of the SFTP server
sftp_username = 'tse'  # Username for SFTP
sftp_password = 'tse'  # Password for SFTP
remote_directory = '/srv/sftp/dossier_partage'  # Remote directory on VM2
remote_filename = 'test100.sql'  # Name of the SQL file to upload

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
    # Connect to the SFTP server
    with pysftp.Connection(host=sftp_host, port=sftp_port, username=sftp_username, password=sftp_password)  as sftp:
        print(f"Connected to SFTP server {sftp_host} on port {sftp_port}")         

        # Change to the remote directory
        sftp.chdir(remote_directory)
        print(f"Changed to remote directory: {remote_directory}")

        ### # Check if the remote file exists ###
        if sftp.exists(remote_filename):
            print(f"The remote file {remote_filename} exists. Checking if it has been modified...")

            ### # Get the remote file's attributes (size, modification time, etc.) ###
            remote_file_info = sftp.stat(remote_filename)

            ### # Get the size of the local file ###
            local_file_size = os.path.getsize(local_sql_file_path)

            ### # Compare file sizes ###
            if local_file_size == remote_file_info.st_size:
                print("The file has not been modified (same size). No need to upload.")
            else:
                print("The file has been modified (size mismatch). Proceeding with upload.")

                # Upload the SQL file if it has been modified
                sftp.put(local_sql_file_path, remote_filename)
                print(f"File {remote_filename} uploaded successfully to SFTP server.")

        else:
            print(f"The remote file {remote_filename} does not exist. Uploading now.")
            sftp.put(local_sql_file_path, remote_filename)
            print(f"File {remote_filename} uploaded successfully to SFTP server.")

except Exception as e:
    print(f"An error occurred during the upload: {e}")
