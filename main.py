from draw import Drawer, Polygon
from shapefile import Reader
from data import Extractor

if __name__ == "__main__":

    drawer = Drawer()
    extractor = Extractor()

    infos = extractor.get(77)

    drawer.polygons.append(Polygon(infos["points"], infos["bbox"]))

    drawer.run()
