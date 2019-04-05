from OSMPythonTools.overpass import overpassQueryBuilder
from OSMPythonTools.overpass import Overpass
import DB_eOSMGenerator as DB

'''Gets all ways contained in the area defined by box (lat/lon)'''
def GetOSMWaysData(box):
    overpass = Overpass()
    query = overpassQueryBuilder(bbox=[box.latMin,box.lonMin,box.latMax,box.lonMax], elementType='way', out='body')
    try:
        ways = overpass.query(query, timeout=60)
    except:
        print(box.latMax,box.lonMax)
        return
    if ways._json['elements'] == []:
        box.lonMin-=0.5
        box.latMin-=0.5
        box.lonMax+=0.5
        box.latMax+=0.5
        GetOSMWaysData(box)
    else:
        StoreWaysData (ways._json['elements'])

'''Stores ways data in DB, (WayID,NodeIDs,StreetName)'''
def StoreWaysData(ways):
    for w in ways:
        if w['type'] == "way" and 'tags' in w:
            tags = w['tags']
            if 'name' in tags:
                DB.InsertIntoWays(w.get('id'),w.get('nodes'),tags.get('name'))


