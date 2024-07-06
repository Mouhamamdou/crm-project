import pytest
from datetime import datetime
from models import Client, Contract, ValidationError, Collaborator
from unittest.mock import patch
from views.con_views import add_contract, update_contract

def test_get_all_contracts(contract_handler, session):
    client = Client(name='Client 1', email='client1@gmail.com', telephone='+1234567890', company_name='Company 1', commercial_id=1)
    session.add(client)
    session.commit()
    
    contract1 = Contract(client_id=client.id, commercial_id=1, total_amount=1000, amount_due=500, status=True)
    contract2 = Contract(client_id=client.id, commercial_id=1, total_amount=2000, amount_due=1500, status=False)
    session.add_all([contract1, contract2])
    session.commit()

    contracts = contract_handler.get_all_contracts()
    assert len(contracts) == 2

def test_create_contract(contract_handler, session):
    client = Client(name='Client 3', email='client3@gmail.com', telephone='+1234567892', company_name='Company 3', commercial_id=1)
    session.add(client)
    session.commit()

    data = {
        'client_id': client.id,
        'total_amount': 3000,
        'amount_due': 1000,
        'status': False
    }
    
    contract = contract_handler.create_contract(data)
    assert contract.id is not None
    assert contract.client_id == client.id
    assert contract.total_amount == 3000
    assert contract.amount_due == 1000
    assert contract.status is False

def test_update_contract(contract_handler, session):
    client = Client(name='Client 4', email='client4@gmail.com', telephone='+1234567893', company_name='Company 4', commercial_id=1)
    session.add(client)
    session.commit()
    
    contract = Contract(client_id=client.id, commercial_id=1, total_amount=4000, amount_due=2000, status=True)
    session.add(contract)
    session.commit()

    data = {
        'total_amount': 5000,
        'amount_due': 2500,
        'status': False
    }

    updated_contract = contract_handler.update_contract(contract.id, data)
    assert updated_contract.total_amount == 5000
    assert updated_contract.amount_due == 2500
    assert updated_contract.status is False

def test_contract_model(session):
    client = Client(name='Client 5', email='client5@gmail.com', telephone='+1234567890', company_name='CliCo', commercial_id=1)
    client.save(session)

    contract = Contract(client_id=client.id, commercial_id=1, total_amount=1000, amount_due=500, status=True)
    contract.save(session)

    retrieved_contract = session.query(Contract).filter_by(client_id=client.id).first()
    assert retrieved_contract is not None
    assert retrieved_contract.total_amount == 1000
    assert retrieved_contract.amount_due == 500
    assert retrieved_contract.status is True

def test_contract_validation(session):
    contract = Contract(client_id=1, commercial_id=1, total_amount=-100, amount_due=500, status=True)
    with pytest.raises(ValidationError):
        contract.save(session)

def test_add_contract_view(session, runner, contract_handler):

    collaborator = Collaborator(
        name='Collab', 
        email='collab@gmail.com', 
        department='gestion', 
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
        commercial_id=1
        )
    client.save(session)

    data = {
        'client_id': client.id,
        'total_amount': 1000,
        'amount_due': 500,
        'status': True
    }

    input_data = f"{data['client_id']}\n{data['total_amount']}\n{data['amount_due']}\n{data['status']}\n"

    with patch('views.con_views.SessionLocal', return_value=session):
        result = runner.invoke(add_contract, args=[token], input=input_data)
        print("voir le résultat de contrat"+result.output)
        assert 'Contract added successfully.' in result.output

'''
def test_update_contract_view(session, runner, contract_handler):

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
        commercial_id=1
    )
    client.save(session)

    contract = Contract(
        client_id=client.id,
        total_amount=1000,
        amount_due=500,
        status=True,
        #commercial_id=collaborator.id
    )
    contract.save(session)

    new_data = {
        'contract_id': contract.id,
        'total_amount': 1500,
        'amount_due': 750,
        'status': False
    }

    input_data = f"{new_data['contract_id']}\n{new_data['total_amount']}\n{new_data['amount_due']}\n{new_data['status']}\n"

    with patch('views.con_views.SessionLocal', return_value=session):
        result = runner.invoke(update_contract, args=[token], input=input_data)

    assert 'Contract updated successfully.' in result.output
'''