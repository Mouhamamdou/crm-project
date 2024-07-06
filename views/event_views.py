import click
from rich.console import Console
from rich.table import Table
from models import Collaborator, Client
from controllers import EventHandler
from config.database import SessionLocal
from datetime import datetime
from sentry_sdk import capture_exception


console = Console()

session = SessionLocal()

@click.command()
@click.argument('token')
def add_event(token):
    """
    Add a new event.

    Args:
        token (str): JWT token for authentication.
    """
    contract_id = click.prompt("Contract ID", type=int)
    end_date_str = click.prompt("End Date (YYYY-MM-DD)")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
    location = click.prompt("Location")
    attendees = click.prompt("Attendees", type=int)
    notes = click.prompt("Notes")

    handler = EventHandler(session, token)
    data = {
        'contract_id': contract_id,
        'end_date': end_date,
        'location': location,
        'attendees': attendees,
        'notes' : notes
    }

    try:
        handler.create_event(data)
        console.print("[green]Event added successfully.[/green]")
    except Exception as e:
        capture_exception(e)
        console.print(f"[red]{e}[/red]")

def update_event(token):
    """
    Update an existing event.

    Args:
        token (str): JWT token for authentication.
    """
    event_id = click.prompt("Event ID")
    end_date_str = click.prompt("End Date (YYYY-MM-DD)")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
    location = click.prompt("Location")
    attendees = click.prompt("Attendees", type=int)
    notes = click.prompt("Notes")

    handler = EventHandler(session, token)
    data = {
        'end_date': end_date,
        'location': location,
        'attendees': attendees,
        'notes' : notes
    }

    try:
        handler.update_event(event_id, data)
        console.print("[green]Event updated successfully.[/green]")
    except Exception as e:
        capture_exception(e)
        console.print(f"[red]{e}[/red]")

def show_events(token):
    """
    Display all events in a table.

    Args:
        token (str): JWT token for authentication.
    """
    handler = EventHandler(session, token)
    try:
        events = handler.get_all_events()
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
            table.add_row(str(event.id), str(event.contract_id), client.name, client.email + '\n' + client.telephone, str(event.start_date), 
                        str(event.end_date), support_contact.name if support_contact is not None else "", 
                        event.location, str(event.attendees), event.notes)
            
        console.print(table)

    except Exception as e:
        capture_exception(e)
        console.print(f"[red]{e}[/red]")


def filter_events_ws(token):
    """
    Display all events without support in a table.

    Args:
        token (str): JWT token for authentication.
    """
    handler = EventHandler(session, token)
    try:
        events = handler.filter_events_without_support()
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
            table.add_row(str(event.id), str(event.contract_id), client.name, client.email + '\n' + client.telephone, str(event.start_date), 
                        str(event.end_date), support_contact.name if support_contact is not None else "", 
                        event.location, str(event.attendees), event.notes)
            
        console.print(table)

    except Exception as e:
        capture_exception(e)
        console.print(f"[red]{e}[/red]")

def filter_my_events(token):
    """
    Display all events assigned to the current collaborator in a table.

    Args:
        token (str): JWT token for authentication.
    """
    handler = EventHandler(session, token)
    try:
        events = handler.filter_my_events()
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
            table.add_row(str(event.id), str(event.contract_id), client.name, client.email + '\n' + client.telephone, str(event.start_date), 
                        str(event.end_date), support_contact.name if support_contact is not None else "", 
                        event.location, str(event.attendees), event.notes)
            
        console.print(table)

    except Exception as e:
        capture_exception(e)
        console.print(f"[red]{e}[/red]")


def add_support_contact(token):
    """
    Add a support contact for an event.

    Args:
        token (str): JWT token for authentication.
    """
    event_id = click.prompt("Event ID", type=int)
    support_contact_id = click.prompt("Support Contact ID", type=int)

    handler = EventHandler(session, token)
    try:
        handler.add_support_contact(event_id, support_contact_id)
        console.print("Support contact designated successfully.")
    except Exception as e:
        capture_exception(e)
        console.print(f"[red]{e}[/red]")