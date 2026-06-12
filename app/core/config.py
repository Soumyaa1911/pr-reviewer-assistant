from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    LLM_API_KEY: str
    CHROMA_DB_PATH: str = "./data/chroma_db"

    class Config:
        env_file = ".env"


settings = Settings()