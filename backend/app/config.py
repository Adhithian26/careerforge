import os
from typing import List
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    PROJECT_NAME: str = "CareerForge AI"
    VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api/v1"
    
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # Comma-separated or list of allowed origins
    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000,http://127.0.0.1:5173"
    
    # Database
    DATABASE_URL: str = "sqlite:///./careerforge.db"
    
    # Security
    SECRET_KEY: str = "local_development_careerforge_secret_key_2026_safe"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 day
    
    # AI / Gemini
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-flash-lite-latest"
    DEFAULT_AI_PROVIDER: str = "gemini"
    
    # MCP
    MCP_SERVER_PORT: int = 8080
    MCP_AUTH_TOKEN: str = "local_mcp_dev_token_2026"
    
    # Sandbox Limits
    CODE_EXEC_TIMEOUT_SECONDS: int = 3
    MAX_CODE_LENGTH: int = 10000

    @property
    def cors_origin_list(self) -> List[str]:
        if isinstance(self.CORS_ORIGINS, str):
            return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]
        return ["*"]

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
