#!/usr/bin/python
import cv2
import math
import numpy as np
np.seterr(over='ignore')

image = cv2.imread("przyklad1.png")

imageHeight = image.shape[0]
#imageWidth = image.shape[1]
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

numberOfEmitters = 5 # liczba nieparzysta
halfNumberOfEmitters = math.floor(numberOfEmitters / 2)
detectorValues = np.zeros(numberOfEmitters, dtype = np.int32)
angleOfEmitters = 0 # {0; 90; 180; 270}
spaceBetweenEmitters = 1
numberOfSpaces = numberOfEmitters - 1
emitterOverallWidth = numberOfSpaces * spaceBetweenEmitters + numberOfEmitters
halfOfOverall = math.floor(emitterOverallWidth / 2)

if angleOfEmitters == 0 or angleOfEmitters == 180:
    currentCoordX = imageCenterX - halfOfOverall
    for i in range(numberOfEmitters):
        currentCoordX = currentCoordX + spaceBetweenEmitters + 1
        for j in range(imageHeight):
            d = math.sqrt(pow((currentCoordX - imageCenterX),2) + pow((j - imageCenterY),2))
            if d <= imageCircleRadius:
                detectorValues[i] += imageCircle[j,i]
        detectorValues[i] = math.floor(detectorValues[i] / imageHeight)
elif angleOfEmitters == 90 or angleOfEmitters == 270:
    currentCoordY = imageCenterY - halfOfOverall
    for i in range(numberOfEmitters):
        currentCoordY = currentCoordY + spaceBetweenEmitters + 1
        for j in range(imageWidth):
            d = math.sqrt(pow((currentCoordX - imageCenterX),2) + pow((j - imageCenterY),2))
            if d <= imageCircleRadius:
                detectorValues[i] += imageCircle[u,j]
        detectorValues[i] = math.floor(detectorValues[i] / imageHeight)



print('Image original shape', image.shape)
print('Image circle shape:', imageCircle.shape)
print('Detector normalized values:', detectorValues)