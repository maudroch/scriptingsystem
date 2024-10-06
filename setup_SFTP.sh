#!/bin/bash

# Met à jour la liste des paquets
sudo apt update

# Installe OpenSSH (inclut le serveur SFTP)
sudo apt install openssh-server -y

# Sauvegarde du fichier de configuration d'origine
sudo cp /etc/ssh/sshd_config /etc/ssh/sshd_config.bak

# Configuration de sshd_config pour activer SFTP
sudo bash -c 'cat >> /etc/ssh/sshd_config <<EOF

# Configuration SFTP
Subsystem sftp internal-sftp

# Crée un groupe pour les utilisateurs SFTP
Match Group sftpusers
    ChrootDirectory /srv/sftp/%u
    ForceCommand internal-sftp
    AllowTcpForwarding no
EOF'

# Crée les répertoires pour SFTP
sudo mkdir -p /srv/sftp
sudo groupadd sftpusers  # Crée le groupe sftpusers
sudo chown root:root /srv/sftp
sudo chmod 755 /srv/sftp

# Crée un répertoire de partage pour un utilisateur (à adapter selon vos besoins)
sudo mkdir -p /srv/sftp/dossier_partage
sudo chown :sftpusers /srv/sftp/dossier_partage
sudo chmod 777 /srv/sftp/dossier_partage

# Redémarre le service SSH pour appliquer les changements
sudo systemctl restart ssh

# Active OpenSSH pour qu'il démarre au boot
sudo systemctl enable ssh

# Vérifie l'état du service
sudo systemctl status ssh

# Permet l'accès SFTP à travers le firewall
sudo ufw allow OpenSSH

# Affiche l'adresse IP
hostname -I  # Pour voir l'IP
