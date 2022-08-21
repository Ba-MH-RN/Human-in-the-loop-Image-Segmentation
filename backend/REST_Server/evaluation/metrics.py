from PIL import Image, ImageDraw
from sklearn import metrics
from numpy import asarray
import numpy as np

def calculateIoU(y_true, y_pred):
    iou = 0
    for i in range(len(y_pred)):
        y_p = y_pred[i].flatten()
        y_v = y_true[i].flatten()
        iou += metrics.jaccard_score(y_v, y_p, zero_division=0)
    iou = iou / len(y_pred)
    return iou

def calculateDiceCoef(y_true, y_pred):
    dice = 0
    for i in range(len(y_pred)):
        y_p = y_pred[i].flatten()
        y_v = y_true[i].flatten()
        dice += metrics.f1_score(y_v, y_p, zero_division=0)
    dice = dice / len(y_pred)
    return dice

def calculatePixelAccuracy(y_true, y_pred):
    pixelAcc = 0
    for i in range(len(y_pred)):
        y_p = y_pred[i].flatten()
        y_v = y_true[i].flatten()
        pixelAcc += metrics.accuracy_score(y_v, y_p)
    pixelAcc = pixelAcc / len(y_pred)
    return pixelAcc

def convertImageToNdNumpyArray(image:Image)->np.ndarray:
    channel = len(image.split())
    ndArray = asarray(image)
    height, width = ndArray.shape
    shapedNdArray = ndArray.astype(np.float16).reshape(1,height, width, channel)
    return shapedNdArray

def convertPolygonsToImage(polygons:list,widthImage:int,heightImage:int) -> Image:
    image = Image.new("1", (widthImage,heightImage), "black")
    if polygons: #list is not empty
        for polygon in polygons:
            canvas = ImageDraw.Draw(image)
            canvas.polygon(polygon, fill = "white", outline ="white")
    return image

def calculateMetricsFromPolygons(predPolygons:list,truePolygons:list,widthImage:int,heightImage:int)->dict:
    predImage = convertPolygonsToImage(predPolygons, widthImage, heightImage)
    trueImage = convertPolygonsToImage(truePolygons, widthImage, heightImage)

    predArray = convertImageToNdNumpyArray(predImage)
    trueArray = convertImageToNdNumpyArray(trueImage)

    iou = calculateIoU(trueArray,predArray)
    dice = calculateDiceCoef(trueArray,predArray)
    pixelAcc = calculatePixelAccuracy(trueArray,predArray)

    return {"IoU":iou,"DiceCoef":dice, "PixelAcc":pixelAcc}