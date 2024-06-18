import click
from rich.console import Console
from rich.table import Table
from models import Collaborator
from controllers import ClientHandler
from config.database import SessionLocal


console = Console()

session = SessionLocal()


def login():
    email = click.prompt("Please enter your email")
    password = click.prompt("Please enter your password", hide_input=True)
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
    employee_number = click.prompt("Employee Number", type=int)
    name = click.prompt("Name")
    email = click.prompt("Email")
    department = click.prompt("Department")
    password = click.prompt("Password", hide_input=True)

    collaborator = Collaborator()
    collaborator.register(session, employee_number, name, email, department, password)
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

    response = handler.create_client(data)
    if isinstance(response, tuple):
        console.print(f"[red]{response[0]}[/red]")
    else:
        console.print("[green]Client added successfully.[/green]")


def show_clients(token):
    handler = ClientHandler(session, token)
    response = handler.get_all_clients()
    if isinstance(response, tuple):
        console.print(f"[red]{response[0]}[/red]")
        return

    clients = response
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
        commercial_name = session.query(Collaborator).filter_by(id=client.commercial_id).first().name
        table.add_row(str(client.id), client.name, client.email, 
                      client.telephone, client.company_name,str(client.creation_date), str(client.last_update), commercial_name)
        
    console.print(table)