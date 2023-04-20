import subprocess
import csv

# class UserManagementFunctions:
def create_account(username = None, password = None):
    if username is None or password is None:
        username = input("Enter the username: ")
        password = input("Enter the password: ")
    subprocess.call(["net", "user", username, password, "/ADD"])
    print("User " + username + " has been created with the password " + password)

def bulk_account_creation():
    csv_file = input("Enter the location of the CSV file: ")
    with open(csv_file) as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            username = row[0]
            password = row[1]
            subprocess.call(["net", "user", username, password, "/ADD"])
            print("User " + username + " has been created with the password " + password)

def delete_account():
    username = input("Enter the username: ")
    subprocess.call(["net", "user", username, "/DELETE"])
    print(username + " has been deleted")

def bulk_account_deletion():
    csv_file = input("Enter the location of the CSV file: ")
    with open(csv_file) as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            username = row[0]
            subprocess.call(["net", "user", username, "/DELETE"])
            print("User " + username + " has been deleted")
    
def change_password():
    username = input("Enter the username: ")
    password = input("Enter the new password: ")
    subprocess.call(["net", "user", username, password])
    print("The password has been changed for " + username)

def change_account_to_admin():
    username = input("Enter the username: ")
    subprocess.call(["net", "localgroup", "Administrators", username, "/ADD"])
    print(username + " has been added to the Administrators group")

def change_account_to_standard():
    username = input("Enter the username: ")
    
    subprocess.call(["net", "localgroup", "Administrators", username, "/DELETE"])
    print(username + " has been removed from the Administrators group")

def list_standard_accounts():
    subprocess.call(["net", "localgroup", "Users"])

def list_admin_accounts():
    subprocess.call(["net", "localgroup", "Administrators"])

def expire_password():
    username = input("Enter the username: ")
    subprocess.call(["wmic", "useraccount", "where", "name='" + username + "'", "set", "PasswordExpires=True"])
    print("The password for " + username + " will expire at next login")

def disable_account():
    username = input("Enter the username: ")
    subprocess.call(["wmic", "useraccount", "where", "name='" + username + "'", "set", "Disabled=True"])
    print(username + " has been disabled")

def enable_account():
    username = input("Enter the username: ")
    subprocess.call(["wmic", "useraccount", "where", "name='" + username + "'", "set", "Disabled=False"])
    print(username + " has been enabled")

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
    print("13. Exit")
    print("===============================================================================================================")
def main():
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
            break
        else:
            print("Invalid choice")
if __name__ == "__main__":
    main()
