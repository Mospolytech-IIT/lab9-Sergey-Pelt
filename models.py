"""1. Модели данных"""
from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class User(Base):
    """Класс для пользователя"""
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    posts = relationship('Post', back_populates='user')

class Post(Base):
    """Класс для постов"""
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship('User', back_populates='posts')
