import click
from views import (login as login_view, register as register_view, 
                   show_clients, add_client, update_client,
                   show_contracts, add_contract,update_contract,
                   show_events, add_event, add_support_contact, update_event,
                   show_collaborators, add_collaborator, update_collaborator, delete_collaborator)
from config.database import init_db


init_db()


@click.group()
def cli():
    pass

@click.command(name='login')
def login_command():
    login_view()

@click.command(name='register')
def register_command():
    register_view()

@click.command()
def run():
    try:
        with open('token.txt', 'r') as f:
            token = f.read()

        while True:
            command = click.prompt("Enter a command (view_clients, add_client, view_contracts, add_contract, view_events, add_event, add_support_contact, exit)", type=str)
            if command == 'exit':
                break
            elif command == 'view_clients':
                show_clients(token)
            elif command == 'add_client':
                add_client(token)
            elif command == 'update_client':
                update_client(token)
            elif command == 'view_contracts':
                show_contracts(token)
            elif command == 'add_contract':
                add_contract(token)
            elif command == 'update_contract':
                update_contract(token)
            elif command == 'view_events':
                show_events(token)
            elif command == 'add_event':
                add_event(token)
            elif command == 'add_support_contact':
                add_support_contact(token)
            elif command == 'update_event':
                update_event(token)
            elif command == 'view_collaborators':
                show_collaborators(token)
            elif command == 'add_collaborator':
                add_collaborator(token)
            elif command == 'update_collaborator':
                update_collaborator(token)
            elif command == 'delete_collaborator':
                delete_collaborator(token)
            else:
                click.echo("Unknown command.")
    except FileNotFoundError:
        click.echo("Please login first.")

cli.add_command(register_command, name='register')
cli.add_command(login_command, name='login')
cli.add_command(run)

if __name__ == '__main__':
    cli()