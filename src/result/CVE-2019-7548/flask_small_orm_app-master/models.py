from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, ForeignKey

from flask_login import UserMixin


Base = declarative_base()


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    category = Column(String)
    description = Column(String)
    priority = Column(Integer)
    status = Column(String)
    user_id = Column(Integer, ForeignKey('users.id') , nullable=False)

    comments = relationship("Comment", backref="task_ref", cascade="all, delete-orphan")


class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(Integer, ForeignKey('tasks.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    content = Column(String, nullable=False)

    task = relationship("Task", backref="comments_ref")


class User(Base, UserMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)

    tasks = relationship("Task", backref="user_ref", cascade="all, delete-orphan")
    comments = relationship("Comment", backref="user_ref", cascade="all, delete-orphan")
