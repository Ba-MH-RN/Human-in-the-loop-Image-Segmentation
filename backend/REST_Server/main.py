import sys, os 
#change sytempath for imports to parent folder "backend"
sys.path.append(os.path.abspath(os.path.join('..', 'backend')))
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
from REST_Server.endpoints import general,imageSegmentation
from REST_Server.database import tables
from REST_Server.database.database import engine

#run configuration
if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)

description = """
<a href="/dashboard">Go to the Dashboard</a>
"""

app = FastAPI(title="Human-in-the-loop Image-Segmentation", description=description)

#Set static Folder for Jinja2 Templates
app.mount("/REST_Server/responsesHTML/static",StaticFiles(directory="REST_Server/responsesHTML/static"),name="staticFiles")

#Set up SQL Database
tables.Base.metadata.create_all(bind=engine)

#CORS Middleware for the communication on the same machine with React
origins = ['http://localhost:3000']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials = True,
    allow_methods=['*'],
    allow_headers =['*']
)

#Set endpoints
api_router = APIRouter()
api_router.include_router(general.router)
api_router.include_router(imageSegmentation.router)
app.include_router(api_router)
