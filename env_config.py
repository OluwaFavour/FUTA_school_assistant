from functools import lru_cache
from pydantic_settings import BaseSettings


class EnvSettings(BaseSettings):
    allow_credentials: bool = True
    allowed_methods: list[str] = ["*"]
    allowed_origins: list[str] = ["*"]
    app_name: str = "FUTA SCHOOL OF COMPUTING ASSISTANT API"
    app_version: str = "0.0.1"
    database_url: str = "sqlite:///./test.db"
    debug: bool = True
    openai_key: str
    openai_max_tokens: int = 1000
    openai_soc_model: str
    openai_admission_model: str
    openai_organization_id: str
    openai_project_id: str
    session_expire_days: int = 7
    session_same_site: str = "lax"
    session_secret_key: str
    session_secure: bool = False

    class Config:
        env_file = ".env"


@lru_cache()
def get_env_settings():
    return EnvSettings()


env = get_env_settings()
