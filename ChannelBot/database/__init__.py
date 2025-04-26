from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from Config import DATABASE_URL

# Create a base class for declarative models
BASE = declarative_base()

# Create a database engine
engine = create_engine(DATABASE_URL)

# Create a session factory
session_factory = sessionmaker(bind=engine, autoflush=False)
SESSION = scoped_session(session_factory)

# Function to initialize the database
def init_db():
    # Import all modules here that define models
    # This avoids circular imports
    # Uncomment and add your model imports as needed:
    # from ChannelBot.database import users_sql, channel_sql
    
    BASE.metadata.bind = engine
    BASE.metadata.create_all(bind=engine)
    
    return SESSION

# Initialize the database on import
init_db()
