import click
from rich.console import Console
from rich.table import Table
from models import Collaborator
from controllers import ClientHandler
from config.database import SessionLocal


console = Console()

session = SessionLocal()


def login():
    email = click.prompt("Email")
    password = click.prompt("Password", hide_input=True)
    collaborator = session.query(Collaborator).filter_by(email=email).first()
    token = collaborator.authenticate(session, email, password)
    if token:
        console.print("[green]Login successful![/green]")
        with open('token.txt', 'w') as f:
            f.write(token)
        return token
    else:
        console.print("[red]Invalide email or password.[/red]")
        return None


def register():
    name = click.prompt("Name")
    email = click.prompt("Email")
    password = click.prompt("Password", hide_input=True)
    department = click.prompt("Department(gestion/commercial/support)")

    collaborator = Collaborator()
    collaborator.register(session, name, email, department, password)
    console.print("[green]Registration successful![/green]")


def add_client(token):
    name = click.prompt("Name")
    email = click.prompt("Email")
    telephone = click.prompt("Telephone")
    company_name = click.prompt("Company Name")

    handler = ClientHandler(session, token)
    data = {
        'name': name,
        'email': email,
        'telephone': telephone,
        'company_name': company_name
    }

    try:
        handler.create_client(data)
        console.print("[green]Client added successfully.[/green]")
    except Exception as e:
        console.print(f"[red]{e}[/red]")

def update_client(token):
    client_id = click.prompt("Client ID")
    name = click.prompt("Name")
    email = click.prompt("Email")
    telephone = click.prompt("Telephone")
    company_name = click.prompt("Company Name")

    handler = ClientHandler(session, token)
    data = {
        'name': name,
        'email': email,
        'telephone': telephone,
        'company_name': company_name
    }

    try:
        handler.update_client(client_id, data)
        console.print("[green]Client updated successfully.[/green]")
    except Exception as e:
        console.print(f"[red]{e}[/red]")


def show_clients(token):
    handler = ClientHandler(session, token)
    try:
        clients = handler.get_all_clients()
        table = Table(title="Clients")
        table.add_column('ID', justify="right", style="cyan", no_wrap=True)
        table.add_column("Name", style="magenta")
        table.add_column("Email", style="magenta")  
        table.add_column("Telephone", style="magenta")
        table.add_column("Company Name", style="magenta")
        table.add_column("Creation Date", style="magenta")
        table.add_column("Last Update", style="magenta")
        table.add_column("Contact Commercial", style="magenta")

        for client in clients:
            try:
                commercial_name = session.query(Collaborator).filter_by(id=client.commercial_id).first().name
            except Exception:
                commercial_name = None
            table.add_row(str(client.id), client.name, client.email, client.telephone, client.company_name, str(client.creation_date), 
                          str(client.last_update), commercial_name)
        
        console.print(table)
    except Exception as e:
        console.print(f"[red]{e}[/red]")
    