from draw import Drawer, Region, Place
from shapefile import Reader
from data import DataManager

if __name__ == "__main__":

    drawer = Drawer()
    data_manager = DataManager()

    idf = data_manager.get_all()

    for dep in idf[0]:
        drawer.regions.append(Region(data_manager.mercarize_points(dep["points"]), data_manager.mercarize_bbox(dep["bbox"])))

    for crous in idf[1]:
        drawer.places.append(Place((crous["longitude"], data_manager.mercarize_int(crous["latitude"])), 5, crous))

    drawer.run()
