import DB_eOSMGenerator as DB
import pickle
import xml.etree.cElementTree as ET
from OSMPythonTools.api import Api
api = Api()
import math
fact = 1.00

def MatchNodesWithOSMWays(nodes):
    conn = DB.GetConnection()
    c=conn.cursor()
    n=nodes[0]
    print(n.data['addr:street'])
    #for n in nodes:
    data = DB.SelectWayByStreetName('August Town Road')
    if len(data)==1:
        DB.InsertIntoAssociatedNodes(data[0][0], pickle.dumps(n))
    else:
        wayId=FindBestWay(data,n)
        DB.InsertIntoAssociatedNodes(wayId, pickle.dumps(n))

    n=0
    root = ET.Element('root')
    c.execute("SELECT distinct WayID FROM TBL_ASSOCIATED_NODES;")
    ways = c.fetchall()
    for way in ways:
        n+=1
        hns = ET.SubElement(root, 'HouseNumbers', osmObjectID=way[0])
        qry="select * from TBL_ASSOCIATED_NODES where WayID = '%s'"%(way[0])
        c.execute(qry)
        data= c.fetchall()
        for d in data:
            node = pickle.loads(d[1])
            hn=ET.SubElement(hns,'HouseNumber', id=node.id, version="1", lat=node.latitude, lon=node.longitude,
                                     t="enhancedOSM")

    xml = ET.ElementTree(root)
    print("done")
    #xml.write("tem.xml")

def FindBestWay(waysList,node):
    dist = float("inf")
    id = 0
    for way in waysList:
        d=GetAvgDist(way,node)
        if(d<dist):
            id=way[0]
            dist=d
    return (id)

def GetAvgDist(way,node):

    s=str(way[1])
    s=s.replace("]"," ")
    s=s.replace("["," ")
    s = s.split(',')
    num=0
    denom=len(s)
    for nodeId in s:

        n = api.query('node/%s'%nodeId.strip())
        num+=calcDist(float(node.latitude)*fact,float(node.longitude)*fact,float(n.lat())*fact,float(n.lon())*fact)
    print(num/denom)
    return(num/denom)


def calcDist(lat1,lon1,lat2,lon2):
    R=3961
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.pow((math.sin(dlat/2)),2) + math.cos(lat1) * math.cos(lat2) * math.pow((math.sin(dlon/2)),2)
    c = 2 * math.atan2( math.sqrt(a), math.sqrt(1-a) )
    d = R * c
    return d
    #print(way[1])

