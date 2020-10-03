import os
from sqlalchemy import Column, String, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
import json
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

database_path = os.getenv('DATABASE_URI')

db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


def db_drop_and_create_all():
    """drops the database tables and starts fresh
    can be used to initialize a clean database"""
    db.drop_all()
    db.create_all()


class Workout(db.Model):
    __tablename__='workout'

    id = Column(Integer, primary_key=True)
    theme = Column(String)
    description = Column(String)
    exercises = relationship("Exercise", secondary='link')

    def __init__(self, theme, description):
        self.theme = theme
        self.description = description

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'theme': self.theme,
            'description': self.description
        }


class Exercise(db.Model):
    __tablename__='exercise'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    instructions = Column(String)
    workouts = relationship('Workout', secondary='link')

    def __init__(self, name, instructions):
        self.name = name
        self.instructions = instructions

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'instructions': self.instructions
        }


class Link(db.Model):
    __tablename__='link'
    workout_id = Column(Integer, ForeignKey('workout.id'), primary_key=True)
    exercise_id = Column(Integer, ForeignKey('exercise.id'), primary_key=True)
