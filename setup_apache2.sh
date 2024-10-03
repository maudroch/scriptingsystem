#!/bin/bash

# Vérifier si l'utilisateur est root
if [ "$EUID" -ne 0 ]; then
  echo "Veuillez exécuter ce script en tant que root ou avec sudo."
  exit 1
fi

echo "Mise à jour des paquets..."
# Mettre à jour les paquets existants
sudo apt update -y

echo "Installation d'Apache2..."
# Installer Apache2
sudo apt install apache2 -y

echo "Activation d'Apache2 au démarrage..."
# Activer Apache2 pour qu'il démarre au démarrage du système
sudo systemctl enable apache2

echo "Démarrage d'Apache2..."
# Démarrer le service Apache2
sudo systemctl start apache2

echo "Configuration du pare-feu..."
# Vérifier si UFW (Uncomplicated Firewall) est installé et activer les règles pour Apache
if command -v ufw >/dev/null 2>&1; then
  sudo ufw allow 'Apache Full'
  sudo ufw enable
fi

# Autoriser le trafic HTTP dans le firewall (si UFW est activé)
sudo ufw allow 80/tcp

echo "Vérification du statut d'Apache2..."
# Vérifier que le service est actif
sudo systemctl status apache2

echo "Installation et configuration d'Apache2 terminée avec succès."

# Chemin du répertoire où placer les fichiers du serveur web
WEB_DIR="/var/www/html"

# URL du fichier à télécharger
GIT_REPO_DIR="/home/tpuser/scriptingsystem"

# Nom du fichier à enregistrer localement
FILE_NAME="test100.sql.zip"

# Vérifier que le fichier existe dans le dépôt Git cloné
if [ -f "$GIT_REPO_DIR/$FILE_NAME" ]; then
    echo "Le fichier $FILE_NAME a été trouvé dans le dépôt Git."
else
    echo "Le fichier $FILE_NAME n'a pas été trouvé dans le dépôt Git."
    exit 1
fi

# Copier le fichier du dépôt Git vers le répertoire du serveur web
cp "$GIT_REPO_DIR/$FILE_NAME" "$WEB_DIR/"

# Vérifier si le fichier a été copié avec succès
if [ -f "$WEB_DIR/$FILE_NAME" ]; then
    echo "Fichier copié avec succès dans $WEB_DIR"
else
    echo "Échec de la copie du fichier."
    exit 1
fi

# Changer les permissions pour s'assurer que le fichier est accessible
sudo chmod 644 $WEB_DIR/$FILE_NAME

# Afficher l'adresse IP de la machine
IP_ADDRESS=$(hostname -I | awk '{print $1}')
echo "Le fichier est accessible à l'adresse suivante : http://$IP_ADDRESS/$FILE_NAME"
