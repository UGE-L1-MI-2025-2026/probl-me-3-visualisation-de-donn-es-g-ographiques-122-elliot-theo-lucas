import shapefile
import random as rd
class Extractor:
    def __init__(self):
        self.sf: shapefile.Reader = shapefile.Reader("src/departements-20140306-50m")

    def get(self, shape_id: int):
        info = {}
        shape : shapefile.Polygon = self.sf.shape(shape_id)
        if not shape: return {}
        info["bbox"] = shape.bbox
        info["points"] = shape.points
        info["parts"] = shape.parts
        return info



        



