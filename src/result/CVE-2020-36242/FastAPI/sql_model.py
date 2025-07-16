from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, DateTime
import datetime
from dateutil.relativedelta import relativedelta


SQLALCHEMY_DATABASE_URL = "sqlite:///./userdb.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class User(Base):
    __tablename__ = "user_reg"

    uid = Column(Integer, primary_key = True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True)
    regdate = Column(DateTime, default=datetime.datetime.utcnow())
    expdate = Column(DateTime, default=datetime.datetime.utcnow()+relativedelta(years=1))
    api_key = Column(String, unique=True)


    
