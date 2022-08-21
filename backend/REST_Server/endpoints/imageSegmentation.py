# Libs
import fastapi
from fastapi import APIRouter, UploadFile, File, Depends, Response, BackgroundTasks
from fastapi.encoders import jsonable_encoder
from starlette.status import HTTP_200_OK
from ImageSegmentation.Predictor import Predictor
from sqlalchemy.orm import Session
import random, string, json, os, shutil
from datetime import datetime

# Program
from REST_Server.database import crud, database
from REST_Server.models import pydanticSchemas as schemas
from REST_Server.evaluation import metrics
from REST_Server import config
from Data.COCO_JSON import cocoHandler
from ImageSegmentation.imageSegmentationInterface import imageSegmentationInterface

#--------- Script / Constants ---------
_imageSegmentation: imageSegmentationInterface = None

retrainTriggerNumber = 5 #After x Corrections the Retraining of the Model beginns
retrainBatchSize = 5

supportedExtensions = [".jpg",".JPG",".png",".PNG"]

responses = {
    415: {"detail": "Item not found"},
    406: {"detail":"Something went wrong"}
}

# APIRouter creates path operations for item module
router = APIRouter(
    prefix="/ImageSegmentation",
    tags=["Image Segmentation"],
)

#--------- Functions ---------
def getImageSegmentation() -> imageSegmentationInterface:
    global _imageSegmentation
    if _imageSegmentation == None:
        _imageSegmentation = Predictor()
    return _imageSegmentation

def getSavePath():
    return config.saveDirectory

def generateUniqueToken(db: Session):
    length = 64
    code = ''.join(random.choices(string.ascii_uppercase, k=length))
    # unique in database check
    while (crud.readToken(db=db, token=code) is not None):
        code = ''.join(random.choices(string.ascii_uppercase, k=length))
    return code

def generateUniqueImageName(db: Session):
    length = 64
    name = ''.join(random.choices(string.ascii_uppercase, k=length))
    # unique in database check
    while (crud.readImageName(db=db, name=name) is not None):
         name = ''.join(random.choices(string.ascii_uppercase, k=length))
    return name

async def backgroundCheckTriggerRetrain(db: Session, imageSegmentation: imageSegmentationInterface):
    numberOfCorrections = crud.readHighestIDinCorrectiontable(db=db)
    CorrectionsUntilRetrain = numberOfCorrections % retrainTriggerNumber
    if CorrectionsUntilRetrain == 0:
        print("start Retrain")
        trainPaths = crud.readLatestImagePathsWithCorrectionPaths(db=db,maxPaths=retrainBatchSize)
        trainImagePaths = trainPaths["imagePaths"]
        trainCocoJsonPaths = trainPaths["correctionPaths"]
        retrainInfo = imageSegmentation.retrain(trainImagePaths, trainCocoJsonPaths)
        crud.createNewModelVersion(db, retrainInfo["versionName"], retrainInfo["history"])
        print("end Retrain")


# Define Routes
@router.get("/getCategories", response_model=schemas.cocoCategoriesReturnSchema)
async def get_Categories(imageSegmentation: imageSegmentationInterface=Depends(getImageSegmentation)):
    return imageSegmentation.getCategories()

@router.post("/uploadImage", response_model=schemas.segmentationReturnSchema, responses={415: responses[415]})
async def upload_Image_for_Segmentation(file: UploadFile = File(...),
                                        db: Session=Depends(database.getDatabase),
                                        savePath: str=Depends(getSavePath), 
                                        imageSegmentation: imageSegmentationInterface=Depends(getImageSegmentation)):
    jobData = schemas.segmentationJobSchema
    
    imageName = generateUniqueImageName(db=db)
    jobData.imageName = imageName

    fileExtension = os.path.splitext(file.filename)[-1]
    if (fileExtension not in supportedExtensions):
        raise fastapi.HTTPException(status_code=415, detail=responses[415]["detail"])

    imagePath = savePath + "images/" + imageName + fileExtension
    jobData.imagePath = imagePath

    #Save Image local
    with open(imagePath, "wb") as outfile:
        shutil.copyfileobj(file.file, outfile)

    token = generateUniqueToken(db=db)
    jobData.token = token

    jobData.status = "open"

    #Prediction
    jobData.tsStartSegmentation = datetime.now()
    result = imageSegmentation.predict(imagePath)
    jobData.tsEndSegmentation = datetime.now()
    jobData.modelVersion = result["info"]["ModelVersion"]

    jsonPath = savePath + "jsonPredictions/"+ imageName + ".json"
    jobData.jsonPredictedPath = jsonPath

    #Save JSON Prediction
    with open(jsonPath, "w") as outfile:
        json.dump(result, outfile)

    #Save data in database
    crud.createSegmentationJob(db, jobData)
    
    return {"cocoJSON": result, "token": token}


@router.post("/uploadCorrection", responses={406: responses[406]})
async def upload_Correction(correctionInput: schemas.correctionInputSchema,
                            background_tasks: BackgroundTasks,
                            db: Session=Depends(database.getDatabase), 
                            savePath: str=Depends(getSavePath), 
                            imageSegmentation: imageSegmentationInterface=Depends(getImageSegmentation)):
    #check valid token
    tokenRow = crud.readToken(db=db, token=correctionInput.token)
    if tokenRow == None:
        raise fastapi.HTTPException(status_code=406, detail=responses[406]["detail"])

    jobData = schemas.correctionJobSchema

    jobData.tsCorrectionReceived = datetime.now()

    imageName = crud.readImageNamefromToken(db=db, token=correctionInput.token)
    jsonPath = savePath + "jsonCorrections/"+ imageName + ".json"
    jobData.correctionPath = jsonPath

    #save JSON Correction
    encodedCocoJson = jsonable_encoder(correctionInput.cocoJSON)
    with open(jsonPath, "w") as outfile:
        json.dump(encodedCocoJson, outfile)

    #calculate metrics
    cocoCategories = imageSegmentation.getCategories()
    categoireDict = cocoHandler.getCategorieDictFromCocoJsonCategories(cocoCategories)
    predJsonPath = crud.readJsonPredictedPathFromToken(db=db, token=correctionInput.token)
    widthImage,heightImage = cocoHandler.getWidthAndHeightFromCocoJsonPath(predJsonPath)
    predPolysDict = cocoHandler.getPolygonsDictFromCocoJsonPath(predJsonPath, cocoCategories)
    truthPolysDict = cocoHandler.getPolygonsDictFromCocoJsonPath(jsonPath, cocoCategories)

    iou = {}
    dice = {}
    pixelAcc = {}
    for catId, cat in categoireDict.items():
        predPolygons = predPolysDict[catId]
        truthPolygons = truthPolysDict[catId]
        metricsDict = metrics.calculateMetricsFromPolygons(predPolygons, truthPolygons, widthImage, heightImage)
        pixelAcc[cat] = float(metricsDict["PixelAcc"])
        iou[cat] = float(metricsDict["IoU"])
        dice[cat] = float(metricsDict["DiceCoef"])

    jobData.pixelAccuracy = pixelAcc
    jobData.IoU = iou
    jobData.diceCoefficient = dice

    if tokenRow.status != "closed":
        #add Backgroundtask which will check retrain after the response
        background_tasks.add_task(backgroundCheckTriggerRetrain, db,imageSegmentation)

        #Save data in database
        crud.createCorrectionForSegmentation(db=db, correction=correctionInput, jobData=jobData)
        crud.updateTokenStatus(db=db, token=correctionInput.token, status="closed")
    else:
        crud.updateMetrics(db=db, jobData=jobData)

    return Response(status_code=HTTP_200_OK)

@router.post("/uploadNoCorrection", responses={406: responses[406]})
async def upload_No_Correction(noCorrectionInput: schemas.noCorrectionInputSchema, db: Session=Depends(database.getDatabase)):
    #check valid token
    tokenRow = crud.readToken(db=db, token=noCorrectionInput.token)
    if tokenRow == None:
        raise fastapi.HTTPException(status_code=406, detail=responses[406]["detail"])

    crud.updateTokenStatus(db=db, token=noCorrectionInput.token, status="exit")
    return Response(status_code=HTTP_200_OK)