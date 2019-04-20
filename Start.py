#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
import csv
import glob
import os
import OSMPythonToolsHandler as OSM
import AssociateNodesAndWays as ANW
import DB_eOSMGenerator as DB
import Logger as Log
import XMLHandler as XML
import time

'''
Store each node data received from OpenAddresses
OpenAddresses data is in CSV.
It is parsed to object.
'''
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

'''
Holds the coordinated within which OSM data has to be fetched
Values are calculated from OpenAddresses CSV
'''
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

'''
Calculates the min/max latitude and longitude required for OSM data fetch
'''
def ResetBox(box, lon, lat):
    if lat<(box.latMin):
        box.latMin=lat
    if lat>box.latMax:
        box.latMax=lat
    if lon<box.lonMin:
        box.lonMin=lon
    if lon>box.lonMax:
        box.lonMax=lon

'''
OpenAddresses data is in CSV format.
Converts CSV data to Node objects
'''
def GetNodesFromCsv(path):
    global xml
    nodes = []
    box = Coordinates()
    try:
        with open(path, encoding="utf8") as csvfile:
            csvData = csv.reader(csvfile)
            next(csvData, None)  # Skips headers for each file

            for row in csvData:

                nodeObj = AssignRowToObject(row)
                if nodeObj.longitude and nodeObj.latitude and nodeObj.number and nodeObj.street:
                    nodes.append(nodeObj)
                    ResetBox(box,float(nodeObj.longitude),float(nodeObj.latitude))
            nodes.append(box)   #appends the coordinates object to nodes list

            return nodes
    except Exception as e:
        Log.logging.error("In Start.py, GetNodesFromCsv()", exc_info=True)


'''
Assigns each row of the CSV file to the Node object
'''
def AssignRowToObject(row):
    nodeObj = Node()
    try:

        nodeObj.longitude = (row[0])
        nodeObj.latitude = (row[1])
        nodeObj.number = row[2]
        nodeObj.street = row[3]
        nodeObj.streetPhoneticCode = OSM.GetPhoneticCode(nodeObj.street)
        nodeObj.data['addr:housenumber'] = str(row[2])
        nodeObj.data['addr:street'] = (row[3])
        nodeObj.data['addr:unit'] = row[4]
        nodeObj.data['addr:city'] = row[5]
        nodeObj.data['addr:district'] = row[6]
        nodeObj.data['addr:reqion'] = row[7]
        nodeObj.data['addr:postcode'] = row[8]
        nodeObj.id = row[9]
        nodeObj.hash = row[10]
    except IndexError as e:
        Log.logging.error("In file Start.py, AssignRowToObject()", exc_info=True)

    return nodeObj


def Main(path):
    DB.CreateDBConnection()
    nodes=[]
    xml=""

    try:
        for path in glob.glob(os.path.join(path, '*.csv')):
            '''Gets nodes data from Open Address'''
            nodes=GetNodesFromCsv(path)
            '''
            Gets ways data from OSM based on Lat/Lon values calculated from nodes
            Stores the data in DB
            '''
            if (OSM.GetOSMWaysData(nodes[-1])):
                del nodes[-1]   #Remove coordinates object as we do not need it anymore

                '''Compare ways and nodes data and matches nodes with ways'''
                start_time = time.time()
                ANW.MatchNodesWithOSMWays(nodes)
                print("--- %s seconds ---" % (time.time() - start_time))
    except Exception as e:
        Log.logging.error("In file Start.py, Main()", exc_info=True)


    print("done")
    XML.WriteToXML()

if __name__== "__main__":
    path="S:/data/"
    Main(path)
