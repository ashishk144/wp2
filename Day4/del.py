import os
from users import *
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"), echo=True)
db = scoped_session(sessionmaker(bind=engine))

val = db.query(User).delete()
print("Executed", val)
db.commit()
print("Final Execution")