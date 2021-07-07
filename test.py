import os

imagesPath = 'F:\\baby\\40-50-OIDv4_ToolKit_download_google_public_images\\OID\\Dataset\\train\\Human_face\\images'
xmlPath = 'F:\\baby\\40-50-OIDv4_ToolKit_download_google_public_images\\OID\\Dataset\\train\\Human_face\\xml'

os.chdir(imagesPath)

allimages = os.listdir()
count = 0
for images in allimages:
    fileName = os.path.splitext(os.path.basename(images))[0]
    print(fileName)
    if os.path.isfile(xmlPath+'\\'+fileName+'.xml'):
        print("find this file")
    else:
        os.remove(images)
        print("this file isn't such")
