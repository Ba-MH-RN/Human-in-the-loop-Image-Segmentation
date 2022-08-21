import tensorflow as tf
import csv
from os.path import exists
from ImageSegmentation.modelControl import customKearasObjects

class ModelVersionControl():
    modelDirectory:str
    currentVersionName = "0"
    modelExtension = ".h5"
    currentModel:tf.keras.Model

    def __init__(self, modelDirectory:str, baselineModelPath:str) -> None:
        self.modelDirectory = modelDirectory
        history = self._readHistory()
        if history is not None:
            self.currentVersionName = history[-1][0]
        else:
            baselineModel =tf.keras.models.load_model(baselineModelPath, custom_objects=customKearasObjects.getCustomObjects())
            baselineModel.save(self._getCurrentModelPath())
            self._writeHistory()
        self.currentModel = tf.keras.models.load_model(self._getCurrentModelPath(), custom_objects=customKearasObjects.getCustomObjects())

    def _readHistory(self) -> list:
        historyPath = self.modelDirectory + 'history.csv'
        if exists(historyPath):
            with open(historyPath, 'r', encoding='UTF8', newline='') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                data = list(csv_reader)
            return data
        else:
            return None

    def _writeHistory(self) -> None:
        historyPath = self.modelDirectory + 'history.csv'
        if exists(historyPath):
            with open(historyPath, 'a', encoding='UTF8', newline='') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow([self.currentVersionName])
        else:
            with open(historyPath, 'w', encoding='UTF8', newline='') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(["Model Version"])
                csv_writer.writerow([self.currentVersionName])

    def _getCurrentModelPath(self)->str:
        return self.modelDirectory + self.currentVersionName+ self.modelExtension
    
    def getCurrentModel(self) -> tf.keras.Model:
        lastVersionInHistory = self._readHistory()[-1][0]
        if lastVersionInHistory is not self.currentVersionName:
            self._updateVersionName(lastVersionInHistory)
            self.currentModel = tf.keras.models.load_model(self._getCurrentModelPath(), custom_objects=customKearasObjects.getCustomObjects())
        return self.currentModel

    def getCurrentModelVersionName(self) -> str:
        return self.currentVersionName

    def _nextVersionName(self) -> str:
        return str(int(self.currentVersionName)+1)
    
    def _updateVersionName(self, name:str) -> None:
        self.currentVersionName = name

    def updateModel(self, model:tf.keras.Model) -> str:
        nextVersionName = self._nextVersionName()
        model.save(self.modelDirectory + nextVersionName + self.modelExtension)
        self.currentModel = model
        self._updateVersionName(nextVersionName)
        self._writeHistory()
    