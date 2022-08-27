import cv2
import numpy as np
from shapely.geometry import Polygon
from shapely.validation import make_valid

class postprocess():
    def probabilityAreaToDiscreteArea(area:np.ndarray,threshholdProbability:float) -> np.ndarray:
        ret, disArea = cv2.threshold(area, threshholdProbability, 255, 0)
        return disArea.astype(np.uint8)
    
    def DiscreteAreaToPolygons(area:np.ndarray)-> list:
        contours, _ = cv2.findContours(area, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE) #for polygon approximation: CHAIN_APPROX_TC89_KCOS
        polygons = []
        for i,contour in enumerate(contours):
            epsilon = 0.5 #for epsilon depending on polygon size: 0.005*cv2.arcLength(contour,True)
            approx = cv2.approxPolyDP(contour,epsilon,True)

            poly = []
            for object in approx:
                for point in object:
                    poly.append(int(point[0])) #x
                    poly.append(int(point[1])) #y
            #repeat the first point to create a 'closed loop'
            poly.append(poly[0])
            poly.append(poly[1])
            polygons.append(poly)
        return polygons
    
    def scalePolygonsToImageCoordinate(polygons:list,predWidth,predHeight,imageWidth,imageHeight):
        scaledPolygons = polygons.copy()
        xScale = imageWidth/predWidth
        yScale = imageHeight/predHeight

        for polygon in scaledPolygons:
            for i in range(0, len(polygon),2):
                polygon[i] = int(round(polygon[i]*xScale))
                polygon[i+1] = int(round(polygon[i+1]*yScale))

        return scaledPolygons
    
    def polygonIsInsidePolygon(polyIn:list,polyOut:list) -> bool:
        polyInner = make_valid(Polygon(list(zip(polyIn[::2],polyIn[1::2]))))
        polyOuter = make_valid(Polygon(list(zip(polyOut[::2],polyOut[1::2]))))
        return polyOuter.contains(polyInner)
    
    def polygonIsInsidePolygonFromPolygons(polyIn:list, polygons:list) -> bool:
        for polyOut in polygons:
            if not polyOut == polyIn:
                if postprocess.polygonIsInsidePolygon(polyIn=polyIn,polyOut=polyOut):
                    return True
        return False
    
    def filterPolygonsInsideOtherPolygons(polygons:list) -> list:
        filteredPolys =[]
        for polygon in polygons:
            if not postprocess.polygonIsInsidePolygonFromPolygons(polygon,polygons):
                filteredPolys.append(polygon)
        return filteredPolys
    
    def checkValidPolygon(polygon:list) -> bool:
        #Polygon must have at least eight x and y values in order to span an area
        if len(polygon)<8: 
            return False
        #Polygon must be closed
        elif polygon[0]!=polygon[-2] or polygon[1]!=polygon[-1]:
            return False 
        return True
    
    def filterInvalidPolygons(polygons:list) -> list:
        filteredPolys =[]
        for polygon in polygons:
            if postprocess.checkValidPolygon(polygon):
                filteredPolys.append(polygon)
        return filteredPolys
