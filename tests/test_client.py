import pytest
from datetime import datetime
from models import Client, ValidationError, Collaborator
from unittest.mock import patch
from views.cli_views import login, register, add_client, update_client, show_clients
from click.testing import CliRunner

def test_get_all_clients(client_handler, session):
    client1 = Client(name='Client 1', email='client1@gmail.com', telephone='+1234567890', company_name='Company 1', commercial_id=1)
    client2 = Client(name='Client 2', email='client2@gmail.com', telephone='+1234567891', company_name='Company 2', commercial_id=1)
    session.add_all([client1, client2])
    session.commit()

    clients = client_handler.get_all_clients()
    assert len(clients) == 2


def test_create_client(client_handler):
    data = {
        'name': 'Client',
        'email': 'client@gmail.com',
        'telephone': '+1234567892',
        'company_name': 'Company'
    }
    
    client = client_handler.create_client(data)
    assert client.id is not None
    assert client.name == 'Client'
    assert client.email == 'client@gmail.com'
    assert client.telephone == '+1234567892'
    assert client.company_name == 'Company'


def test_update_client(client_handler, session):
    client = Client(name='Client', email='client@gmail.com', telephone='+1234567893', company_name='Company', commercial_id=1)
    session.add(client)
    session.commit()

    data = {
        'name': 'Client 2',
        'email': 'client2@gmail.com',
        'telephone': '+1234567894',
        'company_name': 'Updated Company'
    }

    updated_client = client_handler.update_client(client.id, data)
    assert updated_client.name == 'Client 2'
    assert updated_client.email == 'client2@gmail.com'
    assert updated_client.telephone == '+1234567894'
    assert updated_client.company_name == 'Updated Company'
    assert updated_client.last_update is not None


def test_client_model(session):
    client = Client(name='Allou', email='allou@gmail.com', telephone='+1234567890', company_name='AllCo', commercial_id=1)
    client.save(session)

    retrieved_client = session.query(Client).filter_by(email='allou@gmail.com').first()
    assert retrieved_client is not None
    assert retrieved_client.name == 'Allou'
    assert retrieved_client.telephone == '+1234567890'
    assert retrieved_client.company_name == 'AllCo'


def test_client_validation(session):
    client = Client(name='Fallou', email='invalid_email', telephone='+1234567890', company_name='AllCo', commercial_id=1)
    with pytest.raises(ValidationError):
        client.save(session)


def test_register(session, runner):
    collaborator_data = {
        'name': 'Client',
        'email': 'client@gmail.com',
        'password': 'password123',
        'department': 'gestion'
    }
    with patch('views.cli_views.session', session):
        result = runner.invoke(register, input=f"{collaborator_data['name']}\n{collaborator_data['email']}\n{collaborator_data['password']}\n{collaborator_data['department']}\n")
        assert 'Registration successful!' in result.output
        assert session.query(Collaborator).filter_by(email='client@gmail.com').first() is not None


def test_login(session, runner):
    collaborator = Collaborator(name='collab', email='collab@gmail.com', password='password123', department='gestion')
    collaborator.set_password('password123')
    session.add(collaborator)
    session.commit()

    data = {
        'email': 'collab@gmail.com',
        'password': 'password123'
    }

    with patch('views.cli_views.session', session):
        result = runner.invoke(login, input=f"{data['email']}\n{data['password']}\n")

        assert 'Login successful!' in result.output

'''
def test_add_client_views(session, runner, client_handler):

    collaborator = Collaborator(
        name='Collab', 
        email='collab2@gmail.com', 
        department='commercial', 
        password='password123'
        )
    collaborator.set_password('password123')
    collaborator.save(session)
    token = collaborator.create_token()

    data = {
        'name': 'Client',
        'email': 'client@gmail.com',
        'telephone': '+123456789',
        'company_name': 'CliCo'
    }

    input_data = f"{data['name']}\n{data['email']}\n{data['telephone']}\n{data['company_name']}\n"

    with patch('views.cli_views.SessionLocal', return_value=session):
        result = runner.invoke(add_client, args=[token], input=input_data)
        print("voir le résultat"+result.output)
        assert 'Client added successfully.' in result.output


def test_update_client_view(session, client_handler, runner):

    collaborator = Collaborator(
        name='Collab', 
        email='collab2@gmail.com', 
        department='commercial', 
        password='password123'
    )
    collaborator.set_password('password123')
    collaborator.save(session)

    token = collaborator.create_token()

    client = Client(
        name='Old Client',
        email='oldclient@gmail.com',
        telephone='+1234567890',
        company_name='OldCompany',
        commercial_id=collaborator.id
    )
    client.save(session)
    
    new_data = {
        'name': 'New Client',
        'email': 'newclient@gmail.com',
        'telephone': '+0987654321',
        'company_name': 'NewCompany'
    }
    input_data = f"{client.id}\n{new_data['name']}\n{new_data['email']}\n{new_data['telephone']}\n{new_data['company_name']}\n"

    result = runner.invoke(update_client, args=[token], input=input_data)

    assert 'Client updated successfully.' in result.output

'''