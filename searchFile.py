from PIL import Image
from PIL.ExifTags import TAGS
import os
import csv
import numpy
import time

time_start = time.time()

classList = ['Human face', 'Human eye', 'Human nose', 'Human mouth']
classCsvFilePath = 'F:\\python\\40-50-OIDv4_ToolKit_download_google_public_images\\OID\\csv_folder\\class-descriptions-boxable.csv'
labelFolderPath = 'F:\\python\\40-50-OIDv4_ToolKit_download_google_public_images\\OID\\Dataset'
annotationsbaseCsvPath = 'F:\\python\\40-50-OIDv4_ToolKit_download_google_public_images\\OID\\csv_folder\\'
annotationCsv = '-annotations-bbox.csv'
dataList = ['train', 'validation', 'test']


def searchClassCode(className):
    classCode = []
    className2 = []
    with open(classCsvFilePath, newline='') as df:
        rows = csv.reader(df)
        for row in rows:
            if row[1] in className:
                classCode.append(row[0])
                className2.append(row[1])
    return classCode, className2


def writeFileData(imageName, row, classCode, className, folderPath, size):
    with open(folderPath, 'a') as out_file:
        a = []
        for i in range(4, 8):
            if i < 6:
                a.append(float(row[i])*size[0])
            else:
                a.append(float(row[i])*size[1])
        out_file.write("{} {} {} {} {}\n".format(className[classCode.index(
            row[2])], a[0], a[2], a[1], a[3]))


def searchFileData(imageNameList, classCode, className, folderName, secondFolderName):
    dataList = []
    with open(annotationsbaseCsvPath+folderName+annotationCsv, newline='') as df:
        rows = csv.reader(df)
        for row in rows:
            if row[0] in imageNameList and row[2] in classCode:
                img = Image.open(labelFolderPath+'\\'+folderName +
                                 '\\'+secondFolderName+'\\'+row[0]+'.jpg')
                writeFileData(row[0], row, classCode, className, labelFolderPath +
                              '\\'+folderName+'\\'+secondFolderName+'\\Label\\'+row[0]+'.txt', img.size)


imageList = []
classCode, className = searchClassCode(classList)

os.chdir(labelFolderPath)
folderList = os.listdir()

for folderName in folderList:
    if folderName in dataList:
        secondFolderList = os.listdir(labelFolderPath+'\\'+folderName)
        for secondFolderName in secondFolderList:
            imageList2 = os.listdir(
                labelFolderPath+'\\'+folderName+'\\'+secondFolderName)
            for imageName in imageList2:
                if imageName != 'Label':
                    imageName = imageName.split('.')[0]
                    imageList.append(imageName)
            searchFileData(imageList, classCode, className,
                           folderName, secondFolderName)

time_end = time.time()
print('test cost', time_end-time_start, 's')
