from PIL import Image
import os
import csv
import numpy
import time
import pandas

time_start = time.time()

classList = ['Human face', 'Human eye', 'Human nose', 'Human mouth']
classCsvFilePath = 'F:\\python\\40-50-OIDv4_ToolKit_download_google_public_images\\OID\\csv_folder\\class-descriptions-boxable.csv'
labelFolderPath = 'C:\\Users\\User\\Desktop\\pythontest'
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


def writeFileData(csv_df, classCode, className, folderPath, size):
    with open(folderPath, 'w') as out_file:
        for row in range(csv_df.shape[0]):
            a = []
            for i in range(4, 8):
                if i < 6:
                    a.append(float(csv_df.iloc[row][i])*size[0])
                else:
                    a.append(float(csv_df.iloc[row][i])*size[1])
            out_file.write("{} {} {} {} {}\n".format(className[classCode.index(
                csv_df.iloc[row][2])], a[0], a[2], a[1], a[3]))


def searchFileData(imageNameList, classCode, className, folderName, secondFolderName):
    dataList = []
    with open(annotationsbaseCsvPath+folderName+annotationCsv, newline='') as df:
        csv_data = pandas.read_csv(df)
        csv_df = pandas.DataFrame(csv_data)
        for imageName in imageNameList:
            a = csv_df["ImageID"] == imageName
            c = csv_df["LabelName"].isin(classCode)
            b = csv_df[a & c]
            img = Image.open(labelFolderPath+'\\'+folderName +
                             '\\'+secondFolderName+'\\'+imageName+'.jpg')
            writeFileData(b, classCode, className, labelFolderPath +
                          '\\'+folderName+'\\'+secondFolderName+'\\Label\\'+imageName+'.txt', img.size)


classCode, className = searchClassCode(classList)

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
            searchFileData(imageList, classCode, className,
                           folderName, secondFolderName)

time_end = time.time()
print('test cost', time_end-time_start, 's')
