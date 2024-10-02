#!/bin/bash

# Script pour installer et configurer Apache2 sur une VM Linux

# Fonction pour afficher un message d'erreur et quitter
function error_exit {
    echo "$1" 1>&2
    exit 1
}

# Mettre à jour le système
echo "Mise à jour du système..."
sudo apt update && sudo apt upgrade -y || error_exit "Erreur lors de la mise à jour du système."

# Installer Apache2
echo "Installation d'Apache2..."
sudo apt install apache2 -y || error_exit "Erreur lors de l'installation d'Apache2."

# Démarrer le service Apache2
echo "Démarrage du service Apache2..."
sudo systemctl start apache2 || error_exit "Erreur lors du démarrage d'Apache2."

# Activer Apache2 pour démarrer au démarrage du système
sudo systemctl enable apache2 || error_exit "Erreur lors de l'activation d'Apache2 au démarrage."

# Configurer le pare-feu (si ufw est utilisé)
if command -v ufw >/dev/null 2>&1; then
    echo "Configuration du pare-feu..."
    sudo ufw allow 'Apache Full' || error_exit "Erreur lors de la configuration du pare-feu."
    sudo ufw enable || error_exit "Erreur lors de l'activation du pare-feu."
fi

# Vérifier l'état du service Apache
echo "Vérification de l'état du service Apache2..."
sudo systemctl status apache2

# (Optionnel) Cloner un dépôt Git dans le répertoire par défaut d'Apache
read -p "Souhaitez-vous cloner un dépôt Git dans /var/www/html ? (y/n): " clone_choice
if [[ "$clone_choice" == "y" ]]; then
    read -p "Entrez l'URL du dépôt Git : " git_repo
    echo "Clonage du dépôt Git..."
    sudo git clone "$git_repo" /var/www/html || error_exit "Erreur lors du clonage du dépôt Git."
fi

echo "Configuration terminée ! Vous pouvez accéder à votre serveur Apache sur http://localhost"
