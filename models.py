from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, create_engine, ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship

Base = declarative_base()

class Client(Base):
    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    telephone = Column(String)
    company_name = Column(String)
    creation_date = Column(datetime)
    last_update = Column(datetime)
    commercial = Column(String)

    contracts = relationship('Contract', backref='client')
    events = relationship('Event', backref='client')

    def __repr__(self):
        return f'User {self.name}'
    

class Contract(Base):
    __tablename__ = 'contracts'
    id = Column(Integer, primary_key=True)
    client = Column(String, ForeignKey('clients.name'))
    commercial = Column(String)
    total_amount = Column(String)
    amount_due = Column(String)
    creation_date = Column(datetime)
    status = Column(bool)

    client = relationship('Client', backref='contracts')
    events = relationship('Event', backref='contract')

    def __repr__(self):
        return f'User {self.name}'
    

class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    Contract_id = Column(Integer, ForeignKey('contracts.id'))
    client_name = Column(String, ForeignKey('clients.name'))
    client_contact = Column(String, ForeignKey('clients.email'))
    start_date = Column(datetime)
    end_date = Column(datetime)
    support_contact = Column(String)
    location = Column(String)
    attendees = Column(Integer)
    notes = Column(String)

    client = relationship('Client', backref='events')
    contract = relationship('Contract', backref='events')

    def __repr__(self):
        return f'User {self.name}'
    

engine = create_engine('sqlite:///:memory:', echo=True)
Base.metadata.create_all(engine)
