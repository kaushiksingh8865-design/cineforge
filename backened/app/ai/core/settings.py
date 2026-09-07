from pydantic_settings import BaseSettings # provide us configuration system 
from pydantic_settings import SettingsConfigDict  # how should those settings be loaded
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[4]

class Settings(BaseSettings):
    gemini_api_key:str
    database_url:str
    parallel_api_key:str
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",


       
    ) 


settings = Settings()  # create an instance of the settings class