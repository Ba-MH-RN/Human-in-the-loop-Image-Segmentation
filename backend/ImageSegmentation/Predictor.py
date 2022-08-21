import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' #disable debugging infos from tensorflow
import numpy as np
import json
from ImageSegmentation.imageSegmentationInterface import imageSegmentationInterface
from ImageSegmentation.processing.preprocess import preprocess
from ImageSegmentation.modelControl.ModelVersionControl import ModelVersionControl
from ImageSegmentation.processing.postprocess import postprocess
from Data.COCO_JSON.cocoParser import cocoParser
from Data.COCO_JSON import cocoHandler
from ImageSegmentation.modelControl.retrainer import retrainer

class Predictor(imageSegmentationInterface):
    modelDirectory : str
    baselineModelPath : str
    modelVC : ModelVersionControl
    modelInputShape:tuple #typical example: (None, 256, 128, 3)
    modelOutputShape:tuple
    coco:cocoParser

    def __init__(self, configPath:str = None) -> None:
        if configPath is None:
            config = json.load(open('ImageSegmentation/config.json'))
        else:
            config = json.load(open(configPath))
        self.coco = cocoParser(categories= config["annotations"])
        self.modelVC = ModelVersionControl(modelDirectory=config["modelDirectory"], baselineModelPath=config["baselineModelPath"])
        model = self.modelVC.getCurrentModel()
        self.modelInputShape = model.layers[0].input_shape[0]
        self.modelOutputShape = model.layers[-1].output_shape

    def predict(self, imagePath: str) -> dict:
        image = preprocess.loadImageFromPath(imagePath)
        self.coco.width = image.width
        self.coco.height = image.height
        scaledImage = preprocess.scaleImage(image,self.modelInputShape[1],self.modelInputShape[2])

        model = self.modelVC.getCurrentModel()
        self.coco.modelVersion = self.modelVC.getCurrentModelVersionName()
        prediction = model.predict(np.asarray(scaledImage).reshape(1,self.modelInputShape[1],self.modelInputShape[2],self.modelInputShape[3]), verbose=0)

        prediction = np.asarray(prediction.reshape(self.modelOutputShape[1],self.modelOutputShape[2],self.modelOutputShape[3]))

        polysDict = {}
        for i in range(self.modelOutputShape[3]):
            area = postprocess.probabilityAreaToDiscreteArea(prediction[:,:,i], 0.6)
            polygons = postprocess.DiscreteAreaToPolygons(area)
            polygons = postprocess.filterInvalidPolygons(polygons)
            polygons = postprocess.filterPolygonsInsideOtherPolygons(polygons)
            scaledPolygons = postprocess.scalePolygonsToImageCoordinate(polygons,self.modelOutputShape[1],self.modelOutputShape[2],self.coco.width,self.coco.height)
            polysDict[i] = scaledPolygons
        self.coco.polygonsDict = polysDict

        cocoJSON = self.coco.generateCocoJSON()

        return cocoJSON


    def retrain(self, trainImagePaths:list, trainCocoJsonPaths:list) -> dict:
        if(len(trainImagePaths) != len (trainCocoJsonPaths)):
            return None

        X_train_images = []
        for imagePath in trainImagePaths:
            image = preprocess.loadImageFromPath(imagePath)
            scaledImage = preprocess.scaleImage(image,self.modelInputShape[1],self.modelInputShape[2])
            X_train_images.append(scaledImage)
        X_train = retrainer.convertImagesToX(X_train_images)

        Y_train_imageDicts = []
        for jsonPath in trainCocoJsonPaths:
            polysDict = cocoHandler.getPolygonsDictFromCocoJsonPath(jsonPath,self.getCategories())
            imageSize = cocoHandler.getWidthAndHeightFromCocoJsonPath(jsonPath)
            scaledPolygons = retrainer.scalePolygonsToModelInput(polysDict,imageSize[0],imageSize[1],self.modelInputShape[1],self.modelInputShape[2])
            gtImageDict = retrainer.convertPolygonsDictToGroundTruthImageDict(scaledPolygons,self.modelInputShape[1],self.modelInputShape[2])
            Y_train_imageDicts.append(gtImageDict)
        Y_train = retrainer.convertImageDictsToY(Y_train_imageDicts)

        model = self.modelVC.getCurrentModel()
        history = retrainer.retrainModel(model,X_train,Y_train)

        self.modelVC.updateModel(model)
        return {"versionName": self.modelVC.getCurrentModelVersionName(), "history": history}
    
    
    def getCategories(self) -> dict:
        return self.coco.getCategories()