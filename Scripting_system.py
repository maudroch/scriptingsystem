import urllib.request
import zipfile
import os
import paramiko 
import tarfile
import logging  
from datetime import datetime 
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import smtplib
import json

# Lire le fichier de configuration JSON pour configurer les adresses IP
with open('config.json') as config_file:
    config = json.load(config_file)


ip1 = config['serveur']['ip1']
ip2 = config['serveur']['ip2']

# Générer la date actuelle au format AAAADDMM pour le nom de fichier
date_str = datetime.now().strftime('%Y%d%m')  # Générer le nom du fichier basé sur la date
tgz_filename = f'{date_str}.tgz'  # Nom du fichier .tgz
log_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f'backup_log_{date_str}.log')  # Nouveau chemin du fichier de log

# Configuration pour les fichiers back_log
logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')  # Configuration de la journalisation

#Config de la VM1 pour 
server_ip = ip1  # IP de la VM contenant le fichier ZIP 
file_path = 'test100.sql.zip'
file_url = f'{server_ip}/{file_path}'  # URL pour télécharger le fichier

# Obtenir le répertoire actuel du projet
current_dir = os.path.dirname(os.path.abspath(__file__))  # Chemin du script exécuté
local_filename = os.path.join(current_dir, 'test100.sql.telechargement.zip')  # Fichier local pour le ZIP
extraction_directory = os.path.join(current_dir, 'extracted_files')  # Répertoire pour les fichiers extraits

# Configuration du serveur SFTP 
sftp_host = ip2  
sftp_port = 22  # Port du serveur SFTP
sftp_username = 'tse'  
sftp_password = 'tse' 
remote_directory = '/srv/sftp/dossier_partage'  

# Étape 1 : Télécharger le fichier ZIP depuis VM1
try:
    urllib.request.urlretrieve(file_url, local_filename)
    logging.info(f"Fichier téléchargé et enregistré sous {local_filename}") 
except Exception as e:
    logging.error(f"Erreur lors du téléchargement : {e}")  

# Étape 2 : Dézipper le fichier téléchargé
try:
    if not os.path.exists(extraction_directory):
        os.makedirs(extraction_directory)

    with zipfile.ZipFile(local_filename, 'r') as zip_ref:
        zip_ref.extractall(extraction_directory)
    logging.info(f"Fichiers extraits dans : {extraction_directory}") 
except Exception as e:
    logging.error(f"Erreur lors de l'extraction : {e}")  

# Chemin vers le fichier SQL extrait
local_sql_file_path = os.path.join(extraction_directory, 'test100.sql') 

# Étape 3 : Créer un fichier .tgz à partir du fichier SQL extrait
tgz_file_path = os.path.join(current_dir, tgz_filename)  

try:
    with tarfile.open(tgz_file_path, "w:gz") as tar:  # Compresser le fichier en .tgz
        tar.add(local_sql_file_path, arcname=os.path.basename(local_sql_file_path))
    logging.info(f"Fichier compressé sous {tgz_file_path}") 
except Exception as e:
    logging.error(f"Erreur lors de la compression : {e}")  

# Étape 4 : Télécharger le fichier .tgz sur le serveur SFTP
try:
    client = paramiko.SSHClient()

    # Si il ne connaît pas la clé, il accepte la connection et il l'enregistre
    known_hosts_file = os.path.expanduser("~/.ssh/known_hosts")
    if os.path.exists(known_hosts_file):
        client.load_host_keys(known_hosts_file)

    
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Connection au serveur SFTP
    client.connect(hostname=sftp_host, port=sftp_port, username=sftp_username, password=sftp_password)
    logging.info(f"Connecté au serveur SFTP {sftp_host} sur le port {sftp_port}")  

  
    sftp = client.open_sftp()

    # Met le fichier sur le répertoire distant
    sftp.chdir(remote_directory)
    logging.info(f"Changement au répertoire distant : {remote_directory}") 

    # Télécharger le fichier .tgz 
    sftp.put(tgz_file_path, tgz_filename)  
    logging.info(f"Fichier {tgz_filename} téléchargé avec succès sur le serveur SFTP.") 

    sftp.close()
    client.close()

except Exception as e:
    logging.error(f"Erreur lors du téléchargement : {e}") 
    
#Etape 5: envoyer un e-mail
def send_email(smtp_server, smtp_port, smtp_username, smtp_password, to_email, subject, body, log_file=None):
    try:
        msg = MIMEMultipart()
        msg['From'] = smtp_username
        msg['To'] = to_email
        msg['Subject'] = subject
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Attacher le fichier de log 
        if log_file:
            with open(log_file, 'rb') as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(log_file)}')
                msg.attach(part)

        # Connexion et envoi de l'e-mail
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Activer TLS
            server.login(smtp_username, smtp_password)
            server.send_message(msg)

        logging.info(f"E-mail envoyé à {to_email} avec succès.")
    except Exception as e:
        logging.error(f"Erreur lors de l'envoi de l'e-mail : {e}")

# Paramètres de l'e-mail
smtp_server = 'smtp.gmail.com'  
smtp_port = 587  # Port SMTP
smtp_username = 'hunt3r73000@gmail.com'
smtp_password = 'mkfgxoyufjmedupf'  
to_email = 'moreau.romain730@gmail.com' 
subject = f"Rapport de sauvegarde pour {date_str}"  
body = f"Le processus de sauvegarde a été exécuté avec succès. Consultez le fichier de log ci-joint pour plus de détails."

# Envoyer l'e-mail avec le fichier de log attaché
send_email(smtp_server, smtp_port, smtp_username, smtp_password, to_email, subject, body, log_file_path)
