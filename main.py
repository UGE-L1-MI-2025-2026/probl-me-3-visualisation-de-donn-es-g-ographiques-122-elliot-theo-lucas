from draw import Drawer, Polygon
from shapefile import Reader
from data import Extractor

if __name__ == "__main__":

    drawer = Drawer()
    extractor = Extractor()

    idf = [ extractor.get(i) for i in [ 75, 92, 93, 94, 77, 91, 78, 95 ] ]

    for dep in idf:
        drawer.polygons.append(Polygon(dep["points"], dep["bbox"]))

    drawer.run()
