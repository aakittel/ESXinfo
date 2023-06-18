import xml.dom.minidom
import xml.etree.ElementTree as ET
xmlfile = "/home/admin/ESXinfo/esx-testesx2.-2023-06-16--13.29-2460058/commands/esxcfg-info.xml"
#doc = xml.dom.minidom.parse(xmlfile);
#print(doc.nodeName)

doc = ET.parse(xmlfile)
root = doc.getroot()
print(root)
for item in root.findall():
    print(item)