#imports from other directory
import sys, os 
sys.path.append(os.path.abspath(os.path.join('..', 'backend')))
from Data.COCO_JSON.cocoParser import cocoParser

def test_calculate_Polygon_Area_correct():
    coco = cocoParser()
    x = [10,20,20,10,10]
    y = [10,10,20,20,10]
    areaOfSquare = 100
    calculatedArea = coco.polygonArea(x,y)
    assert calculatedArea == areaOfSquare

def test_generate_cat_COCO_not_None():
    coco = cocoParser()
    coco.width = 256
    coco.height = 128
    coco.modelVersion = "1"
    coco.polygonsDict={0:[[2,6,3,4,1,5],[3,5,3,3,3,5,3,3]]}
    cocoJSON = coco.generateCocoJSON()
    assert cocoJSON is not None

def test_generate_cat_COCO_polygon_correct_order():
    coco = cocoParser()
    coco.width = 256
    coco.height = 128
    coco.modelVersion = "0.1"
    twoPolygons = {0:[[2,6,3,4,1,5,2,6],[3,5,3,3,3,5,3,3,3,5]]}
    coco.polygonsDict= twoPolygons
    cocoJSON = coco.generateCocoJSON()
    assert cocoJSON["annotations"][0]["segmentation"][0] == twoPolygons[0][0][0]
    assert cocoJSON["annotations"][0]["segmentation"][1] == twoPolygons[0][0][1]

def test_generate_cat_COCO_correct_modelVersion():
    coco = cocoParser()
    coco.width = 256
    coco.height = 128
    modelVersion = "0.1"
    coco.modelVersion = modelVersion
    coco.polygonsDict= {0:[[2,6,3,4,1,5,2,6],[3,5,3,3,3,5,3,3,3,5]]}
    cocoJSON = coco.generateCocoJSON()
    assert cocoJSON["info"]["ModelVersion"] == modelVersion

def test_generate_cat_COCO_correct_height_width():
    coco = cocoParser()
    width = 256
    height = 128
    coco.width = width
    coco.height = height
    coco.modelVersion = "0.1"
    coco.polygonsDict= {0:[[2,6,3,4,1,5,2,6],[3,5,3,3,3,5,3,3,3,5]]}
    cocoJSON = coco.generateCocoJSON()
    assert cocoJSON["images"][0]["width"] == width
    assert cocoJSON["images"][0]["width"] != height
    assert cocoJSON["images"][0]["height"] == height
    assert cocoJSON["images"][0]["height"] != width

def test_get_Categories_returns_dict():
    coco = cocoParser()
    coco.categories = [{'id': 0, 'name': 'cat'}]
    cat = coco.getCategories()
    assert type(cat) == dict