class SupernovaException(Exception):
    """Base exception for this library."""
    pass
class CredentialsNotFoundError(SupernovaException):
    """Raised when credentials are not found for a device in the inventory."""
    pass
class ConnectionError(SupernovaException):
    """Raised for issues related to device connection."""
    pass

class CommandExecutionError(SupernovaException):
    """Raised when a command fails to execute properly."""
    pass