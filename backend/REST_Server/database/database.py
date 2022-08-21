import sqlalchemy as sql
import sqlalchemy.ext.declarative as declarative
import sqlalchemy.orm as orm
from REST_Server import config

SQLALCHEMY_DATABASE_URL = "sqlite:///./" + config.saveDirectory + "database.db"
#check same thread false: allows multiple threads to access the db (normally only one)
engine=sql.create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative.declarative_base()

def getDatabase():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
