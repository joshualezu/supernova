from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoBaseException
from ..models.net_device import NetworkDevice
from ..exceptions import ConnectionError, CommandExecutionError

class SupernovaSession:
    """Manages the connection and interaction with a single Cisco device."""

    def __init__(self, device: NetworkDevice):
        self.device = device
        self.connection = None

    def __enter__(self):
        """Allows using the 'with' statement for automatic connection handling."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Ensures disconnection when the 'with' block is exited."""
        self.disconnect()

    def connect(self):
        """Establishes the SSH connection to the device."""
        if self.connection:
            print("Already connected.")
            return

        device_params = {
            'device_type': self.device.device_type,
            'host': self.device.ip,
            'username': self.device.credentials.username,
            'password': self.device.credentials.password,
            'secret': self.device.credentials.secret,
        }
        try:
            print(f"Connecting to {self.device.hostname}...")
            self.connection = ConnectHandler(**device_params)
            if self.device.credentials.secret:
                self.connection.enable()
            print("Connection successful.")
        except NetmikoBaseException as e:
            raise ConnectionError(f"Failed to connect to {self.device.hostname}: {e}") from e

    def disconnect(self):
        """Closes the SSH connection."""
        if self.connection:
            self.connection.disconnect()
            self.connection = None
            print(f"Disconnected from {self.device.hostname}.")

    def send_show_command(self, command: str) -> str:
        """Sends a single 'show' command and returns the raw output."""
        if not self.connection:
            raise ConnectionError("Not connected to device.")
        try:
            output = self.connection.send_command(command)
            return output
        except NetmikoBaseException as e:
            raise CommandExecutionError(f"Failed to execute command '{command}': {e}") from e

    def send_config_commands(self, commands: list[str]) -> str:
        """Sends a list of configuration commands."""
        if not self.connection:
            raise ConnectionError("Not connected to device.")
        try:
            output = self.connection.send_config_set(commands)
            return output
        except NetmikoBaseException as e:
            raise CommandExecutionError(f"Failed to execute config commands: {e}") from e