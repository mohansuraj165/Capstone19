import DBScript as DB
import pickle
import xml.etree.cElementTree as ET
import OSMPythonToolsHandler as OSM
import math
import Logger as Log
import XMLHandler as XML

fact = 100000000.00

#Used in FindBestWay().
#2 implies every 2nd node is used in distance calculation
#3 implies every 3rd node is used in distance calculation
step = 2

'''
Matches nodes with ways data retrieved from OSM
Compares street name from nodes and matches to the best way ID
Result is stored in DB
'''
def MatchNodesWithOSMWays(nodes):
    for n in nodes:
        data = DB.SelectWayByStreetName(n.streetPhoneticCode)
        try:
            if len(data)==0:
                continue
            if len(data)==1:
                DB.InsertIntoAssociatedNodes(data[0][0], pickle.dumps(n))
            else:
                wayId=FindBestWay(data,n)
                DB.InsertIntoAssociatedNodes(wayId, pickle.dumps(n))
        except Exception as e:
            Log.logging.error("In AssociateNodesAndWays.py, MatchNodesWithOSMWays()", exc_info=True)

    OSM.OSMNodesCache = {}


    ways = DB.SelectDistinctWayID()
    for way in ways:
        hns = ET.SubElement(XML.root, 'HouseNumbers', osmObjectID=way[0])

        data = DB.SelectAllAssociatedNodesByWayID(way[0])

        for d in data:
            node = pickle.loads(d[1])
            hn=ET.SubElement(hns,'HouseNumber', value=node.number, lat=node.latitude, lon=node.longitude, street=node.street,
                                     t="enhancedOSM", version="1", externalProvider="OpenAddr")


    return

'''
Returns WayID
Finds the nearest way for a given node
'''
def FindBestWay(waysList,node):
    dist = float("inf")
    id = 0
    for i in range(0,len(waysList),step):
        d=GetAvgDist(waysList[i],node)
        if(d<dist):
            id=waysList[i][0]
            dist=d
    return (id)

'''
Calculates average diatance from a given node to all nodes in a way
'''
def GetAvgDist(way,node):
    s=str(way[1])
    s=s.replace("]"," ")
    s=s.replace("["," ")
    s = s.split(',')
    num=0
    denom=len(s)
    for nodeId in s:
        n= OSM.GetOSMNode(nodeId.strip())
        num+=calcPythagoreanDist(float(node.latitude)*fact,float(node.longitude)*fact,float(n.lat())*fact,float(n.lon())*fact)
    return(num/denom)

'''
Calculates the distance between 2 coordinates using Haversine Formula
dlon = lon2 - lon1 
dlat = lat2 - lat1 
a = (sin(dlat/2))^2 + cos(lat1) * cos(lat2) * (sin(dlon/2))^2 
c = 2 * atan2( sqrt(a), sqrt(1-a) ) 
d = R * c (where R is the radius of the Earth, 3961 miles or 6373 km)
'''
def calcHarversineDist(lat1,lon1,lat2,lon2):
    R=3961
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.pow((math.sin(dlat/2)),2) + math.cos(lat1) * math.cos(lat2) * math.pow((math.sin(dlon/2)),2)
    c = 2 * math.atan2( math.sqrt(a), math.sqrt(1-a) )
    d = R * c
    return d

'''
Calculates distance between 2 coordinates using PythagoreanDistanceFormula
'''
def calcPythagoreanDist(lat1,lon1,lat2,lon2):
    return math.pow((lat2-lat1),2)+math.pow((lon2-lon1),2)
