import unittest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from supernova.models.credentials import Credentials
from supernova.exceptions import CredentialsNotFoundError

class TestCredentialsModel(unittest.TestCase):

    def test_credentials_creation_success(self):

        creds = Credentials(
            username='bob',
            password='steve',
            secret='bob2'
        )
        self.assertIsNotNone(creds)
        self.assertEqual(creds.username, 'bob')
        self.assertEqual(creds.password, 'steve')
        self.assertEqual(creds.secret, 'bob2')

    def test_credentials_creation_no_secret(self):

        creds = Credentials(
            username='testuser',
            password='password456'
        )
        self.assertEqual(creds.username, 'testuser')
        self.assertEqual(creds.password, 'password456')
        self.assertIsNone(creds.secret, "Secret should default to None")

    def test_secure_representation(self):

        creds = Credentials(
            username='secure_user',
            password='very_secret_password',
            secret='top_secret_enable'
        )
        
        creds_repr = repr(creds)

        self.assertIn("username='secure_user'", creds_repr)
        
        self.assertNotIn('very_secret_password', creds_repr)
        self.assertNotIn('top_secret_enable', creds_repr)
        
        self.assertIn("password='****'", creds_repr)
        self.assertIn("secret='****'", creds_repr)

    def test_secure_representation_no_secret(self):

        creds = Credentials(
            username='no_secret_user',
            password='a_password'
        )
        creds_repr = repr(creds)
        
        self.assertIn("username='no_secret_user'", creds_repr)
        self.assertIn("password='****'", creds_repr)

        self.assertIn("secret=None", creds_repr)
        self.assertNotIn("secret='****'", creds_repr)
        
    def test_validation_missing_required_fields(self):


        with self.assertRaisesRegex(CredentialsNotFoundError, "Username cannot be empty"):
            Credentials(username=None, password='pw')

        with self.assertRaisesRegex(CredentialsNotFoundError, "Username cannot be empty"):
            Credentials(username="", password='pw')
            
        with self.assertRaisesRegex(CredentialsNotFoundError, "Password cannot be empty"):
            Credentials(username='user', password=None)

        with self.assertRaisesRegex(CredentialsNotFoundError, "Password cannot be empty"):
            Credentials(username='user', password="")

if __name__ == '__main__':
    unittest.main()