from draw import Drawer, Polygon, Cercle
from shapefile import Reader
from data import Extractor

if __name__ == "__main__":

    drawer = Drawer()
    extractor = Extractor()

    idf = extractor.get_multiple([77, 94])

    for dep in idf[0]:
        drawer.polygons.append(Polygon(dep["points"], dep["bbox"]))

    for crous in idf[1]:
        drawer.circles.append(Cercle())

    drawer.run()
    
