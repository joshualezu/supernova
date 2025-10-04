import unittest
import csv
import tempfile
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from supernova.inventory.loader import load_devices_from_csv
from supernova.models.credentials import Credentials
from supernova.exceptions import CredentialsNotFoundError

class TestInventoryLoader(unittest.TestCase):

    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.csv', newline='')
        self.inventory_data = [
            ['switch_ip', 'device_os'],
            ['192.168.3.32', 'cisco_xe'],
            ['192.167.4.2', ''], 
        ]
        with self.temp_file as f:
            writer = csv.writer(f)
            writer.writerows(self.inventory_data)
        
        self.temp_filepath = self.temp_file.name
        self.temp_file.close()
    
    def tearDown(self):
        """Clean up the temporary file."""
        os.unlink(self.temp_filepath)

    def test_load_devices_from_csv_success(self):
        device_creds = Credentials(username="bob", password="steve", secret="bob2")
        devices = load_devices_from_csv(self.temp_filepath, device_creds)

        self.assertEqual(len(devices), 2)

        device1 = devices[0]
        self.assertEqual(device1.ip, '192.168.3.32')
        self.assertEqual(device1.device_type, 'cisco_xe')
        self.assertIsInstance(device1.credentials, Credentials)
        self.assertEqual(device1.credentials.username, "bob")
        self.assertEqual(device1.credentials.password, "steve")
        self.assertEqual(device1.credentials.secret, "bob2")

        device2 = devices[1]
        self.assertEqual(device2.ip, '192.167.4.2')
        self.assertEqual(device2.device_type, 'cisco_ios')
        self.assertIsInstance(device2.credentials, Credentials)
        self.assertEqual(device2.credentials.username, "bob")
        self.assertEqual(device2.credentials.password, "steve")
        self.assertEqual(device2.credentials.secret, "bob2")

    def test_missing_required_column(self):
        bad_data = [
            ['device_os'],
            ['192.168.3.32', 'cisco_xe'],
        ]
        
        with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.csv', newline='') as bad_file:
            writer = csv.writer(bad_file)
            writer.writerows(bad_data)
            bad_filepath = bad_file.name

        with self.assertRaises(KeyError):
            device_creds = Credentials(username="bob", password="steve", secret="bob2")
            load_devices_from_csv(bad_filepath, creds=device_creds)
        
        os.unlink(bad_filepath)

    def test_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            device_creds = Credentials(username="bob", password="steve", secret="bob2")
            load_devices_from_csv("non_existent_file.csv", creds=device_creds)

    def test_credentials_not_found(self):
        with self.assertRaises(CredentialsNotFoundError):
            device_creds = Credentials(username="", password="steve", secret="bob2")
            devices = load_devices_from_csv(self.temp_filepath, device_creds)

if __name__ == '__main__':
    unittest.main()

