# Windows Account Management Tool

The Windows Account Management Tool is a Python script designed to provide administrators with the ability to create, delete, and manage user accounts on a system. The tool provides a simple menu-based interface to perform various account management tasks.


## Installation
To install the project, follow these steps:

1. **Clone the repository**: git clone https://github.com/NathanGitHubCode/Windows-Account-Management-Tool.git
2. **Navigate to the project directory**: cd User-Account-Management-Tool
3. **Install the dependencies**: pip install -r requirements.txt
4. **Functionality**: To test that functionality is working correctly, start by running test_project.py file and ensure all tests pass.

## Requirements

The User Account Management Tool requires the following Python packages installed to run:
pytest
logging
datetime
### Script must be ran as an administrator in order for program to function properly. 

## Functions

1. **Create a new user account**: Allows an administrator to create a new user account by providing a username and password. The tool will validate the username for uniqueness to ensure they meet the system's requirements before creating the account.

2. **Bulk create user accounts**: Allows an administrator to create multiple user accounts at once by providing a CSV file with a list of usernames and passwords.

3. **Delete a user account**: Allows an administrator to delete a user account by providing the username. By default the tool will prompt for confirmation before deleting the account.

4. **Bulk delete user accounts**: Allows an administrator to delete multiple user accounts at once by providing a CSV file with a list of usernames. By default the tool will prompt for confirmation before deleting the accounts. 

5. **Change a user's password**: Allows an administrator to change a user's password by providing the username and a new password.

6. **Change a user's account to admin**: Allows an administrator to change a user's account to an admin account by providing the username. By default the tool will prompt for confirmation before changing the account type.

7. **Change a user's account to standard**: Allows an administrator to change an admin user's account to a standard account by providing the username. By default the tool will prompt for confirmation before changing the account type.

8. **List all user accounts**: Displays a list of all standard user accounts on the system.

9. **List all admin accounts**: Displays a list of all admin user accounts on the system.

10. **Expire a user's password**: Allows an administrator to expire a user's password by providing the username. The next time the user logs in, they will be prompted to create a new password.

11. **Disable a user account**: Allows an administrator to disable a user's account by providing the username. The user will no longer be able to log in.

12. **Enable a user account**: Allows an administrator to enable a disabled user account by providing the username.

13. **Delete inactive audit logs**: Deletes all inactive audit log files.

14. **Change confirmation settings**: Allows an administrator to enable or disable confirmation prompts for certain account management tasks, such as deleting user accounts.

## Logging

The User Account Management Tool uses a custom logger to log all account management activity to an audit log file. The logger provides two log levels: INFO and ERROR. INFO logs all account management activity, while ERROR logs any errors that occur during account management tasks.


