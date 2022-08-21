import json

def getPolygonsDictFromCocoJsonPath(jsonPath:str, cocoCategories:dict) -> dict:
    polyDict = {}

    categories = cocoCategories["categories"]

    for cat in categories:
        polyDict[cat["id"]] = []

    with open(jsonPath) as jsonFile:
        coco = json.load(jsonFile)
        for anno in coco["annotations"]:
            categoryId = anno["category_id"]
            if categoryId in polyDict:
                polyDict[categoryId].append(anno["segmentation"])
    return polyDict
    
def getWidthAndHeightFromCocoJsonPath(jsonPath:str) -> tuple:
        with open(jsonPath) as jsonFile:
            coco = json.load(jsonFile)
            size = (coco["images"][0]["width"],coco["images"][0]["height"])
        return size

def getCategorieDictFromCocoJsonCategories(coco:dict) -> dict:
    dict = {}
    catList = coco["categories"]
    for cat in catList:
        dict[cat["id"]] = cat["name"]
    return dict
