import fltk
from typing import List, Tuple

class Drawer:

    def __init__(self) -> None:

        self.window : Tuple[int, int] = 500, 300
        fltk.cree_fenetre(self.window[0], self.window[1])
    
    @staticmethod
    def draw_departement(points : List[Tuple[float, float]]) -> None:

        fltk.polygone(points)

    def update(self) -> bool:
        event = fltk.attend_ev()
        event_type = fltk.type_ev(event)

        if event_type == "Quitte": return False 

        return True

    def exit(self) -> None: fltk.ferme_fenetre()