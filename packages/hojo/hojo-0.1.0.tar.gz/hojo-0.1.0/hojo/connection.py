import json
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, scoped_session, sessionmaker


class ConnectionCredentialError(RuntimeError):
    pass


class Connection:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Connection, cls).__new__(cls)
        return cls._instance

    def __init__(
        self,
        user: str = None,
        endpoint: str = None,
        port: int = None,
        name: str = None,
        password: str = None,
    ) -> None:
        self._initialized = True
        self._session = None
        self._engine = None
        self.user = user or os.environ.get("DB_USER")
        self.endpoint = endpoint or os.environ.get("DB_ENDPOINT")
        self.port = port or os.environ.get("DB_PORT", "5432")
        self.name = name or os.environ.get("DB_NAME")
        self.password = password or os.environ.get("DB_PASSWORD", None)
        self.region = os.environ.get("AWS_REGION")
        self.environment = os.environ.get("ENVIRONMENT", "development")

        if not (
            self.user and self.endpoint and self.name and self.port and self.password
        ):
            raise ConnectionCredentialError("Invalid database credentials.")

    @property
    def session(self) -> Session:
        if self._session:
            return self._session

        self._session = self.create_session()
        return self._session

    def create_session(self) -> Session:
        session_factory = sessionmaker(
            bind=self._get_engine(), future=True, expire_on_commit=False
        )
        session: Session = scoped_session(session_factory)
        return session

    def get_connection_string(self):
        conn = "postgresql+pg8000://{}:{}@{}:{}/{}".format(
            self.user, self.password, self.endpoint, self.port, self.name
        )

        return conn

    def _get_engine(self):
        if self._engine:
            return self._engine

        self._engine = create_engine(self.get_connection_string())

        return self._engine
