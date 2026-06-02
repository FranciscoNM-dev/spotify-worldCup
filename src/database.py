from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv
#We read from .env
load_dotenv()

database = os.getenv('DATABASE_URL')
#To connect with the database (we need the link to know which db we connecting to)
engine = create_engine(database)
#Open a session, a "communication" with the db. Changes will not save themselves nor be sent
#until commit is made. bind is to know which engine we connecting to
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#Classes which inherit from Base will correspond to tables in our DB so in advance we do:
Base = declarative_base()

class Result(Base):
    #first the table name
    __tablename__ = 'results'
    #Now its columns. We import from sqlalchemy these technicisms. We also have a primary key
    id = Column(Integer, primary_key=True)
    winner_name = Column(String)
    winner_image = Column(String)
    game_mode = Column(String)
    participants = Column(Integer)
    timestamp = Column(DateTime)

#Base knows all classes that inherit from it. It will create all those tables (just 1 in our case)
#in our database via the engine
Base.metadata.create_all(bind=engine)
