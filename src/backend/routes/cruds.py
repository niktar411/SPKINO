from fastapi import APIRouter, Depends, Form
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from datetime import datetime
from src.database.client import get_db
from src.database.data_create import create_movie
from src.database import model
router = APIRouter(prefix='/cruds', tags=['CRUD Tasks', 'CRUD-задачи'])



# Добавление фильма по id
@router.post("/add_api_movie")
async def add_movie_by_id(
    imdb_id: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        # Ищем фильм по id и сохраняем
        movie_data = create_movie(IMDB_ID=imdb_id)
        model.insert_movie_to_db(db, movie_data)
        
    except Exception as e:
        print(f"Фильм не найдел или произошла ошибка: {e}")
        
    return RedirectResponse(url="/create", status_code=303) #303 - успешно

# Создание сессии
@router.post("/add_api_session")
async def add_movie_by_id(
    movie_id: str = Form(...),
    session_time: str = Form(...),
    hall: str = Form(...),
    price: str = Form(...),
    db: Session = Depends(get_db)
):
    try:  
        # Создаем сеанс на указанное время
        dt_object = datetime.fromisoformat(session_time)
        model.sessions_db(db=db, movie_id=movie_id, start_dt=dt_object, hall=hall, row=5, seat=8, price=price)
        
    except Exception as e:
        print(f"Ошибка при создании сеанса: {e}")
        
    return RedirectResponse(url="/create", status_code=303)