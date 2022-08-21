#imports from other directory
import sys, os 
sys.path.append(os.path.abspath(os.path.join('..', 'backend')))
from PIL import Image
import numpy as np
from ImageSegmentation.modelControl.retrainer import retrainer
from ImageSegmentation.processing.preprocess import preprocess
from ImageSegmentation.modelControl.ModelVersionControl import ModelVersionControl
from Data.COCO_JSON.cocoParser import cocoParser
from Data.COCO_JSON import cocoHandler

def test_convert_Polygons_Dict_to_GroundTruthImage_correct_dimensions():
    polysDict = {0:[[147, 51, 97, 54, 93, 81, 83, 91, 87, 151, 77, 152, 120, 172, 157, 169, 199, 145, 251, 134, 209, 113, 199, 100, 170, 104, 155, 96, 147, 51],[10,10,100,10,100,100,10,100,10,10]],
                1:[[20,20,90,20,90,90,20,90,20,20]]}
    heightImage =  191
    widthImage = 265
    gtImageDict = retrainer.convertPolygonsDictToGroundTruthImageDict(polysDict,widthImage,heightImage)
    assert gtImageDict[0].height == heightImage
    assert gtImageDict[0].width == widthImage

def test_convert_Images_to_X_correct_diemensions_type():
    modelDirectory = "tests/Data/tests/models/"
    baselineModelPath = "tests/ImageSegmentation/baselineModels/catModel.h5"
    modelVSC = ModelVersionControl(modelDirectory=modelDirectory, baselineModelPath=baselineModelPath)
    model = modelVSC.getCurrentModel()
    config = model.get_config()
    modelInputShape = config["layers"][0]["config"]["batch_input_shape"]

    images = 5
    imagePath = "tests/Data/tests/testImages/testCat.jpg"
    
    imagePaths = []
    for i in range(images):
        image = preprocess.loadImageFromPath(imagePath)
        scaledImage = preprocess.scaleImage(image,modelInputShape[1],modelInputShape[2])
        imagePaths.append(scaledImage)
    X_train = retrainer.convertImagesToX(imagePaths)
    assert X_train.shape == (images,modelInputShape[1],modelInputShape[2],modelInputShape[3])
    assert X_train.dtype == np.uint8

def test_convert_Images_to_Y_correct_diemensions():
    modelDirectory = "tests/Data/tests/models/"
    baselineModelPath = "tests/ImageSegmentation/baselineModels/catModel.h5"
    coco = cocoParser(categories=[{'id': 0, 'name': 'cat'}])
    modelVSC = ModelVersionControl(modelDirectory=modelDirectory, baselineModelPath=baselineModelPath)
    model = modelVSC.getCurrentModel()
    config = model.get_config()
    modelInputShape = config["layers"][0]["config"]["batch_input_shape"]

    jsons = 5
    jsonPath = "tests/Data/tests/testCorrection/testCOCO.json"
    jsonPaths = []
    for i in range(jsons):
        jsonPaths.append(jsonPath)

    Y_train_imageDicts = []
    for jsonPath in jsonPaths:
        polysDict = cocoHandler.getPolygonsDictFromCocoJsonPath(jsonPath,coco.getCategories())
        imageSize = cocoHandler.getWidthAndHeightFromCocoJsonPath(jsonPath)
        scaledPolygons = retrainer.scalePolygonsToModelInput(polysDict,imageSize[0],imageSize[1],modelInputShape[1],modelInputShape[2])
        gtImageDict = retrainer.convertPolygonsDictToGroundTruthImageDict(scaledPolygons,modelInputShape[1],modelInputShape[2])
        Y_train_imageDicts.append(gtImageDict)
    Y_train = retrainer.convertImageDictsToY(Y_train_imageDicts)

    assert Y_train.shape == (jsons,modelInputShape[1],modelInputShape[2],1)
    assert Y_train.dtype == bool

def test_retrain_Model_successful():
    modelDirectory = "tests/Data/tests/models/"
    baselineModelPath = "tests/ImageSegmentation/baselineModels/catModel.h5"
    coco = cocoParser(categories=[{'id': 0, 'name': 'cat'}])
    modelVSC = ModelVersionControl(modelDirectory=modelDirectory, baselineModelPath=baselineModelPath)
    model = modelVSC.getCurrentModel()
    config = model.get_config()
    modelInputShape = config["layers"][0]["config"]["batch_input_shape"]

    imagePath = "tests/Data/tests/testImages/testCat.jpg"
    jsonPath = "tests/Data/tests/testCorrection/testCOCO.json"
    imagePaths = []
    jsonPaths = []
    for i in range(5):
        imagePaths.append(imagePath)
        jsonPaths.append(jsonPath)

    X_train_images = []
    for imagePath in imagePaths:
        image = preprocess.loadImageFromPath(imagePath)
        scaledImage = preprocess.scaleImage(image,modelInputShape[1],modelInputShape[2])
        X_train_images.append(scaledImage)
    X_train = retrainer.convertImagesToX(X_train_images)

    Y_train_imageDicts = []
    for jsonPath in jsonPaths:
        polysDict = cocoHandler.getPolygonsDictFromCocoJsonPath(jsonPath,coco.getCategories())
        imageSize = cocoHandler.getWidthAndHeightFromCocoJsonPath(jsonPath)
        scaledPolygons = retrainer.scalePolygonsToModelInput(polysDict,imageSize[0],imageSize[1],modelInputShape[1],modelInputShape[2])
        gtImageDict = retrainer.convertPolygonsDictToGroundTruthImageDict(scaledPolygons,modelInputShape[1],modelInputShape[2])
        Y_train_imageDicts.append(gtImageDict)
    Y_train = retrainer.convertImageDictsToY(Y_train_imageDicts)

    model = modelVSC.getCurrentModel()
    newModel = retrainer.retrainModel(model,X_train,Y_train)
    assert newModel is not None

def test_convert_ImageDicts_To_Y_with_2_categories_correct():
    modelInputShape = (2,128,128,2)

    trueImage = Image.new("1", (128,128), "white")
    falseImage = Image.new("1", (128,128), "black")
    #two Images with two categories
    imageDicts = [{0:trueImage, 1:falseImage},
                    {0:falseImage, 1:trueImage}]

    Y_train = retrainer.convertImageDictsToY(imageDicts)
    assert Y_train.shape == modelInputShape
    assert Y_train[0,0,0,0] == True
    assert Y_train[0,0,0,1] == False
    assert Y_train[1,0,0,0] == False
    assert Y_train[1,0,0,1] == True