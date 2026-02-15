import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 1. Identifica o ambiente (padrão é 'dev')
# Esta variável virá do seu terminal ou do seu Makefile
env_state = os.getenv("APP_ENV", "dev")

# 2. Define o caminho para o arquivo .env correto baseado no estado
# Usamos o caminho relativo à raiz para evitar erros de diretório
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if env_state == "test":
    dotenv_path = os.path.join(base_dir, ".env.test")
else:
    dotenv_path = os.path.join(base_dir, ".env.dev")

# Carrega as variáveis do arquivo específico
load_dotenv(dotenv_path)

# 3. Obtém a DATABASE_URL ou monta a partir das variáveis
# Dica: É mais robusto pegar a URL pronta se ela existir no .env
URL_DATABASE = os.getenv("DATABASE_URL")

if not URL_DATABASE:
    # Caso não exista a URL pronta, monta usando as variáveis individuais
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")
    URL_DATABASE = f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

# 4. Criação do engine com pool_pre_ping para evitar conexões "zumbis"
engine = create_engine(URL_DATABASE, pool_pre_ping=True)

# 5. Configuração da sessão e classe base
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()