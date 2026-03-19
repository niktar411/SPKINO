from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from src.database.client import get_db
from src.database import model

router = APIRouter(prefix='/pages', tags=['Pages', 'Страницы'])

templates = Jinja2Templates(directory="src/frontend/templates")


@router.get("/createSessionPage")
async def gotopage(request: Request, db: Session = Depends(get_db)):
    tickets = db.query(model.MovieTicket).order_by(model.MovieTicket.start_time.desc()).all()
    sessions = db.query(model.MovieSessions).order_by(model.MovieSessions.start_time.desc()).all()
    movies = db.query(model.MovieInfo).all()

    return templates.TemplateResponse("create.html", {
        "request": request,
        "tickets": tickets,
        "sessions": sessions,
        "movies": movies
    })

