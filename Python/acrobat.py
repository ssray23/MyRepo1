import xml.etree.ElementTree as ET
mytree = ET.parse("C:\\Program Files (x86)\\Adobe\\Acrobat DC\\Acrobat\\AMT\\application.xml")
myroot = mytree.getroot()
print(myroot)

# for x in myroot[1]:
#     print(x.text)

print('')

print('')
print('------- PRINTING ALL LINES OF Other ELEMENT --------')
for y in myroot.findall('Other'):
    for line in y:
        print(line.attrib)
        print(line.text)
        print('')

print('')
print('------- PRINTING key attribute of every line OF Other ELEMENT --------')
for y in myroot.findall('Other'):
    for line in y:
        print(line.attrib['key'])
        print(line.text)
        # if line.attrib['key'] == 'TrialSerialNumber':
            # new_serial = int(line.text) - 1
            # y.text = str(new_serial)
            # print('New Serial is : ' + str(new_serial))
            # y.set
        print('')
        
# my_d = {}
 
