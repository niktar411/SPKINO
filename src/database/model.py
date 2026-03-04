from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.orm import sessionmaker, declarative_base, DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_session, async_sessionmaker
from datetime import datetime
from src.database.config import DBConfig

config = DBConfig()

# Настройка базы данных
# SQLALCHEMY_DATABASE_URL = "sqlite:///./cinema_pro.db"
# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Настройка базы данных (асинхронный вариант)
SQLALCHEMY_DATABASE_URL = config.url
engine = create_async_engine(SQLALCHEMY_DATABASE_URL)
session_maker = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    ...


# 1. Модель для хранения информации о фильмах
class MovieInfo(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    year = Column(String)
    rated = Column(String)
    released = Column(String)
    runtime = Column(String)
    genre = Column(String)
    director = Column(String)
    writer = Column(Text)
    actors = Column(Text)
    plot = Column(Text)
    language = Column(String)
    country = Column(String)
    awards = Column(String)
    poster = Column(String)
    metascore = Column(String)
    imdb_rating = Column(String)
    imdb_votes = Column(String)
    imdb_id = Column(String, index=True)
    type = Column(String)
    box_office = Column(String)
    production = Column(String)
    season = Column(String)
    episode = Column(String)
    series_id = Column(String)
    response = Column(String)
    created_at = Column(DateTime, default=datetime.now)


# 2. Шаблон билета
class MovieSessions(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(Integer)
    hall = Column(String)
    row = Column(Integer)
    seat = Column(Integer)
    start_time = Column(DateTime)
    price = Column(String)
    created_at = Column(DateTime, default=datetime.now)


# 3. Модель для покупки билетов
class MovieTicket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(Integer)
    hall = Column(String)
    row = Column(Integer)
    seat = Column(Integer)
    start_time = Column(DateTime)
    email = Column(String)
    price = Column(String)
    is_available = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)


# Создание таблиц
def init_db():
    Base.metadata.create_all(bind=engine)


def insert_movie_to_db(db, movie_data):
    """Добавляет фильм в базу"""

    info = movie_data

    # Получаем название фильма
    movie_title = info.get('Title')

    if not movie_title:
        raise ValueError("API не вернуло ключ 'Title' в данных о фильме")

    # Проверяем, есть ли фильм (лучше проверять по imdb_id, если он есть, но оставим по title)
    existing_movie = db.query(MovieInfo).filter(MovieInfo.title == movie_title).first()

    if not existing_movie:
        new_movie = MovieInfo(
            title=movie_title,
            year=info.get('Year'),
            rated=info.get('Rated'),
            released=info.get('Released'),
            runtime=info.get('Runtime'),
            genre=info.get('Genre'),
            director=info.get('Director'),
            writer=info.get('Writer'),
            actors=info.get('Actors'),
            plot=info.get('Plot'),
            language=info.get('Language'),
            country=info.get('Country'),
            awards=info.get('Awards'),
            poster=info.get('Poster'),
            metascore=info.get('Metascore'),
            imdb_rating=info.get('imdbRating'),
            imdb_votes=info.get('imdbVotes'),
            imdb_id=info.get('imdbID'),
            type=info.get('Type'),
            box_office=info.get('BoxOffice'),
            production=info.get('Production'),
            season=info.get('Season'),
            episode=info.get('Episode'),
            series_id=info.get('seriesID'),
            response=info.get('Response')
        )
        db.add(new_movie)
        db.commit()
        db.refresh(new_movie)
        print(f"Фильм '{movie_title}' добавлен.")
        return new_movie

    print(f"Фильм '{movie_title}' уже существует.")
    return existing_movie


def sessions_db(db, movie_id, start_dt, hall, price, row=5, seat=8):
    """Создает билет"""
    new_ticket = MovieSessions(
        movie_id=movie_id,
        hall=hall,
        row=row,
        seat=seat,
        price=price,
        start_time=start_dt
    )
    db.add(new_ticket)
    db.commit()


def add_ticket_to_db(db, movie_id, start_dt, hall, price, row, seat, email):
    """Создает билет"""
    new_ticket = MovieTicket(
        movie_id=movie_id,
        hall=hall,
        row=row,
        seat=seat,
        email=email,
        price=price,
        is_available=False,
        start_time=start_dt
    )
    db.add(new_ticket)
    db.commit()


if __name__ == "__main__":
    init_db()  # Создаем таблицы
