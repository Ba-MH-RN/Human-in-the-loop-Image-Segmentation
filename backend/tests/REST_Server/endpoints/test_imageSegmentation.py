from tests.REST_Server.clientFastApi import client
from REST_Server.endpoints import imageSegmentation
from tests.REST_Server.database.dummyDatabase import *
from REST_Server.endpoints.imageSegmentation import retrainTriggerNumber

prefix = "/ImageSegmentation"

def test_generate_unique_token_is_not_none(db_session):
    token = imageSegmentation.generateUniqueToken(db_session)
    assert token is not None

def test_generate_unique_imagename_is_not_none(db_session):
    name = imageSegmentation.generateUniqueImageName(db_session)
    assert name is not None

def test_get_categories_successful():
    response = client.get(prefix + "/getCategories")
    assert response.status_code==200

def test_image_post_successful():
    filename = "tests/Data/tests/testImages/test.png"
    response = client.post(prefix + "/uploadImage", files={"file": ("test.png", open(filename, "rb"), "image/png")})
    assert response.status_code==200

def test_image_post_unknown_FileExtension():
    filename = "tests/Data/tests/testImages/test.unknown"
    response = client.post(prefix + "/uploadImage", files={"file": ("test.unknown", open(filename, "rb"), "image/unknown")})
    assert response.status_code==415

def test_correction_post_successful():
    filename = "tests/Data/tests/testImages/test.png"
    responseImage = client.post(prefix + "/uploadImage", files={"file": ("test.png", open(filename, "rb"), "image/png")})
    coco = responseImage.json()["cocoJSON"]
    token = responseImage.json()["token"]
    responseCorrection = client.post(prefix + "/uploadCorrection", json={"cocoJSON": coco,"token": token},)
    assert responseCorrection.status_code==200

def test_two_correction_on_the_same_post_successful():
    filename = "tests/Data/tests/testImages/test.png"
    responseImage = client.post(prefix + "/uploadImage", files={"file": ("test.png", open(filename, "rb"), "image/png")})
    coco = responseImage.json()["cocoJSON"]
    token = responseImage.json()["token"]
    responseCorrection = client.post(prefix + "/uploadCorrection", json={"cocoJSON": coco,"token": token},)
    responseCorrection = client.post(prefix + "/uploadCorrection", json={"cocoJSON": coco,"token": token},)
    assert responseCorrection.status_code==200

def test_correction_post_false_token():
    filename = "tests/Data/tests/testImages/test.png"
    responseImage = client.post(prefix + "/uploadImage", files={"file": ("test.png", open(filename, "rb"), "image/png")})
    coco = responseImage.json()["cocoJSON"]
    token = "FALSETOKEN"
    responseCorrection = client.post(prefix + "/uploadCorrection", json={"cocoJSON": coco,"token": token},)
    assert responseCorrection.status_code==406

def test_no_correction_post_successful():
    filename = "tests/Data/tests/testImages/test.png"
    responseImage = client.post(prefix + "/uploadImage", files={"file": ("test.png", open(filename, "rb"), "image/png")})
    token = responseImage.json()["token"]
    responseCorrection = client.post(prefix + "/uploadNoCorrection", json={"token": token},)
    assert responseCorrection.status_code==200

def test_no_correction_post_false_token():
    responseCorrection = client.post(prefix + "/uploadNoCorrection", json={"token": "FALSETOKEN"},)
    assert responseCorrection.status_code==406

def test_retrain_has_been_triggerd_after_nessesary_number_of_posts(capfd):
    filename = "tests/Data/tests/testImages/testCat.jpg"
    for i in range(retrainTriggerNumber):
        responseImage = client.post(prefix + "/uploadImage", files={"file": ("test.png", open(filename, "rb"), "image/png")})
        coco = responseImage.json()["cocoJSON"]
        token = responseImage.json()["token"]
        client.post(prefix + "/uploadCorrection", json={"cocoJSON": coco,"token": token},)
    #Check if Consol output has been printed -> updaten mit MockTest
    out, err = capfd.readouterr()
    assert "start Retrain" in out

def test_retrain_has_been_triggerd_with_empty_posts(capfd):
    filename = "tests/Data/tests/testImages/testCat.jpg"
    for i in range(retrainTriggerNumber):
        responseImage = client.post(prefix + "/uploadImage", files={"file": ("test.png", open(filename, "rb"), "image/png")})
        coco = responseImage.json()["cocoJSON"]
        coco["annotations"]= []
        token = responseImage.json()["token"]
        client.post(prefix + "/uploadCorrection", json={"cocoJSON": coco,"token": token},)
    #Check if Consol output has been printed -> updaten mit MockTest
    out, err = capfd.readouterr()
    assert "start Retrain" in out