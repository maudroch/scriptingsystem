Le but de ce projet est de réaliser un system d'archivage.
Pour cela nous utilisons une machine Linus sous VirtualBox en temps que serveur web (apache2).
Sur ce serveur nous récupérons le fichier "test100.sql.zip", nous le téléchargeons et le dézippons et nous l'archivons sur une seconde VM (ubuntu).

Vérifier que vos deux VM sont bien en mode Bridge (Configuration->réseaux).

SERVEUR WEB - APACHE
Lier votre première VM (debian) à ce repositary.
Pour configurer le serveur web apache (sur la VM), mettez-vous en root. Ensuite, il suffit d'éxecuter le fichier "setup_apache2.sh", il est possible que vous n'ayez pas les droits d'exécution sur ce fichier. Dans ce cas utiliser la commande "chmod +x setup_apache2.sh". 
Une fois votre fichier bash exécuté, appuyer sur "q", vous verrez afficher l'adresse de votre serveur. Récupérer l'adresse ip de votre VM n°1 et mettez la dans votre script python.

SERVEUR DISTANT - SFTP
Lier votre deuxième VM (ubuntu) à ce repositary.
Pour configurer le serveur distant sftpe (sur la VM), éxecutez le fichier "setup_SFTP.sh", il est possible que vous n'ayez pas les droits d'exécution sur ce fichier. Dans ce cas utiliser la commande "chmod +x setup_SFTP.sh". 
Une fois votre fichier bash exécuté, appuyer sur "q", vous verrez afficher l'adresse de votre serveur.
Rendez-vous dans "srv/sftp/dossier_partage" 
Récupérer l'adresse ip de votre VM n°2 et mettez la dans votre script python.


Lancer le script python "Scripting_system.py" depuis votre hôte, ici nous utilisons vscode. 
Pour que ce code fonctionne vérifier que l'adresse ip corresponde bien à celle de votre VM.

Normalement, après run de votre code python vous devrier avoir les fichier téléchargés et dézippés.
