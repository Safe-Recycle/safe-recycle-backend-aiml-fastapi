from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str
    ENV: str
    
    GEMINI_API_KEY: str
    GEMINI_MODEL_NAME: str

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    
    DATABASE_URL: str
    DB_DRIVER: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    
    class Config:
        env_file = ".env"
        
settings = Settings()