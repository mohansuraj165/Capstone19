import csv
import xml.etree.cElementTree as ET
import xml.dom.minidom
import time
import glob
import os

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

#path = "S:\Course work\Spring 19\Garmin\openaddr-collected-us_northeast\us\ct"
fn="Test_data"
path="S:/Course work/Spring 19/Garmin/openaddr-collected-north_america-sa/jm"


def GetFilenameFromPath(path):
    pathArr = path.split("\\")
    fn = pathArr[len(pathArr)-1]
    fn = fn[:fn.index('.csv')]
    return(fn)


for path in glob.glob(os.path.join(path, '*.csv')):
    with open (path, 'rt') as csvfile:
        fn = GetFilenameFromPath(path)
        csvData = csv.reader(csvfile)
        next(csvData,None)#Skips headers
        root = ET.Element("root")
        for row in csvData:
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
            #print (node.longitude)
            #print (node.street)

            if nodeObj.longitude and nodeObj.latitude and nodeObj.data['addr:housenumber'] and nodeObj.data['addr:street'] and nodeObj.id:
                node = ET.SubElement(root,"node",version="1", lat = nodeObj.latitude, lon = nodeObj.longitude, t="enhancedOSM")
                for key,val in nodeObj.data.items():
                    if val:
                         ET.SubElement(node,"tag", k=key, v=val)


            xml = ET.ElementTree(root)
    opfn = fn + str(int(time.time()))

    xml.write("%s.xml"%opfn)


