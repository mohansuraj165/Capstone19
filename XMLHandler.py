import xml.etree.cElementTree as ET
import datetime
import uuid

currentDT = datetime.datetime.now()
currentDT = currentDT.strftime("%Y-%m-%d%H:%M")
root = ET.Element('root')
file = "OSM-OA-%s.xml"%(str)(uuid.uuid4())

def WriteToXML():
    xml=ET.ElementTree(root)
    xml.write(file)
