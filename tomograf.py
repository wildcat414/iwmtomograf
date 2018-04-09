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

def bresenhamLineDraw(x1, y1, x2, y2, value):
    x = int(x1)
    y = int(y1)
    if x1 < x2:
        xi = 1
        dx = x2 - x1
    else:
        xi = -1
        dx = x1 - x2
    if y1 < y2:
        yi = 1
        dy = y2 - y1
    else:
        yi = -1
        dy = y1 - y2
    imageReconstructed[y,x] += value
    pixelOverlapping[y,x] += 1
    if dx > dy:
        ai = (dy - dx) * 2
        bi = dy * 2
        d = bi - dx
        while x != x2:
            if d >= 0:
                x += xi
                y += yi
                d += ai
            else:
                d += bi
                x += xi
                imageReconstructed[y,x] += value
                pixelOverlapping[y,x] += 1
    else:
        ai = (dx - dy) * 2
        bi = dx * 2
        d = bi - dy
        while y != y2:
            if d >= 0:
                x += xi
                y += yi
                d += ai
            else:
                d += bi
                y += yi
            imageReconstructed[y,x] += value
            pixelOverlapping[y,x] += 1

def normalizeimageReconstructed():
    for i in range(imageHeight):
        for j in range(imageWidth):
            overlappingCount = pixelOverlapping[i,j]
            pixelValue = imageReconstructed[i,j]
            if overlappingCount > 1:
                normalizedPixelValue = math.floor(float(pixelValue) / overlappingCount)
            else:
                normalizedPixelValue = pixelValue
            imageReconstructed[i,j] = normalizedPixelValue
    maxPixelValue = imageReconstructed.max()
    dzielnik = maxPixelValue / 255.0
    for i in range(imageHeight):
        for j in range(imageWidth):
            imageReconstructed[i,j] = math.floor(float(imageReconstructed[i,j]) / dzielnik)

def calculateDiameterSection(angleParam):
    angle = math.radians(angleParam)
    x = math.floor(radius * math.sin(angle))
    y = math.floor(radius * math.cos(angle))
    Ax = Sx + x
    Ay = Sy - y
    Bx = Sx - x
    By = Sy + y
    sectionCoords = (Ax, Ay, Bx, By)
    #print("section coords for angle", angleParam, " are ", sectionCoords)
    return sectionCoords

print("Reading source image...")

image = cv2.imread("picture2.jpg") # obraz powinien być kwadratowy
imageGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#print("Original image shape (height, width, color): ", image.shape)
#print("Gray image shape (height, width, color): ", imageGray.shape)

imageHeight = image.shape[0]
imageWidth = image.shape[1]
imageDepth = image.shape[2]

Sx = math.floor(imageWidth / 2) # image center X coord
Sy = math.floor(imageHeight / 2) # image center Y coord

radius = math.floor((imageHeight - 1) / 2.0) # image circle radius

imageCircle = np.zeros([imageHeight, imageWidth], dtype = np.uint8)
print("Creating circle image from source image...")

for i in range(imageWidth):
    for j in range(imageHeight):
        d = math.sqrt(pow((i - Sx),2) + pow((j - Sy),2))
        if d <= radius:
            imageCircle[j,i] = imageGray[j,i]


# PARAMETRY TOMOGRAFU
numberOfEmitters = 75 # liczba nieparzysta >= 3
spaceBetweenEmitters = 1 # odstęp kątowy pomiędzy emiterami, w stopniach
emittersRotationStep = 1 # krok obrotu emiterów, w stopniach


halfNumberOfEmitters = math.floor(numberOfEmitters / 2)
emittersAngularSpread = (numberOfEmitters - 1) * spaceBetweenEmitters # rozpiętość kątowa emiterów


currentAngleOfMiddleEmitter = 0 # początkowy kąt ustawienia centralnego emitera, w stopniach
rotationDegreesPassed = 0
detectorValuesAll = {}
emiterDetectorSectionsAll = set()
emitterDetectorSectionCurrent = (0, 0, 0, 0, 0) # (Ax, Ay, Bx, By, DetectorValue)

print("Examinaiton of circle image started. Emitter rotation in progress...")

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

    
    detectorValuesCurrent = np.zeros(numberOfEmitters, dtype = np.int32) # lista zmierzonych wartości dla detektorów

    tempSection = calculateDiameterSection(currentAngleOfMiddleEmitter)
    mx1 = tempSection[0]
    my1 = tempSection[1]
    mx2 = tempSection[2]
    my2 = tempSection[3]
    normalizedValue = bresenhamLineValue(mx1, my1, mx2, my2)
    detectorValuesCurrent[halfNumberOfEmitters] = normalizedValue # wartość dla centralnego emitera
    emitterDetectorSectionCurrent = (mx1, my1, mx2, my2, normalizedValue)
    emiterDetectorSectionsAll.add(emitterDetectorSectionCurrent)

    for i in range(halfNumberOfEmitters):
        # emitery boczne lewe
        lx1 = leftSideBeamCoordsA[i][0]
        ly1 = leftSideBeamCoordsA[i][1]
        lx2 = leftSideBeamCoordsB[i][0]
        ly2 = leftSideBeamCoordsB[i][1]
        normalizedValue = bresenhamLineValue(lx1, ly1, lx2, ly2)
        detectorValuesCurrent[halfNumberOfEmitters - 1 - i] = normalizedValue
        emitterDetectorSectionCurrent = (lx1, ly1, lx2, ly2, normalizedValue)
        emiterDetectorSectionsAll.add(emitterDetectorSectionCurrent)
    for i in range(halfNumberOfEmitters):
        # emitery boczne prawe
        rx1 = rightSideBeamCoordsA[i][0]
        ry1 = rightSideBeamCoordsA[i][1]
        rx2 = rightSideBeamCoordsB[i][0]
        ry2 = rightSideBeamCoordsB[i][1]
        normalizedValue = bresenhamLineValue(rx1, ry1, rx2, ry2)
        detectorValuesCurrent[halfNumberOfEmitters + 1 + i] = normalizedValue
        emitterDetectorSectionCurrent = (rx1, ry1, rx2, ry2, normalizedValue)
        emiterDetectorSectionsAll.add(emitterDetectorSectionCurrent)

    detectorValuesAll[currentAngleOfMiddleEmitter] = detectorValuesCurrent
    
    currentAngleOfMiddleEmitter += emittersRotationStep
    if currentAngleOfMiddleEmitter > 360:
        currentAngleOfMiddleEmitter = currentAngleOfMiddleEmitter - 360

    rotationDegreesPassed += emittersRotationStep

    if rotationDegreesPassed >= 180:
        break

'''
# Wypisz kąty skanowania i wartości uzyskane na detektorach
print("Angle of emitters arrangement and values measured by detectors:")
for key, value in detectorValuesAll.items():
    print(str(key) + "\t" + str(value))
'''

print("Creating sinogram...")

# Utwórz sinogram
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(16, 5))
ax1.set_title("Original image")
ax1.imshow(imageCircle, cmap='gray', aspect='auto')
imageSinogram = np.zeros((numberOfEmitters, 181), dtype='float')
for key, value in detectorValuesAll.items():
    for n in range(numberOfEmitters):
        imageSinogram[n, key] = value[n]
ax2.set_title("Sinogram")
ax2.set_ylim([0, numberOfEmitters])
ax2.set_xlabel("Projection angle (deg)")
ax2.set_ylabel("Detector number")
ax2.imshow(imageSinogram, cmap='gray', aspect='auto')


print("Generating reconstructed image based on sinogram data...")

# Transformacja odwrotna
imageReconstructed = np.zeros((imageHeight, imageWidth), dtype=np.int32)
pixelOverlapping = np.zeros((imageHeight, imageWidth), dtype=np.int32)
for elem in emiterDetectorSectionsAll:
    Ax = elem[0]
    Ay = elem[1]
    Bx = elem[2]
    By = elem[3]
    grayValue = elem[4]
    bresenhamLineDraw(Ax, Ay, Bx, By, grayValue)    
normalizeimageReconstructed()

print("Ready!")

ax3.set_title("Recreated image")
cv2.imwrite('abc.jpg',imageReconstructed)
img = cv2.imread('abc.jpg',0)
blur = cv2.blur(img,(3,3))
equ = cv2.equalizeHist(blur)
clahe = cv2.createCLAHE(clipLimit=2.0,tileGridSize=(8,8))
cl1 = clahe.apply(equ)
ax3.imshow(cl1, cmap='gray', aspect='auto')
plt.show()