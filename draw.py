import fltk
from typing import List, Tuple, Dict
from math import log, tan, pi, radians, degrees

MERC = lambda x: degrees(log(tan(radians(x) / 2 + pi / 4)))

class Polygon:

    def __init__(self, points : List[Tuple[int, int]], bbox : Tuple[int, int, int, int], colour : str = "black", fill : str = "", thickness : float = 2.0) -> None:
        self.bbox : Tuple[int, int, int, int] = bbox
        self.points : List[Tuple[int, int]] = points
        self.colour : str = colour
        self.fill : str = fill
        self.thickness : float = thickness
    
    def draw(self) -> int:
        return fltk.polygone(self.points, couleur = self.colour, remplissage = self.fill, epaisseur = self.thickness)

    def flatten_points(self) -> None:
        for i in range(len(self.points)):
            self.points[i] = self.points[i][0], MERC(self.points[i][1])
        self.bbox = self.bbox[0], MERC(self.bbox[1]), self.bbox[2], MERC(self.bbox[3])

    def recalc_bbox(self) -> None:
        minw : float = self.points[0][0]; maxw : float = self.points[0][1]; minh : float = self.points[0][0]; maxh : float = self.points[0][1]
        for point in self.points:
            if point[0] < minw: minw = point[0]
            if point[0] > maxw: maxw = point[0]
            if point[1] < minh: minh = point[1]
            if point[1] > maxh: maxh = point[1]
        self.bbox = minw, maxw, minh, maxh

class Drawer:

    def __init__(self) -> None:

        self.window : Tuple[int, int] = 1000, 500
        fltk.cree_fenetre(self.window[0], self.window[1])

        self.thickness : float = 2.0

        self.functions : List[function] = []
        self.polygons : List[Polygon] = []

    def initialize_polygon(self, polygon : Polygon, target_box : Tuple[int, int, int, int]) -> None:
        polygon.flatten_points()
        a = min(target_box[2] / (polygon.bbox[2] - polygon.bbox[0]), target_box[3] / (polygon.bbox[3] - polygon.bbox[1]))
        B, C = target_box[0] - a * polygon.bbox[0], target_box[1] + a * polygon.bbox[3]
        for i in range(len(polygon.points)):
            polygon.points[i] = a * polygon.points[i][0] + B, - a * polygon.points[i][1] + C
        
    def update_polygons_boxes(self):
        for polygon in self.polygons:
            pass

    def run(self) -> int:

        return_code : int = 0

        for polygon in self.polygons: 
            self.initialize_polygon(polygon, (100, 100, 500, 500))

        while True:
            event = fltk.donne_ev()
            event_type = fltk.type_ev(event)

            fltk.efface_tout()

            for p in self.polygons: p.draw()
            for f in self.functions: f()

            if event_type == "Quitte": break

            fltk.mise_a_jour()

        fltk.ferme_fenetre()

        return return_code