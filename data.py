from shapefile import Reader


class Extractor:
    def __init__(self):
        self.sf: Reader = Reader("fr_100km.shp")

    def get(self, shape_id: int):
        info = {}
        shape = self.sf.shape(shape_id)
        info["bbox"] = shape.bbox
        info["points"] = shape.points
        info["m"] = shape.m
        info["parts"] = shape.parts
        return info



