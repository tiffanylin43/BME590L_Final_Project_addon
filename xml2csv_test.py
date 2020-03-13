import xml.etree.ElementTree as ET
import json


def create_json(filename):
    path = 'G:\\Duke\\19 Spring\\BME 590\\final project\\tuberculosis-phonecamera\\' + str(filename)
    tree = ET.parse(path)
    root = tree.getroot()
    
    xmin = []
    xmax = []
    ymin = []
    ymax = []
    
    for x1 in root.iter('xmin'):
        xmin1 = int(x1.text)
        xmin.append(xmin1)

    for x2 in root.iter('xmax'):
        xmax1 = int(x2.text)
        xmax.append(xmax1)

    for y1 in root.iter('ymin'):
        ymin1 = int(y1.text)
        ymin.append(ymin1)

    for y2 in root.iter('ymax'):
        ymax1 = int(y2.text)
        ymax.append(ymax1)

    loc = {'xmin': xmin,
           'xmax': xmax,
           'ymin': ymin,
           'ymax': ymax
           }
    
    name, _ = str(filename).split('.')
    output_name = str(name) + '.json'
    out_file = open(output_name, "w")
    json.dump(loc, out_file)
    out_file.close()
    
    
for i in range(1265):
    num = str(i+1).zfill(4)
    filename = 'tuberculosis-phone-' + str(num) + '.xml'
    create_json(filename)





    