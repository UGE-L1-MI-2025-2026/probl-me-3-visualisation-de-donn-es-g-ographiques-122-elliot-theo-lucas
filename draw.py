import fltk
from typing import List, Tuple, Dict

class Drawer:

    def __init__(self) -> None:

        self.window : Tuple[int, int] = 1000, 500
        fltk.cree_fenetre(self.window[0], self.window[1])

        self.thickness : float = 2.0

        self.functions : List[function] = []
        self.polygons : List[int] = []
    
    def add_polygon(self, points : List[Tuple[float, float]], colour : str = "black", fill : str = "") -> None:
        self.polygons.append(fltk.polygone(points, couleur = colour, remplissage = fill, epaisseur = self.thickness))

    def run(self) -> int:

        return_code : int = 0

        while True:
            event = fltk.attend_ev()
            event_type = fltk.type_ev(event)

            fltk.efface_tout()

            for f in self.functions: f()

            if event_type == "Quitte": break

        fltk.ferme_fenetre()

        return return_code