from draw import Drawer, Polygon
from shapefile import Reader
from data import Extractor

if __name__ == "__main__":
    sf = Reader("fr_100km.shp")
    sf.records()

    drawer = Drawer()
    extractor = Extractor()

    infos = extractor.get(47)

    drawer.polygons.append(Polygon(infos["points"], infos["bbox"]))

    drawer.run()
