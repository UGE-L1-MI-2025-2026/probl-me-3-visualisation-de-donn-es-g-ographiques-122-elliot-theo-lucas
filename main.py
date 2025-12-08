from draw import Drawer, Polygon
from shapefile import Reader
from data import Extractor

if __name__ == "__main__":

    drawer = Drawer()
    extractor = Extractor()

    idf = extractor.get_multiple([77, 94])

    for dep in idf:
        drawer.polygons.append(Polygon(dep["points"], dep["bbox"]))

    drawer.run()
    
