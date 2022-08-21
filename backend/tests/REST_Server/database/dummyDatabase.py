import pytest
from REST_Server.database import crud, tables
import sqlalchemy as sql
import sqlalchemy.ext.declarative as declarative
from sqlalchemy.orm import scoped_session, sessionmaker

@pytest.fixture(scope="session")
def connection():
    engine = sql.create_engine("sqlite:///./tests/Data/tests/dummyDatabase.db" )
    return engine.connect()

@pytest.fixture(scope="session")
def setup_database(connection):
    tables.Base.metadata.bind = connection
    tables.Base.metadata.create_all()
    yield
    tables.Base.metadata.drop_all()

@pytest.fixture
def db_session(setup_database, connection):
    transaction = connection.begin()
    yield scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=connection)
    )
    transaction.rollback()
