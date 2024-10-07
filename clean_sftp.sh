#!/bin/bash

# Répertoire où sont stockés les fichiers SFTP
SFTP_DIR="/srv/sftp/dossier_partage"

# Nombre de minutes après lesquelles un fichier doit être supprimé
AGE_LIMIT=10

# Trouver et supprimer les fichiers modifiés il y a plus de 10 minutes
find "$SFTP_DIR" -type f -mmin +$AGE_LIMIT -exec rm {} \;

echo "Les fichiers de plus de $AGE_LIMIT minutes ont été supprimés."
