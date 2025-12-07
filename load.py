import json

class loads:
    def __init__(self,fichiers="ensemble-des-lieux-de-restauration-des-crous.json"):
        self.fichiers=fichiers
        with open(self.fichiers) as f:
            self.data=json.load(f)
            self.info=self.trouver_info()

    def trouver_info(self):
        s = []
        for r in self.data:
            # on garde toutes les infos utiles dans un dict
            s.append({
                "lon": r["geolocalisation"]["lon"],
                "lat": r["geolocalisation"]["lat"],
                "title": r.get("title", ""),
                "contact": r.get("contact", ""),
                "infos": r.get("infos", ""),
                "photo": r.get("photo", "")
            })
        return s






