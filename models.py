from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import datetime


engine = create_engine('postgresql://username:password@localhost:5432/BC_refID')
Session = sessionmaker(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime

class Video(Base):
    __tablename__ = "videos"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    #description = Column(String)
    ref_id = Column(String, nullable=False)
    video_id = Column(String, nullable=False)
    start_time = Column(DateTime, default=datetime.utcnow)


Base.metadata.create_all(engine)

