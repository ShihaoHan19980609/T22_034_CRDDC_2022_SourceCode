# 南京邮电大学
# 韩世豪
# 开发时间: 2022/9/27 13:49
import os
from tqdm import tqdm
import xml.etree.ElementTree as ET


def ReadXml(xml):
    if os.path.exists(xml) is False:
        return None
    tree = ET.parse(xml)
    objects = []
    for object in tree.findall('object'):
        obj_struct = object.find('name').text
        if obj_struct not in ['D00', 'D10', 'D20', 'D40']:
            continue
        objects.append(obj_struct)
    return objects


def CountLabelKind(xmls):
    LabelDict = {}
    print("Star to count label kinds....")
    for xml in tqdm(xmls):
        Infos = ReadXml(xml)
        for Info in Infos:
            if Info not in LabelDict.keys():
                LabelDict[Info] = 1
            else:
                LabelDict[Info] += 1

    return dict(sorted(LabelDict.items(), key=lambda x: x[0]))


if __name__ == '__main__':
    f = open('Japan.txt', "r")  # ***************************
    img_list = f.readlines()
    f.close()
    xml_list = []
    for img in img_list:
        xml = img.strip().replace('images', 'annotations')
        xml = xml.replace('jpg', 'xml')
        xml_list.append(xml)
    LabelDict = CountLabelKind(xml_list)
    KeyDict = sorted(LabelDict)
    print("%d kind labels and %d labels in total:" % (len(KeyDict), sum(LabelDict.values())))
    print(KeyDict)
    print("Label Name and it's number:")
    for key in KeyDict:
        print("%s\t: %d" % (key, LabelDict[key]))
