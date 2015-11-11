import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
 
Base = declarative_base()
 
class Entity(Base):
    __tablename__ = 'entity'
    id = Column(Integer, primary_key=True)
    text = Column(String(250), nullable=False)
    enType = Column(String(30), nullable=False)
    posTag = Column(String(10), nullable=False)
    locationID = Column(Integer, ForeignKey('location.id'))

class Location(Base):
    __tablename__ = 'location'
    id = Column(Integer, primary_key=True)
    fileName = Column(String(250), nullable=False)
    startLoc = Column(Integer, nullable=False)
    endLoc = Column(Integer, nullable=False)
    annID = Column(String(5), nullable=False)

if __name__=="__main__":
    # Create an engine that stores data in the local directory's
    engine = create_engine('sqlite:///../DB/entity.db')
    # Create all tables in the engine. This is equivalent to "Create Table"
    # statements in raw SQL.
    Base.metadata.create_all(engine)
    
