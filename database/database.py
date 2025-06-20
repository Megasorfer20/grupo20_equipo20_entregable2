import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from symptoms import symptoms, diseases

DB_FILE = "pacientes.db"
DB_URL = f"sqlite:///{DB_FILE}"

engine = create_engine(DB_URL, echo=True)

SessionLocal = sessionmaker(bind=engine)

session = SessionLocal()

def create_database():
    if not os.path.exists(DB_FILE):
        print(f"Database {DB_FILE} created.")
        Base.metadata.create_all(engine)
    else:
        print(f"Database {DB_FILE} already exists.")
    return session

def cerrar_db():
    session.close()
    engine.dispose()

if __name__ == "__main__":
    create_database()