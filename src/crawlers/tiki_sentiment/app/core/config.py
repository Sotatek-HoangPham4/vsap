from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "tiki_sentiment"

    DB_HOST: str = "localhost"
    DB_PORT: int = 5433
    DB_NAME: str = "tiki_sentiment"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "123456789"

    TIKI_BASE_URL: str = "https://tiki.vn"

    CATEGORY_CONCURRENCY: int = 10
    PRODUCT_CONCURRENCY: int = 30
    REVIEW_CONCURRENCY: int = 50

    class Config:
        env_file = ".env"


settings = Settings()