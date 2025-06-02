from sqlalchemy import Column, Integer, String, Numeric, Date, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Client(Base):
    __tablename__ = 'clients'
    id        = Column(Integer, primary_key=True)
    name      = Column(String, nullable=False)
    email     = Column(String, nullable=False, unique=True)
    phone     = Column(String)
    address   = Column(String)
    jobs      = relationship("Job", back_populates="client")

class Crew(Base):
    __tablename__ = 'crews'
    id        = Column(Integer, primary_key=True)
    name      = Column(String, nullable=False)
    jobs      = relationship("Job", back_populates="crew")

class Job(Base):
    __tablename__ = 'jobs'
    id         = Column(Integer, primary_key=True)
    client_id  = Column(Integer, ForeignKey('clients.id'), nullable=False)
    crew_id    = Column(Integer, ForeignKey('crews.id'))
    service    = Column(String, nullable=False)
    scheduled  = Column(Date, nullable=False)
    price      = Column(Numeric(10,2), nullable=False)
    latitude   = Column(Float, nullable=True)
    longitude  = Column(Float, nullable=True)
    client     = relationship("Client", back_populates="jobs")
    crew       = relationship("Crew", back_populates="jobs")
    payments   = relationship("Payment", back_populates="job")

class Payment(Base):
    __tablename__ = 'payments'
    id       = Column(Integer, primary_key=True)
    job_id   = Column(Integer, ForeignKey('jobs.id'), nullable=False)
    amount   = Column(Numeric(10,2), nullable=False)
    paid_on  = Column(Date, nullable=False)
    job      = relationship("Job", back_populates="payments")
