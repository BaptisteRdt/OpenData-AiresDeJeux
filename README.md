# OpenData-AiresDeJeux
Projet universitaire visant à créer une application utilisant des données publiques et libres d'accès

## Installation de l’application “AttractKids33“ : 

```bash 
git clone https://github.com/BaptisteRdt/OpenData-AiresDeJeux.git
cd OpenData-AiresDeJeux
```

Une fois dans le répertoire du projet, il vous suffit d’installer un environnement virtuel python, comme tel : 

```bash
python -m venv Env
```

Windows : 

```bash
Env\Scripts\activate
```

Linux : 
```bash
source Env\Scripts\activate
```

Si les commandes précédentes ne fonctionnent pas, vous pouvez  aller voir la doc pour régler votre soucis : https://docs.python.org/3/library/venv.html 

Une fois dans l’environnement virtuel installons les librairies nécessaires pour le bon fonctionnement de l’application avec la commande suivante : 

```bash
pip install -r requirements.txt
```

Enfin, lorsque toutes les étapes précédentes ont été effectuées, il suffit de lancer l’application comme tel : 

```bash
python .\src\main.py
```