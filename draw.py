import fltk
from typing import List, Tuple, Dict
from math import log, tan, pi, radians, degrees, sqrt

MERC = lambda x: degrees(log(tan(radians(x) / 2 + pi / 4)))

class PolygonPrimitive:

    def __init__(self, points : List[Tuple[int, int]], bbox : Tuple[int, int, int, int], colour : str = "black", fill : str = "", thickness : float = 2.0) -> None:
        self.bbox : Tuple[int, int, int, int] = bbox
        self.points : List[Tuple[int, int]] = points
        self.colour : str = colour
        self.fill : str = fill
        self.thickness : float = thickness

    def render(self) -> int:
        return fltk.polygone(self.points, couleur = self.colour, remplissage = self.fill, epaisseur = self.thickness)


class CirclePrimitive:

    def __init__(self, position : Tuple[int, int], radius : float, colour : str = black, fill : str = ""):
        self.position : Tuple[int, int] = position
        self.radius : float = radius
        self.colour : str = colour
        self.fill : str = fill

    def render(self) -> int:
        return fltk.cercle(self.position[0], self.position[1], self.radius, couleur = self.colour, remplissage = self.fill)


class Polygon:

    def __init__(self, points : List[Tuple[int, int]], bbox : Tuple[int, int, int, int], colour : str = "black", fill : str = "", thickness : float = 2.0) -> None:
        self.bbox : Tuple[int, int, int, int] = bbox
        self.points : List[Tuple[int, int]] = points
        self.base_poly : PolygonPrimitive = PolygonPrimitive(self.points, self.bbox)
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

    def draw(self):
        fltk.cercle(self.position[0], self.position[1], self.radius, couleur= "red", remplissage="red")

    def detect_click(self, client_x, client_y):
        return (client_x - self.position[0]) ** 2 + (client_y - self.position[1]) ** 2 <= self.radius ** 2


class SubWindow:

    def __init__(self):
        pass


class Drawer:

    def __init__(self) -> None:

        self.window : Tuple[int, int] = 1000, 500
        fltk.cree_fenetre(self.window[0], self.window[1])

        self.thickness : float = 2.0
        self.circles : List[Cercle] = []
        self.polygons : List[Polygon] = []

        self.a, self.B, self.C = 0, 0, 0

    def translate_polygons(self):
        for polygon in self.polygons:
            for i in range(len(polygon.points)):
                polygon.points[i] = self.a * polygon.points[i][0] + self.B, - self.a * polygon.points[i][1] + self.C

    def translate_circles(self):
        for circle in self.circles:
            circle.position = self.a * circle.position[0] + self.B, - self.a * circle.position[1] + self.C
        
    def define_parameters(self, target_box : Tuple[int, int, int, int]):
        all_bbox : List[int] = [ 0xffffffff, 0xffffffff, -0xffffffff, -0xffffffff ]
        for polygon in self.polygons:
            polygon.flatten_points()
            
            if polygon.bbox[0] < all_bbox[0]: all_bbox[0] = polygon.bbox[0]
            if polygon.bbox[1] < all_bbox[1]: all_bbox[1] = polygon.bbox[1]
            if polygon.bbox[2] > all_bbox[2]: all_bbox[2] = polygon.bbox[2]
            if polygon.bbox[3] > all_bbox[3]: all_bbox[3] = polygon.bbox[3]

        for circle in self.circles: circle.flatten()

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
        

    def get_infos_from_click(self, client_x, client_y):
        for circle in self.circles:
            if circle.detect_click(client_x, client_y): return circle.metadata


    def run(self) -> int:

        return_code : int = 0

        self.define_parameters((0, 0, self.window[0], self.window[1]))
        self.translate_polygons()
        self.translate_circles()

        while True:
            event = fltk.donne_ev()
            event_type = fltk.type_ev(event)

            fltk.efface_tout()
            for p in self.polygons: p.draw()
            for circle in self.circles: circle.draw()

            if event_type == "ClicGauche":
                metadata = self.get_infos_from_click(fltk.abscisse(event), fltk.ordonnee(event))
                while True:
                    ev = fltk.attend_ev()
                    tev = fltk.type_ev(ev)
                    if tev == "Touche":
                        tch = fltk.touche(ev)
                        if tch == "Escape": break
                    if tev=="Quitte": break
                fltk.mise_a_jour()
                if event_type == "Quitte": break

            fltk.mise_a_jour()

        fltk.ferme_fenetre()

        return return_code

