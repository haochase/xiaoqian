import os
from pydantic import Field, AnyUrl
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # 基础项目信息
    PROJECT_NAME: str = "XiaoQian"
    VERSION: str = "0.1.0"

    # 数据库（Postgres）
    POSTGRES_HOST: str = Field(default="localhost")
    POSTGRES_PORT: int = Field(default=5434)  # 使用 5434，避免冲突
    POSTGRES_DB: str = Field(default="xiaoqian")
    POSTGRES_USER: str = Field(default="postgres")
    POSTGRES_PASSWORD: str = Field(default="postgres")
    DATABASE_URL: AnyUrl = Field(default_factory=lambda: f"postgresql+asyncpg://{os.getenv('POSTGRES_USER','postgres')}:{os.getenv('POSTGRES_PASSWORD','postgres')}@{os.getenv('POSTGRES_HOST','localhost')}:{int(os.getenv('POSTGRES_PORT','5434'))}/{os.getenv('POSTGRES_DB','xiaoqian')}")

    # Redis
    REDIS_HOST: str = Field(default="localhost")
    REDIS_PORT: int = Field(default=6379)
    REDIS_DB: int = Field(default=0)
    REDIS_URL: str = Field(default_factory=lambda: f"redis://{os.getenv('REDIS_HOST','localhost')}:{int(os.getenv('REDIS_PORT','6379'))}/{int(os.getenv('REDIS_DB','0'))}")

    # JWT
    SECRET_KEY: str = Field(default="super-secret-key")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=60 * 24 * 7)  # 7 天

    # 第三方服务
    OTP_PROVIDER: str = Field(default="sms")  # sms or email
    # 示例短信服务环境变量（请自行替换）
    SMS_API_KEY: str = Field(default="your_sms_api_key")
    EMAIL_SMTP_SERVER: str = Field(default="smtp.example.com")
    EMAIL_SMTP_PORT: int = Field(default=587)
    EMAIL_USERNAME: str = Field(default="your_email@example.com")
    EMAIL_PASSWORD: str = Field(default="email_password")

    # LLM Settings
    LLM_API_KEY: str = Field(default="")
    LLM_API_BASE_URL: str = Field(default="https://api.openai.com/v1")
    LLM_MODEL_NAME: str = Field(default="gpt-3.5-turbo")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
