from .cli_views import login, register, show_clients, add_client, update_client
from .con_views import show_contracts, add_contract
from .event_views import show_events, add_event, add_support_contact, update_event
from .col_views import show_collaborators, add_collaborator, update_collaborator, delete_collaborator

__all__ = [login, register, show_clients, add_client, update_client, show_contracts, add_contract, show_events, add_event, 
           add_support_contact, update_event, show_collaborators, add_collaborator, update_collaborator, delete_collaborator]
