import os
from flask import Flask, request, abort, jsonify, json
from flask_cors import CORS
# from auth.auth import AuthError, requires_auth
# from database.models import setup_db, Workout, Exercise, Link
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


# app = Flask(__name__)
# setup_db(app)
# app.secret_key = os.getenv("SECRET")
# CORS(app)


# @app.after_request
# def after_request(response):
#     response.headers.add(
#         'Access-Control-Allow-Headers',
#         'Content-Type,Authorization,true')
#     response.headers.add(
#         'Access-Control-Allow-Methods',
#         'GET,POST,PUT,DELETE,OPTIONS')
#     return response

# @app.route('/workouts')
# @requires_auth('get:workouts')
# def workouts(*args, **kwargs):

#     data = []
#     workouts = Workout.query.all()
#     for workout in workouts:
#         all_ex = []
#         result = []
#         exercises = workout.exercises
#         for exercise in exercises:
#             all_ex.append(exercise)
#         for ex in all_ex:
#             result.append({
#                 'exercise_id': ex.id,
#                 'exercise_name': ex.name,
#                 'exercise_instructions': ex.instructions
#             })
#         data.append({
#             'workout_id': workout.id,
#             'workout_theme': workout.theme,
#             'workout_description': workout.description,
#             'workout_exercises': result
#         })

#     if len(workouts) == 0:
#         data = []

#     return jsonify({
#         'success': True,
#         'workouts': data,
#         'total_workouts': len(Workout.query.all())
#     })

# @app.route('/exercises')
# @requires_auth("get:exercises")
# def exercises(*args, **kwargs):

#     data = []
#     exercises = Exercise.query.all()
#     for exercise in exercises:
#         data.append({
#             'exercise_id': exercise.id,
#             'exercise_name': exercise.name,
#             'exercise_instructions': exercise.instructions
#         })

#     if len(exercises) == 0:
#         data = []

#     return jsonify({
#         'success': True,
#         'exercises': data,
#         'total_exercises': len(Exercise.query.all())
#     })

# @app.route('/workouts', methods=['POST'])
# @requires_auth("post:workouts")
# def post_workout(*args, **kwargs):

#     body = request.get_json()
#     ex = []

#     theme = body.get("theme", None)
#     description = body.get("description", None)

#     exerciseOne = body.get("exerciseOne", None)
#     exOne = Exercise.query.filter(
#             Exercise.name == exerciseOne).one_or_none()

#     exerciseTwo = body.get("exerciseTwo", None)
#     exTwo = Exercise.query.filter(
#             Exercise.name == exerciseTwo).one_or_none()

#     exerciseThree = body.get("exerciseThree", None)
#     exThree = Exercise.query.filter(
#             Exercise.name == exerciseThree).one_or_none()

#     ex.append(exOne)
#     ex.append(exTwo)
#     ex.append(exThree)

#     try:
#         workout = Workout(
#             theme=theme, description=description)
#         workout.insert()

#         new_workout = Workout.query.order_by(Workout.id.desc()).first()
#         if (new_workout is None) or (ex is None):
#             abort(404)
#         for exercise in ex:
#             new_workout.exercises.append(exercise)

#         new_workout.update()

#         try:
#             data = {}
#             all_ex = []
#             result = []
#             new_new_workout = Workout.query.order_by(
#                     Workout.id.desc()).first()
#             exercises = new_new_workout.exercises
#             for exercise in exercises:
#                 all_ex.append(exercise)
#             for ex in all_ex:
#                 result.append({
#                     'exercise_id': ex.id,
#                     'exercise_name': ex.name,
#                     'exercise_instructions': ex.instructions
#                 })
#             data = {
#                 'workout_id': new_new_workout.id,
#                 'workout_theme': new_new_workout.theme,
#                 'workout_description': new_new_workout.description,
#                 'workout_exercises': result
#             }
#         except():
#             abort(422)

#         return jsonify({
#             'success': True,
#             'created': new_new_workout.id,
#             'created_workout_theme': new_new_workout.theme,
#             'new_workout': data,
#             'total_workouts': len(Workout.query.all())
#         })
#     except():
#         abort(422)

# @app.route('/exercises', methods=['POST'])
# @requires_auth('post:exercises')
# def post_exercise(*args, **kwargs):

#     body = request.get_json()

#     name = body.get("name", None)
#     instructions = body.get("instructions", None)

#     if (name is None) or (instructions is None):
#         abort(422)

#     try:
#         exercise = Exercise(
#                 name=name, instructions=instructions)
#         exercise.insert()

#         new_exercise = Exercise.query.order_by(Exercise.id.desc()).first()
#         data = {
#             'exercise_id': new_exercise.id,
#             'exercise_name': new_exercise.name,
#             'exercise_instructions': new_exercise.instructions
#         }

#         return jsonify({
#             'success': True,
#             'created': exercise.id,
#             'exercise': data,
#             'total_exercises': len(Exercise.query.all())
#         })
#     except():
#         abort(422)

# @app.route('/exercises/<int:exercise_id>/edit', methods=['PATCH'])
# @requires_auth('patch:exercises')
# def edit_exercise(*args, **kwargs):

#     exercise_id = kwargs['exercise_id']

#     body = request.get_json()

#     name = body.get("name", None)
#     instructions = body.get("instructions", None)

#     if (name is None) or (instructions is None):
#         abort(422)

#     try:
#         exercise = Exercise.query.filter(
#                 Exercise.id == exercise_id).one_or_none()
#         exercise.name = name
#         exercise.instructions = instructions

#         exercise.update()

#         data = {
#             'exercise_id': exercise.id,
#             'exercise_name': exercise.name,
#             'exercise_instructions': exercise.instructions
#         }

#         return jsonify({
#             'success': True,
#             'edited': exercise.id,
#             'exercise': data,
#             'total_exercises': len(Exercise.query.all())
#         })
#     except():
#         abort(422)

# @app.route('/workouts/<int:workout_id>', methods=['DELETE'])
# @requires_auth('delete:workouts')
# def delete_workout(*args, **kwargs):

#     workout_id = kwargs['workout_id']
#     try:
#         workout = Workout.query.filter(
#             Workout.id == workout_id).one_or_none()
#         if workout is None:
#             abort(422)
#         workout.delete()

#         return jsonify({
#             'success': True,
#             'deleted': workout.id,
#             'total_workouts': len(Workout.query.all())
#         })
#     except():
#         abort(422)

# # ERROR HANDLING
# @app.errorhandler(422)
# def unprocessable(error):
#     return jsonify({
#         "success": False,
#         'error': 422,
#         'message': "unprocessable"
#     }), 422

# @app.errorhandler(404)
# def not_found(error):
#     return jsonify({
#         "success": False,
#         'error': 404,
#         'message': "resource not found"
#     }), 404

# @app.errorhandler(400)
# def bad_request(error):
#     return jsonify({
#         "success": False,
#         'error': 400,
#         'message': "bad request"
#     }), 400

# @app.errorhandler(405)
# def not_found(error):
#     return jsonify({
#         "success": False,
#         'error': 405,
#         'message': "method not allowed"
#     }), 405

# @app.errorhandler(AuthError)
# def auth_failed(AuthError):
#     res = jsonify(AuthError.error)
#     res.status_code = AuthError.status_code
#     return res

# if __name__ == '__main__':
#     app.run()

from sqlalchemy import Column, String, Integer, create_engine, ForeignKey, Table
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from flask_wtf import Form
from flask_migrate import Migrate



app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('DATABASE_URL')
db = SQLAlchemy(app)

migrate = Migrate(app, db)

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

if __name__ == '__main__':
    app.run()
