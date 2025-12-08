import shapefile
import json
from typing import List, Dict, Tuple
import re


class Extractor:
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

        info["crous"] = []

        pattern : str = str(shape_id) + r"\d{3}"

        for metadata in self.data:
            if re.search(pattern, metadata["contact"]):
                info["crous"].append({
                    "title": metadata.get("title", ""),
                    "contact": metadata.get("contact", ""),
                    "infos": metadata.get("infos", ""),
                    "photo": metadata.get("photo", "")
                })
        return info

    def get_multiple(self, shape_ids : List[int]):
        
        data : Tuple[List[Dict], List[Dict]] = [], []
        total_bbox : List[int] = [ 0xffffffff, 0xffffffff, -0xffffffff, -0xffffffff ]
        pattern : str = r"(?:" + "|".join(map(str, shape_ids)) + r")\d{3}"

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

        with open("ensemble-des-lieux-de-restauration-des-crous.json") as f:
            all_metadata : Dict = json.load(f)

            for metadata in all_metadata: # each metadata is a dict
                if re.search(pattern, metadata.get("contact", "")):
                    data[1].append({
                        "longitude": metadata["geolocalisation"].get("lon", ""),
                        "latitude": metadata["geolocalisation"].get("lat", ""),
                        "title": metadata.get("title", ""),
                        "contact": metadata.get("contact", ""),
                        "infos": metadata.get("infos", ""),
                        "photo": metadata.get("photo", "")
                    })
        
        return data 

    def get_all(self):

        data : Tuple[List[Dict], List[Dict]] = [], []
    
        for shape_id in shape_ids: 
            shape : shapefile.Polygon = self.sf.shape(shape_id)
            data[0].append({
                "bbox": shape.bbox,
                "points": shape.points,
                "parts": shape.parts
            })
    
        with open("ensemble-des-lieux-de-restauration-des-crous.json") as f:
            all_metadata : Dict = json.load(f)
    
            for metadata in all_metadata: # each metadata is a dict
                data[1].append({
                    "longitude": metadata["geolocalisation"].get("lon", ""),
                    "latitude": metadata["geolocalisation"].get("lat", ""),
                    "title": metadata.get("title", ""),
                    "contact": metadata.get("contact", ""),
                    "infos": metadata.get("infos", ""),
                    "photo": metadata.get("photo", "")
                })

    return data
