from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean
from datetime import datetime, timedelta
from sqlalchemy.orm import relationship
import bcrypt
import jwt
import os
import re


class ValidationError(Exception):
    pass


Base = declarative_base()


class Client(Base):
    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    telephone = Column(String, nullable=False)
    company_name = Column(String, nullable=False)
    creation_date = Column(DateTime, default=datetime.utcnow)
    last_update = Column(DateTime)
    commercial_id = Column(Integer, ForeignKey('collaborators.id'), nullable=False)

    contracts = relationship('Contract', back_populates='client')
    events = relationship('Event', back_populates='client')

    def validate(self):
        errors = []
        
        if not self.name:
            errors.append("Name is required.")
        
        if not self.email or not re.match(r"[^@]+@[^@]+\.[^@]+", self.email):
            errors.append("Valid email is required.")
        
        if not self.telephone or not re.match(r"^\+?[1-9]\d{1,14}$", self.telephone):
            errors.append("Valid telephone number is required.")
        
        if not self.company_name:
            errors.append("Company name is required.")
        
        if not isinstance(self.commercial_id, int):
            errors.append("Commercial ID must be an integer.")
        
        if errors:
            raise ValidationError(errors)
    
    def save(self, session):
        self.validate()
        session.add(self)
        session.commit()

    def __repr__(self):
        return f'Client {self.name}'
    

class Contract(Base):
    __tablename__ = 'contracts'
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('clients.id'), nullable=False)
    commercial_id = Column(Integer, ForeignKey('collaborators.id'), nullable=False)
    total_amount = Column(Float, nullable=False)
    amount_due = Column(Float, nullable=False)
    creation_date = Column(DateTime, default=datetime.utcnow)
    status = Column(Boolean, nullable=False)

    client = relationship('Client', back_populates='contracts')
    events = relationship('Event', back_populates='contract')

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
        
        if self.status is None:
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
    contract_id = Column(Integer, ForeignKey('contracts.id'), nullable=False)
    client_id = Column(Integer, ForeignKey('clients.id'), nullable=False)
    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime)
    support_contact_id = Column(Integer, ForeignKey('collaborators.id'), nullable=True)
    location = Column(String, nullable=False)
    attendees = Column(Integer, nullable=False)
    notes = Column(String)

    client = relationship('Client', back_populates='events')
    contract = relationship('Contract', back_populates='events')

    def validate(self):
        errors = []

        if not isinstance(self.contract_id, int):
            errors.append("contract ID must be an integer.")

        if not isinstance(self.client_id, int):
            errors.append("Client ID must be an integer.")
        
        if not isinstance(self.end_date, datetime):
            errors.append("End date must be a valid datetime object.")
        
        print(self.start_date)
        print(self.end_date)
        #if self.start_date >= self.end_date:
        #    errors.append("Start date must be before end date.")
        
        if not self.location:
            errors.append("Location is required.")
        
        if not isinstance(self.attendees, int) or self.attendees < 0:
            errors.append("Attendees must be a non-negative integer.")
        
        if errors:
            raise ValidationError(errors)
    
    def save(self, session):
        self.validate()
        session.add(self)
        session.commit()
    

SECRET_KEY = os.environ.get('SECRET_KEY', 'my_secret_key')

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
        return bcrypt.checkpw(password.encode('utf-8'), self.password)    

    def create_token(self):
        token = jwt.encode({
            'id' : self.id,
            'exp' : datetime.utcnow() + timedelta(days=30),
            'department': self.department
        }, SECRET_KEY, algorithm='HS256')
        return token
    
    def verify_token(self, token):
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            return data
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
        
    def validate(self):
        errors = []
               
        if not isinstance(self.employee_number, int):
            errors.append("Employee number must be an integer.")
        
        if not self.name:
            errors.append("Name is required.")
        
        if not self.email or not re.match(r"[^@]+@[^@]+\.[^@]+", self.email):
            errors.append("Valid email is required.")
               
        if not self.department:
            errors.append("Department is required.")

        if not self.password:
            errors.append("password is required.")    

        if errors:
            raise ValidationError(errors)
    
    def save(self, session):
        self.validate()
        session.add(self)
        session.commit()

    def __repr__(self):
        return f'Collaborator {self.name}'
    