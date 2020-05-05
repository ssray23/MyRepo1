import xml.etree.ElementTree as ET
mytree = ET.parse("C:\\Program Files (x86)\\Adobe\\Acrobat DC\\Acrobat\\AMT\\application.xml")
myroot = mytree.getroot()
print(myroot)
for x in myroot[1]:
    print(x.text)
