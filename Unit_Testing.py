import unittest
from unittest.mock import patch
from io import StringIO
import subprocess
import Capstone

class TestUserManagementFunctions(unittest.TestCase):
        
    def test_create_account(self):
        username = "testuser"
        password = "password"
        Capstone.create_account(username, password)
        output = subprocess.check_output(["net", "user", username])
        self.assertIn(username, output.decode())
    
   




if __name__ == '__main__':
    unittest.main()