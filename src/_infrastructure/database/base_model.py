from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from _infrastructure.database.engine import db_engine

Base = declarative_base()
Base.metadata.create_all(db_engine)
