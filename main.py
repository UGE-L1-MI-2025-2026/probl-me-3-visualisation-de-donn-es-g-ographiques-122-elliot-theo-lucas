from draw import Drawer
from shapefile import Reader

if __name__ == "__main__":
    sf = Reader("fr_100km.shp")
    sf.records()

    drawer = Drawer()

    def draw():
        print(sf.shape(47).points)
        drawer.add_polygon(sf.shape(47).points)

    drawer.functions.append(draw)

    drawer.run()
