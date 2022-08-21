# Lib
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship, backref

# Program
from REST_Server.database.database import Base
from REST_Server.models.sqlAlchemyTypes import TextPickleType

class Correctiontable(Base):
    __tablename__ = "Correction"

    id = Column(Integer, primary_key=True, index=True)
    correctionPath = Column(String, unique=True)
    tsCorrectionReceived = Column(DateTime)
    pixelAccuracy = Column(TextPickleType())
    IoU = Column(TextPickleType())
    diceCoefficient = Column(TextPickleType())

class Segmentationtable(Base):
    __tablename__ = "Segmentation"

    id = Column(Integer, primary_key=True, index=True)
    imageName  = Column(String, unique=True)
    imagePath = Column(String, unique=True)
    jsonPredictedPath = Column(String, unique=True)
    id_Model = Column(Integer, ForeignKey("Model.id"))
    tsStartSegmentation = Column(DateTime)
    tsEndSegmentation = Column(DateTime)

    id_Correction = Column(Integer, ForeignKey("Correction.id"), nullable=True)
    correctiontable = relationship("Correctiontable", backref=backref("Correction", uselist=False))
    
class Modeltable(Base):
    __tablename__ = "Model"

    id = Column(Integer, primary_key=True, index=True)
    versionName = Column(String, unique=True)
    loss = Column(TextPickleType(), nullable=True)
    accuracy = Column(TextPickleType(), nullable=True)
    val_loss = Column(TextPickleType(), nullable=True)
    val_accuracy = Column(TextPickleType(), nullable=True)

    segmentationtable = relationship("Segmentationtable")


class Tokentable(Base):
    __tablename__ = "Token"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, unique=True, index=True)
    status = Column(String)

    id_Segmentation = Column(Integer, ForeignKey("Segmentation.id"))
    segmentationtable = relationship("Segmentationtable", backref=backref("Segmentation", uselist=False))