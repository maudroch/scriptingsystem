import urllib.request
import zipfile
import os

# Variables
server_ip = 'http://192.168.1.45'#mettre l'adresse IP de la VM
file_path = 'test100.sql.zip'
file_url = f'{server_ip}/{file_path}'

# Obtenir le répertoire actuel du projet Git
current_dir = os.path.dirname(os.path.abspath(__file__))  # Chemin du script exécuté (dépôt Git local)
local_filename = os.path.join(current_dir, 'test100.sql.telechargement.zip')  # Enregistre dans le répertoire actuel
extraction_directory = os.path.join(current_dir, 'extracted_files')  # Dossier d'extraction dans le répertoire Git

# Fonction pour télécharger le fichier
def download_file(url, local_filename):
    try:
        urllib.request.urlretrieve(url, local_filename)
        print(f"Fichier téléchargé et enregistré sous {local_filename}")
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")

# Décompression du fichier ZIP
def unzip_file(zip_file_path, extraction_directory):
    try:
        # Crée le dossier d'extraction s'il n'existe pas
        if not os.path.exists(extraction_directory):
            os.makedirs(extraction_directory)
        
        # Ouvre et extrait le fichier ZIP
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(extraction_directory)
        print(f"Fichiers extraits dans le dossier : {extraction_directory}")
    except Exception as e:
        print(f"Une erreur s'est produite lors de l'extraction : {e}")

# Exécution du programme
if __name__ == '__main__':
    # Téléchargement du fichier ZIP
    download_file(file_url, local_filename)
    
    # Chemin local vers le fichier ZIP téléchargé
    zip_file_path = local_filename

    # Décompression du fichier téléchargé
    unzip_file(zip_file_path, extraction_directory)
