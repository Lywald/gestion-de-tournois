# Gestionnaire de Tournois d'Échecs

Bienvenue dans le gestionnaire de tournois d'échecs ! Ce projet vous permet de créer, gérer et suivre des tournois d'échecs facilement. Vous pouvez ajouter des joueurs, organiser des matchs, et générer des rapports détaillés sur les tournois.

## Fonctionnalités

- **Créer un tournoi** : Créez un nouveau tournoi avec des détails tels que le nom, le lieu, les dates, et le nombre de tours.
- **Charger un tournoi** : Chargez un tournoi existant pour le gérer ou le consulter.
- **Afficher les matchs** : Affichez les matchs d'un tour spécifique d'un tournoi.
- **Ajouter un joueur** : Ajoutez de nouveaux joueurs au système.
- **Ajouter un tour** : Ajoutez des tours supplémentaires à un tournoi chargé.
- **Lancer le tournoi** : Lancez le tournoi et suivez les résultats des matchs.
- **Rapports** : Générez des rapports détaillés sur les joueurs, les tournois, et les matchs.

## Prérequis

- Python 3.x
- Les bibliothèques Python suivantes :
  - `os`
  - `sys`
  - `json`
  - `datetime`
  - `random`
  - `msvcrt` (pour Windows)
  - `tty` et `termios` (pour Unix)

- Ce sont des librairies standard donc pas de d'installation de ces dépendances requise.

## Installation

1. Clonez ce dépôt sur votre machine locale :
   ```bash
   git clone https://github.com/Lywald/gestion-de-tournois.git
   ```

2. Accédez au répertoire du projet :
   ```bash
   cd gestion-de-tournois
   ```

3. Assurez-vous d'avoir Python 3.x installé sur votre machine.

## Utilisation

1. Exécutez le script principal pour lancer l'application :
   ```bash
   python tournoi.py
   ```

2. Utilisez les flèches haut et bas pour naviguer dans le menu principal et appuyez sur Entrée pour sélectionner une option.

3. Suivez les instructions à l'écran pour créer des tournois, ajouter des joueurs, lancer des matchs, et générer des rapports.

## Structure du Projet
- `tournoi.py` : Le point d'entrée de l'application.
- `view.py` : Gère l'affichage du menu et les interactions avec l'utilisateur.
- `controller.py` : Gère la logique de l'application et les interactions avec les données.
- `models/` : Contient les classes de modèles pour les joueurs, les tournois, les tours, et les matchs.
- `controllers/matchmaking.py` : Gère la logique de création des matchs et le déroulement des tours.
- `data_tournaments.json` : Fichier de données contenant les informations sur les tournois.
- `data_players.json` : Fichier de données contenant les informations sur les joueurs.

## Auteur

- **Pierre Igor Zarebski**


---