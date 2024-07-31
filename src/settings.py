from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    jwt_secret_key: str
    jwt_algorithm: str
    mongo_address: str
    mongo_username: str
    mongo_password: str
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
