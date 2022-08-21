import numpy as np

class cocoParser():
    width:int
    height:int
    polygonsDict: dict
    modelVersion:str
    categories:list

    def __init__(self, categories:list = [{'id': 0, 'name': 'placeholder'}]) -> None:
        self.categories = categories
    
    def generateCocoJSON(self) -> dict:
        info = {"description": "Human-in-the-loop Image-Segmentation", "ModelVersion": self.modelVersion}
        images = [{"id":0,"file_name": " ","height": self.height, "width": self.width}]

        annotion_id = 0
        annotations = []

        for category, polygons in self.polygonsDict.items():
            for polygon in polygons:
                area = self.polygonArea(polygon[::2],polygon[1::2])
            
                annotations.append({
                    "id": annotion_id,
                    "image_id": 0,
                    "category_id": category,
                    "area": area,
                    "segmentation": polygon,
                })
                annotion_id += 1

        cocoJSON = {"info":info, 'categories':self.categories, 'images':images, 'annotations':annotations}
        return cocoJSON
    
    def polygonArea(self,x,y) -> int:
        return 0.5*np.abs(np.dot(x,np.roll(y,1))-np.dot(y,np.roll(x,1)))
    
    def getCategories(self) -> dict:
        return {'categories':self.categories}
