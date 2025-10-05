"""
A module for securely handling user credentials.

Provides a dataclass for storing, validating, and securely
representing sensitve user information.
"""
from dataclasses import dataclass

from ..exceptions import CredentialsNotFoundError

@dataclass
class Credentials:
    """
    A data class for storing and validating user credentials.

    This class securely holds user information and includes post-initialization
    validation to ensure that essential fields are not empty. It also provides
    a safe string representation that redacts sensitive data.

    Attributes
    ----------
    username : str
        The user's username. Cannot be an empty string.
    password : str
        The user's password. Cannot be an empty string.
    secret(enable) : str or None, optional
        An optional secret key or token (default is None).

    """
    username: str
    password: str
    secret: str | None = None

    def __post_init__(self):
        """
        Validate the credentials after the object is initialized.

        Raises
        ------
        CredentialsNotFoundError
            If `username` or `password` is an empty string.
        """
        if not self.username:
            raise CredentialsNotFoundError("Username cannot be empty")
        if not self.password:
            raise CredentialsNotFoundError("Password cannot be empty")

    def __repr__(self) -> str:
        """
        Return a secure string representation of the Credentials object.

        Returns
        -------
        str
            A string representation of the instance with sensitive data masked.
        """
        secret_repr = "'****'" if self.secret else "None"
        
        return (
            f"{self.__class__.__name__}("
            f"username='{self.username}', "
            f"password='****', "
            f"secret={secret_repr}"
            ")"
        )