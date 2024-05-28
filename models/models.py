from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, create_engine, ForeignKey, DateTime, Boolean
from datetime import datetime
from sqlalchemy.orm import relationship, sessionmaker
import datetime
import bcrypt
import jwt
import os

Base = declarative_base()
SECRET_KEY = os.environ.get('SECRET_KEY', 'my_secret_key')

class Client(Base):
    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String)
    telephone = Column(String)
    company_name = Column(String)
    creation_date = Column(DateTime, default=datetime.datetime.utcnow)
    last_update = Column(DateTime)
    commercial_id = Column(Integer, ForeignKey('collaborators.id'))

    contracts = relationship('Contract', backref='client')
    events = relationship('Event', backref='client')

    def __repr__(self):
        return f'Client {self.name}'
    

class Contract(Base):
    __tablename__ = 'contracts'
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('clients.id'))
    commercial_id = Column(Integer, ForeignKey('collaborators.id'))
    total_amount = Column(String)
    amount_due = Column(String)
    creation_date = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(Boolean)

    client = relationship('Client', backref='contracts')
    events = relationship('Event', backref='contract')
    

class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    contract_id = Column(Integer, ForeignKey('contracts.id'))
    client_id = Column(Integer, ForeignKey('clients.id'))
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    support_contact_id = Column(Integer, ForeignKey('collaborators.id'))
    location = Column(String)
    attendees = Column(Integer)
    notes = Column(String)

    client = relationship('Client', backref='events')
    contract = relationship('Contract', backref='events')
    

class Collaborator(Base):
    __tablename__= 'collaborators'
    id = Column(Integer, primary_key=True)
    employee_number = Column(Integer, unique=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    department = Column(String)
    password = Column(String, nullable=False)
    
    def set_password(self, password):
        salt = bcrypt.gensalt()
        self.password = bcrypt.hashpw(password.encode('utf-8'), salt)

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))    

    def generate_token(self):
        token = jwt.encode({
            'id' : self.id,
            'exp' : datetime.datetime.utcnow() + datetime.timedelta(days=30)
        }, SECRET_KEY, algorithm='HS256')
        return token
    
    def verify_token(self, token):
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            if data['id'] == self.id:
                return True
            return False
        except jwt.ExpiredSignatureError:
            return False
        except jwt.InvalidTokenError:
            return False

    def register(self, session, employee_number, name, email, department, password):
        self.employee_number = employee_number
        self.name = name
        self.email = email
        self.department = department
        self.set_password(password)
        session.add(self)
        session.commit()
        return self

    def authenticate(self, session, email, password):
        collaborator = session.query(Collaborator).filter_by(email=email).first()
        if collaborator and collaborator.check_password(password):
            return collaborator.generate_token()
        else:
            return None

    def __repr__(self):
        return f'Collaborator {self.name}'
    

engine = create_engine('sqlite:///file.db', echo=True)
Base.metadata.create_all(engine)
