from sqlalchemy import Column, DateTime, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Data(Base):
    __tablename__ = 'data'

    resultid = Column(Integer, primary_key=True, autoincrement=True)
    datetime = Column(DateTime, nullable=False)
    config = Column(String(512), nullable=True)
    result = Column(Integer, nullable=False)
    image = Column(Text, nullable=False)
    userid = Column(Integer, ForeignKey('users.userid'), nullable=False)

    # Relationship to the User table to access the related user
    user = relationship("User", back_populates="data_entries")

class User(Base):
    __tablename__ = 'users'

    userid = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(String(255), nullable=True)
    url = Column(Text, nullable=False)
    resultid = Column(String(255), nullable=False)

    # Relationship to the Data table for accessing related data entries
    data_entries = relationship("Data", back_populates="user")

