from fastapi.testclient import TestClient
#imports from other directory
import sys, os
sys.path.append(os.path.abspath(os.path.join('..', 'backend')))
from REST_Server.main import app
from REST_Server.database.database import getDatabase
from REST_Server.endpoints.imageSegmentation import getSavePath, getImageSegmentation
from tests.REST_Server.database.dummyDatabase import *
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from REST_Server.database import tables
from ImageSegmentation.Predictor import Predictor

SQLALCHEMY_DATABASE_URL = "sqlite:///./tests/Data/tests/dummyIntegrationDatabase.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
tables.Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

def override_save_path():
    return "tests/Data/tests/"

configPath = "tests/ImageSegmentation/testConfig.json"
def override_Image_Segmentation_Model():
    return Predictor(configPath=configPath)

app.dependency_overrides[getDatabase] = override_get_db
app.dependency_overrides[getSavePath] = override_save_path
app.dependency_overrides[getImageSegmentation] = override_Image_Segmentation_Model

client = TestClient(app)