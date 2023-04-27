import pytest
import subprocess
from unittest.mock import patch
from project import create_account

@pytest.fixture
def username():
    return "testuser"

@pytest.fixture
def password():
    return "testpassword"

def test_create_account(username, password):
    with patch('builtins.input', side_effect=[username, password]):
        with patch('subprocess.check_output', return_value=b''):
            create_account()

def test_error_create_account(username, password, caplog):
    with patch('builtins.input', side_effect=[username, password]):
        with patch('subprocess.check_output', side_effect=subprocess.CalledProcessError(2, "")):
            create_account()
    assert f"Failed to create account: {username} - The account already exists" in caplog.text

if __name__ == "__main__":
    pytest.main(["-v", "-s", "test_project.py"])