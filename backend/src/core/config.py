from pydantic_settings import BaseSettings, SettingsConfigDict

# enviroment configuration
class Settings(BaseSettings):
    
    
    DATABASE_URL_DEVELOP: str
    DATABASE_URL_DEVELOP_POOLED: str
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )
    
settings = Settings()