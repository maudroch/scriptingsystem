BUT
Le but de ce projet est de réaliser un system d'archivage.
Pour cela nous utilisons une machine Linus sous VirtualBox en temps que serveur web (apache2).
Sur ce serveur nous récupérons le fichier "test100.sql.zip", nous le téléchargeons et le dézippons et nous l'archivons sur une seconde VM (ubuntu).

CONFIGURATION - VMs
Vérifier que vos deux VM sont bien en mode Bridge (Configuration->réseaux).

SERVEUR WEB - APACHE
Lier votre première VM (debian) à ce repositary.
Pour configurer le serveur web apache (sur la VM), mettez-vous en root. Ensuite, il suffit d'éxecuter le fichier "setup_apache2.sh", il est possible que vous n'ayez pas les droits d'exécution sur ce fichier. Dans ce cas utiliser la commande "chmod +x setup_apache2.sh". 
Une fois votre fichier bash exécuté, appuyer sur "q", vous verrez afficher l'adresse de votre serveur. Récupérer l'adresse ip de votre VM n°1 et mettez la dans votre script python.

SERVEUR DISTANT - SFTP
Lier votre deuxième VM (ubuntu) à ce repositary.
Pour configurer le serveur distant sftpe (sur la VM), éxecutez le fichier "setup_SFTP.sh", il est possible que vous n'ayez pas les droits d'exécution sur ce fichier. Dans ce cas utiliser la commande "chmod +x setup_SFTP.sh". 
Une fois votre fichier bash exécuté, appuyer sur "q", vous verrez afficher l'adresse de votre serveur. 
Récupérer l'adresse ip de votre VM n°2 et mettez la dans votre script python.


WINDOWS
Ouvrez un terminal vérifier que python est bien intsallé "python --version" si ce n'est pas le cas installer le "pyhton".
Vérifier que pysftp est installer "pip pysftp" si ce n'est pas le cas "pip install pysftp".
Assurer vous que vous possedez une clef ssh (sinon :"ssh-keygen -t rsa -b 4096 -C "email@adresse.com" ") et un fichier "known_hosts".
La configuration WINDOWS suivante n'est normalement pas nécessaire, cependant si vous renconter des problèmes suiver les instruction ci dessous
(Connectez-vous une première fois au serveur en utilisant l'invite de commande "tse@adresseIPVM2". Mot de passe "tse". Répondre "yes".)

SCRIPT PYTHON
A prèsent vous pouvez éxecuter le script python "Scripting_System.py", ici nous utilisons vscode. 
Pour que ce code fonctionne vérifier que les adresses ip correspondent bien à celles de vos VMs.

Normalement, après run de votre code python vous devrier avoir les fichier téléchargés et dézippés dans vos docs en local et le fichier dézipper sur le serveur distant dans le dossier "dossier_partage".

Pour activer la suppression des fichiers au bout d'un certain temps faire : 
sudo crontab -e
tu choisis le fichier nano (1)
et tu ajoutes cette ligne de commande : 
*/5 * * * * /home/tse/scriptingsystem/clean_sftp.sh


