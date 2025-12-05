import json

class load:
    def __init__(self,fichiers):
        self.fichiers=fichiers
        with open(self.fichiers) as f:
            self.data=json.load(f)
            self.geolocalisation=self.trouver_geolocalisation(self.data)

    def trouver_geolocalisation(self,data):
        s=[]
        for i in range(len(self.data)):
            s.append((self.data[i]["geolocalisation"]['lon'],self.data[i]["geolocalisation"]['lat']))
        return s


s=load("ensemble-des-lieux-de-restauration-des-crous.json")
print(s.data[1]["geolocalisation"])
print(len(s.data))
print(s.geolocalisation)

