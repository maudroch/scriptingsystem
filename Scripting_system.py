import urllib.request
import zipfile
import os
import pysftp
import tarfile
import logging  # Ajouté pour la journalisation
from datetime import datetime  # Ajouté pour récupérer la date actuelle

# Générer la date actuelle au format AAAADDMM pour le nom de fichier
date_str = datetime.now().strftime('%Y%d%m')  # Générer le nom du fichier basé sur la date
tgz_filename = f'{date_str}.tgz'  # Nom du fichier .tgz
log_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f'backup_log_{date_str}.log')  # Nouveau chemin du fichier de log

# Configuration du logging
logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')  # Configuration de la journalisation

# Variables pour le téléchargement (depuis VM1)
server_ip = 'http://192.168.1.100'  # IP de la VM contenant le fichier ZIP (VM1)
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
