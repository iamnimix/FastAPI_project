from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import hashlib

# SQLALCHEMY_DATABASE_URL = "sqlite:///./Core/sql_app.db"
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:mamali1991@/blog"
# pip install psycopg2-binary
# run psql with "sudo --login --user=postgres psql"
# create a database called blog
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    # connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
