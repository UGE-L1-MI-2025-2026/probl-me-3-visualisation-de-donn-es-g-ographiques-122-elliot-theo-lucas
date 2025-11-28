import shapefile

class Extractor:
    def __init__(self):
        self.sf: shapefile.Reader = shapefile.Reader("fr_100km.shp")

    def get(self, shape_id: int):
        info = {}
        shape : shapefile.Polygon = self.sf.shape(shape_id)
        if not shape: return {}

        info["bbox"] = shape.bbox
        info["points"] = shape.points
        info["m"] = shape.m
        info["parts"] = shape.parts
        return info



