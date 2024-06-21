import click
from rich.console import Console
from rich.table import Table
from models import Collaborator, Client
from controllers import ContractHandler
from config.database import SessionLocal
from sentry_sdk import capture_exception


console = Console()

session = SessionLocal()


def add_contract(token):
    client_id = click.prompt("Client ID", type=int)
    total_amount = click.prompt("Total Amount", type=float)
    amount_due = click.prompt("Amount Due", type=float)
    status = click.prompt("Status (true/false)").lower() in ('true', 'yes', '1')

    handler = ContractHandler(session, token)
    data = {
        'client_id': client_id,
        'total_amount': total_amount,
        'amount_due': amount_due,
        'status': status
    }

    try:
        handler.create_contract(data)
        console.print("[green]Contract added successfully.[/green]")
    except Exception as e:
        capture_exception(e)
        console.print(f"[red]{e}[/red]")

def update_contract(token):
    contract_id = click.prompt("Contract ID")
    total_amount = click.prompt("Total Amount", type=float)
    amount_due = click.prompt("Amount Due", type=float)
    status = click.prompt("Status (true/false)").lower() in ('true', 'yes', '1')

    handler = ContractHandler(session, token)
    data = {
        'total_amount': total_amount,
        'amount_due': amount_due,
        'status': status
    }
    
    try:
        handler.update_contract(contract_id, data)
        console.print("[green]Contract updated successfully.[/green]")
    except Exception as e:
        capture_exception(e)
        console.print(f"[red]{e}[/red]")
        
def show_contracts(token):
    handler = ContractHandler(session, token)
    try:
        contracts = handler.get_all_contracts()
    
        table = Table(title="Contracts")
        table.add_column('ID', justify="right", style="cyan", no_wrap=True)
        table.add_column("Client Contact", style="magenta")
        table.add_column("Commercial Contact", style="magenta")  
        table.add_column("Total Amount", style="magenta")
        table.add_column("Amount Due", style="magenta")
        table.add_column("Creation Date", style="magenta")
        table.add_column("Status", style="magenta")

        for contract in contracts:
            try:
                commercial_name = session.query(Collaborator).filter_by(id=contract.commercial_id).first().name
            except Exception:
                commercial_name = None
            client_name = session.query(Client).filter_by(id=contract.client_id).first().name
            table.add_row(str(contract.id), client_name, commercial_name, 
                        str(contract.total_amount), str(contract.amount_due), str(contract.creation_date), str(contract.status))
            
        console.print(table)
    except Exception as e:
        capture_exception(e)
        console.print(f"[red]{e}[/red]")

def filter_contracts(token):
    handler = ContractHandler(session, token)
    try:
        contracts = handler.filter_contacts_not_paid()
    
        table = Table(title="Contracts")
        table.add_column('ID', justify="right", style="cyan", no_wrap=True)
        table.add_column("Client Contact", style="magenta")
        table.add_column("Commercial Contact", style="magenta")  
        table.add_column("Total Amount", style="magenta")
        table.add_column("Amount Due", style="magenta")
        table.add_column("Creation Date", style="magenta")
        table.add_column("Status", style="magenta")

        for contract in contracts:
            try:
                commercial_name = session.query(Collaborator).filter_by(id=contract.commercial_id).first().name
            except Exception:
                commercial_name = None
            client_name = session.query(Client).filter_by(id=contract.client_id).first().name
            table.add_row(str(contract.id), client_name, commercial_name, 
                        str(contract.total_amount), str(contract.amount_due), str(contract.creation_date), str(contract.status))
            
        console.print(table)
    except Exception as e:
        capture_exception(e)
        console.print(f"[red]{e}[/red]")