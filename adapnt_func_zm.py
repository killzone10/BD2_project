import cv2
import numpy as np
import pytesseract
import re
import tkinter as tk
import string
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\plKrajewBa\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
def empty(a):
    pass
cv2.namedWindow('stack')
cv2.resizeWindow('stack' ,600 ,300)

cv2.createTrackbar("z",'stack',11,50,empty)
cv2.createTrackbar("z1",'stack',11,50,empty)
# kernel = np.ones((1, 1), np.uint8)
# kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3,3))  # to manipulate the orientation of dilution , large x means horizonatally dilating  more, large y means vertically dilating more
### dla cookie grisp 18.jpg blur
def img_read_gray(path):
    img = cv2.imread(path)
    # img = cv2.resize(img, None, fx=0.2, fy=0.2)
    # img = cv2.bitwise_not(img) # biały napis !!
    b, g, r = cv2.split(img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return gray,r,img
def adapt_thresh(gray):
    z = cv2.getTrackbarPos('z', "stack")
    if z % 2 == 0:
        z += 1
    z1 = cv2.getTrackbarPos('z1','stack')

    # z1 = cv2.getTrackbarPos('z1', "trackbar")
    # kernel = np.ones((1, 1), np.uint8)
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
    # dilatation = cv2.dilate(gray, kernel, iterations=3)
    # erosion = cv2.erode(gray, kernel, iterations=3)
    # closing = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, kernel)
    opening = cv2.morphologyEx(gray, cv2.MORPH_OPEN, kernel)
    adapt = cv2.adaptiveThreshold(opening, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, z,z1)  # ( optymalne dla 47 7, 10 // git 9,10) 48 -- 15 13   -- 15 11 dla  38
    # 11 11 5  #6 11 /5   #27 ( kartony ) not 21 17
    return adapt

# def adapt_thresh1(r):
#     z = cv2.getTrackbarPos('z', "trackbar")
#     z1 = cv2.getTrackbarPos('z1', "trackbar")
#     # kernel = np.ones((1, 1), np.uint8)
#     kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
#     dilatation = cv2.dilate(r, kernel, iterations=3)
#     erosion = cv2.erode(r, kernel, iterations=3)
#     closing = cv2.morphologyEx(r, cv2.MORPH_CLOSE, kernel)
#     opening = cv2.morphologyEx(r, cv2.MORPH_OPEN, kernel)
#     adapt = cv2.adaptiveThreshold(opening, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, z,z1)  # ( optymalne dla 47 7, 10 // git 9,10) 48 -- 15 13   -- 15 11 dla  38
#     # 11 11 5  #6 11 /5   #27 ( kartony ) not 21 17
#     cv2.imshow('adapt', adapt)
#     cv2.waitKey(1)
#     return adapt
def reading(adapt):
    data = pytesseract.image_to_string(adapt, lang='pol',config='--psm 11')
    y = string.punctuation+'[aąbcćdeęfghijklłmnńoóprstwyz*&^%$#@!,./><:?-]'
    # y= string.punctuation
    # data = re.sub(y,"",data) ## zobacz ktore jest bardziej optymalne dla programu
    data = data.strip() ## usuwa białe znaki na poczatku i na końcu
    # print(data)
    splitted = data.split("\n") #  lista w str po enterach
    # print(f'splitted',splitted) #debug

    new_split = [line for line in splitted if line.strip()!= ""] ## jeśli linia nie  jest pusta zrob to co na dol
    out = ''
    for line in new_split:
        line1 = ''
        # line = line.translate(y) ## sprobowac pozniej
        # li    ne = re.sub(y, "", line) #usuwanie wszystkich znakow \\ sprawdz ktore jest szybsze
        for char in y:  ## usuwanie znakow specjanych all
            line = line.replace(char, '')
        # for char in ['a-z']: ## usuwanie znakow specjanych all
        #     line = line.replace(char,'')
        for char in line:
            line1 += char
            if line1.count('0968') == 1 :
                # out += line1+ "\n"
                line1=''
        # out+=line1 +"\n"
        out += line +"\n"
        # out= out.strip()
    out = out.replace(" ", "")
    out = out.rsplit("\n")
    out.pop()
    print(out)
    return data, out
def textOnImage(data):
    pass
    # text_img = np.zeros((440, 900, 3), dtype=np.uint8) ## mozliwe uzycie w gui przy debugowaniu

    # font = cv2.FONT_HERSHEY_SIMPLEX
    # bottomLeftCornerOfText = (10, 50)
    # fontScale = 1
    # fontColor = (255, 255, 255)
    # lineType = 2
    # cv2.putText(text_img, data, bottomLeftCornerOfText, font, fontScale, fontColor, lineType)

def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver
# def stringChange(data):
#     for x in data :
#         if data[x] is "[a-z]"
def dataImport():
    pass
while True:
    z = cv2.getTrackbarPos('z', "stack")
    z1 = cv2.getTrackbarPos('z1', "stack")
    path = '28.jpg'
    path = '999.png'
    gray,r,img = img_read_gray(path)
    adapt = adapt_thresh(r)
    # adapt=adapt_thresh(gray)
    # adaptr =adapt_thresh1(r)
    data,out= reading(adapt)
    root = tk.Tk()
    T = tk.Text(root, height=30, width=30)
    T.pack()
    T.insert(tk.END, out)
    tk.mainloop()
    imgArray = ([img,adapt])
    stackedImages = stackImages(1,imgArray)
    cv2.imshow("stack",stackedImages)
    cv2.waitKey(1)

