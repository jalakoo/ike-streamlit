from neo4j import GraphDatabase
from pydantic import BaseModel
from typing import Optional


class Neo4jCredentials(BaseModel):
    """Credentials for accessing a Neo4j database instance

    Args:
        uri (str): The URI address of the Neo4j database.
        password (str): The password for authentication with the Neo4j database.
        username (str): The username for authentication with the Neo4j database. Default is "neo4j".
        database (str): The database to use for multi-database instances. Defaults to "neo4j".

    Returns:
        _type_: _description_
    """

    uri: str
    password: str
    username: Optional[str] = "neo4j"
    database: Optional[str] = "neo4j"

    def __hash__(self):
        return hash((type(self),) + tuple(self.items()))

    def __xgetstate__(self):
        return self.__dict__

    def __setstate__(self, state):
        self.__dict__ = state

    def is_ready(self):
        if self.uri is None or self.uri == "":
            return False
        if self.password is None or self.password == "":
            return False
        if self.username is None or self.username == "":
            return False
        if self.database is None or self.database == "":
            return False
        return True
