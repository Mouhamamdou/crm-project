import pytest
from datetime import datetime, timedelta
from models import Client, Contract, Event, ValidationError, Collaborator
from views import add_event
from unittest.mock import patch

def test_get_all_events(event_handler, session):
    client = Client(name='Client 1', email='client1@gmail.com', telephone='+1234567890', company_name='Company 1', commercial_id=1)
    session.add(client)
    session.commit()
    
    contract = Contract(client_id=client.id, commercial_id=1, total_amount=1000, amount_due=500, status=True)
    session.add(contract)
    session.commit()
    
    event1 = Event(contract_id=contract.id, client_id=client.id, end_date=datetime.utcnow() + timedelta(days=1), location='Location 1', attendees=100)
    event2 = Event(contract_id=contract.id, client_id=client.id, end_date=datetime.utcnow() + timedelta(days=2), location='Location 2', attendees=200)
    session.add_all([event1, event2])
    session.commit()

    events = event_handler.get_all_events()
    assert len(events) == 2


def test_create_event(event_handler, session):
    client = Client(name='Client 4', email='client4@gmail.com', telephone='+1234567893', company_name='Company 4', commercial_id=1)
    session.add(client)
    session.commit()
    
    contract = Contract(client_id=client.id, commercial_id=1, total_amount=3000, amount_due=1000, status=True)
    session.add(contract)
    session.commit()

    data = {
        'contract_id': contract.id,
        'end_date': datetime.utcnow() + timedelta(days=3),
        'location': 'Location 3',
        'attendees': 150,
        'notes': 'Event notes'
    }
    
    event = event_handler.create_event(data)
    assert event.id is not None
    assert event.contract_id == contract.id
    assert event.client_id == client.id
    assert event.location == 'Location 3'
    assert event.attendees == 150


def test_event_model(session):
    client = Client(name='Client 8', email='client8@gmail.com', telephone='+1234567890', company_name='Cli8Co', commercial_id=1)
    client.save(session)

    contract = Contract(client_id=client.id, commercial_id=1, total_amount=1000, amount_due=500, status=True)
    contract.save(session)

    event = Event(contract_id=contract.id, client_id=client.id, end_date=datetime.utcnow() + timedelta(days=1), location='Location 4', attendees=10)
    event.save(session)

    retrieved_event = session.query(Event).filter_by(contract_id=contract.id).first()
    assert retrieved_event is not None
    assert retrieved_event.location == 'Location 4'
    assert retrieved_event.attendees == 10


def test_event_validation(session):
    event = Event(contract_id=1, client_id=1, end_date=datetime.utcnow() - timedelta(days=1), location='', attendees=-5)
    with pytest.raises(ValidationError):
        event.save(session)

'''
def test_add_event(session, runner, contract_handler):
    collaborator = Collaborator(
        name='Collab', 
        email='collab@gmail.com', 
        department='commercial', 
        password='password123'
        )
    collaborator.set_password('password123')
    collaborator.save(session)
    token = collaborator.create_token()

    client = Client(
        name='Client A', 
        email='clienta@example.com', 
        telephone='+1234567890', 
        company_name='ClientCo', 
        commercial_id=collaborator.id
        )
    client.save(session)

    contract = Contract(
        client_id=client.id, 
        commercial_id=collaborator.id, 
        total_amount=500, 
        amount_due = 25, 
        status=True
        )
    contract.save(session)

    data = {
        'contract_id': contract.id,
        'end_date': '2025-05-12',
        'location': 'Paris',
        'attendees': 58,
        'notes': 'Notes for the event'
    }

    input_data = f"{data['contract_id']}\n{data['end_date']}\n{data['location']}\n{data['attendees']}\n{data['notes']}\n"

    with patch('views.event_views.SessionLocal', return_value=session):
        result = runner.invoke(add_event, args=[token], input=input_data)
        assert 'Event added successfully.' in result.output
        
'''