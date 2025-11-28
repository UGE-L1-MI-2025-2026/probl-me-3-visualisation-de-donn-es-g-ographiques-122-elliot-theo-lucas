import fltk
from typing import List, Tuple, Dict

class Drawer:

    def __init__(self) -> None:

        self.window : Tuple[int, int] = 1000, 500
        fltk.cree_fenetre(self.window[0], self.window[1])

        self.functions : List[function] = []
    
    @staticmethod
    def draw_departement(points : List[Tuple[float, float]]) -> None:
        fltk.polygone(points)

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