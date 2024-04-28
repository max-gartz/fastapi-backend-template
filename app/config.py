from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class AuthSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='auth_')

    secret_key: SecretStr
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='database_')

    host: str
    port: int
    name: str
    user: str
    password: SecretStr
    protocol: str
    driver: str

    @property
    def url(self) -> str:
        return (
            f"{self.protocol}+{self.driver}://"
            f"{self.user}:{self.password.get_secret_value()}"
            f"@{self.host}:{self.port}/{self.name}"
        )


class LoggerSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='logger_')

    config_path: str = "logging.yaml"


class Settings(BaseSettings):
    auth: AuthSettings = AuthSettings()
    database: DatabaseSettings = DatabaseSettings()
    logger: LoggerSettings = LoggerSettings()


settings = Settings()
