from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    rides = relationship("Ride", back_populates="driver")

class Ride(Base):
    __tablename__ = 'rides'
    
    id = Column(Integer, primary_key=True, index=True)
    origin = Column(String(100), nullable=False)
    destination = Column(String(100), nullable=False)
    driver_id = Column(Integer, ForeignKey('users.id'))
    driver = relationship("User", back_populates="rides")

class Driver(Base):
    __tablename__ = 'drivers'
    
    id = Column(Integer, primary_key=True, index=True)
    license_number = Column(String(20), unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User")