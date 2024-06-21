import click
from views import (login as login_view, register as register_view, 
                   show_clients, add_client, update_client,
                   show_contracts, add_contract,update_contract, filter_contracts,
                   show_events, add_event, add_support_contact, update_event, filter_events_ws, filter_my_events,
                   show_collaborators, add_collaborator, update_collaborator, delete_collaborator)
from config.database import init_db
import sentry_sdk

sentry_sdk.init(
    dsn="https://6d33421778aa9658ef2b700b7467561c@o4507471152349184.ingest.de.sentry.io/4507471164473424",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)

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
            command = click.prompt("Enter a command (add_client, update_client, add_contract, update_contract, add_event, add_support_contact, update_event, add_collaborator, update_collaborator, delete_collaborator, exit)", type=str)
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
            elif command == 'filter_contracts':
                filter_contracts(token)
            elif command == 'view_events':
                show_events(token)
            elif command == 'add_event':
                add_event(token)
            elif command == 'add_support_contact':
                add_support_contact(token)
            elif command == 'update_event':
                update_event(token)
            elif command == 'filter_events_ws':
                filter_events_ws(token)
            elif command == 'filter_my_events':
                filter_my_events(token)
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