from json import loads
from typing import Dict, Tuple

import psycopg2
from boto3 import client as Client
from cryptography.fernet import Fernet

LINEVISION_DATABASES = [  # server, database
    ("masterdata", "masterdata"),
    ("telemetry", "edge_telemetry"),
    # ("emf_telemetry", "emf_telemetry"),
    ("telemetry", "emf_telemetry"),
    ("telemetry", "gwc_weather"),
    ("telemetry", "linevision_calculated"),
    ("portal", "portal_data"),
]


class ConnectionManager:
    """A database connection management class."""

    connections: Dict[Tuple, psycopg2.extensions.connection]

    def __init__(self):
        """Initialize the connection dictionary."""
        self.connections = {
            (env, server, database): None
            for server, database in LINEVISION_DATABASES
            for env in ("prod", "dev")
        }

    def connect(
        self, server: str, database: str, env: str = "prod"
    ) -> psycopg2.extensions.connection:
        """Establish a connection to a database."""
        if self.connections[env, server, database] is None:
            self.connections[env, server, database] = get_connection(
                server, database, env=env
            )

        return self.connections[env, server, database]


def get_secret(server: str, env: str = "prod") -> dict:
    """Retrieve the database secret from AWS Secrets Manager."""
    secret_id = f"{env}/{server}/db"
    client = Client("secretsmanager")
    return loads(client.get_secret_value(SecretId=secret_id)["SecretString"])


def get_connection(
    server: str, database: str, env: str = "prod"
) -> psycopg2.extensions.connection:
    """Return a connection to the specified database."""
    secret = get_secret(server, env=env)
    connection_str = (
        f"dbname={database} user={secret['username']} "
        f"password={secret['password']} host={secret['host']} port={secret['port']}"
    )
    return psycopg2.connect(connection_str)


def encrypt(message: str) -> bytes:
    """Encrypt a message using Fernet."""
    return Fernet(Fernet.generate_key()).encrypt(message.encode("utf-8"))


def decrypt(message: bytes, key: bytes) -> str:
    """Decrypt a message using Fernet."""
    return Fernet(key).decrypt(message).decode("utf-8")


conn_man = ConnectionManager()


if __name__ == "__main__":

    for env, server, database in conn_man.connections:
        conn_man.connect(server, database, env=env)
        print(conn_man.connections[env, server, database])
