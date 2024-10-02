#!/bin/bash

# Mettre à jour les paquets
sudo apt update -y

# Installer Apache2
sudo apt install apache2 -y

# Démarrer Apache2
sudo systemctl start apache2

# Activer Apache2 pour qu'il démarre automatiquement au démarrage de la VM
sudo systemctl enable apache2

# Vérifier le statut du service Apache2
sudo systemctl status apache2

