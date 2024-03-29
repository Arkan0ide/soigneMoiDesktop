## Installation du projet

### Prérequis

Avant de commencer l'installation du projet, veuillez vous assurer que vous disposez des éléments suivants :

- Python 3.x ou supérieur
- Pip: Pip est un gestionnaire de paquets pour Python. Vous pouvez vérifier si pip est déjà installé en tapant `pip --version` dans votre terminal.

### Étapes d'installation

1. Installation des modules Python :

    ```bash
    pip install requests customtkinter
    ```

2. Installation du module JSON :

    ```bash
    pip install json
    ```

   Note : Le module json est généralement inclus dans Python par défaut. Vous pouvez lancer la commande qui retournera une erreur si il est déjà présent

3. Installation de Tkinter (pour les interfaces graphiques):

    ```bash
    sudo apt install python3-tk
    ```

3. Lancer les containers dans le projet web:

    ```bash
    docker compose up -d
    ```

5. Lancement de l'application :
   Se placer dans le dossier de l'application et dans un terminal :

    ```bash
    python3 setup.py
    ```
