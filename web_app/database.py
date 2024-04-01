from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2

DB_NAME = "master"
DB_USER = "postgres"
DB_PASS = "1234"
DB_HOST = "localhost"
DB_PORT = "5432"

db_url = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
engine = create_engine(
    db_url, connect_args={}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()





def connect_to_database():
    DB_NAME = "master"
    DB_USER = "postgres"
    DB_PASS = "1234"
    DB_HOST = "localhost"
    DB_PORT = "5432"

    db_url = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
    conn = psycopg2.connect(  db_url )
    cursor=conn.cursor()
    return cursor,conn