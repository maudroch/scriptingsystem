import urllib.request
import zipfile
import os
import pysftp
import tarfile
import logging  # Ajouté pour la journalisation
from datetime import datetime  # Ajouté pour récupérer la date actuelle
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import smtplib

# Générer la date actuelle au format AAAADDMM pour le nom de fichier
date_str = datetime.now().strftime('%Y%d%m')  # Générer le nom du fichier basé sur la date
tgz_filename = f'{date_str}.tgz'  # Nom du fichier .tgz
log_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f'backup_log_{date_str}.log')  # Nouveau chemin du fichier de log

# Configuration du logging
logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')  # Configuration de la journalisation

# Variables pour le téléchargement (depuis VM1)
server_ip = 'http://192.168.1.107'  # IP de la VM contenant le fichier ZIP (VM1)
file_path = 'test100.sql.zip'
file_url = f'{server_ip}/{file_path}'  # URL pour télécharger le fichier

# Obtenir le répertoire actuel du projet
current_dir = os.path.dirname(os.path.abspath(__file__))  # Chemin du script exécuté
local_filename = os.path.join(current_dir, 'test100.sql.telechargement.zip')  # Fichier local pour le ZIP
extraction_directory = os.path.join(current_dir, 'extracted_files')  # Répertoire pour les fichiers extraits

# Détails du serveur SFTP (VM2)
sftp_host = '192.168.1.101'  # IP du serveur SFTP (VM2)
sftp_port = 22  # Port du serveur SFTP
sftp_username = 'tse'  # Nom d'utilisateur pour SFTP
sftp_password = 'tse'  # Mot de passe pour SFTP
remote_directory = '/srv/sftp/dossier_partage'  # Répertoire distant sur VM2

# Étape 1 : Télécharger le fichier ZIP depuis VM1
try:
    urllib.request.urlretrieve(file_url, local_filename)
    logging.info(f"Fichier téléchargé et enregistré sous {local_filename}")  # Enregistrer l'événement de téléchargement réussi
except Exception as e:
    logging.error(f"Erreur lors du téléchargement : {e}")  # Enregistrer l'erreur

# Étape 2 : Dézipper le fichier téléchargé
try:
    if not os.path.exists(extraction_directory):
        os.makedirs(extraction_directory)

    with zipfile.ZipFile(local_filename, 'r') as zip_ref:
        zip_ref.extractall(extraction_directory)
    logging.info(f"Fichiers extraits dans : {extraction_directory}")  # Enregistrer l'événement d'extraction réussi
except Exception as e:
    logging.error(f"Erreur lors de l'extraction : {e}")  # Enregistrer l'erreur

# Chemin vers le fichier SQL extrait
local_sql_file_path = os.path.join(extraction_directory, 'test100.sql')  # Chemin vers le fichier SQL

# Étape 3 : Créer un fichier .tgz à partir du fichier SQL extrait
tgz_file_path = os.path.join(current_dir, tgz_filename)  # Créer le chemin du fichier .tgz

try:
    with tarfile.open(tgz_file_path, "w:gz") as tar:  # Compresser le fichier en .tgz
        tar.add(local_sql_file_path, arcname=os.path.basename(local_sql_file_path))
    logging.info(f"Fichier compressé sous {tgz_file_path}")  # Enregistrer l'événement de compression réussi
except Exception as e:
    logging.error(f"Erreur lors de la compression : {e}")  # Enregistrer l'erreur

# Étape 4 : Télécharger le fichier .tgz sur le serveur SFTP
try:
    # Connecter au serveur SFTP
    with pysftp.Connection(host=sftp_host, port=sftp_port, username=sftp_username, password=sftp_password) as sftp:
        logging.info(f"Connecté au serveur SFTP {sftp_host} sur le port {sftp_port}")  # Enregistrer la connexion réussie

        # Changer vers le répertoire distant
        sftp.chdir(remote_directory)
        logging.info(f"Changement au répertoire distant : {remote_directory}")  # Enregistrer le changement de répertoire

        # Télécharger le fichier .tgz (indépendamment de la modification)
        sftp.put(tgz_file_path, tgz_filename)  # Téléverser le fichier .tgz
        logging.info(f"Fichier {tgz_filename} téléchargé avec succès sur le serveur SFTP.")  # Enregistrer l'événement de téléchargement réussi

except Exception as e:
    logging.error(f"Erreur lors du téléchargement : {e}")  # Enregistrer l'erreur
    
# Fonction pour envoyer un e-mail
def send_email(smtp_server, smtp_port, smtp_username, smtp_password, to_email, subject, body, log_file=None):
    try:
        msg = MIMEMultipart()
        msg['From'] = smtp_username
        msg['To'] = to_email
        msg['Subject'] = subject
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Attacher le fichier de log si spécifié
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
smtp_server = 'smtp.gmail.com'  # Remplacez par votre serveur SMTP
smtp_port = 587  # Port SMTP (587 pour TLS)
smtp_username = 'hunt3r73000@gmail.com'  # Remplacez par votre adresse e-mail
smtp_password = 'mkfgxoyufjmedupf'  # Remplacez par votre mot de passe
to_email = 'moreau.romain730@gmail.com'  # Adresse e-mail du destinataire
subject = f"Rapport de sauvegarde pour {date_str}"  # Titre de l'e-mail
body = f"Le processus de sauvegarde a été exécuté avec succès. Consultez le fichier de log ci-joint pour plus de détails."

# Envoyer l'e-mail avec le fichier de log attaché
send_email(smtp_server, smtp_port, smtp_username, smtp_password, to_email, subject, body, log_file_path)
