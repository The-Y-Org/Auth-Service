from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    jwt_secret_key: str
    jwt_algorithm: str
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
