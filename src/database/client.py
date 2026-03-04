from src.database import model

def get_db():
    db = model.SessionLocal()
    try:
        yield db
    finally:
        db.close()