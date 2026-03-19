from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy import select
from sqlalchemy.orm import Session
from collections import defaultdict
from src.utils.log import logger
from src.database import model
import src.database.methods as db_methods
from src.backend.routes import routers
from contextlib import asynccontextmanager
import pyprojroot as ppr
rootpath = ppr.here()

static_path = rootpath / "src" / "frontend" / "static"
template_path = rootpath / "src" / "frontend" / "templates"

templates = Jinja2Templates(directory=template_path)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Запуск приложения")

    for router in routers:
        app.include_router(router)
    yield
    logger.info("Завершил работу")

app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory=static_path), name="static")



# Зависимость для получения сессии БД
async def get_db():
    db = model.session_maker()
    try:
        yield db
    finally:
        await db.close()

@app.get("/")
async def home(request: Request, db: Session = Depends(get_db)):

    movies = await db_methods.get_movies()
    tickets = await db_methods.get_tickets()

    return templates.TemplateResponse("index.html", {
        "request": request, 
        "movies": movies,
        "tickets": tickets
    })

