#!/usr/bin/python
import cv2
import math
import numpy as np
np.seterr(over='ignore')

image = cv2.imread("przyklad1.png")

imageHeight = image.shape[0]
#imageWidth = image.shape[1] # obraz kwadratowy
imageWidth = imageHeight
imageDepth = image.shape[2]

imageCenterX = math.floor(imageWidth / 2)
imageCenterY = imageCenterX

imageCircleRadius = math.floor(imageHeight / 2) - 1

imageCircle = np.zeros([imageHeight,imageWidth], dtype = np.int32)

for i in range(imageWidth):
    for j in range(imageHeight):
        d = math.sqrt(pow((i - imageCenterX),2) + pow((j - imageCenterY),2))
        if d <= imageCircleRadius:
            tavg = math.floor(((image[j,i,0] + image[j,i,1] + image[j,i,2]) / 3))
            imageCircle[j,i] = tavg

numberOfEmitters = 9 # liczba nieparzysta
halfNumberOfEmitters = math.floor(numberOfEmitters / 2)
spaceBetweenEmitters = 5
numberOfSpaces = numberOfEmitters - 1
emitterOverallWidth = numberOfSpaces * spaceBetweenEmitters + numberOfEmitters
halfOfOverall = math.floor(emitterOverallWidth / 2)

detectorValues = np.zeros(numberOfEmitters + 1, dtype = np.int16)
angleOfEmitters = 0
currentCoordX = imageCenterX - halfOfOverall
for i in range(numberOfEmitters):
    currentCoordX = currentCoordX + spaceBetweenEmitters + 1
    normCount = 0
    for j in range(imageHeight):
        d = math.sqrt(pow((currentCoordX - imageCenterX),2) + pow((j - imageCenterY),2))
        if d <= imageCircleRadius:
            detectorValues[i] += imageCircle[j,currentCoordX]
            normCount += 1
    detectorValues[i] = math.floor(detectorValues[i] / normCount)
detectorValues[numberOfEmitters] = angleOfEmitters
detectorValuesSaved = detectorValues

detectorValues = np.zeros(numberOfEmitters + 1, dtype = np.int16)
angleOfEmitters = 90
currentCoordY = imageCenterY - halfOfOverall
for i in range(numberOfEmitters):
    currentCoordY = currentCoordY + spaceBetweenEmitters + 1
    normCount = 0
    for j in range(imageWidth):
        d = math.sqrt(pow((j - imageCenterX),2) + pow((currentCoordY - imageCenterY),2))
        if d <= imageCircleRadius:
            detectorValues[i] += imageCircle[currentCoordY,j]
            normCount += 1
    detectorValues[i] = math.floor(detectorValues[i] / normCount)
detectorValues[numberOfEmitters] = angleOfEmitters
detectorValuesSaved = np.vstack([detectorValuesSaved, detectorValues])


print("Image shape (height, width, color): ", image.shape, "\n")
print("Detector normalized values (last value is angle):\n", detectorValuesSaved)