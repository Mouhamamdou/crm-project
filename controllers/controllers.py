from models import Client, Contract, Event, Collaborator, ValidationError
from datetime import datetime


class BaseHandler:

    def __init__(self, session, token):
        self.session = session
        collab = Collaborator()
        self.token_data = collab.verify_token(token)
        if self.token_data and self.token_data != 'expired':
            self.collaborator = session.query(Collaborator).get(self.token_data['id'])
        else:
            self.collaborator = None

    def has_permission(self, department):
        if not self.collaborator:
            return False
        return self.collaborator.department == department  

    def token_is_valid(self):
        if self.token_data and self.token_data != 'expired':
            return None
        return {'token is expired. Please log in again.'}, 401

    def check_permission(self, department):
        token_check = self.token_is_valid()
        if token_check:
            return token_check
        if not self.has_permission(department):
            return {'Permission denied'}, 403
        return None


class ClientHandler(BaseHandler):

    def get_all_clients(self):
        permission_checked = self.check_permission('commercial')
        if permission_checked:
            return permission_checked
        return self.session.query(Client).all()
    
    def create_client(self, data):
        permission_checked = self.check_permission('commercial')
        if permission_checked:
            return permission_checked
        
        commercial_id = self.collaborator.id

        client = Client(
            name=data.get('name'), 
            email=data.get('email'), 
            telephone=data.get('telephone'), 
            company_name=data.get('company_name'), 
            commercial_id=commercial_id
        )

        try:
            client.save(self.session)
        except ValidationError as e:
            return {'errors': e.args[0]}, 400
        
        return client

    def update_client(self, client_id, data):
        permission_checked = self.check_permission('commercial')
        if permission_checked:
            permission_checked

        client = self.session.query(Client).filter_by(id=client_id).first()
        if client:
            client.name = data.get('name', client.name)
            client.email = data.get('email', client.email)
            client.telephone = data.get('telephone', client.telephone)
            client.company_name = data.get('company_name', client.company_name)
            client.commercial_id = data.get('commercial_id', client.commercial_id)
            client.last_update = datetime.datetime.utcnow()

            try:
                client.save(self.session)
            except ValidationError as e:
                return {'errors': e.args[0]}, 400
            
            return client
        return None


class ContractHandler(BaseHandler):

    def get_all_contracts(self):
        permission_check = self.check_permission('gestion')
        if permission_check:
            return permission_check
        return self.session.query(Contract).all()
    
    def create_contract(self, data):
        permission_check = self.check_permission('gestion')
        if permission_check:
            return permission_check
        
        client = self.session.query(Client).get(data.get('client_id'))
        
        contract = Contract(
            client_id=data.get('client_id'), 
            commercial_id=client.commercial_id, 
            total_amount=data.get('total_amount'), 
            amount_due=data.get('amount_due'), 
            status=data.get('status')
        )
        
        try:
            contract.save(self.session)
        except ValidationError as e:
            return {'errors': e.args[0]}, 400

        return contract

    def update_contract(self, contract_id, data):
        permission_check = self.check_permission('gestion')
        if permission_check:
            return permission_check
        
        contract = self.session.query(Contract).filter_by(id=contract_id).first()
        if contract:
            contract.client_id = data.get('client_id', contract.client_id)
            contract.commercial_id = data.get('commercial_id', contract.commercial_id)
            contract.total_amount = data.get('total_amount', contract.total_amount)
            contract.amount_due = data.get('amount_due', contract.amount_due)
            contract.status = data.get('status', contract.status)

            try:
                contract.save(self.session)
            except ValidationError as e:
                return {'errors': e.args[0]}, 400

            return contract
        return None


class EventHandler(BaseHandler):

    def get_all_events(self):
        
        return self.session.query(Event).all()
    
    def create_event(self, data):
        permission_check = self.check_permission('commercial')
        if permission_check:
            return permission_check
        
        contract = self.session.query(Contract).get(data.get('contract_id'))
        
        event = Event(
            contract_id=data.get('contract_id'),
            client_id=contract.client_id, 
            start_date=data.get('start_date'), 
            end_date=data.get('end_date'), 
            #support_contact_id=data.get('support_contact_id'), 
            location=data.get('location'), 
            attendees=data.get('attendees'), 
            notes=data.get('notes')
        )

        try:
            event.save(self.session)
        except ValidationError as e:
            return {'errors': e.args[0]}, 400
    
        return event

    def update_event(self, event_id, data):
        permission_check = self.check_permission('commercial')
        if permission_check:
            return permission_check
        
        event = self.session.query(Event).filter_by(id=event_id).first()
        if event:
            event.contract_id = data.get('contract_id', event.contract_id)
            event.client_id = data.get('client_id', event.client_id)
            event.start_date = data.get('start_date', event.start_date)
            event.end_date = data.get('end_date', event.end_date)
            #event.support_contact_id = data.get('support_contact_id', event.support_contact_id)
            event.location = data.get('location', event.location)
            event.attendees = data.get('attendees', event.attendees)
            event.notes = data.get('notes', event.notes)

            try:
                event.save(self.session)
            except ValidationError as e:
                return {'errors': e.args[0]}, 400
        
            return event
        return None


class CollaboratorHandler(BaseHandler):

    def get_all_collaborators(self):
        permission_check = self.check_permission('gestion')
        if permission_check:
            return permission_check
        return self.session.query(Collaborator).all()
    
    def create_collaborator(self, data):
        permission_check = self.check_permission('gestion')
        if permission_check:
            return permission_check
        
        collaborator = Collaborator(
            employee_number=data.get('employee_number'),
            name=data.get('name'),
            email=data.get('email'),
            department=data.get('department')
        )
        collaborator.set_password(data.get('password'))
        self.session.add(collaborator)
        self.session.commit()
        return collaborator
    
    def update_collaborator(self, collaborator_id, data):
        permission_check = self.check_permission('gestion')
        if permission_check:
            return permission_check
        
        collaborator = self.session.query(Collaborator).filter_by(id=collaborator_id).first()
        if collaborator:
            collaborator.employee_number = data.get('employee_number', collaborator.employee_number)
            collaborator.name = data.get('name', collaborator.name)
            collaborator.email = data.get('email', collaborator.email)
            collaborator.department = data.get('department', collaborator.department)
            collaborator.set_password(data.get('password', collaborator.password))
            self.session.commit()
            return collaborator
        return None
