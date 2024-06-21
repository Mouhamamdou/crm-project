# EpicEvents Application

## Overview
EpicEvents is a client management and contract handling designed to prepare event
management process for a company. It offers functionalities for handling clients,
contracts and events and collaborators with role-based access control and secure
authentication.

## Features

- Collaborator Authentication: Login and registration for collaborators with role-based access.
- Client Management: Add, update and view clients.
- Contract Management: Add, update, view, and filter contracts.
- Event Management: Add, update, view, and filter events. Assign support contacts to events.
- Collaborator Management: View, add, update, and delete collaborators.
- Role-Based Access Control: Permissions based on collaborator roles (commercial, gestion, support).

## Installation

1. Clone the repository:

    ```bash  
   git clone https://github.com/Mouhamamdou/crm-project.git
   cd crm-project

2. Create and activate a virtual environment:
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. Install the required packages:

   ```bash
   pip install -r requirements.txt

## Environment Variables
	
   Add the environment variable:
   SECRET_KEY=your_secret_key_here
   Replace your_secret_key_here with a secure key of your choice.

## Usage
   Register a Collaborator

   python epicEvents.py register
 
   Login
   python epicEvents.py login

   Run the application
   python epicEvents.py run

   Once logged in, you can use the commands within the CLI
