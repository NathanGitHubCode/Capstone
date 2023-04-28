import csv
import pytest
import subprocess
from unittest.mock import patch
import project

@pytest.fixture
def username():
    return "testuser"

@pytest.fixture
def password():
    return "testpassword"

@pytest.fixture
def confirmation():
    return "y"

@pytest.fixture
def test_csv():
    return "test.csv"

@pytest.fixture
def notfound_csv():
    return "notfound.csv"

# Create Account Tests
def test_create_account(username, password, caplog):
    with patch('builtins.input', side_effect=[username, password]):
        with patch('subprocess.check_output', return_value=b''):
            project.create_account()
    assert f"Account created successfully for user: {username}" in caplog.text

def test_error_create_account(username, password, caplog):
    with patch('builtins.input', side_effect=[username, password]):
        with patch('subprocess.check_output', side_effect=subprocess.CalledProcessError(2, "")):
            project.create_account()
    assert f"Failed to create account: {username} - The account already exists" in caplog.text


# Delete Account Tests
def test_delete_account(username, password, confirmation, caplog):
    test_create_account(username, password, caplog)
    caplog.clear()
    with patch('builtins.input', side_effect=[username, confirmation]):
        with patch('subprocess.check_output', return_value=b''):
            project.delete_account()
    assert f"{username} has been deleted" in caplog.text

def test_confirmation_delete_account(username, caplog):
    with patch('builtins.input', side_effect=[username, "n"]):
        with patch('subprocess.check_output', return_value=b''):
            project.delete_account()
    assert f"Account deletion cancelled for {username}" in caplog.text

def test_error_delete_account(username, confirmation, caplog):
    with patch('builtins.input', side_effect=[username, confirmation]):
        with patch('subprocess.check_output', side_effect=subprocess.CalledProcessError(2, "")):
            project.delete_account()
    assert f"Error deleting {username}: The user {username} does not exist" in caplog.text



# Bulk Create Accounts Tests
def test_bulk_account_creation(test_csv, caplog):
    with patch('builtins.input', side_effect=[test_csv]):
        with patch('subprocess.check_output', return_value=b''):
            with open(test_csv) as csvfile:
                reader = csv.reader(csvfile)
                next(reader)
                usernames = []
                for row in reader:
                    usernames.append(row[0])
                project.bulk_account_creation()
    for username in usernames:
            assert f"Created account '{username}'" in caplog.text

def test_error_bulk_account_creation(test_csv, caplog):
    with patch('builtins.input', side_effect=[test_csv]):
        with patch('subprocess.check_output', return_value=b''):
            with open(test_csv) as csvfile:
                reader = csv.reader(csvfile)
                next(reader)
                usernames = []
                for row in reader:
                    usernames.append(row[0])
                project.bulk_account_creation()
    for username in usernames:
        assert f"Failed to create account: {username} - The account already exists" in caplog.text

def test_error_bulk_account_creation_file_not_found(notfound_csv, caplog):
    with patch('builtins.input', side_effect=[notfound_csv]):
        with patch('subprocess.check_output', return_value=b''):
            project.bulk_account_creation()
    assert f"Failed to open CSV file '{notfound_csv}' - not a valid file path" in caplog.text

# Bulk Account Deletion Tests
def test_bulk_account_deletion(test_csv, confirmation, caplog):
    with patch('builtins.input', side_effect=[test_csv, confirmation]):
        with patch('subprocess.check_output', return_value=b''):
            with open(test_csv) as csvfile:
                reader = csv.reader(csvfile)
                next(reader)
                usernames = []
                for row in reader:
                    usernames.append(row[0])
                project.bulk_account_deletion()
    for username in usernames:
            assert f"User {username} has been deleted from bulk deletion file {test_csv}" in caplog.text

def test_confirmation_bulk_account_deletion(test_csv, caplog):
    with patch('builtins.input', side_effect=[test_csv, "n"]):
        with patch('subprocess.check_output', return_value=b''):
            project.bulk_account_deletion()
    assert f"Account deletion cancelled for {test_csv}" in caplog.text

def test_error_bulk_account_deletion(test_csv, confirmation, caplog):
    with patch('builtins.input', side_effect=[test_csv, confirmation]):
        with patch('subprocess.check_output', return_value=b''):
            with open(test_csv) as csvfile:
                reader = csv.reader(csvfile)
                next(reader)
                usernames = []
                for row in reader:
                    usernames.append(row[0])
                project.bulk_account_deletion()
    for username in usernames:
        assert f"Error deleting user {username}: The user {username} does not exist" in caplog.text

def test_error_bulk_account_deletion_file_not_found(notfound_csv, caplog):
    with patch('builtins.input', side_effect=[notfound_csv, "y"]):
        with patch('subprocess.check_output', return_value=b''):
            project.bulk_account_deletion()
    assert f"Failed to open CSV file '{notfound_csv}' - not a valid file path" in caplog.text

if __name__ == "__main__":
    pytest.main(["-v", "-s", "test_project.py"])

