import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from controllers import ClientHandler, ContractHandler, EventHandler, CollaboratorHandler
from click.testing import CliRunner

@pytest.fixture(scope='module')
def engine():
    return create_engine('sqlite:///:memory:', echo=True)

@pytest.fixture(scope='module')
def tables(engine):
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)

@pytest.fixture(scope='function')
def session(engine, tables):
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

@pytest.fixture
def runner():
    return CliRunner()

@pytest.fixture
def client_handler(session, monkeypatch):
    token = "dummy_token"
    
    handler = ClientHandler(session=session, token=token)
    
    monkeypatch.setattr(handler, "token_is_valid", lambda: True)
    monkeypatch.setattr(handler, "check_permission", lambda department: True)
    monkeypatch.setattr(handler, "collaborator", type('obj', (object,), {'id': 1, 'department': 'commercial'}))
    
    return handler

@pytest.fixture
def contract_handler(session, monkeypatch):
    token = "dummy_token"
    
    handler = ContractHandler(session=session, token=token)
    
    monkeypatch.setattr(handler, "token_is_valid", lambda: True)
    monkeypatch.setattr(handler, "check_permission", lambda department: True)
    monkeypatch.setattr(handler, "collaborator", type('obj', (object,), {'id': 1, 'department': 'gestion'}))
    
    return handler

@pytest.fixture
def event_handler(session, monkeypatch):
    token = "dummy_token"
    
    handler = EventHandler(session=session, token=token)
    
    monkeypatch.setattr(handler, "token_is_valid", lambda: True)
    monkeypatch.setattr(handler, "check_permission", lambda department: True)
    monkeypatch.setattr(handler, "collaborator", type('obj', (object,), {'id': 1, 'department': 'support'}))
    
    return handler

@pytest.fixture
def collaborator_handler(session, monkeypatch):
    token = "dummy_token"
    
    handler = CollaboratorHandler(session=session, token=token)
    
    monkeypatch.setattr(handler, "token_is_valid", lambda: True)
    monkeypatch.setattr(handler, "check_permission", lambda department: True)
    monkeypatch.setattr(handler, "collaborator", type('obj', (object,), {'id': 1, 'department': 'gestion'}))
    
    return handler