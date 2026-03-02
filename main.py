from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from datetime import datetime

import database 
from data_create import create_movie as get_data_from_api 

app = FastAPI() # Запуск uvicorn main:app --reload

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

database.init_db()

# Зависимость для получения сессии БД
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def home(request: Request, db: Session = Depends(get_db)):
    movies = db.query(database.MovieInfo).all()
    
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "movies": movies
    })

@app.get("/{movie_id}/hall-seats")
async def hall_seats(request: Request, movie_id: int, db: Session = Depends(get_db)):
    tickets = db.query(database.MovieTicket).filter(database.MovieTicket.movie_id == movie_id).order_by(database.MovieTicket.start_time.desc()).all()

    return templates.TemplateResponse(
        "hall.html", 
        {
            "request": request, 
            "movie_id": movie_id,
            "tickets": tickets
        }
    )

@app.get("/create")
async def create(request: Request, db: Session = Depends(get_db)):
    tickets = db.query(database.MovieTicket).order_by(database.MovieTicket.start_time.desc()).all()
    sessions = db.query(database.MovieSessions).order_by(database.MovieSessions.start_time.desc()).all()
    movies = db.query(database.MovieInfo).all()
    
    return templates.TemplateResponse("create.html", {
        "request": request, 
        "tickets": tickets,
        "sessions": sessions,
        "movies": movies
    })

# --- НОВЫЙ МАРШРУТ ДЛЯ ДОБАВЛЕНИЯ ЧЕРЕЗ IMDB ID ---
@app.post("/add_api_movie")
async def add_movie_by_id(
    imdb_id: str = Form(...),
    session_time: str = Form(...),
    hall: str = Form(...),
    price: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        movie_data = get_data_from_api(IMDB_ID=imdb_id)
        
        movie_obj = database.insert_movie_to_db(db, movie_data)
        
        # 3. Создаем сеанс на указанное время
        dt_object = datetime.fromisoformat(session_time)
        database.sessions_db(db=db, movie_id=movie_obj.id, start_dt=dt_object, hall=hall, row=5, seat=8, price=price)
        
    except Exception as e:
        print(f"Ошибка при добавлении: {e}")
        
    return RedirectResponse(url="/", status_code=303)