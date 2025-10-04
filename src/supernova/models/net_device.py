from dataclasses import dataclass
from .credentials import Credentials

@dataclass
class NetworkDevice:
    hostname: str
    ip: str
    credentials: Credentials
    device_type: str

    def __str__(self):
        return f"{self.hostname} ({self.ip})" 