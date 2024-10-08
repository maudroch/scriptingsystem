#!/bin/bash

# Variables de configuration
DOMAIN=""  # Remplacez par votre nom de domaine, ou laissez vide pour une IP
MAIL_HOSTNAME="mail.192.168.1.101"  # Nom d'hôte du serveur mail
EMAIL="maud.roch@gmail.com"  # Remplacez par votre adresse email

# Mettre à jour le système
sudo apt update
sudo apt upgrade -y

# Installer Postfix et mailutils
sudo apt install postfix mailutils -y

# Configurer Postfix
sudo bash -c "cat > /etc/postfix/main.cf << EOF
# Fichier de configuration principal pour Postfix
myhostname = $MAIL_HOSTNAME
mydomain = $DOMAIN
myorigin = /etc/mailname
mydestination = \$myhostname, localhost.\$mydomain, localhost, \$mydomain
relayhost = 
inet_interfaces = all
inet_protocols = all
EOF"

# Écrire le nom de domaine dans /etc/mailname
echo "$DOMAIN" | sudo tee /etc/mailname

# Redémarrer Postfix pour appliquer les changements
sudo systemctl restart postfix

# Configurer le pare-feu pour autoriser le port SMTP
sudo ufw allow 25

# Tester l'envoi d'un mail
echo "Test de l'envoi de mail via SMTP" | mail -s "Test SMTP" "$EMAIL"

# Fin du script
echo "Configuration terminée. Vérifiez votre boîte de réception pour un e-mail de test."
