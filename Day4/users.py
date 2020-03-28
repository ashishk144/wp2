import os
from sqlalchemy import Column, String, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    user_id = Column(String, primary_key = True)
    pwd = Column(String, nullable = False)
    timestamp = Column(DateTime(timezone = True), nullable = False)
    def __str__(self):
    	return self.user_id +" "+ self.pwd+" " + str(self.timestamp)

engine = create_engine(os.getenv("DATABASE_URL"), echo=True)

Base.metadata.create_all(engine)
