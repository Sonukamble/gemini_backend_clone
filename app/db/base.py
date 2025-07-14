from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine

from app.config import Config


Base = declarative_base()
database_url=f"postgresql+psycopg2://{Config.DB_USERNAME}:{Config.DB_PASSWORD}@{Config.DB_HOST}:{Config.DB_PORT}/{Config.DB_NAME}"

engine= create_engine(database_url, echo=True)

# Create all tables
Base.metadata.create_all(bind=engine)
# To Check connection
try:
    connection = engine.connect()
    print("Database connected successfully!")
except Exception as e:
    print(f"Failed to connect to the database: {e}")