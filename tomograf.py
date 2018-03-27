#!/usr/bin/python
import cv2
import math
import numpy as np
np.seterr(over='ignore')

def bresenhamLineScan(x1, y1, x2, y2, pimage):
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
        dy = dy2 - y1
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


image = cv2.imread("przyklad1.png")
print("Source image shape (height, width, color): ", image.shape, "\n")

imageHeight = image.shape[0]
imageWidth = image.shape[1]
imageDepth = image.shape[2] # 24-bitowy kolor

Sx = math.floor(imageWidth / 2) # image center X coord
Sy = math.floor(imageHeight / 2) # image center Y coord

R = math.floor((imageHeight - 1) / 2.0) - 1 # image circle radius

imageCircle = np.zeros([imageHeight,imageWidth], dtype = np.int32)

for i in range(imageWidth):
    for j in range(imageHeight):
        d = math.sqrt(pow((i - Sx),2) + pow((j - Sy),2))
        if d <= R:
            # uśrednij do skali szarości
            tavg = math.floor(((image[j,i,0] + image[j,i,1] + image[j,i,2]) / 3))
            imageCircle[j,i] = tavg

numberOfEmitters = 9 # liczba nieparzysta
halfNumberOfEmitters = math.floor(numberOfEmitters / 2)
angleOfEmitters = 65 # kąt ustawienia emiterów
spaceBetweenEmitters = 5 # odstęp kątowy pomiędzy emiterami
detectorValues = np.zeros(numberOfEmitters + 1, dtype = np.int16)

# I ćwiartka
if angleOfEmitters >= 0 and angleOfEmitters <= 90:
    angle = math.radians(angleOfEmitters)
    x = math.floor(R * math.sin(angle))
    y = math.floor(R * math.sin(angle))
    Ax = Sx + x
    Ay = Sy + y
    Bx = Sx - x
    By = Sy - y
    detectorValues[0] = bresenhamLineScan(Ax, Ay, Bx, By, imageCircle)
    detectorValues[numberOfEmitters] = angleOfEmitters
    detectorValuesSaved = detectorValues


print("Detector normalized values (last value is angle):\n", detectorValues)