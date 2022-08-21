# Libs
from sqlalchemy.orm import Session
from sqlalchemy import func 

# Program
from REST_Server.database import tables
from REST_Server.models import pydanticSchemas as schemas



def readToken(db: Session, token: str):
    tokenRow = db.query(tables.Tokentable).filter(
        tables.Tokentable.token == token).first()
    return tokenRow

def readImageName(db: Session, name: str):
    imageRow = db.query(tables.Segmentationtable).filter(
        tables.Segmentationtable.imageName == name).first()
    return imageRow

def readImageNamefromToken(db: Session, token: str):
    tokenRow = readToken(db=db, token=token)
    segID = tokenRow.id_Segmentation
    segRow = db.query(tables.Segmentationtable).get(segID)
    return segRow.imageName

def readJsonPredictedPathFromToken(db: Session, token: str):
    tokenRow = readToken(db=db, token=token)
    segID = tokenRow.id_Segmentation
    segRow = db.query(tables.Segmentationtable).get(segID)
    return segRow.jsonPredictedPath

def readHighestIDinCorrectiontable(db: Session):
    return db.query(func.max(tables.Correctiontable.id)).first()[0]

def readLatestImagePathsWithCorrectionPaths(db: Session, maxPaths: int)->dict:
    seg = tables.Segmentationtable
    cor = tables.Correctiontable
    query = db.query(seg, cor).filter(seg.id_Correction==cor.id).order_by(cor.id.desc()).limit(maxPaths).all()
    imPaths = []
    corPaths = []
    for hit in query:
        imPaths.append(hit[0].imagePath)
        corPaths.append(hit[1].correctionPath)
    paths = {"imagePaths": imPaths, "correctionPaths": corPaths}
    return paths

def readMetrics(db: Session):
    cor = tables.Correctiontable
    metrics = db.query(cor.tsCorrectionReceived, cor.pixelAccuracy, cor.IoU, cor.diceCoefficient).all()
    return metrics

def readMetaSegmentation(db: Session):
    seg = tables.Segmentationtable
    meta = db.query(seg.tsStartSegmentation, seg.tsEndSegmentation).all()
    return meta

def readMetaCorrections(db: Session):
    seg = tables.Segmentationtable
    cor = tables.Correctiontable
    query = db.query(seg, cor).filter(seg.id_Correction==cor.id).all()
    meta = {"modelVersion":[], "IoU":[]}
    for hit in query:
        versionName = readVersionNameFromModeltableId(db, hit[0].id_Model)
        meta["modelVersion"].append(versionName)
        meta["IoU"].append(hit[1].IoU)
    return meta

def readMetaModeltable(db:Session):
    mod = tables.Modeltable
    meta = db.query(mod.versionName, mod.loss, mod.accuracy, mod.val_loss, mod.val_accuracy).all()
    return meta

def readVersionNameFromModeltableId(db:Session, id:int):
    modelRow = db.query(tables.Modeltable).filter(tables.Modeltable.id == id).first()
    return modelRow.versionName

def readModeltableIdFromVersionName(db:Session, vName:str):
    modelRow = db.query(tables.Modeltable).filter(tables.Modeltable.versionName == vName).first()
    if modelRow is not None:
        return modelRow.id
    else: 
        db_mod = tables.Modeltable(
            versionName = vName,
            loss = [],
            accuracy = [],
            val_loss = [],
            val_accuracy = []
        )
        db.add(db_mod)
        db.commit()
        db.refresh(db_mod)
        return db_mod.id

def updateTokenStatus(db: Session, token: str, status: str):
    # valid token check
    tokenRow = readToken(db=db, token=token)
    if tokenRow == None:
        return False
    tokenRow.status = status
    db.commit()
    db.refresh(tokenRow)
    return True

def updateMetrics(db:Session, jobData: schemas.correctionJobSchema):
    corRow = db.query(tables.Correctiontable).filter(tables.Correctiontable.correctionPath == jobData.correctionPath).first()
    corRow.tsCorrectionReceived=jobData.tsCorrectionReceived
    corRow.pixelAccuracy=jobData.pixelAccuracy
    corRow.IoU=jobData.IoU
    corRow.diceCoefficient=jobData.diceCoefficient
    db.commit()
    db.refresh(corRow)
    return True

def createSegmentationJob(db: Session, jobData: schemas.segmentationJobSchema):
    modId = readModeltableIdFromVersionName(db, jobData.modelVersion)
    db_seg = tables.Segmentationtable(
        imageName=jobData.imageName, 
        imagePath=jobData.imagePath,
        jsonPredictedPath=jobData.jsonPredictedPath,
        id_Model=modId,
        tsStartSegmentation=jobData.tsStartSegmentation,
        tsEndSegmentation=jobData.tsEndSegmentation
    )
    db.add(db_seg)
    db.commit()
    db.refresh(db_seg)

    db_token = tables.Tokentable(
        token=jobData.token, 
        status=jobData.status, 
        id_Segmentation=db_seg.id
    )
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    return True

def createCorrectionForSegmentation(db: Session, correction: schemas.correctionInputSchema, jobData: schemas.correctionJobSchema):
    # valid token check
    tokenRow = readToken(db=db, token=correction.token)
    if tokenRow == None:
        return False

    # Insert Correction
    db_cor = tables.Correctiontable(
        correctionPath=jobData.correctionPath, 
        tsCorrectionReceived=jobData.tsCorrectionReceived, 
        pixelAccuracy=jobData.pixelAccuracy,
        IoU=jobData.IoU, 
        diceCoefficient=jobData.diceCoefficient
    )
    db.add(db_cor)
    db.commit()
    db.refresh(db_cor)

    # Update Segmentationtable
    segID = tokenRow.id_Segmentation
    segRow = db.query(tables.Segmentationtable).get(segID)
    segRow.id_Correction = db_cor.id
    db.commit()
    db.refresh(segRow)

    return True

def createNewModelVersion(db: Session, versionName:str, history:dict):
    db_mod = tables.Modeltable(
            versionName = versionName,
            loss = history["loss"],
            accuracy = history["accuracy"],
            val_loss = history["val_loss"],
            val_accuracy = history["val_accuracy"]
    )
    db.add(db_mod)
    db.commit()
    db.refresh(db_mod)
    return True