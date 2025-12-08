import fltk
from typing import List, Tuple, Dict


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

    def __init__(self, position : Tuple[int, int], radius : float, colour : str = "black", fill : str = ""):
        self.position : Tuple[int, int] = position
        self.radius : float = radius
        self.colour : str = colour
        self.fill : str = fill

    def render(self) -> int:
        return fltk.cercle(self.position[0], self.position[1], self.radius, couleur = self.colour, remplissage = self.fill)


class Region:

    def __init__(self, points : List[Tuple[int, int]], bbox : Tuple[int, int, int, int], colour : str = "black", fill : str = "", thickness : float = 2.0) -> None:

        self.base_polygon : PolygonPrimitive = PolygonPrimitive(points, bbox)
        self.polygon : PolygonPrimitive = PolygonPrimitive(points.copy(), bbox, colour, fill, thickness)
    
    def render(self) -> int:
        return self.polygon.render()
    
    def translate(self, a : float, B : float, C : float):
        for i in range(len(self.polygon.points)):
            self.polygon.points[i] = a * self.base_polygon.points[i][0] + B, - a * self.base_polygon.points[i][1] + C

class Point:
    def __init__(self, position : Tuple[int, int], radius : float, metadata : Dict):
        
        self.base_circle : CirclePrimitive = CirclePrimitive(position, radius)
        self.circle : CirclePrimitive = CirclePrimitive(position, radius, colour = "red", fill = "red")
        self.metadata : Dict = metadata

    def translate(self, a : float, B : float, C : float):
        self.circle.position = a * self.base_circle.position[0] + B, - a * self.base_circle.position[1] + C

    def render(self):
        return self.circle.render()

    def detect_click(self, client_x, client_y):
        return (client_x - self.circle.position[0]) ** 2 + (client_y - self.circle.position[1]) ** 2 <= self.circle.radius ** 2


class SubWindow:

    def __init__(self):
        pass


class Drawer:

    def __init__(self) -> None:

        self.window : Tuple[int, int] = 1000, 500
        fltk.cree_fenetre(self.window[0], self.window[1])

        self.points : List[Point] = []
        self.regions : List[Region] = []

        self.a, self.B, self.C = 0, 0, 0
        
    def define_parameters(self, target_box : Tuple[int, int, int, int]):
        all_bbox : List[int] = [ 0xffffffff, 0xffffffff, -0xffffffff, -0xffffffff ]
        for region in self.regions:
            if region.base_polygon.bbox[0] < all_bbox[0]: all_bbox[0] = region.base_polygon.bbox[0]
            if region.base_polygon.bbox[1] < all_bbox[1]: all_bbox[1] = region.base_polygon.bbox[1]
            if region.base_polygon.bbox[2] > all_bbox[2]: all_bbox[2] = region.base_polygon.bbox[2]
            if region.base_polygon.bbox[3] > all_bbox[3]: all_bbox[3] = region.base_polygon.bbox[3]

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
        for point in self.points:
            if point.detect_click(client_x, client_y): return point.metadata


    def run(self) -> int:

        return_code : int = 0
        

        self.define_parameters((0, 0, self.window[0], self.window[1]))

        while True:
            event = fltk.donne_ev()
            event_type = fltk.type_ev(event)

            fltk.efface_tout()
            for region in self.regions: region.render()
            for circle in self.points: circle.render()

            for region in self.regions: region.translate(self.a, self.B, self.C)
            for point in self.points: point.translate(self.a, self.B, self.C)

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
        
