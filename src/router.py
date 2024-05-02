from data import MoteurDB


def configuration_app(app):
    moteur = MoteurDB()

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

    return app
