import os
from dotenv import load_dotenv


class Config:
    load_dotenv()
    SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}/{os.getenv('POSTGRES_DB')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = "./static/images"
    MAX_CONTENT_PATH = 3 * 1024 * 1024  # 3 мегабайта
