from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "user"
    userId = Column(Integer, primary_key=True)
    username = Column(String(50))
    hashedPassword = Column(String(100))
