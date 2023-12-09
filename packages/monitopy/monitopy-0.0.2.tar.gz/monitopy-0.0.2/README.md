# monitopy

`monitopy` est une bibliothèque Python simple mais puissante pour la surveillance des changements dans les fichiers et répertoires.

## Fonctionnalités

- Détection des modifications : Surveillez les créations, modifications et suppressions de fichiers et répertoires.
- Filtrage personnalisé : Définissez des filtres pour surveiller uniquement certains types de fichiers, extensions ou répertoires.
- Gestion des événements avancée : Définissez des actions spécifiques à des événements, comme lancer des scripts en réponse à certaines modifications.
- Intégration avec les services cloud : Synchronisation automatique des changements avec des services cloud tels que AWS S3, Google Drive, etc.
- Journalisation améliorée : Stockez des informations détaillées sur les changements survenus au fil du temps.

## Installation

Pas encore mis sur pypi.org
```bash
pip install monitopy==0.0.1
```

## Exemples d'utilisation

```py
import logging

from monitopy.spectator import FileWatcher

# Configuration du module logging
logging.basicConfig(filename='monitopy.log', level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# Fonction de callback pour la gestion des événements
def on_file_change(event):
    if not event.src_path.endswith("monitopy.log"):
        log_message = f"Changement détecté : {event.src_path} ({event.event_type})"
        print(log_message)
        logging.info(log_message)

# Créer une instance du FileWatcher
watcher = FileWatcher("/chemin/vers/le/dossier/", callback=on_file_change)

# Commencer la surveillance
watcher.start()
```

## Contribution
Les contributions sont les bienvenues ! Si vous avez des idées d'amélioration, des problèmes à signaler ou des fonctionnalités à demander, n'hésitez pas à ouvrir une issue ou à créer une pull request.

## Licence
Ce projet est sous licence MIT

