import fltk
from typing import List, Tuple, Dict

class Polygon:

    def __init__(self, points : List[Tuple[int, int]], bbox : Tuple[int, int, int, int], colour : str = "black", fill : str = "", thickness : float = 2.0) -> None:
        self.bbox : Tuple[int, int, int, int] = bbox
        self.points : List[Tuple[int, int]] = points
        self.colour : str = colour
        self.fill : str = fill
        self.thickness : float = thickness
    
    def draw(self) -> int:
        return fltk.polygone(self.points, couleur = self.colour, remplissage = self.fill, epaisseur = self.thickness)

    def scale(self, factor : float) -> None:
        for i in range(len(self.points)):
            self.points[i] = self.points[i][0] * factor, self.points[i][1] * factor
        
    def translate(self, offset : Tuple[int, int]) -> None:
        for i in range(len(self.points)):
            self.points[i] = self.points[i][0] + offset[0], self.points[i][1] + offset[1]
        self.bbox = self.bbox[0] + offset[0], self.bbox[1] + offset[0], self.bbox[2] + offset[1], self.bbox[3] + offset[1]

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

    def update_polygon_points(self):

        middle : Tuple[int, int] = 0, 0
        halfwin : Tuple[int, int] = self.window[0] >> 1, self.window[1] >> 1

        for polygon in self.polygons:
            middle = 0, 0
            for point in polygon.points: middle = middle[0] + point[0], middle[1] + point[1] # middle
            middle = middle[0] // len(polygon.points), middle[1] // len(polygon.points)
            for i in range(len(polygon.points)): 
                polygon.points[i] = polygon.points[i][0] - middle[0] + halfwin[0], - polygon.points[i][1] + middle[1] + halfwin[1]
                # symetry : newy = y - 2(y - midy) = y -2y + 2midy = -y + 2midy
                # translation to window center: newx = x - midx + halfwinx, newy = y - midy + halfwiny
                # together : newx = x - midx + halfwinx, newy = -y + 2midy - midy + halfwiny = -y + midy + halfwiny

        minw : float = self.polygons[0].bbox[0]
        maxw : float = self.polygons[0].bbox[1]
        minh : float = self.polygons[0].bbox[2]
        maxh : float = self.polygons[0].bbox[3]
        for polygon in self.polygons:
            if polygon.bbox[0] < minw: minw = polygon.bbox[0]
            if polygon.bbox[1] < minh: minh = polygon.bbox[1]
            if polygon.bbox[2] > maxw: maxw = polygon.bbox[2]
            if polygon.bbox[3] > maxh: maxh = polygon.bbox[3]

        factor : float = 0

        if (maxw - minw) * (maxh - minh) != 0: 
            factor = min(self.window[0] / (maxw - minw), self.window[1] / (maxh - minh))

        for polygon in self.polygons:
            polygon.scale(factor)
            polygon.recalc_bbox()

    def run(self) -> int:

        return_code : int = 0

        self.update_polygon_points()

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