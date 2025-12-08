import fltk
from load import loads
from typing import List, Tuple, Dict
from math import log, tan, pi, radians, degrees, sqrt

MERC = lambda x: degrees(log(tan(radians(x) / 2 + pi / 4)))

class Polygon:

    def __init__(self, points : List[Tuple[int, int]], bbox : Tuple[int, int, int, int], colour : str = "black", fill : str = "", thickness : float = 2.0) -> None:
        self.bbox : Tuple[int, int, int, int] = bbox
        self.points : List[Tuple[int, int]] = points
        self.colour : str = colour
        self.fill : str = fill
        self.thickness : float = thickness
        self.flattened : bool = False
    
    def draw(self) -> int:
        return fltk.polygone(self.points, couleur = self.colour, remplissage = self.fill, epaisseur = self.thickness)

    def flatten_points(self) -> None:
        if self.flattened: print("! WARNING ! flattening a polygon two times")
        for i in range(len(self.points)):
            self.points[i] = self.points[i][0], MERC(self.points[i][1])
        self.bbox = self.bbox[0], MERC(self.bbox[1]), self.bbox[2], MERC(self.bbox[3])
        self.flattened = True

    def recalc_bbox(self) -> None:
        minw : float = self.points[0][0]; maxw : float = self.points[0][1]; minh : float = self.points[0][0]; maxh : float = self.points[0][1]
        for point in self.points:
            if point[0] < minw: minw = point[0]
            if point[0] > maxw: maxw = point[0]
            if point[1] < minh: minh = point[1]
            if point[1] > maxh: maxh = point[1]
        self.bbox = minw, maxw, minh, maxh

class Cercle:
    def __init__(self, position : Tuple[int, int], radius : float, metadata : Dict):
        self.position : Tuple[int, int] = position
        self.radius : float = radius
        self.metadata : Dict = metadata
        self.flattened : bool = False

    def flatten(self):
        if self.flattened: print("! WARNING ! flattening a circle two times")
        self.position = self.position[0], MERC(self.position[1])
        self.flattened = True

    def boucle(self):
        self.position = []
        for e in self.liste_info:
            # appliquer projection + mise à l'échelle
            x = self.drawer.a * e["lon"] + self.drawer.B
            y = -self.drawer.a * MERC(e["lat"]) + self.drawer.C
            fltk.cercle(x, y, 5, couleur="red", remplissage="red")
            self.position.append((x, y, e))

    def draw(self):
        fltk.cercle(self.position[0], self.position[0], self.radius, couleur= "red", remplissage="red")

    def detect_click(self, client_x, client_y):
        return (client_x - self.position[0]) ** 2 + (client_y - self.position[1]) ** 2 <= self.radius ** 2


class Drawer:

    def __init__(self) -> None:

        self.window : Tuple[int, int] = 1000, 500
        fltk.cree_fenetre(self.window[0], self.window[1])

        self.thickness : float = 2.0
        self.circles = List[Cercle] = []
        self.functions  = []
        self.polygons : List[Polygon] = []

        self.a, self.B, self.C = 0, 0, 0

    def translate_polygons(self):
        for polygon in self.polygons:
            for i in range(len(polygon.points)):
                polygon.points[i] = self.a * polygon.points[i][0] + self.B, - self.a * polygon.points[i][1] + self.C
        
    def define_parameters(self, target_box : Tuple[int, int, int, int]):
        all_bbox : List[int] = [ 0xffffffff, 0xffffffff, -0xffffffff, -0xffffffff ]
        for polygon in self.polygons:
            polygon.flatten_points()
            
            if polygon.bbox[0] < all_bbox[0]: all_bbox[0] = polygon.bbox[0]
            if polygon.bbox[1] < all_bbox[1]: all_bbox[1] = polygon.bbox[1]
            if polygon.bbox[2] > all_bbox[2]: all_bbox[2] = polygon.bbox[2]
            if polygon.bbox[3] > all_bbox[3]: all_bbox[3] = polygon.bbox[3]

        self.a = min(
            target_box[2] / (all_bbox[2] - all_bbox[0]), 
            target_box[3] / (all_bbox[3] - all_bbox[1])
        )
        self.B, self.C = target_box[0] - self.a * all_bbox[0], target_box[1] + self.a * all_bbox[3]

    def affiche_infos(self, restaurant):
        fltk.efface_tout()
        fltk.texte(50, 50, f"Nom : {restaurant['title']}", "black")
        fltk.texte(50, 80, f"Contact : {restaurant['contact']}", "black")
        fltk.texte(50, 110, f"Infos : {restaurant['infos']}", "black")
        fltk.mise_a_jour()
        fltk.attente(5)  # affiche 3 secondes

    def get_infos_from_click(self, client_x, client_y):
        for circle in self.circles:
            if circle.detect_click(client_x, client_y): return circle.metadata


    def run(self) -> int:

        return_code : int = 0
        self.define_parameters((0, 0, self.window[0], self.window[1]))
        self.translate_polygons()

        for circle in self.circles: c.flatten()

        while True:
            event = fltk.donne_ev()
            event_type = fltk.type_ev(event)

            fltk.efface_tout()
            for p in self.polygons: p.draw()
            for f in self.functions: f()

            if event_type == "ClicGauche":
                restaurant = self.get_infos_from_click(fltk.abscisse(event), fltk.ordonnee(event))

            if event_type == "Quitte": break

            fltk.mise_a_jour()

        fltk.ferme_fenetre()

        return return_code

