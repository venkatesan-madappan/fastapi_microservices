from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL

DB_URL = URL.create(
    "postgresql+psycopg2",
    username="venkatesan",
    password="Sriviviji@101",
    host="localhost",
    port="5432",
    database="fcms"
    )

Base = declarative_base()

db_engine = create_engine(DB_URL, echo=True)

SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
# SessionFactory = sessionmaker(bind=db_engine)

print("Db Creation starts")
Base.metadata.create_all(bind=db_engine)
print("Db Creation Ends")

def sess_db():
    db = SessionFactory()
    try:
        yield db
    finally:
        db.close()
