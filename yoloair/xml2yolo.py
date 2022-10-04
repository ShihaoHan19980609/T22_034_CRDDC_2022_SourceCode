import argparse
import math
import os
import sys
import xml.etree.ElementTree as ET
from PIL import Image
from collections import defaultdict
from random import shuffle
from tqdm import tqdm

# Type of image in Dataset
imageType = ["jpg", "png", "jpeg", "JPEG", "JPG", "PNG"]
# dictionary to store list of image paths in each class
imageListDict = defaultdict(set)
path = os.path.join('RDD2022', 'VOCdevkit')
yolo = os.path.join(path, 'labels')
if os.path.exists(yolo):
    print('labels exists')
    pass
else:
    os.makedirs(yolo)


def convert(size, box):
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return [x, y, w, h]


# convert minX,minY,maxX,maxY to normalized numbers required by Yolo
def getYoloNumbers(imagePath, minX, minY, maxX, maxY):
    image = Image.open(imagePath)
    w = int(image.size[0])
    h = int(image.size[1])
    b = (minX, maxX, minY, maxY)
    bb = convert((w, h), b)
    image.close()
    return bb


def main():
    parser = argparse.ArgumentParser(description='xml to yolo')
    parser.add_argument('--xml_file', type=str,
                        help='location to the list of images/xml files(absolute path).',
                        default='all_country.txt')  # image列表
    args = parser.parse_args()

    # assign each class of dataset to a number
    outputCtoId = {}
    lines = ['D00', 'D10', 'D20', 'D40']  # 类别
    for i in range(len(lines)):
        outputCtoId[lines[i].strip()] = i

    # read the path of the directory where XML and images are present
    f = open(args.xml_file, "r")
    xmlFiles = f.readlines()
    f.close()
    list_index = range(len(xmlFiles))
    for i in list_index:
        xmlFiles[i] = xmlFiles[i].replace('images', 'annotations')
        xmlFiles[i] = xmlFiles[i].replace('.jpg', '.xml')
    print("total files:", len(xmlFiles))

    # loop over each file under dirPath
    for file in tqdm(xmlFiles):
        filePath = file.strip()
        # print(filePath)
        tree = ET.parse(filePath)
        root = tree.getroot()

        i = 0
        imageFile = filePath[:-4].replace("annotations", "images") + "." + imageType[i]
        while (not os.path.isfile(imageFile) and i < 2):
            i += 1
            imageFile = filePath[:-4].replace("annotations", "images") + "." + imageType[i]

        if not os.path.isfile(imageFile):
            print("File not found:", imageFile)
            continue
        txtFile = imageFile.split('/')[-1]
        txtFile = imageFile.replace("images", "labels")
        txtFile = txtFile[:-4] + ".txt"
        txtFile = os.path.join(txtFile)
        yoloOutput = open(txtFile, "w")

        # loop over each object tag in annotation tag
        for objects in root.findall('object'):
            surfaceType = objects.find('name').text.replace(" ", "")

            # try:
            if surfaceType == "D00" or surfaceType == "D10" or surfaceType == "D20" or surfaceType == "D40":
                bndbox = objects.find('bndbox')
                try:
                    [minX, minY, maxX, maxY] = [int(child.text) for child in bndbox]
                except:
                    [minX, minY, maxX, maxY] = [int(float(child.text)) for child in bndbox]
                [x, y, w, h] = getYoloNumbers(imageFile, minX, minY, maxX, maxY)
                yoloOutput.write(
                    str(outputCtoId[surfaceType]) + " " + str(x) + " " + str(y) + " " + str(w) + " " + str(
                        h) + "\n")
                imageListDict[outputCtoId[surfaceType]].add(imageFile)

        yoloOutput.close()

    for cl in imageListDict:
        print(lines[cl].strip(), ":", len(imageListDict[cl]))


if __name__ == "__main__":
    main()
