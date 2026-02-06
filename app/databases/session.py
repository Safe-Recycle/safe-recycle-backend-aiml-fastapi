from app.core.config import settings
from sqlmodel import SQLModel, Session, create_engine

DATABASE_URL = settings.DATABASE_URL

engine = create_engine(
    DATABASE_URL,
    echo=True, # Melihat query SQL
    pool_pre_ping=False
)

def get_session():
    """
    Dependency FastAPI untuk mendapatkan DB session.
    Session akan otomatis ditutup setelah request selesai.
    """
    with Session(engine) as session:
        yield session
                
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)