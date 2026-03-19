from pydantic_settings import BaseSettings, SettingsConfigDict
import pyprojroot as ppr

env_path = ppr.here() / '.env'


class DBConfig(BaseSettings):
    DB_NAME: str = ''
    DB_HOST: str = ''
    DB_PORT: str = ''
    DB_USER: str = ''
    DB_PASSWORD: str = ''

    model_config = SettingsConfigDict(extra='ignore', env_file=env_path)

    @property
    def url(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"



