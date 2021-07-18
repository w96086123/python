from PIL import Image
from PIL.ExifTags import TAGS
import os
import csv
import numpy

classList = ['Human face', 'Human eye', 'Human nose', 'Human mouth']
classCsvFilePath = 'F:\\python\\40-50-OIDv4_ToolKit_download_google_public_images\\OID\\csv_folder\\class-descriptions-boxable.csv'
labelFolderPath = 'F:\\python\\40-50-OIDv4_ToolKit_download_google_public_images\\OID\\Dataset'
annotationsbaseCsvPath = 'F:\\python\\40-50-OIDv4_ToolKit_download_google_public_images\\OID\\csv_folder\\'
annotationCsv = '-annotations-bbox.csv'
dataList = ['train', 'validation', 'test']

# 查詢編號


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
# 搜尋各圖片數值


def searchFileData(imageNameList, classCode, folderName):
    dataList = []
    with open(annotationsbaseCsvPath+folderName+annotationCsv, newline='') as df:
        rows = csv.reader(df)
        for row in rows:
            if row[0] in imageNameList and row[2] in classCode:
                dataList.append(row)
    return dataList
# 寫入圖片資料


def writeFileData(imageName, fileDataList, classCode, className, folderPath, size):
    with open(folderPath, 'w') as out_file:
        for row in fileDataList:
            if row[0] == imageName and row[2] in classCode:
                a = []
                for i in range(4, 8):
                    if i < 6:
                        a.append(float(row[i])*size[0])
                    else:
                        a.append(float(row[i])*size[1])
                out_file.write("{} {} {} {} {}\n".format(className[classCode.index(
                    row[2])], a[0], a[2], a[1], a[3]))


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
                fileDataList = searchFileData(imageList, classCode, folderName)
            for imageName in imageList:
                img = Image.open(labelFolderPath+'\\'+folderName +
                                 '\\'+secondFolderName+'\\'+imageName+'.jpg')
                writeFileData(imageName, fileDataList, classCode, className, labelFolderPath +
                              '\\'+folderName+'\\'+secondFolderName+'\\Label\\'+imageName+'.txt', img.size)
