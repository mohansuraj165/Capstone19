import csv
import xml.etree.cElementTree as ET
import xml.dom.minidom
import time
import glob
import os
from OSMPythonTools.overpass import overpassQueryBuilder
from OSMPythonTools.overpass import Overpass

class Node():

    longitude = ""
    latitude = ""
    id = ""
    data={
        "addr:housenumber" : "",
        "addr:street" : "",
        "addr:unit" : "",
        "addr:city" : "",
        "addr:district" : "",
        "addr:reqion" : "",
        "addr:postcode" : ""

    }
    hash = ""

class Coordinates():
    latMin = 90
    latMax = -90
    lonMin = 180
    lonMax = -180

def GetFilenameFromPath(path):
    pathArr = path.split("\\")
    fn = pathArr[len(pathArr)-1]
    fn = fn[:fn.index('.csv')]
    return(fn)


def ResetBox(box, lon, lat):
    if lat<(box.latMin):
        box.latMin=lat
    if lat>box.latMax:
        box.latMax=lat
    if lon<box.lonMin:
        box.lonMin=lon
    if lon>box.lonMax:
        box.lonMax=lon


def GenerateXmlFromCsv(path):
    global xml
    nodes = []
    box = Coordinates()
    with open(path, 'rt') as csvfile:
        fn = GetFilenameFromPath(path)
        csvData = csv.reader(csvfile)
        next(csvData, None)  # Skips headers
        #root = ET.Element("root")

        for row in csvData:
            nodeObj = AssignRowToObject(row)
            if nodeObj.longitude and nodeObj.latitude and nodeObj.data['addr:housenumber'] and nodeObj.data[
                'addr:street'] and nodeObj.id:
                nodes.append(nodeObj)
                ResetBox(box,float(nodeObj.longitude),float(nodeObj.latitude))
        nodes.append(box)
        return nodes


'''
                node = ET.SubElement(root, "node", id=nodeObj.id, version="1", lat=nodeObj.latitude, lon=nodeObj.longitude,
                                     t="enhancedOSM")
                for key, val in nodeObj.data.items():
                    if val:
                        ET.SubElement(node, "tag", k=key, v=val)

            xml = ET.ElementTree(root)
    opfn = fn + str(int(time.time()))
    #xml.write("%s.xml" % opfn)
    '''


def AssignRowToObject(row):
    nodeObj = Node()
    nodeObj.longitude = (row[0])
    nodeObj.latitude = (row[1])
    nodeObj.data['addr:housenumber'] = (row[2])
    nodeObj.data['addr:street'] = (row[3])
    nodeObj.data['addr:unit'] = row[4]
    nodeObj.data['addr:city'] = row[5]
    nodeObj.data['addr:district'] = row[6]
    nodeObj.data['addr:reqion'] = row[7]
    nodeObj.data['addr:postcode'] = row[8]
    nodeObj.id = row[9]
    nodeObj.hash = row[10]
    return nodeObj


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


def Main():
    nodes=[]
    path="S:/Course work/Spring 19/Garmin/openaddr-collected-north_america-sa/jm"
    #path="S:/Course work/Spring 19/Garmin/openaddr-collected-us_midwest/us/mi"
    for path in glob.glob(os.path.join(path, '*.csv')):
        nodes=GenerateXmlFromCsv(path)

    ways = GetWaysData(nodes[-1])
    print (ways)


if __name__== "__main__":
  Main()
