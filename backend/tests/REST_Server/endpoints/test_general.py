from tests.REST_Server.clientFastApi import client

def test_root_answers_successful():
    response = client.get("/")
    assert response.status_code==200
    assert response.template.name == 'root.html'

def test_heartbeat_answers_successful():
    response = client.get("/heartbeat")
    assert response.status_code==200

def test_dashboard_answers_successful():
    filename = "tests/Data/tests/testImages/test.png"
    responseImage = client.post("/ImageSegmentation/uploadImage", files={"file": ("test.png", open(filename, "rb"), "image/png")})
    coco = responseImage.json()["cocoJSON"]
    token = responseImage.json()["token"]
    responseCorrection = client.post("/ImageSegmentation/uploadCorrection", json={"cocoJSON": coco,"token": token},)
    response = client.get("/dashboard")
    assert response.status_code==200
    assert response.template.name == 'dashboard.html'