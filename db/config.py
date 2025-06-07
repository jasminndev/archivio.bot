from os import getenv
from dotenv import load_dotenv

load_dotenv(".env")


class DB:
    DB_NAME = getenv('DB_NAME')
    DB_USER = getenv('DB_USER')
    DB_PORT = getenv('DB_PORT')
    DB_HOST = getenv('DB_HOST')
    DB_PASSWORD = getenv('DB_PASSWORD')
    DB_ENGINE = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
