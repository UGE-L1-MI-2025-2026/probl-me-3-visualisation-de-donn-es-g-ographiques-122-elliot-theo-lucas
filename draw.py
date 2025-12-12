import fltk
from typing import List, Tuple, Dict


class PolygonPrimitive:

    def __init__(self, points : List[Tuple[int, int]], parts : List[int], bbox : Tuple[int, int, int, int], colour : str = "black", fill : str = "", thickness : float = 2.0) -> None:
        self.bbox : Tuple[int, int, int, int] = bbox
        self.points : List[Tuple[int, int]] = points
        self.parts : List[int] = parts
        self.colour : str = colour
        self.fill : str = fill
        self.thickness : float = thickness

        self.current_polygons : List[int] = []

        print(fltk.get_pos(fltk.polygone([ (2, 3), (5, 9), (6, 4) ])))

    def render(self) -> int:
        if self.__is_outside:
            return -1
        elif len(self.current_polygons) > 0:
            pass
        else:
            self.__rerender()

    def __is_outside(self):
        return self.bbox[0] > Drawer.WINDOW_SIZE[0] or self.bbox[1] < 0 or self.bbox[2] < 0 or self.bbox[3] > Drawer.WINDOW_SIZE[1]


    def move(self, offsetX : float, offsetY : float):
        for polygon in self.current_polygons:
            fltk.deplace(polygon, offsetX, offsetY)
        return 0

    def __rerender(self):
        self.current_polygons : List[int] = []
        self.parts.append(len(self.points) - 1)
        for i in range(len(self.parts) - 1):
            self.current_polygons.append(
                fltk.polygone(
                    self.points[self.parts[i]:self.parts[i + 1]], 
                    couleur = self.colour, 
                    remplissage = self.fill, 
                    epaisseur = self.thickness
                )
            )


class CirclePrimitive:

    def __init__(self, position : Tuple[int, int], radius : float, colour : str = "black", fill : str = ""):
        self.position : Tuple[int, int] = position
        self.radius : float = radius
        self.colour : str = colour
        self.fill : str = fill

    def render(self) -> int:
        return fltk.cercle(self.position[0], self.position[1], self.radius, couleur = self.colour, remplissage = self.fill)


class Region:

    def __init__(self, points : List[Tuple[int, int]], parts : List[int], bbox : Tuple[int, int, int, int], colour : str = "black", fill : str = "", thickness : float = 2.0) -> None:

        self.base_polygon : PolygonPrimitive = PolygonPrimitive(points, parts, bbox)
        self.polygon : PolygonPrimitive = PolygonPrimitive(points.copy(), bbox, colour, fill, thickness)
    
    def render(self) -> int:
        return self.polygon.render()
    
    def translate(self, a : float, B : float, C : float):
        for i in range(len(self.polygon.points)):
            self.polygon.points[i] = a * self.base_polygon.points[i][0] + B, - a * self.base_polygon.points[i][1] + C
        self.polygon.bbox = (
            a * self.base_polygon.bbox[0] + B,
            - a * self.base_polygon.bbox[1] + C,
            a * self.base_polygon.bbox[2] + B,
            - a * self.base_polygon.bbox[3] + C
        )

class Place:
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

    WINDOW_SIZE : Tuple[int, int] = 1000, 500

    def __init__(self) -> None:

        fltk.cree_fenetre(Drawer.WINDOW_SIZE[0], Drawer.WINDOW_SIZE[1], redimension = True)

        self.places : List[Place] = []
        self.regions : List[Region] = []

        self.old_mouse_pos : Tuple[float, float] = 0, 0
        self.mouse_pos : Tuple[float, float] = 0, 0
        self.map_velocity : Tuple[float, float] = 0, 0

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
        for place in self.places:
            if place.detect_click(client_x, client_y): return place.metadata


    def update_and_render(self):
        fltk.efface_tout()

        for region in self.regions: region.render()
        for place in self.places: place.render()

        for region in self.regions: region.translate(self.a, self.B, self.C)
        for place in self.places: place.translate(self.a, self.B, self.C)


    def update_map_movements(self):
        
        growth : float = self.a / 100

        if fltk.touche_pressee("space"):
            self.map_velocity = self.old_mouse_pos[0] - self.mouse_pos[0], self.old_mouse_pos[1] - self.mouse_pos[1]

        elif fltk.touche_pressee("Up"):
            self.B += growth * (self.B - (Drawer.WINDOW_SIZE[0] >> 1)) / self.a
            self.C += growth * (self.C - (Drawer.WINDOW_SIZE[1] >> 1)) / self.a
            self.a += growth

        elif fltk.touche_pressee("Down"):
            self.B -= growth * (self.B - (Drawer.WINDOW_SIZE[0] >> 1)) / self.a
            self.C -= growth * (self.C - (Drawer.WINDOW_SIZE[1] >> 1)) / self.a
            self.a -= growth

        self.B -= self.map_velocity[0]
        self.C -= self.map_velocity[1]
        self.map_velocity = self.map_velocity[0] * 0.93, self.map_velocity[1] * 0.93


    def run_subwindow(self, metadata : Dict[str, str]) -> int:

        while True:
            event = fltk.donne_ev()
            event_type = fltk.type_ev(event)

            fltk.efface_tout()

            fltk.texte(50, 50, f"Nom : {metadata.get('title', '')}", "black")
            fltk.texte(50, 80, f"Contact : {metadata.get('contact', '')}", "black")
            fltk.texte(50, 110, f"Infos : {metadata.get('infos', '')}", "black")

            fltk.texte(50, 300, "Appuyez sur une touche pour revenir à la carte.", "red")

            if event_type == "Touche": return 0

            if event_type == "Quitte": return 1

            fltk.mise_a_jour()




    def run(self):

        self.define_parameters((0, 0, Drawer.WINDOW_SIZE[0], Drawer.WINDOW_SIZE[1]))

        while True:
            event = fltk.donne_ev()
            event_type = fltk.type_ev(event)

            self.mouse_pos = fltk.abscisse_souris(), fltk.ordonnee_souris()

            self.update_and_render()
            self.update_map_movements()

            if event_type == "ClicGauche":
                metadata = self.get_infos_from_click(fltk.abscisse(event), fltk.ordonnee(event))
                if metadata: 
                    if self.run_subwindow(metadata) > 0: break

            elif event_type == "Redimension":
                Drawer.WINDOW_SIZE = fltk.largeur_fenetre(), fltk.hauteur_fenetre()

            elif event_type == "Quitte": break

            self.old_mouse_pos = self.mouse_pos

            fltk.mise_a_jour()

        fltk.ferme_fenetre()

