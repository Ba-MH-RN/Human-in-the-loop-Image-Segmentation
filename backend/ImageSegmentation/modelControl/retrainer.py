from PIL import Image, ImageDraw
from sklearn.model_selection import train_test_split
from numpy import ndarray
import numpy as np
import tensorflow as tf
import copy


class retrainer():
    def convertPolygonsDictToGroundTruthImageDict(polysDict:dict,widthImage:int,heightImage:int) -> dict:
        imageDict = {}
        
        for category, polygons in polysDict.items():
            image = Image.new("1", (widthImage,heightImage), "black")

            if polygons: #list is not empty
                for polygon in polygons:
                    canvas = ImageDraw.Draw(image)
                    canvas.polygon(polygon, fill = "white", outline ="white")

            imageDict[category] = image

        return imageDict

    
    def convertImagesToX(images:list) -> ndarray:
        channels = np.array(images[0]).shape[2]
        X_train = np.zeros((len(images),images[0].height,images[0].width,channels),dtype=np.uint8)
        for i,image in enumerate(images,start=0):
            X_train[i]= tf.keras.preprocessing.image.img_to_array(image)
        return X_train
    
    def convertImageDictsToY(imageDicts:list) ->ndarray:
        maxCategory = max(imageDicts[0])
        Y_train = np.zeros((len(imageDicts),imageDicts[0][0].height,imageDicts[0][0].width,maxCategory+1),dtype=bool)
        for i,imageDict in enumerate(imageDicts,start=0):
            for category, image in imageDict.items():
                Y_train[i,:,:,category]= tf.keras.preprocessing.image.img_to_array(image)[:,:,0]
        return Y_train
    
    def scalePolygonsToModelInput(polysDict:dict,currentWidth:int,currentHeight:int,modelWidth:int,modelHeight:int) -> dict:
        scaledPolysDict = copy.deepcopy(polysDict)
        xScale = modelWidth/currentWidth
        yScale = modelHeight/currentHeight

        for polygons in scaledPolysDict.values():
            for polygon in polygons:
                for i in range(0, len(polygon), 2):
                    polygon[i] = int(round(polygon[i]*xScale)) #x
                    polygon[i+1] = int(round(polygon[i+1]*yScale)) #y
        return scaledPolysDict
    

    def retrainModel(model:tf.keras.Model,X_train:ndarray,Y_train:ndarray) -> dict:
        x_train, x_val, y_train, y_val = train_test_split(X_train, Y_train, test_size=0.2, random_state=24)

        data_gen_args = dict(horizontal_flip=True,
                     rotation_range=90,
                     width_shift_range=0.2,
                     height_shift_range=0.2,
                     zoom_range=0.2,
                     validation_split=0.2
                     )
        image_datagen = tf.keras.preprocessing.image.ImageDataGenerator(**data_gen_args)
        mask_datagen =  tf.keras.preprocessing.image.ImageDataGenerator(**data_gen_args)

        seed = 1
        image_datagen.fit(x_train, augment=True, seed=seed)
        mask_datagen.fit(y_train, augment=True, seed=seed)

        image_generator = image_datagen.flow(x_train, seed=seed)
        mask_generator = mask_datagen.flow(y_train, seed=seed)

        train_generator = zip(image_generator, mask_generator)
        history = model.fit(train_generator, validation_data=(x_val, y_val), steps_per_epoch=5, epochs=2)
        return history.history