from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy import select
from sqlalchemy.orm import Session
from collections import defaultdict
from src.utils.log import logger
from src.database import model
from src.backend.routes import routers
from contextlib import asynccontextmanager
from pathlib import Path

templates = Jinja2Templates(directory=Path(__file__).parent.parent / "frontend" / "templates")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Запуск приложения")
    await model.init_db()

    for router in routers:
        app.include_router(router)
    yield
    logger.info("Завершил работу")

app = FastAPI(lifespan=lifespan)

static_path = Path(__file__).parent.parent / "frontend" / "static"
app.mount("/static", StaticFiles(directory=static_path), name="static")



# Зависимость для получения сессии БД
async def get_db():
    db = model.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def home(request: Request, db: Session = Depends(get_db)):

    stmt = select(model.MovieSessions).order_by(model.MovieSessions.start_time)
    result = await db.execute(stmt)
    sessions = result.scalars().all()
    
    data = {session.start_time for session in sessions}
    print([s.strftime("%d-%m-%Y %H:%M") for s in data])
    active_movie_ids = {session.movie_id for session in sessions}
    
    if active_movie_ids:
        movies = db.query(model.MovieInfo).filter(model.MovieInfo.id.in_(active_movie_ids)).all()
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

