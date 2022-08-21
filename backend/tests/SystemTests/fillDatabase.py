from fastapi.testclient import TestClient
#imports from other directory
import sys, os
sys.path.append(os.path.abspath(os.path.join('..', 'backend')))
from REST_Server.main import app
from tests.REST_Server.database.dummyDatabase import *
from fastapi.testclient import TestClient
from random import randint
from time import sleep
import json

if __name__ == "__main__":
    client = TestClient(app)
    imageDirectory = "tests/SystemTests/data/testImages/"
    cocoDirectory = "tests/SystemTests/data/testCoco/"
    filename = "tests/REST_Server/data/testImages/testCat.jpg"

    postNumber = 490

    for i in range(postNumber):
        name = str(randint(0, 29))

        responseImage = client.post("/ImageSegmentation/uploadImage", files={"file": ("cat.jpg", open(imageDirectory+name+ ".jpg", "rb"), "image/jpg")})
        # Sleep a random number of seconds
        sleep(randint(0,30))

        with open(cocoDirectory+name+ ".json") as jsonFile:
            cocoCor = json.load(jsonFile)
        coco = cocoCor
        token = responseImage.json()["token"]
        client.post("/ImageSegmentation/uploadCorrection", json={"cocoJSON": coco,"token": token},)
        # Sleep a random number of seconds
        sleep(randint(0,30))
        print("Posted " + name +  "\tNr." + str(i) + " from " + str(postNumber))