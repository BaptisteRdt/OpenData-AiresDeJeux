import tkinter
import tkintermapview
from PIL import Image, ImageTk
import requests
import glob
from tkinter.simpledialog import askinteger, askfloat

# Définir des variables globales pour stocker les valeurs d'entrée de l'utilisateur
age_min = None
age_max = None
surface_max = None

app_tk = tkinter.Tk()
app_tk.geometry(f"{1000}x{600}")

map_widget = tkintermapview.TkinterMapView(app_tk, width=2000, height=2000, corner_radius=5)
map_widget.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

button_frame = tkinter.Frame(app_tk)
button_frame.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER)


def set_age_min():
    global age_min
    age_min = askinteger("Age minimum", "Entrez l'âge minimum:")
    if age_min is not None:
        print(f"Age minimum choisi: {age_min}")


def set_age_max():
    global age_max
    age_max = askinteger("Age maximum", "Entrez l'âge maximum:")
    if age_max is not None:
        print(f"Age maximum choisi: {age_max}")


def set_surface_max():
    global surface_max
    surface_max = askfloat("Surface maximum", "Entrez la surface maximum (en m²):")
    if surface_max is not None:
        print(f"Surface maximum choisie: {surface_max}")


def update_data():
    global age_min, age_max, surface_max

    # Filtrer les données en fonction des critères spécifiés
    filtered_data = [aire for aire in data.aires if (age_min is None or aire.age_min >= age_min)
                     and (age_max is None or aire.age_max <= age_max)
                     and (surface_max is None or aire.surface <= surface_max)]

    # Effacer tous les polygones de la carte
    map_widget.delete_all_polygon()

    # Afficher les aires de jeux filtrées sur la carte
    for aire in filtered_data:
        for polygone_id in aire.polygone_coords:
            map_widget.set_polygon(aire.polygone_coords[polygone_id], command=polygon_click, name=aire.nom,
                                   outline_color="purple", data=aire)


button_ageMin = tkinter.Button(button_frame, text="Bouton Age Min", width=15, height=2, command=set_age_min)
button_ageMin.pack(side=tkinter.LEFT, padx=10)

button_ageMax = tkinter.Button(button_frame, text="Bouton Age Max", width=15, height=2, command=set_age_max)
button_ageMax.pack(side=tkinter.LEFT, padx=10)

button_Surface = tkinter.Button(button_frame, text="Bouton Surface", width=15, height=2, command=set_surface_max)
button_Surface.pack(side=tkinter.LEFT, padx=10)

button_Actualisation = tkinter.Button(button_frame, text="Bouton Actualisation", width=15, height=2,
                                      command=update_data)
button_Actualisation.pack(side=tkinter.LEFT, padx=10)

button_frame.lift()


def load_api() -> dict:
    url = ("https://opendata.bordeaux-metropole.fr/api/explore/v2.1/catalog/datasets/bor_airejeux/records?select="
           "age_min%2C%20age_max%2C%20geo_shape%2C%20nom_site%2C%20nb_jeux%2C%20surface%2C%20geo_point_2d%2C%20gid&"
           "limit=-1")
    response = requests.get(url)
    return response.json()['results']


def define_polygone_coords(air):
    if air['geo_shape']['geometry']['type'] == 'Polygon':
        return {idx: [(point[1], point[0]) for point in polygone] for idx, polygone in
                enumerate(air['geo_shape']['geometry']['coordinates'])}
    elif air['geo_shape']['geometry']['type'] == 'MultiPolygon':
        return {idx: [(point[1], point[0]) for point in polygone[0]] for idx, polygone in
                enumerate(air['geo_shape']['geometry']['coordinates'])}


def polygon_click(polygone):
    latitude, longitude = polygone.data.point_coords
    map_widget.set_position(latitude + 0.0005, longitude)
    map_widget.set_zoom(18)
    polygone.data.change_marker()
    print(f"Vous avez cliqué sur l'air de jeux : {polygone.name}")


def image_click(marker):
    marker.data.change_marker()


class AireDeJeux:
    def __init__(self, gid: int, age_min: int, age_max: int, polygone_coords: dict, polygone_type: str,
                 nom: str, surface: float, nombre_de_jeux: int, point_coords: list):
        self.id = gid
        self.age_min = age_min
        self.age_max = age_max
        self.polygone_coords = polygone_coords
        self.type_polygone = polygone_type
        self.nom = nom
        self.surface = surface
        self.nombre_de_jeux = nombre_de_jeux
        self.point_coords = point_coords
        self.image_filename = glob.glob(f"images/{nom}.*")[0][7:] if glob.glob(f"images/{nom}.*") != [] \
            else "no_photo.jpg"
        self.hidden_marker = True
        self.marker = None

    def show_marker(self):
        self.marker = map_widget.set_marker(self.point_coords[0] + 0.001,
                                            self.point_coords[1],
                                            data=self,
                                            command=image_click,
                                            icon=ImageTk.PhotoImage(
                                                Image.open(f"images/{self.image_filename}").resize((300, 300))))
        self.hidden_marker = False

    def hide_marker(self):
        self.marker.delete()
        self.hidden_marker = True

    def change_marker(self):
        if self.hidden_marker:
            self.show_marker()
        else:
            self.hide_marker()

    def __str__(self):
        return (f'{self.nom}: \n\tsurface : {self.surface}\n\tage minimum : {self.age_min}'
                f'\n\tage maximum : {self.age_max}\n\tnombre de jeux : {self.nombre_de_jeux}'
                f'\n\tpolygones : \n\t\t{[print(f'\t\tpolygone {polygone_id} : {self.polygone_coords[polygone_id]}\n')
                                          for polygone_id in self.polygone_coords]}')


class AiresDeJeux:
    def __init__(self):
        data = load_api()
        self.aires = [AireDeJeux(gid=aire['gid'],
                                 age_min=aire['age_min'],
                                 age_max=aire['age_max'],
                                 polygone_coords=define_polygone_coords(aire),
                                 polygone_type=aire['geo_shape']['geometry']['type'],
                                 nom=aire['nom_site'],
                                 surface=aire['surface'],
                                 nombre_de_jeux=aire['nb_jeux'] if aire['nb_jeux'] is not None else 0,
                                 point_coords=[float(aire['geo_point_2d']['lat']), float(aire['geo_point_2d']['lon'])])
                      for aire in data]
        self.nombre_aires = len(data)

    def draw_polygones(self, map_widget):
        for aire in self.aires:
            for polygone_id in aire.polygone_coords:
                map_widget.set_polygon(aire.polygone_coords[polygone_id], command=polygon_click, name=aire.nom,
                                       outline_color="purple", data=aire)
        return map_widget

    def __str__(self):
        return f"Nombre d'airs de jeux: {self.nombre_aires}, {[f"\n{print(aire)}" for aire in self.aires]}"


if __name__ == "__main__":
    data = AiresDeJeux()
    map_widget = data.draw_polygones(map_widget)

    map_widget.set_position(44.86596236872216, -0.5757273765736807)
    map_widget.set_zoom(18)
    app_tk.mainloop()
