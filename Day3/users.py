from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
import os

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    user_id = Column(String, primary_key = True)
    pwd = Column(String, nullable = False)
    timestamp = Column(DateTime(timezone = True), nullable = False)

engine = create_engine(os.getenv("DATABASE_URL"), echo=True)

Base.metadata.create_all(engine)


#Superfluous code
# from users import *
# import os
# app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = os.getenv("DATABASE_URL")
# db.init_app(app)

# db = SQLAlchemy()

# class User(db.model):
#     def __init__(self, usr, pwd, time):
#         __tablename__ = "users"
#         id = db.column(db.String, primary_key = True)
#         pwd = db.column(db.String, nullable = False)
#         timestamp = db.column(db.String, primary_key = True)

# def main():
#   db.create_all()
#   app.run(debug = True)



# engine = create_engine('postgres://dzfsgqgmtgypmj:a6b4fbac38a9bb0a87ffbe7b4af6855d067998f6dd8cfb85621c87d309ca9d4d@ec2-18-213-176-229.compute-1.amazonaws.com:5432/d8muda130eogs8', echo = True)
# meta = MetaData()

# with app.app_context():
#   main()

# users = Table(
#    'users', meta, 
#    Column('user_id', String, primary_key = True), 
#    Column('password', String, nullable = False), 
#    Column('timestamp', DateTime, default=datetime.utcnow), 
# )
# meta.create_all(engine)