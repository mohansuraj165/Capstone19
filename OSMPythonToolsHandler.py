from OSMPythonTools.overpass import overpassQueryBuilder
from OSMPythonTools.overpass import Overpass
from OSMPythonTools.api import Api
api = Api()
import DB_eOSMGenerator as DB
import Logger as Log
import jeIlyfish

OSMNodesCache={}

'''Gets all ways contained in the area defined by box (lat/lon)'''
def GetOSMWaysData(box):
    overpass = Overpass()
    query = overpassQueryBuilder(bbox=[box.latMin,box.lonMin,box.latMax,box.lonMax], elementType='way', out='body')
    try:
        ways = overpass.query(query, timeout=60)
    except:
        Log.logging.error("In OSMPythonToolsHandler.py, GetOSMWaysData", exc_info=True)
        return False
    if ways._json['elements'] == []:
        box.lonMin-=0.5
        box.latMin-=0.5
        box.lonMax+=0.5
        box.latMax+=0.5
        GetOSMWaysData(box)
    else:
        StoreWaysData (ways._json['elements'])
    return True


'''Stores ways data in DB, (WayID,NodeIDs,StreetName)'''
def StoreWaysData(ways):
    for w in ways:
        if w['type'] == "way" and 'tags' in w:
            tags = w['tags']
            if 'name' in tags:
                streetName=tags.get('name').replace("'","")
                DB.InsertIntoWays(w.get('id'),w.get('nodes'),streetName,GetPhoneticCode(streetName))

def GetOSMNode(nodeID):
    n = OSMNodesCache.get(nodeID)
    if n==None:
        n = api.query('node/%s'%nodeID)
        OSMNodesCache[nodeID]=n
    return n


def GetPhoneticCode(street):
    code = jeIlyfish.metaphone(street)
    code.rsplit(' ', 1)[0]
    return code


