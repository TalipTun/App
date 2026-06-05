from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from urllib.parse import quote_plus

def get_postgres_password():
    with open("/run/secrets/postgres_password", "r") as file:
        return file.read().strip()
    
POSTGRES_USER = "gitpulse_user"
POSTGRES_PASSWORD = quote_plus(get_postgres_password())
POSTGRES_HOST = "db"
POSTGRES_PORT = "5432"
POSTGRES_DB = "gitpulse_db"

DATABASE_URL = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
    f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

Base.metadata.create_all(bind=engine)
