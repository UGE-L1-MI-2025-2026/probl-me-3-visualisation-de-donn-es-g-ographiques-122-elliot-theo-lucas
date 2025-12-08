from draw import Drawer, Region, Point
from shapefile import Reader
from data import DataManager

if __name__ == "__main__":

    drawer = Drawer()
    data_manager = DataManager()

    idf = data_manager.get_multiple([ 75 ])

    for dep in idf[0]:
        drawer.regions.append(Region(data_manager.mercarize_points(dep["points"]), data_manager.mercarize_bbox(dep["bbox"])))

    for crous in idf[1]:
        drawer.points.append(Point((crous["longitude"], data_manager.mercarize_int(crous["latitude"])), 5, crous))

    drawer.run()
    
