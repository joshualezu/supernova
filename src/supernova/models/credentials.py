from dataclasses import dataclass

from ..exceptions import CredentialsNotFoundError

@dataclass
class Credentials:
    """A data class to securely hold device credentials."""
    username: str
    password: str
    secret: str | None = None

    def __post_init__(self):
        """Validate that required fields are not empty."""
        if not self.username:
            raise CredentialsNotFoundError("Username cannot be empty")
        if not self.password:
            raise CredentialsNotFoundError("Password cannot be empty")

    def __repr__(self) -> str:
        """Return a secure representation of the credentials."""
        # Determine how to display the secret securely
        secret_repr = "'****'" if self.secret else "None"
        
        return (
            f"{self.__class__.__name__}("
            f"username='{self.username}', "
            f"password='****', "
            f"secret={secret_repr}"
            ")"
        )
