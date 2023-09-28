from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import time
from .config import app_settings

# Define the database URL using app_settings for database configuration
SQLALCHEMY_DATABASE_URL = f"postgresql://{app_settings.DATABASE_USERNAME}:{app_settings.DATABASE_PASSWORD}@{app_settings.DATABASE_HOSTNAME}/{app_settings.DATABASE_NAME}"

# Create a database engine using SQLAlchemy
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a session maker with specific settings for database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define the base class for SQLAlchemy models
Base = declarative_base()

# Dependency function to get a database session
def get_db():
    # Create a new database session
    db = SessionLocal()
    try:
        # Yield the session for use in a route or function
        yield db
    finally:
        # Close the session when it's no longer needed
        db.close()

# Establish a connection to a PostgreSQL database using psycopg2
# while True:
#     try:
#         conn = psycopg2.connect(host=app_settings.DATABASE_HOSTNAME, user=app_settings.DATABASE_USERNAME, password=app_settings.DATABASE_PASSWORD, database=app_settings.DATABASE_NAME, 
#                                 cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         # Print a success message when the connection is established
#         print("Connecting to online-classroom-api database Successful✅")
#         break
#     except:
#         # If the connection fails, print an error message and retry after a delay
#         print("Connection to online-classroom-api database failed❌")
#         time.sleep(2)

