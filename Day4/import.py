import csv
import os
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker


Base = declarative_base()

class Book(Base):
    __tablename__ = "books"
    isbn = Column(String, primary_key = True)
    title = Column(String, nullable = False)
    author = Column(String, nullable = False)
    year = Column(Integer, nullable = False)
    def __str__(self):
        return str(self.isbn) +" "+ self.title+" " + self.author + " " + str(year)

engine = create_engine(os.getenv("DATABASE_URL"), echo=True)
db = scoped_session(sessionmaker(bind=engine))
Base.metadata.create_all(engine)


def main():
    f = open("books.csv")
    reader = csv.reader(f)
    itr = 0
    for row in reader:
        print(row)
        if itr != 0:
            b = Book(isbn=row[0],title = row[1],author=row[2],year = int(row[3]))
            db.add(b)
        if(itr!=0 and itr%100 == 0):
            db.commit()
            print(itr)
        itr += 1        
    db.commit()
    print("Executed")

if __name__ == "__main__":
    main()
