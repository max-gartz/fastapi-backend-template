import os
from unittest.mock import MagicMock

from fastapi.testclient import TestClient

ENV = dict(
    APP_HOST="0.0.0.0",  # nosec
    APP_PORT="8080",
    APP_WORKERS="1",
    APP_TIMEOUT="60",
    AUTH_SECRET_KEY="secret",  # nosec
    LOGGER_CONFIG_PATH="logging.yaml",
    DATABASE_PROTOCOL="postgresql",
    DATABASE_DRIVER="psycopg",
    DATABASE_HOST="localhost",
    DATABASE_PORT="5432",
    DATABASE_USER="postgres",
    DATABASE_PASSWORD="password",  # nosec
    DATABASE_NAME="postgres"
)

for key, value in ENV.items():
    os.environ[key] = value


def override_get_db_session() -> MagicMock:
    mock_db_session = MagicMock()
    return mock_db_session


from app.main import root  # noqa E402
from app.api.dependencies import get_db_session  # noqa E402

root.dependency_overrides[get_db_session] = override_get_db_session
client = TestClient(root)
