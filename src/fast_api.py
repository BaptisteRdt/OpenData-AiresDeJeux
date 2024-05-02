from fastapi import FastAPI
from router import configuration_app
from main import AiresDeJeux
from data import MoteurDB
import uvicorn

# initialisation de la BDD
try:
    moteur = MoteurDB()
except FileNotFoundError as e:
    raise f"Couldn't find the MoteurDB database due to {e}"

# Définition des données :
aires_de_jeux = AiresDeJeux()
if aires_de_jeux.nombre_aires > moteur.nombre_aires:
    aires_de_jeux.to_sqlite()

# Définir l'application FastAPI
app = FastAPI()

app = configuration_app(app)

if __name__ == "__main__":
    uvicorn.run(app)
