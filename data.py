import shapefile
import json
from typing import List, Dict, Tuple
from math import log, tan, pi, radians, degrees
import re

MERC = lambda x: degrees(log(tan(radians(x) / 2 + pi / 4)))

class DataManager:
    def __init__(self):
        self.sf: shapefile.Reader = shapefile.Reader("src/departements-20140306-50m")
        self.data = {}

        with open("ensemble-des-lieux-de-restauration-des-crous.json") as f:
            self.data = json.load(f)

    def get(self, shape_id: int):
        info = {}
        shape : shapefile.Polygon = self.sf.shape(shape_id)
        if not shape: return {}
        info["bbox"] = shape.bbox
        info["points"] = shape.points
        info["parts"] = shape.parts

        info["theatre"] = []

        for metadata in self.data:
            if int(metadata.get("id_secteur_postal", 0) / 1000) == shape_id:
                info["theatre"].append({
                    "longitude" : metadata.get("x",""),
                    "latitude"  : metadata.get("y",""),
                    "title" : metadata.get("eq_nom_equipement",""),
                    "contact": metadata.get("eq_nom_equipement"),
                })

        return info

    def get_multiple(self, shape_ids : List[int]):

        data : Tuple[List[Dict], List[Dict]] = [], []
        total_bbox : List[int] = [ 0xffffffff, 0xffffffff, -0xffffffff, -0xffffffff ]

        for shape_id in shape_ids:
            shape : shapefile.Polygon = self.sf.shape(shape_id)
            data[0].append({
                "bbox": shape.bbox,
                "points": shape.points,
                "parts": shape.parts
            })

            if shape.bbox[0] < total_bbox[0]: total_bbox[0] = shape.bbox[0]
            if shape.bbox[1] < total_bbox[1]: total_bbox[1] = shape.bbox[1]
            if shape.bbox[2] > total_bbox[2]: total_bbox[2] = shape.bbox[2]
            if shape.bbox[3] > total_bbox[3]: total_bbox[3] = shape.bbox[3]

        with open("theatres-et-salles-de-spectacles.json") as f:
            all_metadata : Dict =json.load(f)
            for metadata in all_metadata:
                if int(metadata.get("id_secteur_postal", 0) / 1000) in shape_ids:
                    data[1].append({
                        "longitude": metadata["geolocaisation"].get("lon", ""),
                        "latitude": metadata["geolocalisation"].get("lat", ""),
                        "title" : metadata.get("eq_nom_equipement",""),
                        "contact": metadata.get("eq_nom_equipement"),
                    })
                
        return data

    def get_all(self):

        data : Tuple[List[Dict], List[Dict]] = [], []

        for shape in self.sf.shapes():
            data[0].append({
                "bbox": shape.bbox,
                "points": shape.points,
                "parts": shape.parts
            })

        with open("theatres-et-salles-de-spectacles.json") as f:
            all_metadata : Dict =json.load(f)

            for metadata in all_metadata: # each metadata is a dict
                data[1].append({
                    "longitude": metadata["geolocaisation"].get("lon", ""),
                    "latitude": metadata["geolocalisation"].get("lat", ""),
                    "title" : metadata.get("eq_nom_equipement",""),
                    "contact": metadata.get("eq_nom_equipement"),
                })

        return data
    
    def mercarize_points(self, points : List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        return [ ( points[i][0], MERC(points[i][1]) ) for i in range(len(points)) ]
    
    def mercarize_bbox(self, bbox : Tuple[int, int, int, int]) -> Tuple[int, int, int, int]:
        return bbox[0], MERC(bbox[1]), bbox[2], MERC(bbox[3])
    
    def mercarize_int(self, x : int):
        return MERC(x)
