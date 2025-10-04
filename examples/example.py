import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from supernova.inventory.loader import load_devices_from_csv
from supernova.models.credentials import Credentials

def main():
    inventory_file = os.path.join(os.path.dirname(__file__), '..', 'config', 'network_devices.csv')

    device_creds = Credentials(username="bob", password="bob", secret="bob")

    try:
        devices = load_devices_from_csv(inventory_file, device_creds)

    except Exception as e:
        print(e)

main()