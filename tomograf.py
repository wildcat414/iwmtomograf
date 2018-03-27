#!/usr/bin/python
import cv2
import math
import numpy as np
np.seterr(over='ignore')

def bresenhamLineValue(x1, y1, x2, y2, pimage):
    # zmienne pomocnicze
    x = int(x1)
    y = int(y1)
    suma = 0
    dlugosc = 0
    # ustalenie kierunku rysowania
    if x1 < x2:
        xi = 1
        dx = x2 - x1
    else:
        xi = -1
        dx = x1 - x2
    # ustalenie kierunku rysowania
    if y1 < y2:
        yi = 1
        dy = y2 - y1
    else:
        yi = -1
        dy = y1 - y2
    # pierwszy piksel
    suma += pimage[y,x]
    dlugosc += 1
    # oś wiodąca X
    if dx > dy:
        ai = (dy - dx) * 2
        bi = dy * 2
        d = bi - dx
        # pętla po kolejnych x
        while x != x2:
            # test współczynnika
            if d >= 0:
                x += xi
                y += yi
                d += ai
            else:
                d += bi
                x += xi
            suma += pimage[y,x]
            dlugosc += 1
    # oś wiodąca Y
    else:
        ai = (dx - dy) * 2
        bi = dx * 2
        d = bi - dy
        # pętla po kolejnych y
        while y != y2:
            if d >= 0:
                x += xi
                y += yi
                d += ai
            else:
                d += bi
                y += yi
            suma += pimage[y,x]
            dlugosc += 1
    # normalizacja
    srednia = round(float(suma) / dlugosc)
    return srednia

def runEmitter(angleOfEmitter, r, image):
    if angleOfEmitter >= 0 and angleOfEmitter <= 90:
        # I ćwiartka
        angle = math.radians(angleOfEmitter)
        x = math.floor(r * math.sin(angle))
        y = math.floor(r * math.cos(angle))
        Ax = Sx + x
        Ay = Sy - y
        Bx = Sx - x
        By = Sy + y
    elif angleOfEmitter > 90 and angleOfEmitter <= 180:
        # II ćwiartka
        angle = math.radians(angleOfEmitter - 90)
        x = math.floor(r * math.cos(angle))
        y = math.floor(r * math.sin(angle))
        Ax = Sx + x
        Ay = Sy + y
        Bx = Sx - x
        By = Sy - y
    elif angleOfEmitter > 180 and angleOfEmitter <= 270:
        # III ćwiartka
        angle = math.radians(angleOfEmitter - 180)
        x = math.floor(r * math.sin(angle))
        y = math.floor(r * math.cos(angle))
        Ax = Sx - x
        Ay = Sy + y
        Bx = Sx + x
        By = Sy - y
    elif angleOfEmitter > 270 and angleOfEmitter <= 360:
        # IV ćwiartka
        angle = math.radians(angleOfEmitter - 270)
        x = math.floor(r * math.cos(angle))
        y = math.floor(r * math.sin(angle))
        Ax = Sx - x
        Ay = Sy - y
        Bx = Sx + x
        By = Sy + y
    return bresenhamLineValue(Ax, Ay, Bx, By, image)
    

image = cv2.imread("przyklad1.png")
print("Source image shape (height, width, color): ", image.shape, "\n")

imageHeight = image.shape[0]
imageWidth = image.shape[1]
imageDepth = image.shape[2] # 24-bitowy kolor

Sx = math.floor(imageWidth / 2) # image center X coord
Sy = math.floor(imageHeight / 2) # image center Y coord

R = math.floor((imageHeight - 1) / 2.0) # image circle radius

imageCircle = np.zeros([imageHeight,imageWidth], dtype = np.int32)

for i in range(imageWidth):
    for j in range(imageHeight):
        d = math.sqrt(pow((i - Sx),2) + pow((j - Sy),2))
        if d <= R:
            # uśrednij do skali szarości
            tavg = math.floor(((image[j,i,0] + image[j,i,1] + image[j,i,2]) / 3))
            imageCircle[j,i] = tavg

numberOfEmitters = 7 # liczba nieparzysta
halfNumberOfEmitters = math.floor(numberOfEmitters / 2)
angleOfMiddleEmitter = 65 # kąt ustawienia emitera centralnego
spaceBetweenEmitters = 5 # odstęp kątowy pomiędzy emiterami

emitterAngles = np.zeros(numberOfEmitters, dtype = np.int32)
angleofCurrentEmitter = angleOfMiddleEmitter
for i in range(halfNumberOfEmitters - 1, -1, -1):
    angleofCurrentEmitter -= spaceBetweenEmitters
    if angleofCurrentEmitter < 0:
        angleofCurrentEmitter = 360 - angleofCurrentEmitter
    emitterAngles[i] = angleofCurrentEmitter
angleofCurrentEmitter = angleOfMiddleEmitter
for i in range(halfNumberOfEmitters + 1, numberOfEmitters, 1):
    angleofCurrentEmitter += spaceBetweenEmitters
    emitterAngles[i] = angleofCurrentEmitter
emitterAngles[halfNumberOfEmitters] = angleOfMiddleEmitter

detectorValues = {}

for i in range(numberOfEmitters):
    angleofExaminedEmitter = emitterAngles[i]
    detectorValues[angleofExaminedEmitter] = runEmitter(angleofExaminedEmitter, R, imageCircle)

print("Normalized Detectors\nAngle\tValue")
for key, value in detectorValues.items():
    print(str(key) + "\t" + str(value))