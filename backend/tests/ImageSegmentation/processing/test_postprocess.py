#imports from other directory
import sys, os 
sys.path.append(os.path.abspath(os.path.join('..', 'backend')))
import numpy as np
from ImageSegmentation.processing.preprocess import preprocess
from ImageSegmentation.modelControl.ModelVersionControl import ModelVersionControl
from ImageSegmentation.processing.postprocess import postprocess

def test_probability_Area_to_Boolean_Area_type_correct():
    modelDirectory = "tests/Data/tests/models/"
    baselineModelPath = "tests/ImageSegmentation/baselineModels/catModel.h5"
    modelVSC = ModelVersionControl(modelDirectory=modelDirectory, baselineModelPath=baselineModelPath)
    model = modelVSC.getCurrentModel()
    config = model.get_config()
    modelInputShape = config["layers"][0]["config"]["batch_input_shape"]

    imagePath = "tests/Data/tests/testImages/testCat.jpg"
    image = preprocess.loadImageFromPath(imagePath)
    width = image.width
    height = image.height
    scaledImage = preprocess.scaleImage(image,modelInputShape[1],modelInputShape[2])

    model = modelVSC.getCurrentModel()
    
    prediction = model.predict(np.asarray(scaledImage).reshape(1,modelInputShape[1],modelInputShape[2],modelInputShape[3]))

    prediction = np.asarray(prediction.reshape(modelInputShape[1],modelInputShape[2]))
    
    area = postprocess.probabilityAreaToDiscreteArea(prediction, 0.25)

    assert type(area)==np.ndarray

def test_discrete_area_to_polygon_type_correct():
    modelDirectory = "tests/Data/tests/models/"
    baselineModelPath = "tests/ImageSegmentation/baselineModels/catModel.h5"
    modelVSC = ModelVersionControl(modelDirectory=modelDirectory, baselineModelPath=baselineModelPath)
    model = modelVSC.getCurrentModel()
    config = model.get_config()
    modelInputShape = config["layers"][0]["config"]["batch_input_shape"]

    imagePath = "tests/Data/tests/testImages/testCat.jpg"
    image = preprocess.loadImageFromPath(imagePath)
    width = image.width
    height = image.height
    scaledImage = preprocess.scaleImage(image,modelInputShape[1],modelInputShape[2])

    model = modelVSC.getCurrentModel()
    
    prediction = model.predict(np.asarray(scaledImage).reshape(1,modelInputShape[1],modelInputShape[2],modelInputShape[3]))

    prediction = np.asarray(prediction.reshape(modelInputShape[1],modelInputShape[2]))
    
    area = postprocess.probabilityAreaToDiscreteArea(prediction, 0.25)
    polygons = postprocess.DiscreteAreaToPolygons(area)
    scaledPolygons = postprocess.scalePolygonsToImageCoordinate(polygons,modelInputShape[1],modelInputShape[2],width,height)

    assert type(scaledPolygons)==list

def test_Polygon_is_inside_Polygon_correct():
    polyOut = [0,0,100,0,100,100,0,100,0,0]
    polyIn = [10,10,90,10,90,90,10,90,10,10]
    inside = postprocess.polygonIsInsidePolygon(polyOut=polyOut,polyIn=polyIn)
    assert inside == True

def test_Polygon_is_inside_Polygon_false():
    polyOut = [0,0,100,0,100,100,0,100,0,0]
    polyIn = [10,10,200,10,90,90,10,90,10,10]
    inside = postprocess.polygonIsInsidePolygon(polyOut=polyOut,polyIn=polyIn)
    assert inside == False

def test_Polygon_is_inside_Polygon_are_the_same_polygon():
    poly = [0,0,100,0,100,100,0,100,0,0]
    inside = postprocess.polygonIsInsidePolygon(polyOut=poly,polyIn=poly)
    assert inside == True

def test_Polygon_Is_Inside_Polygon_From_Polygons_correct():
    polygons = [[0,0,100,0,100,100,0,100,0,0], [10,10,90,10,90,90,10,90,10,10]]
    inside = postprocess.polygonIsInsidePolygonFromPolygons(polygons[1],polygons)
    assert inside == True

def test_Polygon_Is_Inside_Polygon_From_Polygons_false():
    polygons = [[0,0,100,0,100,100,0,100,0,0], [10,10,200,10,90,90,10,90,10,10]]
    inside = postprocess.polygonIsInsidePolygonFromPolygons(polygons[0],polygons)
    assert inside == False

def test_filter_Polygons_Inside_Other_Polygons_correct():
    polygons = []
    polyOutside = [0,0,100,0,100,100,0,100,0,0]
    polyInside = [10,10,90,10,90,90,10,90,10,10]
    polygons.append(polyOutside)
    polygons.append(polyInside)
    polygons = postprocess.filterPolygonsInsideOtherPolygons(polygons)
    assert len(polygons) == 1

def test_Check_Polygon_is_valid_True():
    polygon = [0,0,100,0,100,100,0,100,0,0]
    valid = postprocess.checkValidPolygon(polygon)
    assert valid == True

def test_Check_Polygon_is_not_closed():
    polygon = [0,0,100,0,100,100,0,100,0,200]
    valid = postprocess.checkValidPolygon(polygon)
    assert valid == False

def test_Check_Polygon_is_valid_to_short():
    polygon = [0,0,100,0,100,100]
    valid = postprocess.checkValidPolygon(polygon)
    assert valid == False

def test_filter_Invalid_polygons_correct():
    polygons = []
    polyValid = [0,0,100,0,100,100,0,100,0,0]
    polyInvalid = [10,10,90,10]
    polygons.append(polyValid)
    polygons.append(polyInvalid)
    polygons = postprocess.filterInvalidPolygons(polygons)
    assert len(polygons) == 1