from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, create_engine, ForeignKey, DateTime, Boolean
from datetime import datetime
from sqlalchemy.orm import relationship
import datetime
import bcrypt

Base = declarative_base()

class Client(Base):
    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String)
    telephone = Column(String)
    company_name = Column(String)
    creation_date = Column(DateTime, default=datetime.datetime.utcnow)
    last_update = Column(DateTime)
    commercial = Column(String)

    contracts = relationship('Contract', backref='client')
    events = relationship('Event', backref='client')

    def __repr__(self):
        return f'Client {self.name}'
    

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
    

class User(Base):
    __tablename__= 'users'
    id = Column(Integer, primary_key=True)
    employee_number = Column(Integer, unique=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    department = Column(String)
    password = Column(String, nullable=False)
    
    def set_password(self, password):
        salt = bcrypt.gensalt()
        self.password = bcrypt.hashpw(password.encode('utf-8'), salt)

    def __repr__(self):
        return f'User {self.name}'
    

engine = create_engine('sqlite:///file.db', echo=True)
Base.metadata.create_all(engine)
