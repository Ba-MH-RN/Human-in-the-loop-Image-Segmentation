from pydantic import BaseModel, conlist, validator
from typing import List, Union, Optional

class segmentationJobSchema(BaseModel):
    imageName:str
    imagePath:str
    jsonPredictedPath:str
    modelVersion:str
    tsStartSegmentation:str
    tsEndSegmentation:str

    token:str
    status:str

class cocoInfo(BaseModel):
    description:str
    ModelVersion:str

class cocoCategories(BaseModel):
    id:int
    name:str

class cocoImages(BaseModel):
    id:int
    file_name: str
    height: int
    width: int

class cocoAnnotations(BaseModel):
    id: int
    image_id: int
    category_id: int
    area: Optional[float] = None
    segmentation: List[int]

    @validator("segmentation")
    def segmentation_valid_polygon(cls, segmentation: List[int]):
        if len(segmentation)<8: 
            raise ValueError('Polygon must have at least eight x and y values in order to span an area')

        elif segmentation[0]!=segmentation[-2] or segmentation[1]!=segmentation[-1]:
            raise ValueError('Polygon must be closed')

        return segmentation

class cocoJSON(BaseModel):
    info:cocoInfo
    categories: conlist(cocoCategories, min_items=1)
    images: conlist(cocoImages, min_items=1)
    annotations:List[cocoAnnotations]

class cocoCategoriesReturnSchema(BaseModel):
    categories: List[cocoCategories]

class correctionInputSchema(BaseModel):
    cocoJSON:cocoJSON
    token:str

class segmentationReturnSchema(BaseModel):
    cocoJSON:cocoJSON
    token:str

class noCorrectionInputSchema(BaseModel):
    token:str

class correctionJobSchema(BaseModel):
    correctionPath:str
    tsCorrectionReceived:str
    pixelAccuracy:dict
    IoU:dict
    diceCoefficient:dict
