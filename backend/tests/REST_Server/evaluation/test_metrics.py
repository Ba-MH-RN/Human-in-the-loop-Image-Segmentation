#imports from other directory
import sys, os
sys.path.append(os.path.abspath(os.path.join('..', 'backend')))
from REST_Server.evaluation.metrics import *
from PIL import Image
from numpy import asarray
import numpy as np

def test_calculate_max_IoU_correct():
    trueImage = Image.new("1", (128,128), "white")
    trueImage = asarray(trueImage).astype(np.float16).reshape(1,128,128,1)
    iou = calculateIoU(trueImage,trueImage)
    assert iou == 1

def test_calculate_min_IoU_correct():
    trueImage = Image.new("1", (128,128), "white")
    falseImage = Image.new("1", (128,128), "black")
    trueImage = asarray(trueImage).astype(np.float16).reshape(1,128,128,1)
    falseImage = asarray(falseImage).astype(np.float16).reshape(1,128,128,1)
    iou = calculateIoU(trueImage,falseImage)
    assert -0.01 < iou < 0.01

def test_calculate_max_Dice_Coefficent_correct():
    trueImage = Image.new("1", (128,128), "white")
    trueImage = asarray(trueImage).astype(np.float16).reshape(1,128,128,1)
    dice = calculateDiceCoef(trueImage,trueImage)
    assert dice == 1

def test_calculate_min_Dice_Coefficent_correct():
    trueImage = Image.new("1", (128,128), "white")
    falseImage = Image.new("1", (128,128), "black")
    trueImage = asarray(trueImage).astype(np.float16).reshape(1,128,128,1)
    falseImage = asarray(falseImage).astype(np.float16).reshape(1,128,128,1)
    dice = calculateDiceCoef(trueImage,falseImage)
    assert -0.01 < dice < 0.01

def test_calculate_max_Pixel_Accuracy_correct():
    trueImage = Image.new("1", (128,128), "white")
    trueImage = asarray(trueImage).astype(np.float16).reshape(1,128,128,1)
    pixelAcc = calculatePixelAccuracy(trueImage,trueImage)
    assert pixelAcc == 1

def test_calculate_min_Pixel_Accuracy_correct():
    trueImage = Image.new("1", (128,128), "white")
    falseImage = Image.new("1", (128,128), "black")
    trueImage = asarray(trueImage).astype(np.float16).reshape(1,128,128,1)
    falseImage = asarray(falseImage).astype(np.float16).reshape(1,128,128,1)
    pixelAcc = calculatePixelAccuracy(trueImage,falseImage)
    assert -0.01 < pixelAcc < 0.01

def test_convert_Image_To_NdNumpy_Array_shape_correct():
    shape = (1,128,128,1)
    image = Image.new("1", (128,128), "white")
    array = convertImageToNdNumpyArray(image)
    assert shape == array.shape

def test_convert_Polygons_To_Image_type_correct():
    polygons = [[0,0,10,0,10,10,0,0],[0,0,0,10,10,10,0,0]]
    image =convertPolygonsToImage(polygons,128,128)
    assert type(image) == Image.Image

def test_calculate_Metrics_From_Polygons_max_correct():
    polygons = [[0,0,10,0,10,10,0,0],[0,0,0,10,10,10,0,0]]
    metrics = calculateMetricsFromPolygons(polygons,polygons,128,128)
    assert metrics["IoU"] == 1
    assert metrics["DiceCoef"] == 1

def test_calculate_Metrics_From_Polygons_min_correct():
    polygonsPred = [[0,0,0,10,10,10,0,0]]
    polygonsTrue = [[100,100,50,100,50,50,100,100]]
    metrics = calculateMetricsFromPolygons(polygonsPred,polygonsTrue,128,128)
    assert -0.01 < metrics["IoU"] < 0.01
    assert -0.01 < metrics["DiceCoef"] < 0.01


def test_calculate_Metrics_From_complex_Polygons_between_range_correct():
    polygonsPred = [[2, 9, 0, 190, 263, 190, 263, 0, 17, 0, 2, 9]]
    polygonsTrue = [[100,100,50,100,50,50,100,100]]
    metrics = calculateMetricsFromPolygons(polygonsPred,polygonsTrue,191,265)
    assert 0.01 < metrics["IoU"] < 0.99
    assert 0.01 < metrics["DiceCoef"] < 0.99
