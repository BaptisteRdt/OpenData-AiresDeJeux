from data import MoteurDB
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi import Request


def configuration_app(app):

    moteur = MoteurDB()

    app.mount(
        "/static",
        StaticFiles(directory="src/static"),
        name="static")
    templates = Jinja2Templates(directory="src/templates")

    @app.get('/')
    def home():
        return "Bienvenue dans notre API Aires de jeux Bordelaise"

    @app.get('/get_authorization')
    def get_authorization():
        return moteur.get_authorization()

    @app.get('/get_schema')
    def get_schema(key: str):
        return moteur.get_schema(key)

    @app.get('/get_aire')
    def get_aires(key: str, champs: str = '*', condition: str = None):
        return moteur.get_aires(key, champs, condition)

    @app.get('/application_js', response_class=HTMLResponse)
    def application_js(request: Request):
        return templates.TemplateResponse("index.html", {"request": request})

    return app
