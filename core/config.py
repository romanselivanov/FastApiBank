from pydantic import AnyHttpUrl, BaseSettings, EmailStr, validator
from typing import Any, Dict, List, Optional, Union


class Settings(BaseSettings):
    SECRET_KEY: str = "pkrLcCsRuKm-NxCiFLaho6WruPbgjSdlhh4WKbj2YcE"
    ALGORITHM: str = "HS256"
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    SERVER_HOST: str = "http://localhost:8000"

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    SQLALCHEMY_DATABASE_URI: Optional[str] = "sqlite:///example.db"
    TEST_SQLALCHEMY_DATABASE_URI: Optional[str] = "sqlite:///example_test.db"
    FIRST_SUPERUSER: EmailStr = "admin@rt.com"

    PROJECT_NAME: str = "TestBank"

    SMTP_TLS: bool = False
    SMTP_PORT: Optional[int] = 8025
    SMTP_HOST: Optional[str] = "localhost"
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: Optional[EmailStr] = "testbank@gmail.com"
    EMAILS_FROM_NAME: Optional[str] = "TestBank"

    @validator("EMAILS_FROM_NAME")
    def get_project_name(cls, v: Optional[str], values: Dict[str, Any]) -> str:
        if not v:
            return values["PROJECT_NAME"]
        return v

    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48
    EMAIL_TEMPLATES_DIR: str = "utils/email-templates/build"
    EMAILS_ENABLED: bool = True

    @validator("EMAILS_ENABLED", pre=True)
    def get_emails_enabled(cls, v: bool, values: Dict[str, Any]) -> bool:
        return bool(
            values.get("SMTP_HOST")
            and values.get("SMTP_PORT")
            and values.get("EMAILS_FROM_EMAIL")
        )

    class Config:
        case_sensitive = True


settings = Settings()
