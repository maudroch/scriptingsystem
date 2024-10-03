Le but de ce projet est de réaliser un system d'archivage.
Pour cela nous utilisons une machine Linus sous VirtualBox en temps que serveur web (apache2).
Sur ce serveur nous récupérons le fichier "test100.sql.zip", nous le téléchargeons et le dézippons et nous l'archivons sur une seconde VM.

Lier votre VM à ce repositary.
Pour configurer le server web apache (sur la VM) il suffit d'éxecuter le fichier "setup_apache2.sh".
Vérifier que votre machine est bien en mode Bridge (Configuration->réseaux).
Lancer le script python "Scripting_system.py" depuis votre hôte, ici nous utilisons vscode. 
Pour que ce code fonctionne vérifier que l'adresse ip corresponde bien à celle de votre VM.

Normalement, après run de votre code python vous devrier avoir les fichier téléchargés et dézippés.
