from PIL import Image
import os
import csv
import numpy
import time
import pandas

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


def writeFileData(boxes, className, folderPath, size):
    with open(folderPath, 'a') as out_file:
        for box in boxes:
            a = []
            for i in range(4):
                if i < 2:
                    a.append(float(box[i])*size[0])
                else:
                    a.append(float(box[i])*size[1])
            out_file.write("{} {} {} {} {}\n".format(
                className, a[0], a[2], a[1], a[3]))


def searchFileData(imageNameList, classCode, className, folderName, secondFolderName):
    dataList = []
    csv_df = pandas.read_csv(annotationsbaseCsvPath+folderName+annotationCsv)
    a = csv_df["LabelName"] == classCode
    groups = csv_df[a].groupby("ImageID")

    for imageName in imageNameList:
        try:
            boxes = groups.get_group(imageName)[
                ['XMin', 'XMax', 'YMin', 'YMax']].values.tolist()
            img = Image.open(labelFolderPath+'\\'+folderName +
                             '\\'+secondFolderName+'\\'+imageName+'.jpg')
            writeFileData(boxes, className, labelFolderPath + '\\' +
                          folderName+'\\'+secondFolderName+'\\Label\\'+imageName+'.txt', img.size)
        except:
            continue


classCodeList, classNameList = searchClassCode(classList)

os.chdir(labelFolderPath)
folderList = os.listdir()

for folderName in folderList:
    if folderName in dataList:
        secondFolderList = os.listdir(labelFolderPath+'\\'+folderName)
        for secondFolderName in secondFolderList:
            imageList = []
            imageList2 = os.listdir(
                labelFolderPath+'\\'+folderName+'\\'+secondFolderName)
            for imageName in imageList2:
                if imageName != 'Label':
                    imageName = imageName.split('.')[0]
                    imageList.append(imageName)
            count = len(classCodeList)
            for i in range(count):
                searchFileData(imageList, classCodeList[i], classNameList[i],
                               folderName, secondFolderName)


time_end = time.time()
print('test cost', time_end-time_start, 's')
