#imports from other directory
import sys, os
sys.path.append(os.path.abspath(os.path.join('..', 'backend')))
from Data.COCO_JSON.cocoHandler import *

def test_get_Categorie_Dict_From_Coco_Json_Categories_correct():
    Dict = {0:"cat",1:"dog"}
    categorieDict = {'categories':[{'id': 0, 'name': 'cat'},{'id': 1, 'name': 'dog'}]}
    dict = getCategorieDictFromCocoJsonCategories(categorieDict)
    assert dict[0] == Dict[0]
    assert dict[1] == Dict[1]

def test_get_Width_and_Height_from_Coco_Json_Path_returns_tuple():
    jsonPath = "tests/Data/tests/testJson/testCOCO.json"
    size = getWidthAndHeightFromCocoJsonPath(jsonPath)
    assert type(size) == tuple

def test_get_Polygons_Dict_From_Coco_Json_Path_correct_first_point():
    jsonPath = "tests/Data/tests/testJson/testCOCO.json"
    categorieDict = {'categories':[{'id': 0, 'name': 'cat'},{'id': 1, 'name': 'dog'}]}
    polysDict = getPolygonsDictFromCocoJsonPath(jsonPath, categorieDict)
    assert polysDict[0][0][0] == 147 #x
    assert polysDict[0][0][1] == 51 #y