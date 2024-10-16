from .env_config import env
from .openai_client import OpenAIClient

# Session Settings
SESSION_EXPIRE_DAYS = env.session_expire_days
SESSION_SAME_SITE = env.session_same_site
SESSION_SECRET_KEY = env.session_secret_key
SESSION_SECURE = env.session_secure

# Debug Settings
DEBUG = env.debug

# Application Settings
APP_NAME = env.app_name
APP_VERSION = env.app_version

# CORS Settings
ALLOW_CREDENTIALS = env.allow_credentials
ALLOWED_METHODS = env.allowed_methods
ALLOWED_ORIGINS = env.allowed_origins


# Database URL
SQLALCHEMY_DATABASE_URL = env.database_url

# OpenAI Settings
OPENAI_KEY = env.openai_key
OPENAI_MAX_TOKENS = env.openai_max_tokens
OPENAI_SOC_MODEL = env.openai_soc_model
OPENAI_ADMISSION_MODEL = env.openai_admission_model
OPENAI_ORGANIZATION_ID = env.openai_organization_id
OPENAI_PROJECT_ID = env.openai_project_id
OPENAI_CLIENT = OpenAIClient(
    api_key=OPENAI_KEY,
    organization=OPENAI_ORGANIZATION_ID,
    project=OPENAI_PROJECT_ID,
    soc_model=OPENAI_SOC_MODEL,
    admission_model=OPENAI_ADMISSION_MODEL,
    max_tokens=OPENAI_MAX_TOKENS,
)
