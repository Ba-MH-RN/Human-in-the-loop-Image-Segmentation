#imports from other directory
import sys, os 
sys.path.append(os.path.abspath(os.path.join('..', 'backend')))
from os.path import exists
from ImageSegmentation.modelControl.ModelVersionControl import ModelVersionControl
import tensorflow as tf

def test_modelVSC_instantiatable():
    modelPath = "tests/Data/tests/models/"
    baselineModelPath = "tests/ImageSegmentation/baselineModels/catModel.h5"
    modelVSC = ModelVersionControl(modelDirectory=modelPath,baselineModelPath=baselineModelPath)
    assert modelVSC is not None

def test_updated_versionName_not_old_versionName():
    modelPath = "tests/Data/tests/models/"
    baselineModelPath = "tests/ImageSegmentation/baselineModels/catModel.h5"
    modelVSC = ModelVersionControl(modelDirectory=modelPath,baselineModelPath=baselineModelPath)
    oldVersionName = modelVSC.getCurrentModelVersionName()
    nextVersion = modelVSC._nextVersionName()
    modelVSC._updateVersionName(nextVersion)
    newVersionName = modelVSC.getCurrentModelVersionName()
    assert oldVersionName != newVersionName

def test_get_current_model_type_correct():
    modelPath = "tests/Data/tests/models/"
    baselineModelPath = "tests/ImageSegmentation/baselineModels/catModel.h5"
    modelVSC = ModelVersionControl(modelDirectory=modelPath,baselineModelPath=baselineModelPath)
    model = modelVSC.getCurrentModel()
    assert issubclass(type(model), tf.keras.Model)

def test_update_model_version_not_old_version():
    modelPath = "tests/Data/tests/models/"
    baselineModelPath = "tests/ImageSegmentation/baselineModels/catModel.h5"
    modelVSC = ModelVersionControl(modelDirectory=modelPath,baselineModelPath=baselineModelPath)
    model = modelVSC.getCurrentModel()
    oldVersion = modelVSC.getCurrentModelVersionName()
    modelVSC.updateModel(model)
    newVersion = modelVSC.getCurrentModelVersionName()
    assert oldVersion != newVersion

def test_read_not_existing_history():
    modelPath = "tests/Data/tests/models/"
    baselineModelPath = "tests/ImageSegmentation/baselineModels/catModel.h5"
    modelVSC = ModelVersionControl(modelDirectory=modelPath,baselineModelPath=baselineModelPath)
    modelVSC.modelDirectory = "tests/Data/"
    history = modelVSC._readHistory()
    assert history == None

def test_write_not_existing_history():
    modelPath = "tests/Data/tests/models/"
    baselineModelPath = "tests/ImageSegmentation/baselineModels/catModel.h5"
    modelVSC = ModelVersionControl(modelDirectory=modelPath,baselineModelPath=baselineModelPath)
    modelVSC.modelDirectory = "tests/Data/"
    modelVSC._writeHistory()
    historyExists = exists("tests/Data/history.csv")
    os.remove("tests/Data/history.csv")
    assert historyExists == True

def test_read_last_written_modelversion_from_history_correct():
    modelPath = "tests/Data/tests/models/"
    baselineModelPath = "tests/ImageSegmentation/baselineModels/catModel.h5"
    modelVSC = ModelVersionControl(modelDirectory=modelPath,baselineModelPath=baselineModelPath)
    modelVSC.modelDirectory = "tests/Data/"
    modelVSC._writeHistory()
    modelVSC._writeHistory()
    history = modelVSC._readHistory()
    os.remove("tests/Data/history.csv")
    assert history[-1][0] == modelVSC.currentVersionName

def test_get_Current_Model_while_model_was_updated_correct():
    modelPath = "tests/Data/tests/models/"
    baselineModelPath = "tests/ImageSegmentation/baselineModels/catModel.h5"
    modelVSC = ModelVersionControl(modelDirectory=modelPath,baselineModelPath=baselineModelPath)
    modelVSC2 = ModelVersionControl(modelDirectory=modelPath,baselineModelPath=baselineModelPath)
    model = modelVSC.getCurrentModel()
    modelVSC.updateModel(model)
    modelVSC.getCurrentModel()
    modelVSC2.getCurrentModel()
    assert modelVSC.getCurrentModelVersionName() == modelVSC2.getCurrentModelVersionName()