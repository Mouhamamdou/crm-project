import click
from rich.console import Console
from rich.table import Table
from models import Collaborator, Client
from controllers import ContractHandler
from config.database import SessionLocal


console = Console()

session = SessionLocal()


def add_contract(token):
    client_id = click.prompt("Client ID", type=int)
    #commercial_id = click.prompt("Commercial ID", type=int)
    total_amount = click.prompt("Total Amount", type=float)
    amount_due = click.prompt("Amount Due", type=float)
    status = click.prompt("Status (true/false)").lower() in ('true', 'yes', '1')

    handler = ContractHandler(session, token)
    data = {
        'client_id': client_id,
        #'commercial_id': commercial_id,
        'total_amount': total_amount,
        'amount_due': amount_due,
        'status': status
    }

    response = handler.create_contract(data)
    if isinstance(response, tuple):
        console.print(f"[red]{response[0]}[/red]")
    else:
        console.print("[green]Contract added successfully.[/green]")

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

    response = handler.update_contract(contract_id, data)
    if isinstance(response, tuple):
        console.print(f"[red]{response[0]}[/red]")
    else:
        console.print("[green]Contract updated successfully.[/green]")

def show_contracts(token):
    handler = ContractHandler(session, token)
    response = handler.get_all_contracts()
    if isinstance(response, tuple):
        console.print(f"[red]{response[0]}[/red]")
        return
    
    contracts = response
    table = Table(title="Contracts")
    table.add_column('ID', justify="right", style="cyan", no_wrap=True)
    table.add_column("Client Contact", style="magenta")
    table.add_column("Commercial Contact", style="magenta")  
    table.add_column("Total Amount", style="magenta")
    table.add_column("Amount Due", style="magenta")
    table.add_column("Creation Date", style="magenta")
    table.add_column("Status", style="magenta")

    for contract in contracts:
        commercial_name = session.query(Collaborator).filter_by(id=contract.commercial_id).first().name
        client_name = session.query(Client).filter_by(id=contract.client_id).first().name
        table.add_row(str(contract.id), client_name, commercial_name, 
                      str(contract.total_amount), str(contract.amount_due), str(contract.creation_date), str(contract.status))
        
    console.print(table)