from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
import os

DB_URL = os.getenv("DB_URL","postgresql://root:password@db:5432/test_db")
print(DB_URL)
engine = create_engine(DB_URL,echo=False)
db_session = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )
)