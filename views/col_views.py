import click
from rich.console import Console
from rich.table import Table
from models import Collaborator
from controllers import CollaboratorHandler
from config.database import SessionLocal


console = Console()

session = SessionLocal()


def add_collaborator(token):
    employee_number = click.prompt("Employee Number")
    name = click.prompt("Name")
    email = click.prompt("Email")
    department = click.prompt("Department(gestion/commercial/support)")
    password = click.prompt("Name", hide_input=True)

    handler = CollaboratorHandler(session, token)
    data = {
        'employee number': employee_number,
        'name': name,
        'email': email,
        'department': department,
        'password': password
    }

    response = handler.create_collaborator(data)
    if isinstance(response, tuple):
        console.print(f"[red]{response[0]}[/red]")
    else:
        console.print("[green]Client added successfully.[/green]")

def update_collaborator(token):
    collaborator_id = click.prompt("Collaborator ID")
    name = click.prompt("Name")
    email = click.prompt("Email")
    department = click.prompt("Department(gestion/commercial/support)")
    password = click.prompt("Name", hide_input=True)

    handler = CollaboratorHandler(session, token)
    data = {
        'name': name,
        'email': email,
        'department': department,
        'password': password
    }

    response = handler.update_collaborator(collaborator_id, data)
    if isinstance(response, tuple):
        console.print(f"[red]{response[0]}[/red]")
    else:
        console.print("[green]Collaborator updated successfully.[/green]")

def show_collaborators(token):
    handler = CollaboratorHandler(session, token)
    response = handler.get_all_collaborators()
    if isinstance(response, tuple):
        console.print(f"[red]{response[0]}[/red]")
        return

    collaborators = response
    table = Table(title="Collaborators")
    table.add_column('ID', justify="right", style="cyan", no_wrap=True)
    table.add_column("Employee Number", style="magenta")
    table.add_column("Name", style="magenta")
    table.add_column("Email", style="magenta")
    table.add_column("Department", style="magenta")

    for collaborator in collaborators:
        table.add_row(str(collaborator.id), str(collaborator.employee_number), collaborator.name, 
                      collaborator.email, collaborator.department)
        
    console.print(table)

def delete_collaborator(token):
    collaborator_id = click.prompt("Collaborator ID")
    handler = CollaboratorHandler(session, token)
    response, status_code = handler.delete_collaborator(collaborator_id)

    if status_code == 200:
        console.print(f"[green]{response['message']}[/green]")
    else:
        console.print(f"[red]{response['error']}[/red]")
    