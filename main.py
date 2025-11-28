from draw import Drawer, Polygon
from shapefile import Reader
from data import Extractor

if __name__ == "__main__":
    sf = Reader("fr_100km.shp")
    sf.records()

    drawer = Drawer()
    extractor = Extractor()

    print(extractor.get(47))

    drawer.polygons.append(Polygon(sf.shape(47).points))

    drawer.run()
