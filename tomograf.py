#!/usr/bin/python
import cv2
import math
import numpy as np
import matplotlib.pyplot as plt
np.seterr(over='ignore')

def bresenhamLineValue(x1, y1, x2, y2):
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
    suma += imageCircle[y,x]
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
            suma += imageCircle[y,x]
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
            suma += imageCircle[y,x]
            dlugosc += 1
    # normalizacja
    srednia = round(float(suma) / dlugosc)
    return srednia

def calculateDiameterSection(angleOfEmitter):
    angle = math.radians(angleOfEmitter)
    x = math.floor(r * math.sin(angle))
    y = math.floor(r * math.cos(angle))
    Ax = Sx + x
    Ay = Sy - y
    Bx = Sx - x
    By = Sy + y
    sectionCoords = (Ax, Ay, Bx, By)
    return sectionCoords
    

image = cv2.imread("picture1.jpg")
#print("Source image shape (height, width, color): ", image.shape, "\n")

imageHeight = image.shape[0]
imageWidth = image.shape[1]
imageDepth = image.shape[2] # 24-bitowy kolor

Sx = math.floor(imageWidth / 2) # image center X coord
Sy = math.floor(imageHeight / 2) # image center Y coord

r = math.floor((imageHeight - 1) / 2.0) # image circle radius

imageCircle = np.zeros([imageHeight,imageWidth], dtype = np.int32)

for i in range(imageWidth):
    for j in range(imageHeight):
        d = math.sqrt(pow((i - Sx),2) + pow((j - Sy),2))
        if d <= r:
            # uśrednij do skali szarości
            tavg = math.floor(((image[j,i,0] + image[j,i,1] + image[j,i,2]) / 3))
            imageCircle[j,i] = tavg


# PARAMETRY TOMOGRAFU
numberOfEmitters = 15 # liczba nieparzysta >= 3
starterAngleOfMiddleEmitter = 30 # początkowy kąt ustawienia centralnego emitera
spaceBetweenEmitters = 1 # odstęp kątowy pomiędzy emiterami
emittersRotationStep = 1 # krok obrotu emiterów w stopniach


halfNumberOfEmitters = math.floor(numberOfEmitters / 2)
emittersAngularSpread = (numberOfEmitters - 1) * spaceBetweenEmitters # rozpiętość kątowa emiterów

if(emittersAngularSpread > 180):
	print("Rozpiętość kątowa emiterów przekracza 180 stopni!")
	quit()

currentAngleOfMiddleEmitter = starterAngleOfMiddleEmitter
rotationDegreesPassed = 0
detectorValuesAll = {}

while True:
    leftSideBeamCoordsA = np.zeros(halfNumberOfEmitters, dtype = (np.int32, 2))
    leftSideBeamCoordsB = np.zeros(halfNumberOfEmitters, dtype = (np.int32, 2))
    rightSideBeamCoordsA = np.zeros(halfNumberOfEmitters, dtype = (np.int32, 2))
    rightSideBeamCoordsB = np.zeros(halfNumberOfEmitters, dtype = (np.int32, 2))
    angleOfSideEmitter = currentAngleOfMiddleEmitter
    for i in range(halfNumberOfEmitters):
        # emitery boczne lewe
        angleOfSideEmitter -= spaceBetweenEmitters
        if angleOfSideEmitter < 0:
            angleOfSideEmitter = 360 + angleOfSideEmitter
        elif angleOfSideEmitter > 360:
            angleOfSideEmitter = angleOfSideEmitter - 360
        tempSection = calculateDiameterSection(angleOfSideEmitter)
        x1 = tempSection[0]
        y1 = tempSection[1]
        x2 = tempSection[2]
        y2 = tempSection[3]
        leftSideBeamCoordsA[i] = (x1, y1)
        rightSideBeamCoordsB[i] = (x2, y2)
    angleOfSideEmitter = currentAngleOfMiddleEmitter
    for i in range(halfNumberOfEmitters):
        # emitery boczne prawe
        angleOfSideEmitter += spaceBetweenEmitters
        if angleOfSideEmitter < 0:
            angleOfSideEmitter = 360 + angleOfSideEmitter
        elif angleOfSideEmitter > 360:
            angleOfSideEmitter = angleOfSideEmitter - 360
        tempSection = calculateDiameterSection(angleOfSideEmitter)
        x1 = tempSection[0]
        y1 = tempSection[1]
        x2 = tempSection[2]
        y2 = tempSection[3]
        rightSideBeamCoordsA[i] = (x1, y1)
        leftSideBeamCoordsB[i] = (x2, y2)

    
    detectorValuesCurrent = np.zeros(numberOfEmitters, dtype = np.int32)

    tempSection = calculateDiameterSection(currentAngleOfMiddleEmitter)
    mx1 = tempSection[0]
    my1 = tempSection[1]
    mx2 = tempSection[2]
    my2 = tempSection[3]
    normalizedValue = bresenhamLineValue(mx1, my1, mx2, my2)
    detectorValuesCurrent[halfNumberOfEmitters] = normalizedValue # wartość dla centralnego emitera

    for i in range(halfNumberOfEmitters):
        # emitery boczne lewe
        lx1 = leftSideBeamCoordsA[i][0]
        ly1 = leftSideBeamCoordsA[i][1]
        lx2 = leftSideBeamCoordsB[i][0]
        ly2 = leftSideBeamCoordsB[i][1]
        normalizedValue = bresenhamLineValue(lx1, ly1, lx2, ly2)
        detectorValuesCurrent[halfNumberOfEmitters - 1 - i] = normalizedValue
    for i in range(halfNumberOfEmitters):
        # emitery boczne prawe
        rx1 = rightSideBeamCoordsA[i][0]
        ry1 = rightSideBeamCoordsA[i][1]
        rx2 = rightSideBeamCoordsB[i][0]
        ry2 = rightSideBeamCoordsB[i][1]
        normalizedValue = bresenhamLineValue(rx1, ry1, rx2, ry2)
        detectorValuesCurrent[halfNumberOfEmitters + 1 + i] = normalizedValue

    detectorValuesAll[currentAngleOfMiddleEmitter] = detectorValuesCurrent

    currentAngleOfMiddleEmitter += emittersRotationStep
    if currentAngleOfMiddleEmitter > 360:
        currentAngleOfMiddleEmitter = currentAngleOfMiddleEmitter - 360

    rotationDegreesPassed += emittersRotationStep

    if rotationDegreesPassed >= 360:
        break

# Wypisz kąty skanowania i wartości uzyskane na detektorach
print("Angle of emitters and values of detectors per phase")
for key, value in detectorValuesAll.items():
    print(str(key) + "\t" + str(value))

# Utwórz i wyświetl sinogram
fig, (ax1,ax2) = plt.subplots(1, 2, figsize=(8, 4.5))
ax1.set_title("Original")
ax1.imshow(image)
R = np.zeros((361, numberOfEmitters), dtype='float')
for key, value in detectorValuesAll.items():
    R[key, :] = value[math.floor(len(value)/2)+1]

'''
M1 = np.zeros((imageWidth,imageHeight),dtype='int32')
M2 = np.zeros((imageWidth,imageHeight),dtype='int32')
a = 0
for key, value in detectorValuesAll.items():
 a = math.atan(key)
 cv2.line(M1
'''

ax2.set_title("Sinogram")
ax2.set_xlim([0, numberOfEmitters])
#ax2.xaxis.set_ticks(np.arange(0, numberOfEmitters, 1))
ax2.set_xlabel("Detector number")
ax2.set_ylabel("Projection angle (deg)")
ax2.imshow(R)
plt.imshow(R, cmap='gray', aspect='auto')
plt.show()