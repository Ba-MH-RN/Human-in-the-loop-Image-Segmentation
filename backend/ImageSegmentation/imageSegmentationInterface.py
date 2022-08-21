import abc

class imageSegmentationInterface(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'predict') and 
                callable(subclass.predict) and
                hasattr(subclass, 'retrain') and 
                callable(subclass.retrain)  and
                hasattr(subclass, 'getCategories') and 
                callable(subclass.getCategories)  or 
                NotImplemented)

    @abc.abstractmethod
    def predict(self, imagePath: str) -> dict:
        """Predict and return COCO JSON"""
        raise NotImplementedError
    
    @abc.abstractmethod
    def retrain(self, trainImagePaths:list, trainCocoJsonPaths:list) -> dict:
        """Retrains the model and returns Retraining Infos"""
        raise NotImplementedError
    
    @abc.abstractmethod
    def getCategories(self) -> dict:
        """Returns the possible Categories of the model"""
        raise NotImplementedError