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

echo "Vérification du statut d'Apache2..."
# Vérifier que le service est actif
sudo systemctl status apache2

# Optionnel: Ouvrir le navigateur pour vérifier que le serveur web fonctionne (uniquement pour environnement de bureau)
if command -v xdg-open >/dev/null 2>&1; then
  xdg-open http://localhost
fi

echo "Installation et configuration d'Apache2 terminée avec succès."
