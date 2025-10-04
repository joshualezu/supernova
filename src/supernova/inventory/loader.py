import csv
from ..models.net_device import NetworkDevice
from ..models.credentials import Credentials
from ..exceptions import CredentialsNotFoundError

def load_devices_from_csv(filepath: str, creds:Credentials) -> list[NetworkDevice]:
    devices = []
    if not creds.username or not creds.password:
        raise CredentialsNotFoundError(
            f"Missing username or password in credentials!"
        )
    try:
        with open(filepath, 'r', newline='') as csvfile:
            dict_reader = csv.DictReader(csvfile)

            for row in dict_reader:
                device = NetworkDevice(
                    hostname='unknown',
                    ip = row['switch_ip'],
                    credentials= creds,
                    device_type = row.get('device_os') or 'cisco_ios',
                )
                devices.append(device)
        
    except KeyError as e:
        print(f"Error: Missing required column in CSV file: {e}")
        raise
    except FileNotFoundError:
        print(f"Error: Inventory file not found at {filepath}")
        raise

    return devices