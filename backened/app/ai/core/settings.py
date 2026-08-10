from pydantic_settings import BaseSettings # provide us configuration system 
from pydantic_settings import SettingsConfigDict  # how should those settings be loaded


class Settings(BaseSettings):
    gemini_api_key:str
    model_config = SettingsConfigDict(env_file=".env")  # load settings from .env file....#


settings = Settings()  # create an instance of the settings class