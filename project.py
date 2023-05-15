import csv
import ctypes
import subprocess
import audit_logging


def create_account():
    print("This will create an account")
    username = input("Enter the username: ")
    password = input("Enter the password: ")
    try:
        output = subprocess.check_output(["net", "user", username, password, "/ADD"], stderr=subprocess.STDOUT)
        print("User - " + username + " has been created with the password - " + password)
        audit_logging.log_info(f"Account created successfully for user: {username}")
    except subprocess.CalledProcessError as e:
        if e.returncode == 2:
            print("Error: The account already exists.")
            audit_logging.log_error(f"Failed to create account: {username} - The account already exists")
        else:
            print("Error:", str(e.output))
            audit_logging.log_error(f"Failed to create account: {username} - {str(e.output)}")
  

def bulk_account_creation():
    print("Function reads first row as header, and creates accounts from the second row onwards")
    print("The first column is the username, the second column is the password")
    print("This will create accounts from a CSV file")
    csv_file = input("Enter the location of the CSV file: ")
    try:
        with open(csv_file) as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            for row in reader:
                username = row[0]
                password = row[1]
                try:
                    subprocess.check_call(["net", "user", username, password, "/ADD"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
                    print(f"Created account '{username}'")
                    audit_logging.log_info(f"Created account '{username}'")
                except subprocess.CalledProcessError as e:
                    if  e.returncode == 2:
                        print(f"User {username} already exists")
                        audit_logging.log_error(f"Failed to create account: {username} - The account already exists")
                    else:
                        print(f"Failed to create account '{username}'")
                        audit_logging.log_error(f"Failed to create account: {username} - {str(e)}")
    except FileNotFoundError as e:
         print(f"'{csv_file}' is not a valid file path")
         audit_logging.log_error(f"Failed to open CSV file '{csv_file}' - not a valid file path")


def delete_account():
    print("This will delete an account")
    username = input("Enter the username to delete: ")
    if(script_confirmation == True or is_admin_account(username) == True):
        if(is_admin_account(username) == True):
            confirmation = input(f"This user is an administrator. Are you sure you want to delete this account {username}? (Y/N): ")
            if(confirmation.lower() == "y"):
                try:
                    subprocess.check_output(["net", "user", username, "/DELETE"], stderr=subprocess.STDOUT)
                    audit_logging.log_info(f"{username} has been deleted")
                    print(username + " has been deleted")
                except subprocess.CalledProcessError as e:
                    if e.returncode == 2:
                        print(f"Error: The user name {username} does not exist.")
                        audit_logging.log_error(f"Error deleting {username}: The user {username} does not exist")
                    else:
                        print("Error:", str(e.output))
                        audit_logging.log_error(f"Error deleting {username}: {str(e.output)}")
            else:
                print("Account deletion cancelled")
                audit_logging.log_info(f"Account deletion cancelled for {username}")
        elif(is_admin_account(username) == False):
            confirmation = input(f"Are you sure you want to delete this account {username}? (Y/N): ")
            if(confirmation.lower() == "y"):
                try:
                    subprocess.check_output(["net", "user", username, "/DELETE"], stderr=subprocess.STDOUT)
                    audit_logging.log_info(f"{username} has been deleted")
                    print(username + " has been deleted")
                except subprocess.CalledProcessError as e:
                    if e.returncode == 2:
                        print(f"Error: The user name {username} does not exist.")
                        audit_logging.log_error(f"Error deleting {username}: The user {username} does not exist")
                    else:
                        print("Error:", str(e.output))
                        audit_logging.log_error(f"Error deleting {username}: {str(e.output)}")
            else:
                print("Account deletion cancelled")
                audit_logging.log_info(f"Account deletion cancelled for {username}")
    else:        
        try:
            subprocess.check_output(["net", "user", username, "/DELETE"], stderr=subprocess.STDOUT)
            audit_logging.log_info(f"{username} has been deleted")
            print(username + " has been deleted")
        except subprocess.CalledProcessError as e:
            if e.returncode == 2:
                print(f"Error: The user name {username} does not exist.")
                audit_logging.log_error(f"Error deleting {username}: The user {username} does not exist")
            else:
                print("Error:", str(e.output))
                audit_logging.log_error(f"Error deleting {username}: {str(e.output)}")

def bulk_account_deletion():
    print("This will delete accounts from a CSV file")
    print("Function reads first row as header, and deletes accounts from the second row onwards")
    print("The first column is the username")
    csv_file = input("Enter the location of the CSV file: ")
    try:
        if script_confirmation == True:
            with open(csv_file) as csvfile:
                reader = csv.reader(csvfile)
                next(reader)
                print("You are about to delete the following accounts:")            
                for row in reader:
                    
                    if(is_admin_account(row[0]) == True):
                        print(row[0] + " (Administrator account)")
                    elif(does_account_exist(row[0]) == False):
                        print(row[0] + " (Account does not exist)")
                    else:
                        print(row[0])
                confirmation = input("Are you sure you want to delete these accounts? (Y/N): ")
                if(confirmation.lower() == "y"):
                    with open(csv_file) as csvfile:
                        reader = csv.reader(csvfile)
                        next(reader)
                        for row in reader:
                            username = row[0]
                            try:
                                subprocess.check_call(["net", "user", username, "/DELETE"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
                                
                                print("User " + username + " has been deleted")

                                audit_logging.log_info(f"User {username} has been deleted from bulk deletion file {csv_file}")
                            except subprocess.CalledProcessError as e:

                                if e.returncode == 2:
                                    print(f"Error: The user {username} does not exist.")
                                    audit_logging.log_error(f"Error deleting user {username}: The user {username} does not exist")
                                else:
                                    print("Error:", str(e))
                                    audit_logging.log_error(f"Error deleting user {username} from {csv_file}: {str(e)}")
                else:
                    print("Account deletion cancelled")
                    audit_logging.log_info(f"Account deletion cancelled for {csv_file}")
        else:
            with open(csv_file) as csvfile:
                reader = csv.reader(csvfile)
                next(reader)
                for row in reader:
                    username = row[0]
                    try:
                        subprocess.check_call(["net", "user", username, "/DELETE"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
                        
                        print("User " + username + " has been deleted")

                        audit_logging.log_info(f"User {username} has been deleted from bulk deletion file {csv_file}")
                    except subprocess.CalledProcessError as e:

                        if e.returncode == 2:
                            print(f"Error: The user {username} does not exist.")
                            audit_logging.log_error(f"Error deleting user {username}: The user {username} does not exist")
                        else:
                            print("Error:", str(e))
                            audit_logging.log_error(f"Error deleting user {username} from {csv_file}: {str(e)}")        
    except FileNotFoundError:
        print(f"Error: The file {csv_file} does not exist.")
        audit_logging.log_error(f"Failed to open CSV file '{csv_file}' - not a valid file path")
        
    
def change_password():
    print("This will change the password for an account")
    username = input("Enter the username: ")
    password = input("Enter the new password: ")
    if(script_confirmation == True or is_admin_account(username) == True):
        confirmation = input(f"Are you sure you want to change the password for {username}? (Y/N): ")
        if(confirmation.lower() == "y"):
            try:
                subprocess.check_call(["net", "user", username, password], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
                audit_logging.log_info(f"The password has been changed for {username}")
                print(f"The password has been changed for {username}")
            except subprocess.CalledProcessError as e:
                if e.returncode == 2:
                    print(f"Error: The user name {username} does not exist.")
                    audit_logging.log_error(f"Error changing password for {username}: The user {username} does not exist")
                else:
                    audit_logging.log_error(f"Failed to change password for {username}: {e}")
                    print(f"Failed to change password for {username}")
        else:
            print("Password change cancelled")
    else:
        try:
            subprocess.check_call(["net", "user", username, password], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
            audit_logging.log_info(f"The password has been changed for {username}")
            print(f"The password has been changed for {username}")
        except subprocess.CalledProcessError as e:
            if e.returncode == 2:
                print(f"Error: The user name {username} does not exist.")
                audit_logging.log_error(f"Error changing password for {username}: The user {username} does not exist")
            else:
                audit_logging.log_error(f"Failed to change password for {username}: {e}")
                print(f"Failed to change password for {username}")

def change_account_to_admin():
    print("This will add an account to the Administrators group")
    username = input("Enter the username: ")
    if(script_confirmation == True):
        confirmation = input(f"Are you sure you want to add {username} to the Administrators group? (Y/N): ")
        if(confirmation.lower() == "y"):
            try:
                subprocess.check_call(["net", "localgroup", "Administrators", username, "/ADD"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                audit_logging.log_info(f"Changed account '{username}' to Administrator")
                print(f"{username} has been added to the Administrators group")
            except subprocess.CalledProcessError as e:
                if e.returncode == 1:
                    audit_logging.log_error(f"Failed to change account: {username} - The user name could not be found.")
                    print(f"Failed to change account '{username}' - The user name could not be found.")
                elif e.returncode == 2:
                    audit_logging.log_error(f"Failed to change account: {username} - The specified account name is already an administrator.")
                    print(f"Failed to change account '{username}' - The specified account name is already an administrator.")
                else:
                    audit_logging.log_error(f"Failed to change account: {username} - {e}")
        else:
            print("Account change cancelled")
    else:
        try:
            subprocess.check_call(["net", "localgroup", "Administrators", username, "/ADD"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            audit_logging.log_info(f"Changed account '{username}' to Administrator")
            print(f"{username} has been added to the Administrators group")
        except subprocess.CalledProcessError as e:
            if e.returncode == 1:
                audit_logging.log_error(f"Failed to change account: {username} - The user name could not be found.")
                print(f"Failed to change account '{username}' - The user name could not be found.")
            elif e.returncode == 2:
                audit_logging.log_error(f"Failed to change account: {username} - The specified account name is already an administrator.")
                print(f"Failed to change account '{username}' - The specified account name is already an administrator.")
            else:
                audit_logging.log_error(f"Failed to change account: {username} - {e}")
                print(f"Failed to change account '{username}' - {e}")

def change_account_to_standard():
    print("This will remove the account from the Administrators group")
    username = input("Enter the username: ")
    if(script_confirmation == True):
        confirmation = input(f"Are you sure you want to remove {username} from the Administrators group? (Y/N): ")
        if(confirmation.lower() == "y"):
            try:
                subprocess.check_call(["net", "localgroup", "Administrators", username, "/DELETE"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                audit_logging.log_info(f"Changed account '{username}' to Standard User")
                print(f"{username} has been removed from the Administrators group")
            except subprocess.CalledProcessError as e:
                if e.returncode == 2:
                    audit_logging.log_error(f"Failed to change account: {username} is not a member of the Administrators group")
                    print(f"Failed to change account: {username} is not an Administrator")
                else:
                    print("Failed to change account:", e)
                    audit_logging.log_error(f"Failed to change account: {username} - {e}")
        else:
            print("Account change cancelled")
    else:
        try:
            subprocess.check_call(["net", "localgroup", "Administrators", username, "/DELETE"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            audit_logging.log_info(f"Changed account '{username}' to Standard User")
            print(f"{username} has been removed from the Administrators group")
        except subprocess.CalledProcessError as e:
            if e.returncode == 2:
                audit_logging.log_error(f"Failed to change account: {username} is not a member of the Administrators group")
                print(f"Failed to change account: {username} is not an Administrator")
            else:
                print("Failed to change account:", e)
                audit_logging.log_error(f"Failed to change account: {username} - {e}")

def list_standard_accounts():
    subprocess.call(["net", "localgroup", "Users"])

def list_admin_accounts():
    subprocess.call(["net", "localgroup", "Administrators"])

def expire_password():
    print("This will expire the password for an account")
    username = input("Enter the username: ")
    subprocess.call(["wmic", "useraccount", "where", "name='" + username + "'", "set", "PasswordExpires=True"])
    print("The password for " + username + " will expire at next login")

def disable_account():
    print("This will disable an account")
    username = input("Enter the username: ")
    subprocess.call(["wmic", "useraccount", "where", "name='" + username + "'", "set", "Disabled=True"])
    print(username + " has been disabled")

def enable_account():
    print("This will enable an account")
    username = input("Enter the username: ")
    subprocess.call(["wmic", "useraccount", "where", "name='" + username + "'", "set", "Disabled=False"])
    print(username + " has been enabled")

def disable_y_n_confirmation():
    global script_confirmation
    print("Are you sure you want to disable confirmation prompts? (Y/N)")
    disable_confirmation = input("Enter Y or N: ")
    if disable_confirmation == "Y" or disable_confirmation == "y":
        print("Confirmation prompts have been disabled")
        audit_logging.log_info("Confirmation prompts have been disabled")
        script_confirmation = False
    elif disable_confirmation == "N" or disable_confirmation == "n":
        print("Confirmation prompts are still enabled")
        audit_logging.log_info("Confirmation prompts have not been disabled")
        script_confirmation = True    

def does_account_exist(username):
    try:
        subprocess.check_call(["net", "user", username], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError as e:
        if e.returncode == 2:
            return False
        else:
            print("Error:", str(e))
            audit_logging.log_error(f"Error checking if user {username} exists: {str(e)}")
            return False
        
def is_admin_account(username):
    output = subprocess.check_output(["net", "localgroup", "Administrators"])
    output_str = output.decode("utf-8")
    return username in output_str

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False
    
script_confirmation = True


def main_menu():
    print("===============================================================================================================")
    print("Welcome to the User Account Management Tool")
    print("1. Create a new user account")
    print("2. Bulk create user accounts")
    print("3. Delete a user account")
    print("4. Bulk delete user accounts")
    print("5. Change a user's password")
    print("6. Change a user's account to admin")
    print("7. Change a user's account to standard")
    print("8. List all user accounts")
    print("9. List all admin accounts")
    print("10. Expire a user's password")
    print("11. Disable a user account")
    print("12. Enable a user account")
    print("13. Delete inactive audit logs")
    print("14. Change confirmation settings")
    print("15. Exit")
    print("===============================================================================================================")

def main():
    
    audit_logging.setup_logger()
    if not is_admin():
        print("This script must be run as an administrator")
        exit()
    while True:
        main_menu()
        choice = input("Enter your choice: ")

        if choice == "1":
            create_account()
        elif choice == "2":
            bulk_account_creation()
        elif choice == "3":
            delete_account()
        elif choice == "4":
            bulk_account_deletion()
        elif choice == "5":
            change_password()
        elif choice == "6":
            change_account_to_admin()
        elif choice == "7":
            change_account_to_standard()
        elif choice == "8":
            list_standard_accounts()
        elif choice == "9":
            list_admin_accounts()
        elif choice == "10":
            expire_password()
        elif choice == "11":
            disable_account()
        elif choice == "12":
            enable_account()
        elif choice == "13":
            audit_logging.delete_audit_logs()
        elif choice == "14":
            disable_y_n_confirmation()
        elif choice == "15":
            break
        else:
            print("Invalid choice")
if __name__ == "__main__":
    main()



