from draw import Drawer
from shapefile import Reader

if __name__ == "__main__":
    sf = Reader("fr_100km.dbf")
    sf.records()

    drawer = Drawer()
    
    while True:
        drawer.draw_departement(sf.shape(75).points)
        if not drawer.update(): break

    drawer.exit()
