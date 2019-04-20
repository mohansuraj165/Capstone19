import xml.etree.cElementTree as ET
import datetime

currentDT = datetime.datetime.now()
currentDT = currentDT.strftime("%Y-%m-%d%H:%M")
root = ET.Element('root')

def WriteToXML():
    xml=ET.ElementTree(root)
    xml.write("tem.xml")
