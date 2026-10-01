from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "AI-Based Food Packaging Recommendation System"
    API_V1_STR: str = "/api"
    ENVIRONMENT: str = "development"
    DATABASE_URL: str = "sqlite:///./food_packaging.db"
    CORS_ORIGINS: list[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
    ]

    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=".env",
        extra="ignore",
    )


settings = Settings()
