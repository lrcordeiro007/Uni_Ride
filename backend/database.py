import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

env_state = os.getenv("APP_ENV", "dev")

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if env_state == "test":
    dotenv_path = os.path.join(base_dir, ".env.test")
else:
    dotenv_path = os.path.join(base_dir, ".env.dev")

load_dotenv(dotenv_path)

URL_DATABASE = os.getenv("DATABASE_URL")

if not URL_DATABASE:
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")
    URL_DATABASE = f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

engine = create_engine(URL_DATABASE, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()