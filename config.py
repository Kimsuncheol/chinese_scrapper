import os

from dotenv import load_dotenv

load_dotenv()


def _db_url() -> str:
    url = os.environ.get("DATABASE_URL", "postgresql+psycopg2://postgres:postgres@localhost:5432/chinese_scrapper")
    # Some hosts still hand out postgres://
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql+psycopg2://", 1)
    elif url.startswith("postgresql://"):
        url = url.replace("postgresql://", "postgresql+psycopg2://", 1)
    return url


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-only-change-me")
    SQLALCHEMY_DATABASE_URI = _db_url()
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    KAKAO_REST_API_KEY = os.environ.get("KAKAO_REST_API_KEY", "")
    KAKAO_CLIENT_SECRET = os.environ.get("KAKAO_CLIENT_SECRET", "")
    KAKAO_REDIRECT_URI = os.environ.get("KAKAO_REDIRECT_URI", "http://localhost:5000/auth/kakao/callback")
    KAKAO_SCOPE = os.environ.get("KAKAO_SCOPE", "profile_nickname,profile_image")
