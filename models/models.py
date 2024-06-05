from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, create_engine, ForeignKey, DateTime, Boolean
from datetime import datetime
from sqlalchemy.orm import relationship
import datetime
import bcrypt
import jwt
import os


Base = declarative_base()
SECRET_KEY = os.environ.get('SECRET_KEY', 'my_secret_key')

class ValidationError(Exception):
    pass

class Client(Base):
    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    telephone = Column(String, nullable=False)
    company_name = Column(String, nullable=False)
    creation_date = Column(DateTime, default=datetime.datetime.utcnow)
    last_update = Column(DateTime)
    commercial_id = Column(Integer, ForeignKey('collaborators.id'), nullable=False)

    contracts = relationship('Contract', backref='client')
    events = relationship('Event', backref='client')

    def __repr__(self):
        return f'Client {self.name}'
    

class Contract(Base):
    __tablename__ = 'contracts'
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('clients.id'), nullable=False)
    commercial_id = Column(Integer, ForeignKey('collaborators.id'), nullable=False)
    total_amount = Column(Float, nullable=False)
    amount_due = Column(Float, nullable=False)
    creation_date = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(Boolean, nullable=False)

    client = relationship('Client', backref='contracts')
    events = relationship('Event', backref='contract')

    def validate(self):
        errors = []
        
        if not isinstance(self.client_id, int):
            errors.append("Client ID must be an integer.")
        
        if not isinstance(self.commercial_id, int):
            errors.append("Commercial ID must be an integer.")
        
        if not isinstance(self.total_amount, (int, float)) or self.total_amount <= 0:
            errors.append("Total amount must be a positive number.")
        
        if not isinstance(self.amount_due, (int, float)) or self.amount_due < 0:
            errors.append("Amount due must be a non-negative number.")
        
        if not self.status:
            errors.append("Status is required.")
        
        if errors:
            raise ValidationError(errors)
    
    def save(self, session):
        self.validate()
        session.add(self)
        session.commit()
    

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
    department = Column(String, nullable=False)
    password = Column(String, nullable=False)
    
    def set_password(self, password):
        salt = bcrypt.gensalt()
        self.password = bcrypt.hashpw(password.encode('utf-8'), salt)

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))    

    def create_token(self):
        token = jwt.encode({
            'id' : self.id,
            'exp' : datetime.datetime.utcnow() + datetime.timedelta(days=30),
            'department': self.department
        }, SECRET_KEY, algorithm='HS256')
        return token
    
    def verify_token(self, token):
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            if data['id'] == self.id:
                return data
            return None
        except jwt.ExpiredSignatureError:
            return 'expired'
        except jwt.InvalidTokenError:
            None

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
            return collaborator.create_token()
        else:
            return None

    def __repr__(self):
        return f'Collaborator {self.name}'
    

engine = create_engine('sqlite:///file.db', echo=True)
Base.metadata.create_all(engine)
