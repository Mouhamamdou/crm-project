import pytest
from models import Collaborator, ValidationError
from unittest.mock import patch
from views import add_collaborator, update_collaborator, show_collaborators, delete_collaborator


def test_get_all_collaborators(collaborator_handler, session):
    collaborator1 = Collaborator(name='Collab 1', email='collab1@gmail.com', department='gestion', password='password123')
    collaborator1.set_password('password123')
    collaborator2 = Collaborator(name='Collab 2', email='collab2@gmail.com', department='support', password='password123')
    collaborator2.set_password('password123')
    session.add_all([collaborator1, collaborator2])
    session.commit()

    collaborators = collaborator_handler.get_all_collaborators()
    assert len(collaborators) == 2

def test_create_collaborator(collaborator_handler, session):
    data = {
        'name': 'Collab 3',
        'email': 'collab3@gmail.com',
        'department': 'commercial',
        'password': 'password123'
    }
    
    collaborator = collaborator_handler.create_collaborator(data)
    assert collaborator.id is not None
    assert collaborator.name == 'Collab 3'
    assert collaborator.email == 'collab3@gmail.com'
    assert collaborator.department == 'commercial'

def test_update_collaborator(collaborator_handler, session):
    collaborator = Collaborator(name='Collab 4', email='collab4@gmail.com', department='support', password='password123')
    collaborator.set_password('password123')
    session.add(collaborator)
    session.commit()

    data = {
        'name': 'Collab 8',
        'email': 'collab8@gmail.com',
        'department': 'support',
        'password': 'password123'
    }

    updated_collaborator = collaborator_handler.update_collaborator(collaborator.id, data)
    assert updated_collaborator.name == 'Collab 8'
    assert updated_collaborator.email == 'collab8@gmail.com'
    assert updated_collaborator.department == 'support'
    assert updated_collaborator.check_password('password123')

def test_delete_collaborator(collaborator_handler, session):
    collaborator = Collaborator(name='Collab 7', email='collab7@gmail.com', department='gestion', password='password123')
    collaborator.set_password('password123')
    session.add(collaborator)
    session.commit()

    response, status_code = collaborator_handler.delete_collaborator(collaborator.id)
    assert response['message'] == 'Collaborator deleted successfully'
    assert status_code == 200
    assert session.query(Collaborator).filter_by(id=collaborator.id).first() is None

def test_collaborator_model(session):
    collaborator = Collaborator(name='Collab 9', email='collab9@gmail.com', department='support', password='password123')
    collaborator.set_password('password123')
    collaborator.save(session)

    retrieved_collaborator = session.query(Collaborator).filter_by(email='collab9@gmail.com').first()
    assert retrieved_collaborator is not None
    assert retrieved_collaborator.name == 'Collab 9'
    assert retrieved_collaborator.check_password('password123')

def test_collaborator_validation(session):
    collaborator = Collaborator(name='', email='invalid_email', department='', password='')
    with pytest.raises(ValidationError):
        collaborator.save(session)

'''
def test_add_collaborator_view(session, runner, collaborator_handler):
    collaborator = Collaborator(
        name='Collab', 
        email='collab@gmail.com', 
        department='gestion', 
        password='password123'
    )
    collaborator.set_password('password123')
    collaborator.save(session)
    token = collaborator.create_token()

    input_data = "Collab\ncollab@gmail.com\ngestion\npassword123\n"

    with patch('cli_views.SessionLocal', return_value=session):
        result = runner.invoke(add_collaborator, args=[token], input=input_data)
    
    assert 'Collaborator added successfully.' in result.output

'''