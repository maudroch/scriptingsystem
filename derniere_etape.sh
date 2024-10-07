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
echo "L'adresse IP de la VM est :"
hostname -I

# Fonction pour supprimer les fichiers d'archive après 10 minutes
cleanup_old_files() {
    local retention_time=600  # Durée de rétention en secondes (10 minutes)
    local current_time=$(date +%s)

    echo "Nettoyage des fichiers d'archive plus anciens que 10 minutes dans $SFTP_DIR."

    # Connexion SFTP avec lftp
    lftp -u "$SFTP_USER","$SFTP_PASS" sftp://"$SFTP_HOST" <<EOF
        set ftp:list-options -a  # Inclut les fichiers cachés dans la liste
        cd $SFTP_DIR

        # Liste des fichiers avec leurs détails (date de modification, taille, etc.)
        cls -l --sort=time | while read -r line; do
            # Extraire la date du fichier (colonne 6,7,8) et le nom du fichier (colonne 9)
            file_date=$(echo "$line" | awk '{print $6, $7, $8}')
            file_name=$(echo "$line" | awk '{print $9}')
            
            # Convertir la date du fichier en secondes depuis l'epoch
            file_timestamp=$(date --date="$file_date" +%s 2>/dev/null)

            # Calculer l'âge du fichier
            if [[ -n "$file_timestamp" ]]; then
                file_age=$((current_time - file_timestamp))

                # Si l'âge du fichier dépasse 10 minutes, supprimer le fichier
                if [[ $file_age -gt $retention_time ]]; then
                    echo "Suppression du fichier $file_name (Âge: $((file_age / 60)) minutes)"
                    rm "$file_name"
                fi
            fi
        done
    bye
EOF
}

# Appel de la fonction de nettoyage après 10 minutes
sleep 600  # Attendre 10 minutes
cleanup_old_files
