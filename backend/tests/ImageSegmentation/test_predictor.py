#imports from other directory
import sys, os 
sys.path.append(os.path.abspath(os.path.join('..', 'backend')))
from ImageSegmentation.Predictor import Predictor
from ImageSegmentation.imageSegmentationInterface import imageSegmentationInterface

configPath = "tests/ImageSegmentation/testConfig.json"

def test_predictor_instantiatable():
    predictor = Predictor(configPath=configPath)
    assert predictor is not None

def test_predictor_implements_ImageSegmentation():
    assert issubclass(Predictor,imageSegmentationInterface)

def test_predictor_predict_dictionary():
    predictor = Predictor(configPath=configPath)
    imagePath = "tests/Data/tests/testImages/testCat.jpg"
    result = predictor.predict(imagePath=imagePath)
    assert type(result) == dict

def test_predictor_retrains_model_with_diffrent_training_lengths():
    imagePath = "tests/Data/tests/testImages/testCat.jpg"
    jsonPath = "tests/Data/tests/testCorrection/testCOCO.json"
    
    imagePaths = []
    jsonPaths = []
    jsonPaths.append(jsonPath)
    for i in range(2):
        imagePaths.append(imagePath)

    predictor = Predictor(configPath=configPath)
    history = predictor.retrain(imagePaths,jsonPaths)
    assert history == None

def test_predictor_retrains_model_successful():
    imagePath = "tests/Data/tests/testImages/testCat.jpg"
    jsonPath = "tests/Data/tests/testCorrection/testCOCO.json"
    
    imagePaths = []
    jsonPaths = []
    for i in range(5):
        imagePaths.append(imagePath)
        jsonPaths.append(jsonPath)

    predictor = Predictor(configPath=configPath)
    history = predictor.retrain(imagePaths,jsonPaths)
    assert type(history) == dict

def test_get_Categories_returns_dict():
    predictor = Predictor(configPath=configPath)
    cat = predictor.getCategories()
    assert type(cat) == dict