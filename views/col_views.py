import click
from rich.console import Console
from rich.table import Table
from models import Collaborator
from controllers import CollaboratorHandler
from config.database import SessionLocal
from sentry_sdk import capture_exception

console = Console()

session = SessionLocal()


def add_collaborator(token):
    """
    Prompt user for collaborator details and create a new collaborator.

    Args:
        token (str): JWT token for authentication.
    """
    name = click.prompt("Name")
    email = click.prompt("Email")
    department = click.prompt("Department(gestion/commercial/support)")
    password = click.prompt("Password", hide_input=True)

    handler = CollaboratorHandler(session, token)
    data = {
        'name': name,
        'email': email,
        'department': department,
        'password': password
    }

    try:
        handler.create_collaborator(data)
        console.print("[green]Collaborator added successfully.[/green]")
    except Exception as e:
        capture_exception(e)
        console.print(f"[red]{e}[/red]")


def update_collaborator(token):
    """
    Prompt user for collaborator ID and details, and update the collaborator.

    Args:
        token (str): JWT token for authentication.
    """
    collaborator_id = click.prompt("Collaborator ID")
    name = click.prompt("Name")
    email = click.prompt("Email")
    department = click.prompt("Department(gestion/commercial/support)")
    password = click.prompt("Password", hide_input=True)

    handler = CollaboratorHandler(session, token)
    data = {
        'name': name,
        'email': email,
        'department': department,
        'password': password
    }

    try:
        handler.update_collaborator(collaborator_id, data)
        console.print("[green]Collaborator added successfully.[/green]")
    except Exception as e:
        capture_exception(e)
        console.print(f"[red]{e}[/red]")    


def show_collaborators(token):
    """
    Display all collaborators in a table.

    Args:
        token (str): JWT token for authentication.
    """
    handler = CollaboratorHandler(session, token)
    try:
        collaborators = handler.get_all_collaborators()
        table = Table(title="Collaborators")
        table.add_column('ID', justify="right", style="cyan", no_wrap=True)
        table.add_column("Name", style="magenta")
        table.add_column("Email", style="magenta")
        table.add_column("Department", style="magenta")

        for collaborator in collaborators:
            table.add_row(str(collaborator.id), collaborator.name, collaborator.email, collaborator.department)
            
        console.print(table)
    except Exception as e:
        capture_exception(e)
        console.print(f"[red]{e}[/red]")

def delete_collaborator(token):
    """
    Delete a collaborator by ID.

    Args:
        token (str): JWT token for authentication.
    """
    collaborator_id = click.prompt("Collaborator ID")
    handler = CollaboratorHandler(session, token)
    response, status_code = handler.delete_collaborator(collaborator_id)

    if status_code == 200:
        console.print(f"[green]{response['message']}[/green]")
    else:
        capture_exception(e)
        console.print(f"[red]{response['error']}[/red]")
    