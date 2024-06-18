import click
from rich.console import Console
from rich.table import Table
from models import Collaborator, Client
from controllers import EventHandler
from config.database import SessionLocal
from datetime import datetime


console = Console()

session = SessionLocal()


def add_event(token):
    contract_id = click.prompt("Contract ID", type=int)
    #client_id = click.prompt("Client ID", type=int)
    end_date_str = click.prompt("End Date (YYYY-MM-DD)")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
    location = click.prompt("Location")
    attendees = click.prompt("Attendees", type=int)
    notes = click.prompt("Notes")

    handler = EventHandler(session, token)
    data = {
        'contract_id': contract_id,
        #'client_id': client_id,
        'end_date': end_date,
        'location': location,
        'attendees': attendees,
        'notes' : notes
    }

    response = handler.create_event(data)
    if isinstance(response, tuple):
        console.print(f"[red]{response[0]}[/red]")
    else:
        console.print("[green]Event added successfully.[/green]")


def show_events(token):
    handler = EventHandler(session, token)
    response = handler.get_all_events()
    if isinstance(response, tuple):
        console.print(f"[red]{response[0]}[/red]")
        return

    events = response
    table = Table(title="Events")
    table.add_column('ID', justify="right", style="cyan", no_wrap=True)
    table.add_column("Contract ID", style="magenta")
    table.add_column("Client Name", style="magenta")
    table.add_column("Client Contact", style="magenta")
    table.add_column("Start Date", style="magenta")
    table.add_column("End Date", style="magenta")
    table.add_column("Support Contact", style="magenta")
    table.add_column("Location", style="magenta")
    table.add_column("Attendees", style="magenta")
    table.add_column("Notes", style="magenta")

    for event in events:
        client = session.query(Client).filter_by(id=event.client_id).first()
        support_contact = session.query(Collaborator).filter_by(id=event.support_contact_id).first()
        table.add_row(str(event.id), str(event.contract_id), client.name, client.email + "/n"+ client.telephone, str(event.start_date), 
                      str(event.end_date), support_contact if support_contact is not None else "", 
                      event.location, str(event.attendees), event.notes)
        
    console.print(table)