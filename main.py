from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from datetime import datetime
from collections import defaultdict

import database 
from data_create import create_movie as get_data_from_api 

app = FastAPI() # Запуск: uvicorn main:app --reload

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

    sessions = db.query(database.MovieSessions).order_by(database.MovieSessions.start_time.desc()).all()
    
    active_movie_ids = {session.movie_id for session in sessions}
    
    if active_movie_ids:
        movies = db.query(database.MovieInfo).filter(database.MovieInfo.id.in_(active_movie_ids)).all()
    else:
        movies = []

    sessions_by_movie_id = defaultdict(list)
    for session in sessions:
        sessions_by_movie_id[session.movie_id].append(session)

    movies_data = []
    for movie in movies:
        movies_data.append({
            "movie": movie,
            "sessions": sessions_by_movie_id[movie.id]
        })
    
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "movies": movies_data
    })

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

# Добавление фильма по id
@app.post("/add_api_movie")
async def add_movie_by_id(
    imdb_id: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        # Ищем фильм по id и сохраняем
        movie_data = get_data_from_api(IMDB_ID=imdb_id)
        database.insert_movie_to_db(db, movie_data)
        
    except Exception as e:
        print(f"Фильм не найдел или произошла ошибка: {e}")
        
    return RedirectResponse(url="/create", status_code=303) #303 - успешно

# Создание сессии
@app.post("/add_api_session")
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
        database.sessions_db(db=db, movie_id=movie_id, start_dt=dt_object, hall=hall, row=5, seat=8, price=price)
        
    except Exception as e:
        print(f"Ошибка при создании сеанса: {e}")
        
    return RedirectResponse(url="/create", status_code=303)