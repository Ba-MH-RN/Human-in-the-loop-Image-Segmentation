from REST_Server.database import crud
from REST_Server.models import pydanticSchemas as schemas
from tests.REST_Server.database.dummyDatabase import *
from datetime import datetime
import collections
import pandas as pd

def segmentationJobSchemaDummy():
    jobData = schemas.segmentationJobSchema
    jobData.imageName = "path"
    jobData.imagePath = "path"
    jobData.jsonPredictedPath = "path"
    jobData.modelVersion = "0"
    jobData.tsStartSegmentation = datetime.now()
    jobData.tsEndSegmentation = datetime.now()
    jobData.token = "token"
    jobData.status = "test"
    return jobData

def correctionJobSchemaDummy():
    jobData = schemas.correctionJobSchema
    jobData.correctionPath = "path"
    jobData.tsCorrectionReceived = datetime.now()
    jobData.pixelAccuracy = 0.0
    jobData.IoU = 0.0
    jobData.diceCoefficient = 0.0
    return jobData

def correctionInputSchemaDummy():
    correction = schemas.correctionInputSchema
    correction.cocoJSON = {"annotations":"poly"}
    correction.token = "token"
    return correction


def test_generate_read_false_token(db_session):
    token = crud.readToken(db_session, "NOTEXISTINGTOKEN")
    assert token is None

def test_read_false_imagename(db_session):
    name = crud.readImageName(db_session, "NOTEXISTINGTOKEN")
    assert name is None

def test_create_segmentation_job_successful(db_session):
    jobData = segmentationJobSchemaDummy()
    success = crud.createSegmentationJob(db_session, jobData)
    assert success == True

def test_check_imagename_collision(db_session):
    jobData = segmentationJobSchemaDummy()
    crud.createSegmentationJob(db_session, jobData)
    name = crud.readImageName(db_session, "path")
    assert name is not None

def test_check_token_collision(db_session):
    jobData = segmentationJobSchemaDummy()
    crud.createSegmentationJob(db_session, jobData)
    name = crud.readToken(db_session, "token")
    assert name is not None

def test_update_Token_Status_successful(db_session):
    jobData = segmentationJobSchemaDummy()
    crud.createSegmentationJob(db_session, jobData)
    success = crud.updateTokenStatus(db_session, jobData.token, "new Status")
    assert success == True

def test_update_Token_Status_with_false_token(db_session):
    jobData = segmentationJobSchemaDummy()
    crud.createSegmentationJob(db_session, jobData)
    success = crud.updateTokenStatus(db_session, "false Token", "new Status")
    assert success == False

def test_update_Metrics_successful(db_session):
    segJobData = segmentationJobSchemaDummy()
    segJobData.token = "token"
    crud.createSegmentationJob(db_session, segJobData)

    corJobData = correctionJobSchemaDummy()

    correction = schemas.correctionInputSchema
    correction.token = segJobData.token
    crud.createCorrectionForSegmentation(db_session,correction,corJobData)

    corJobData.IoU = 1.0
    success = crud.updateMetrics(db_session,corJobData)
    assert success == True

def test_read_imagename_from_token_successful(db_session):
    jobData = segmentationJobSchemaDummy()
    crud.createSegmentationJob(db_session, jobData)
    name = crud.readImageNamefromToken(db_session,jobData.token)
    assert name == jobData.imageName

def test_read_json_predicted_path_from_token_successful(db_session):
    jobData = segmentationJobSchemaDummy()
    crud.createSegmentationJob(db_session, jobData)
    name = crud.readJsonPredictedPathFromToken(db_session,jobData.token)
    assert name == jobData.jsonPredictedPath

def test_read_Metrics_returns_Columns_correct(db_session):
    metrics = crud.readMetrics(db_session)
    df = pd.DataFrame.from_records(metrics, columns=["tsCorrectionReceived","pixelAccuracy","IoU","diceCoefficient"])
    assert df is not None

def test_read_Meta_Segmentation_returns_Columns_correct(db_session):
    metrics = crud.readMetaSegmentation(db_session)
    df = pd.DataFrame.from_records(metrics, columns=["tsStartSegmentation", "tsEndSegmentation"])
    assert df is not None

def test_read_Meta_Corrections_returns_Columns_correct(db_session):
    metrics = crud.readMetaCorrections(db_session)
    df = pd.DataFrame.from_records(metrics, columns=["modelVersion","IoU"])
    assert df is not None

def test_read_Meta_Modeltable_returns_Columns_correct(db_session):
    metrics = crud.readMetaSegmentation(db_session)
    df = pd.DataFrame.from_records(metrics, columns=["versionName", "loss", "accuracy", "val_loss", "val_accuracy"])
    assert df is not None

def test_read_VersionName_From_ModeltableId_correct(db_session):
    modId = crud.readModeltableIdFromVersionName(db_session,"2")
    name = crud.readVersionNameFromModeltableId(db_session,modId)
    assert name == "2"

def test_read_ModeltableId_From_VersionName_correct_generation(db_session):
    modId = crud.readModeltableIdFromVersionName(db_session,"2")
    assert modId == 1

def test_read_ModeltableId_From_VersionName_correct_read(db_session):
    crud.readModeltableIdFromVersionName(db_session,"2")
    modId = crud.readModeltableIdFromVersionName(db_session,"2")
    assert modId == 1

def test_create_correction_for_segmentation_successful(db_session):
    segJobData = segmentationJobSchemaDummy()
    segJobData.token = "token"
    crud.createSegmentationJob(db_session, segJobData)

    corJobData = correctionJobSchemaDummy()

    correction = schemas.correctionInputSchema
    correction.token = segJobData.token
    success = crud.createCorrectionForSegmentation(db_session,correction,corJobData)
    assert success == True

def test_create_correction_for_segmentation_with_false_token(db_session):
    segJobData = segmentationJobSchemaDummy()
    segJobData.token = "token"
    crud.createSegmentationJob(db_session, segJobData)

    corJobData = correctionJobSchemaDummy()

    correction = correctionInputSchemaDummy()
    correction.token = "false token"
    success = crud.createCorrectionForSegmentation(db_session,correction,corJobData)
    assert success == False

def test_read_highest_id_in_correctiontable_correct_number(db_session):
    count = 5
    for i in range(5):
        segJobData = segmentationJobSchemaDummy()
        segJobData.token = "token" + str(i)
        segJobData.imageName="name" + str(i)
        segJobData.imagePath="path" + str(i)
        segJobData.jsonPredictedPath="path" + str(i)
        crud.createSegmentationJob(db_session, segJobData)
        corJobData = correctionJobSchemaDummy()
        corJobData.correctionPath="path" + str(i)
        correction = schemas.correctionInputSchema
        correction.token = segJobData.token
        crud.createCorrectionForSegmentation(db_session,correction,corJobData)
    assert count == crud.readHighestIDinCorrectiontable(db_session)

def test_read_latest_image_paths_with_correction_paths_result_is_inorder(db_session):
    corPaths = []
    imgPaths = []
    #Insert without correction
    jobData = segmentationJobSchemaDummy()
    crud.createSegmentationJob(db_session, jobData)

    #Inserts with corrections
    for i in range(5):
        segJobData = segmentationJobSchemaDummy()
        segJobData.token = "token" + str(i)
        segJobData.imageName="name" + str(i)
        imgPath = "path" + str(i)
        imgPaths.append(imgPath)
        segJobData.imagePath=imgPath
        segJobData.jsonPredictedPath="path" + str(i)
        crud.createSegmentationJob(db_session, segJobData)
        corJobData = correctionJobSchemaDummy()
        corPath = "path" + str(i)
        corPaths.append(corPath)
        corJobData.correctionPath=corPath
        correction = schemas.correctionInputSchema
        correction.token = segJobData.token
        crud.createCorrectionForSegmentation(db_session,correction,corJobData)
    paths = crud.readLatestImagePathsWithCorrectionPaths(db=db_session,maxPaths=5)
    readImPaths = paths["imagePaths"]
    readCorPaths = paths["correctionPaths"]
    assert collections.Counter(imgPaths)==collections.Counter(readImPaths)
    assert collections.Counter(corPaths)==collections.Counter(readCorPaths)

def test_read_latest_image_paths_with_correction_paths_result_returns_latest(db_session):
    corPaths = []
    imgPaths = []
    latest = 5
    #Insert without correction
    jobData = segmentationJobSchemaDummy()
    crud.createSegmentationJob(db_session, jobData)

    #Inserts with corrections
    for i in range(10):
        segJobData = segmentationJobSchemaDummy()
        segJobData.token = "token" + str(i)
        segJobData.imageName="name" + str(i)
        imgPath = "path" + str(i)
        if i>=latest:
            imgPaths.append(imgPath)
        segJobData.imagePath=imgPath
        segJobData.jsonPredictedPath="path" + str(i)
        crud.createSegmentationJob(db_session, segJobData)
        corJobData = correctionJobSchemaDummy()
        corPath = "path" + str(i)
        if i>=latest:
            corPaths.append(corPath)
        corJobData.correctionPath=corPath
        correction = schemas.correctionInputSchema
        correction.token = segJobData.token
        crud.createCorrectionForSegmentation(db_session,correction,corJobData)
    paths = crud.readLatestImagePathsWithCorrectionPaths(db=db_session,maxPaths=latest)
    readImPaths = paths["imagePaths"]
    readCorPaths = paths["correctionPaths"]
    assert collections.Counter(imgPaths)==collections.Counter(readImPaths)
    assert collections.Counter(corPaths)==collections.Counter(readCorPaths)