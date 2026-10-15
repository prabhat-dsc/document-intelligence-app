from pathlib import Path
from pydantic_settings import BaseSettings , SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    app_env: str 

    groq_api_key: str
    groq_model: str 

    embedding_model: str 
    reranker_model: str 

    ocr_dpi: int 
    ocr_language: str 
    tesseract_cmd: str 

    chunk_size: int 
    chunk_overlap: int 

    dense_top_k: int
    keyword_top_k: int 
    rerank_top_k: int 

    max_upload_size_mb: int 
    max_memory_messages: int 

    chroma_dir: Path = BASE_DIR / "data" / "chroma_db"
    upload_dir: Path = BASE_DIR / "data" / "uploads"
    sqlite_db: Path = BASE_DIR / "data" / "app.db"

    model_config = SettingsConfigDict(
        env_file= BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra= "ignore"
    )

settings = Settings()






