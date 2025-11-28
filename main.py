from draw import Drawer
from shapefile import Reader

if __name__ == "__main__":
    sf = Reader("fr_100km.shp")
    sf.records()

    drawer = Drawer()

    def draw():
        drawer.draw_departement(sf.shape(75).points)

    drawer.functions.append(draw)

    drawer.run()
