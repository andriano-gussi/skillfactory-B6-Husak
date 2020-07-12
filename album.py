# Данный модуль является вспомагательным, служит для взаимодействия с музыкальной библиотекой (чтение данных, запись новых)

import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_PATH = "sqlite:///albums.sqlite3"
Base = declarative_base()


class Album(Base):
    """ Описывает структуру таблицы album для чтения, записи данных музыкальной библиотеки """
    __tablename__ = "album"

    id = sa.Column(sa.INTEGER, primary_key=True)
    year = sa.Column(sa.INTEGER)
    artist = sa.Column(sa.TEXT)
    genre = sa.Column(sa.TEXT)
    album = sa.Column(sa.TEXT)

    def __eq__(self, other):
        """ магический метод для возможности сравнивать записи базы данных между собой """
        return self.year == other.year and self.artist == other.artist and self.genre == other.genre and self.album == other.album
        
def connect_db():
    """ Устанавливает соединение к базе данных, возвращает объект сессии """
    # создаем соединение к базе данных
    engine = sa.create_engine(DB_PATH)
    # создаем описанную таблицу
    Base.metadata.create_all(engine)
    # создаем фабрику сессию
    session = sessionmaker(engine)
    # возвращаем сессию
    return session()

def find(artist):
    """ Находит и возвращает список всех альбомов указанного исполнителя """
    session = connect_db()
    albums = session.query(Album).filter(Album.artist == artist).all()
    return albums

def save(new_user):
    """ записывает в базу данных новый альбом"""
    session = connect_db()
    # добавляем нового пользователя в сессию
    session.add(new_user)
    # сохраняем изменения
    session.commit()


