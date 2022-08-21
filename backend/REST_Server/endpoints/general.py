# Libs
from fastapi import Response, APIRouter, Request, Depends
from starlette.status import HTTP_200_OK
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, Response
import fastapi
from sqlalchemy.orm import Session
import pandas as pd

# Program
from REST_Server.database import crud, database
from REST_Server.evaluation import plots

#--------- Script / Constants ---------
responses = {
    404: {"detail": "Database not accessible"}
}

# APIRouter creates path operations for item module
router = APIRouter(
    tags=["General"],
)

# Jinja2 Templates for HTML/CSS Response
templates = Jinja2Templates(directory="REST_Server/responsesHTML/templates")


# Define Routes
@router.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("root.html", {"request": request})

@router.get("/heartbeat", response_class=Response)
async def get_heartbeat():
    return Response(status_code=HTTP_200_OK)

@router.get("/dashboard", response_class=HTMLResponse, responses={404: responses[404]})
async def get_dashboard(request: Request,  db: Session=Depends(database.getDatabase)):
    metrics = crud.readMetrics(db)
    metricsDf = pd.DataFrame.from_records(metrics, columns=["tsCorrectionReceived", "pixelAccuracy", "IoU", "diceCoefficient"])
    metaSeg = crud.readMetaSegmentation(db)
    metaSegDf = pd.DataFrame.from_records(metaSeg, columns=["tsStartSegmentation", "tsEndSegmentation"])
    metaCor = crud.readMetaCorrections(db)
    metaCorDf = pd.DataFrame.from_records(metaCor, columns=["modelVersion","IoU"])
    metaMod = crud.readMetaModeltable(db)
    metaModDf = pd.DataFrame.from_records(metaMod, columns=["versionName", "loss", "accuracy", "val_loss", "val_accuracy"])

    if len(metricsDf) == 0 or len(metaSegDf) == 0 or len(metaCorDf) ==0:
        raise fastapi.HTTPException(status_code=404, detail=responses[404]["detail"])

    figMetrics = plots.plotMetrics(metricsDf)
    figSegToCorPie = plots.plotSegToCorPie(len(metaSeg),len(metaCorDf))
    figUsage = plots.plotApiUsage(metaSegDf)
    figModels = plots.plotModels(metaCorDf)
    figSegTime = plots.plotSegmentationTime(metaSegDf)
    figModelLoss = plots.plotModelLoss(metaModDf)
    figModelAccuracy = plots.plotModelAccuracy(metaModDf)

    currentModelVersion = metaModDf.iloc[-1].versionName
    totalSegmentations = len(metaSeg)
    totalCorrections = len(metaCorDf)

    meta = [currentModelVersion,totalSegmentations,totalCorrections]

    return templates.TemplateResponse("dashboard.html", {   "request": request, "figMetrics": figMetrics, "figModels": figModels, 
                                                            "figUsage": figUsage,"figSegTime": figSegTime, "figModelLoss":figModelLoss, 
                                                            "figModelAccuracy":figModelAccuracy, "figSegToCorPie":figSegToCorPie, "meta": meta})