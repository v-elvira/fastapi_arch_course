import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent  # env_file = '.env' with no exact path was not found

class Settings(BaseSettings):
    DB_NAME: str

    model_config = SettingsConfigDict(env_file=os.path.join(BASE_DIR, '.env'))  # default: '.env' (, extra='ignore')


settings = Settings()
