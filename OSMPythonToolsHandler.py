from OSMPythonTools.overpass import overpassQueryBuilder
from OSMPythonTools.overpass import Overpass

def GetWaysData(box):
    overpass = Overpass()
    query = overpassQueryBuilder(bbox=[box.latMin,box.lonMin,box.latMax,box.lonMax], elementType='way', out='body')
    ways = overpass.query(query, timeout=60)
    if ways._json['elements'] == []:
        box.lonMin-=0.5
        box.latMin-=0.5
        box.lonMax+=0.5
        box.latMax+=0.5
        GetWaysData(box)
    else:
        return (ways._json['elements'])
