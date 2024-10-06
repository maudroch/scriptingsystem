#!/bin/bash

# Met à jour la liste des paquets
sudo apt update

# Installe vsftpd
sudo apt install vsftpd -y

# Sauvegarde du fichier de configuration d'origine
sudo cp /etc/vsftpd.conf /etc/vsftpd.conf.bak

# Configuration de vsftpd
sudo bash -c 'cat > /etc/vsftpd.conf <<EOF
# Activer le serveur
listen=YES
listen_ipv6=NO

# Autoriser les connexions anonymes (mettre à NO pour désactiver)
anonymous_enable=YES

# Répertoires et fichiers
local_enable=YES
write_enable=YES
chroot_local_user=YES

# Autoriser l'accès à l'utilisateur anonyme
anon_root=/var/ftp
anon_upload_enable=YES
anon_mkdir_write_enable=YES

# Autres configurations
dirmessage_enable=YES
use_localtime=YES
xferlog_enable=YES
xferlog_file=/var/log/vsftpd.log
xferlog_std_format=YES
connect_timeout=300
pasv_enable=YES
pasv_min_port=10000
pasv_max_port=10100
EOF'

# Crée le répertoire pour les fichiers anonymes
sudo mkdir -p /var/ftp
sudo chown -R ftp:ftp /var/ftp
sudo chmod 755 /var/ftp

# Redémarre le service vsftpd pour appliquer les changements
sudo systemctl restart vsftpd

# Active vsftpd pour qu'il démarre au boot
sudo systemctl enable vsftpd

# Vérifie l'état du service
sudo systemctl status vsftpd

sudo ufw allow 21/tcp

#hostname -I  pour voir l'ip


