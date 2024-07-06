from models import Client, Contract, Event, Collaborator, ValidationError
from datetime import datetime
from sentry_sdk import capture_exception


class BaseHandler:
    """
    Base handler class for managing session and token authentication.
    """
    def __init__(self, session, token):
        """
        Initializes the BaseHandler with session and token.
        
        Args:
            session: The database session.
            token: The JWT token.
        """
        self.session = session
        collab = Collaborator()
        self.token_data = collab.verify_token(token)
        if self.token_data and self.token_data != 'expired':
            self.collaborator = session.query(Collaborator).get(self.token_data['id'])
        else:
            self.collaborator = None

    def token_is_valid(self):
        """
        Checks if the token is valid and not expired.
        
        Raises:
            Exception: If the token is expired.
        """
        if not self.token_data or self.token_data == 'expired':
            raise Exception('Token is expired. Please log in again.')

    def check_permission(self, department):
        """
        Checks if the collaborator has permission based on their department.
        
        Args:
            department (str): The required department for permission.
        
        Raises:
            Exception: If the collaborator does not have the required permission.
        """
        self.token_is_valid()
        if not self.collaborator or self.collaborator.department != department:
            raise Exception('Permission denied')


class ClientHandler(BaseHandler):
    """
    Handler class for managing clients.
    """
    def get_all_clients(self): 
        """
        Retrieves all clients from the database.
        
        Returns:
            List of all clients.
        """
        self.token_is_valid()
        try:
            return self.session.query(Client).all()
        except Exception as e:
            capture_exception(e)
            raise
    
    def create_client(self, data):
        """
        Creates a new client in the database.
        
        Args:
            data (dict): The client data.
        
        Returns:
            The created client instance.
        """
        self.check_permission('commercial')
        
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
            return client
        except Exception as e:
            capture_exception(e)
            raise

    def update_client(self, client_id, data):
        """
        Updates an existing client in the database.
        
        Args:
            client_id (int): The ID of the client to update.
            data (dict): The updated client data.
        
        Returns:
            The updated client instance.
        """
        self.check_permission('commercial')

        client = self.session.query(Client).filter_by(id=client_id).first()

        if not client:
            raise Exception('Client not found')

        if client.commercial_id != self.collaborator.id:
            raise Exception('This commercial is not the responsible of this client')

        client.name = data.get('name', client.name)
        client.email = data.get('email', client.email)
        client.telephone = data.get('telephone', client.telephone)
        client.company_name = data.get('company_name', client.company_name)
        client.last_update = datetime.utcnow()

        try:
            client.save(self.session)  
            return client
        except Exception as e:
            capture_exception(e)
            raise


class ContractHandler(BaseHandler):
    """
    Handler class for managing contracts.
    """
    def get_all_contracts(self):
        """
        Retrieves all contracts from the database.
        
        Returns:
            List of all contracts.
        """
        self.token_is_valid()
        try:
            return self.session.query(Contract).all()
        except Exception as e:
            capture_exception(e)
            raise
    
    def filter_contacts_not_paid(self):
        """
        Retrieves all contracts that are not paid.
        
        Returns:
            List of contracts not paid.
        """
        self.check_permission("commercial")
        try:
            return self.session.query(Contract).filter_by(status=False)
        except Exception as e:
            capture_exception(e)
            raise
    
    def create_contract(self, data):
        """
        Creates a new contract in the database.
        
        Args:
            data (dict): The contract data.
        
        Returns:
            The created contract instance.
        """
        self.check_permission('gestion')
        
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
            return contract
        except Exception as e:
            capture_exception(e)
            raise

    def update_contract(self, contract_id, data):
        """
        Updates an existing contract in the database.
        
        Args:
            contract_id (int): The ID of the contract to update.
            data (dict): The updated contract data.
        
        Returns:
            The updated contract instance.
        """        
        contract = self.session.query(Contract).filter_by(id=contract_id).first()

        self.token_is_valid()
        if self.collaborator.department != 'gestion' and contract.commercial_id != self.collaborator.id:
            raise Exception('You do not have permission to modify this contract')

        if not contract:
            raise Exception('Contract not found')
      
        contract.client_id = data.get('client_id', contract.client_id)
        contract.commercial_id = data.get('commercial_id', contract.commercial_id)
        contract.total_amount = data.get('total_amount', contract.total_amount)
        contract.amount_due = data.get('amount_due', contract.amount_due)
        contract.status = data.get('status', contract.status)

        try:
            contract.save(self.session)
            return contract
        except Exception as e:
            capture_exception(e)
            raise


class EventHandler(BaseHandler):
    """
    Handler class for managing events.
    """
    def get_all_events(self):
        """
        Retrieves all events from the database.
        
        Returns:
            List of all events.
        """
        self.token_is_valid()
        try:
            return self.session.query(Event).all()
        except Exception as e:
            capture_exception(e)
            raise
    
    def filter_events_without_support(self):
        """
        Retrieves all events without a support contact.
        
        Returns:
            List of events without a support contact.
        """
        self.check_permission('gestion')
        try:
            return self.session.query(Event).filter_by(support_contact_id=None)
        except Exception as e:
            capture_exception(e)
            raise

    def filter_my_events(self):
        """
        Retrieves all events assigned to the current collaborator.
        
        Returns:
            List of events assigned to the current collaborator.
        """
        self.check_permission('support')
        try:
            return self.session.query(Event).filter_by(support_contact_id=self.collaborator.id)
        except Exception as e:
            capture_exception(e)
            raise

    def create_event(self, data):
        """
        Creates a new event in the database.
        
        Args:
            data (dict): The event data.
        
        Returns:
            The created event instance.
        """
        self.check_permission('commercial')
 
        contract = self.session.query(Contract).get(data.get('contract_id'))

        if contract.commercial_id != self.collaborator.id :
            raise Exception('You do not have permission to create the event')
        
        event = Event(
            contract_id=data.get('contract_id'),
            client_id=contract.client_id, 
            end_date=data.get('end_date'), 
            location=data.get('location'), 
            attendees=data.get('attendees'), 
            notes=data.get('notes')
        )

        try:
            event.save(self.session)
            return event
        except Exception as e:
            capture_exception(e)
            raise

    def add_support_contact(self, event_id, support_contact_id):
        """
        Adds a support contact to an existing event.
        
        Args:
            event_id (int): The ID of the event.
            support_contact_id (int): The ID of the support contact to add.
        
        Returns:
            The updated event instance.
        """
        self.check_permission('gestion')

        event = self.session.query(Event).filter_by(id=event_id).first()

        if not event:
            raise Exception('Event not found')

        support_contact = self.session.query(Collaborator).filter_by(id=support_contact_id).first()

        if support_contact.department != 'support':
                raise Exception('Support contact must be in support department')
        
        event.support_contact_id = support_contact_id
        self.session.commit()
        return event

    def update_event(self, event_id, data):
        """
        Updates an existing event in the database.
        
        Args:
            event_id (int): The ID of the event to update.
            data (dict): The updated event data.
        
        Returns:
            The updated event instance.
        """
        self.check_permission('support')
        
        event = self.session.query(Event).filter_by(id=event_id).first()
        
        if not event:
            raise Exception('Event not found')

        if event.support_contact_id != self.collaborator.id:
            raise Exception('This support contact is not the responsible of this event') 
 
        event.end_date = data.get('end_date', event.end_date)
        event.location = data.get('location', event.location)
        event.attendees = data.get('attendees', event.attendees)
        event.notes = data.get('notes', event.notes)

        try:
            event.save(self.session)
            return event
        except Exception as e:
            capture_exception(e)
            raise


class CollaboratorHandler(BaseHandler):
    """
    Handler class for managing collaborators.
    """    
    def get_all_collaborators(self):
        self.token_is_valid
        try:
            return self.session.query(Collaborator).all()
        except Exception as e:
            capture_exception(e)
            raise
    
    def create_collaborator(self, data):
        """
        Creates a new collaborator in the database.
        
        Args:
            data (dict): The collaborator data.
        
        Returns:
            The created collaborator instance.
        """
        self.check_permission('gestion')
        
        collaborator = Collaborator(
            name=data.get('name'),
            email=data.get('email'),
            department=data.get('department')
        )
        collaborator.set_password(data.get('password'))
        self.session.add(collaborator)
        self.session.commit()
        return collaborator
    
    def update_collaborator(self, collaborator_id, data):
        """
        Updates an existing collaborator in the database.
        
        Args:
            collaborator_id (int): The ID of the collaborator to update.
            data (dict): The updated collaborator data.
        
        Returns:
            The updated collaborator instance.
        """
        self.check_permission('gestion')
        
        collaborator = self.session.query(Collaborator).filter_by(id=collaborator_id).first()

        if not collaborator:
            raise Exception('Collaborator not found')
        
        collaborator.name = data.get('name', collaborator.name)
        collaborator.email = data.get('email', collaborator.email)
        collaborator.department = data.get('department', collaborator.department)
        collaborator.set_password(data.get('password', collaborator.password))

        try:
            collaborator.save(self.session)
            return collaborator
        except Exception as e:
            capture_exception(e)
            raise

    def delete_collaborator(self, collaborator_id):
        """
        Deletes a collaborator from the database.
        
        Args:
            collaborator_id (int): The ID of the collaborator to delete.
        
        Returns:
            dict: A success message.
        """
        self.check_permission('gestion')
        
        collaborator = self.session.query(Collaborator).filter_by(id=collaborator_id).first()

        if not collaborator:
            raise Exception('Collaborator not found')
        
    
        self.session.delete(collaborator)
        self.session.commit()
        return {'message': 'Collaborator deleted successfully'}, 200
