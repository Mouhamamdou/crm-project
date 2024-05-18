from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, create_engine, ForeignKey, DateTime, Boolean
from datetime import datetime
from sqlalchemy.orm import relationship
import datetime

Base = declarative_base()

class Client(Base):
    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    telephone = Column(String)
    company_name = Column(String)
    creation_date = Column(DateTime, default=datetime.datetime.utcnow)
    last_update = Column(DateTime)
    commercial = Column(String)

    contracts = relationship('Contract', backref='client')
    events = relationship('Event', backref='client')

    def __repr__(self):
        return f'User {self.name}'
    

class Contract(Base):
    __tablename__ = 'contracts'
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('clients.id'))
    commercial = Column(String)
    total_amount = Column(String)
    amount_due = Column(String)
    creation_date = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(Boolean)

    client = relationship('Client', backref='contracts')
    events = relationship('Event', backref='contract')

    def __repr__(self):
        return f'User {self.name}'
    

class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    Contract_id = Column(Integer, ForeignKey('contracts.id'))
    client_id = Column(Integer, ForeignKey('clients.id'))
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    support_contact = Column(String)
    location = Column(String)
    attendees = Column(Integer)
    notes = Column(String)

    client = relationship('Client', backref='events')
    contract = relationship('Contract', backref='events')

    def __repr__(self):
        return f'User {self.name}'
    

engine = create_engine('sqlite:///file.db', echo=True)
Base.metadata.create_all(engine)
