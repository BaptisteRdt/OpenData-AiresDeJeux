# OpenData-AiresDeJeux
Projet universitaire visant à créer une application utilisant des données publiques et libres d'accès

Free-licence

## Python
### Installation 

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
### Utilisation de l’application “AttractKids33“

Une fois l'installation terminée, lorsque toutes les étapes précédentes ont été effectuées, il suffit de lancer l’application comme tel : 

```bash
python .\src\main.py
```

### Utilisation de l'API 

Pour lancer l'API, taper la commande suivante dans le terminal : 

```bash
python .\src\fast_api.py
```

Une fois l'application lancée, vous pouvez vous rendre dans votre navigateur préféré 
sur cette URL "localhost:8000/" et taper dans l'URL les instructions suivante : 

- /get_authorization :

Vous envoie une clef API qui vous permettra d'accéder aux données de l'API 
- /get_schema :

Vous envoie le schéma de la base de données avec le nom des colonnes correspondantes
- /get_aire?key=<span style="color: #26B260">[votre clef API]</span><span style="color: #FF6666">&champs=[vos champs]&condition=[vos conditions]</span> :

Vous envoie les données de l'API, le paramètre key est obligatoire, les paramètres de l'instruction optionnels sont en rouge,
champs vous permet de n'obtenir que ces champs-ci dans la requête, et condition renvoi les 
données respectant les conditions inscrites dans le paramètre

## JavaScript

### Installation 

Dans le dossier **src_js** un fichier <span style="color: #26B260">index.html</span> et
<span style="color: #26B260">airejeux.json</span>. Ces fichiers sont la base de l'application 
web.

Pour les mettres en lignes 

