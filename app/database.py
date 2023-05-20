from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define location of notes sqllite database.
SQLITE_DATABASE_URL = "sqlite:///./note.db"

# Create SQLAlchemy engine and provided it with the database URL.
engine = create_engine(SQLITE_DATABASE_URL,echo=True, connect_args={"check_same_thread": False})

# Create SQLAlchemy session with earlier defined engine.
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

# Define base so that SQLAlchemy can pick up tables from defined models.
Base = declarative_base()

# Create a new database session and close same after applciation is closed.
def get_db():
    '''
    # get database session function.
      input parameters = none.
      response = db connection.       
    '''
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()