import click
from views import login as login_view, show_clients, add_client, register as register_view
from config.database import engine, init_db, Base
from sqlalchemy.orm import sessionmaker


init_db(engine, Base)

SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

@click.group()
def cli():
    pass

@click.command()
def login():
    login_view()

@click.command()
def register():
    register_view()

@click.command()
def run():
    try:
        with open('token.txt', 'r') as f:
            token = f.read()

        while True:
            command = click.prompt("Enter a command (view_clients, add_client, exit)", type=str)
            if command == 'exit':
                break
            elif command == 'view_clients':
                show_clients(token)
            elif command == 'add_client':
                add_client(token)
            else:
                click.echo("Unknown command.")
    except FileNotFoundError:
        click.echo("Please login first.")

cli.add_command(login, name='login')
cli.add_command(register, name='register')
cli.add_command(run)

if __name__ == '__main__':
    cli()
