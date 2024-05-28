from models import Client, Contract, Event, Collaborator


class ClientHandler:

    def __init__(self, session):
        self.session = session

    def get_all_clients(self):
        return self.session.query(Client).all()
    
    def create_client(self, name, email, telephone, company_name, commercial_id):
        client = Client(
            name=name, 
            email=email, 
            telephone=telephone, 
            company_name=company_name, 
            commercial_id=commercial_id
        )
        self.session.add(client)
        self.session.commit()
        return client

    def update_client(self, client_id, name, email, telephone, company_name, commercial_id):
        client = self.session.query(Client).filter_by(id=client_id).first()
        if client:
            client.name = name
            client.email = email
            client.telephone = telephone
            client.company_name = company_name
            client.commercial_id = commercial_id
            self.session.commit()
            return client
        return None


class ContractHandler:
    
    def __init__(self, session):
        self.session = session

    def get_all_contracts(self):
        return self.session.query(Contract).all()
    
    def create_contract(self, client_id, commercial_id, total_amount, amount_due, status):
        contract = Contract(
            client_id=client_id, 
            commercial_id=commercial_id, 
            total_amount=total_amount, 
            amount_due=amount_due, 
            status=status
        )
        self.session.add(contract)
        self.session.commit()
        return contract

    def update_contract(self, contract_id, client_id, commercial_id, total_amount, amount_due, status):
        contract = self.session.query(Contract).filter_by(id=contract_id).first()
        if contract:
            contract.client_id = client_id
            contract.commercial_id = commercial_id
            contract.total_amount = total_amount
            contract.amount_due = amount_due
            contract.status = status
            self.session.commit()
            return contract
        return None


class EventHandler:
    
    def __init__(self, session):
        self.session = session

    def get_all_events(self):
        return self.session.query(Event).all()
    
    def create_event(self, contract_id, client_id, start_date, end_date, support_contact_id, location, attendees, notes):
        event = Event(
            contract_id=contract_id, 
            client_id=client_id, 
            start_date=start_date, 
            end_date=end_date, 
            support_contact_id=support_contact_id, 
            location=location, 
            attendees=attendees, 
            notes=notes
        )
        self.session.add(event)
        self.session.commit()
        return event

    def update_event(self, event_id, contract_id, client_id, start_date, end_date, support_contact_id, location, attendees, notes):
        event = self.session.query(Event).filter_by(id=event_id).first()
        if event:
            event.contract_id = contract_id
            event.client_id = client_id
            event.start_date = start_date
            event.end_date = end_date
            event.support_contact_id = support_contact_id
            event.location = location
            event.attendees = attendees
            event.notes = notes
            self.session.commit()
            return event
        return None


class CollaboratorHandler:

    def __init__(self, session):
        self.session = session

    def get_all_collaborators(self):
        return self.session.query(Collaborator).all()
    
    def create_collaborator(self, employee_number, name, email, department, password):
        collaborator = Collaborator(
            employee_number=employee_number,
            name=name,
            email=email,
            department=department
        )
        collaborator.set_password(password)
        self.session.add(collaborator)
        self.session.commit()
        return collaborator
    
    def update_collaborator(self, collaborator_id, employee_number, name, email, department, password):
        collaborator = self.session.query(Collaborator).filter_by(id=collaborator_id).first()
        if collaborator:
            collaborator.employee_number = employee_number
            collaborator.name = name
            collaborator.email = email
            collaborator.department = department
            collaborator.set_password(password)
            self.session.commit()
            return collaborator
        return None
