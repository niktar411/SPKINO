from src.database import model

async def get_db():
    db = model.SessionLocal()
    try:
        yield db
    finally:
        db.close()