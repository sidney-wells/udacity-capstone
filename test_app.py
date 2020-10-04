from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from database.models import setup_db, Exercise, Workout, db, db_drop_and_create_all
import os
import unittest
import json
from app import app
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

TRAINER_TOKEN = os.getenv("TRAINER_TOKEN")
CLIENT_TOKEN = os.getenv("CLIENT_TOKEN")


def set_auth_header(role):
    if role == 'client':
        return {'Authorization': 'Bearer {}'.format(CLIENT_TOKEN)}
    elif role == 'trainer':
        return {'Authorization': 'Bearer {}'.format(TRAINER_TOKEN)}


class Tests(unittest.TestCase):
    def setUp(self):
        """Define test variables and initialize app."""
        self.database_path = os.getenv('DATABASE_URL')
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

    # GET WORKOUTS YES
    def test_trainer_get_workouts(self):

        response = self.app.get('/workouts',
                                     headers=set_auth_header('trainer'))
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    # GET WORKOUTS YES
    def test_client_get_workouts(self):

        response = self.app.get('/workouts',
                                     headers=set_auth_header('client'))
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    # GET WORKOUTS UNAUTH
    def test_get_workouts_unauthorized(self):

        response = self.app.get('/workouts', headers=set_auth_header(''))
        self.assertEqual(response.status_code, 401)

    # GET EXERCISES YES
    def test_trainer_get_exercises(self):

        response = self.app.get('/exercises',
                                     headers=set_auth_header('trainer'))
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    # GET EXERCISES YES
    def test_client_get_exercises(self):

        response = self.app.get('/exercises',
                                     headers=set_auth_header('client'))
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 403)

    # GET EXERCISES UNAUTH
    def test_get_exercises_unauthorized(self):

        response = self.app.get('/exercises', headers=set_auth_header(''))
        self.assertEqual(response.status_code, 401)

    # POST EXERCISE YES
    def test_trainer_add_exercise(self):
        data = {
            "name": "burpees",
            "instructions": "push weight a lot"
        }
        response = self.app.post('/exercises', json=data,
                                      headers=set_auth_header('trainer'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['success'], True)

    # POST EXERCISE FAIL
    def test_client_add_exercise(self):
        data = {
            "name": "buupees wow",
            "instructions": "push weight a lot"
        }
        response = self.app.post('/exercises', json=data,
                                      headers=set_auth_header('client'))
        self.assertEqual(response.status_code, 403)

    # POST EXERCISE UNAUTH
    def test_add_exercise_unauthorized(self):
        data = {
            "name": "buupees wow",
            "instructions": "push weight a lot"
        }
        response = self.app.post('/exercises', json=data,
                                      headers=set_auth_header(''))
        self.assertEqual(response.status_code, 401)

    # POST WORKOUT YES
    def test_trainer_add_workout(self):
        exercise1 = {
            "name": "burpees",
            "instructions": "do it"
        }
        exercise2 = {
            "name": "jumps",
            "instructions": "do it"
        }
        exercise3 = {
            "name": "squats",
            "instructions": "do it"
        }
        self.app.post('/exercises', json=exercise1,
                           headers=set_auth_header('trainer'))
        self.app.post('/exercises', json=exercise2,
                           headers=set_auth_header('trainer'))
        self.app.post('/exercises', json=exercise3,
                           headers=set_auth_header('trainer'))

        data = {
            "theme": "new workout test",
            "description": "new description test",
            "exerciseOne": "burpees",
            "exerciseTwo": "squats",
            "exerciseThree": "jumps"
        }
        response = self.app.post('/workouts', json=data,
                                      headers=set_auth_header('trainer'))
        self.assertEqual(response.status_code, 200)

    # POST WORKOUT FAIL
    def test_client_add_workout(self):
        exercise1 = {
            "name": "burpees",
            "instructions": "do it"
        }
        exercise2 = {
            "name": "jumps",
            "instructions": "do it"
        }
        exercise3 = {
            "name": "squats",
            "instructions": "do it"
        }

        self.app.post('/exercises', json=exercise1,
                           headers=set_auth_header('trainer'))
        self.app.post('/exercises', json=exercise2,
                           headers=set_auth_header('trainer'))
        self.app.post('/exercises', json=exercise3,
                           headers=set_auth_header('trainer'))

        data = {
            "theme": "new workout test",
            "description": "new description test",
            "exerciseOne": "leg lunge",
            "exerciseTwo": "squat",
            "exerciseThree": "legish"
        }
        response = self.app.post('/workouts', json=data,
                                      headers=set_auth_header('client'))
        self.assertEqual(response.status_code, 403)

    # POST WORKOUT UNAUTH
    def test_add_workout_unauthorized(self):
        exercise1 = {
            "name": "burpees",
            "instructions": "do it"
        }
        exercise2 = {
            "name": "jumps",
            "instructions": "do it"
        }
        exercise3 = {
            "name": "squats",
            "instructions": "do it"
        }

        self.app.post('/exercises', json=exercise1,
                           headers=set_auth_header('trainer'))
        self.app.post('/exercises', json=exercise2,
                           headers=set_auth_header('trainer'))
        self.app.post('/exercises', json=exercise3,
                           headers=set_auth_header('trainer'))

        data = {
            "theme": "new workout test",
            "description": "new description test",
            "exerciseOne": "jumps",
            "exerciseTwo": "squats",
            "exerciseThree": "burpees"
        }
        response = self.app.post('/workouts', json=data,
                                      headers=set_auth_header(''))
        self.assertEqual(response.status_code, 401)

    # PATCH EXERCISE SUCCESS
    def test__trainer_update_exercise(self):
        data = {
            "name": "new exercise",
            "instructions": "new instructions"
        }
        data2 = {
            "name": "updated exercise",
            "instructions": "updated instructions"
        }

        self.app.post('/exercises', json=data,
                           headers=set_auth_header('trainer'))
        exercise_id = Exercise.query.first().id
        response = self.app.patch(
                f'/exercises/{exercise_id}/edit', json=data2,
                headers=set_auth_header('trainer'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['success'], True)

    # PATCH EXERCISE FAILED
    def test_client_update_exercise_failed(self):
        data = {
            "name": "shoulder pushy",
            "instructions": "push weight a lot"
        }
        self.app.post('/exercises', json=data,
                           headers=set_auth_header('client'))

        exercise_id = Exercise.query.order_by(Exercise.id.desc()).first()
        exercise_id = 10
        response = self.app.patch(
                f'/exercises/{exercise_id}/edit', json=data,
                headers=set_auth_header('client'))
        self.assertEqual(response.status_code, 403)

    # DELETE WORKOUT SUCCESS
    def test__trainer_delete_workout(self):
        exercise1 = {
            "name": "burpees",
            "instructions": "do it"
        }
        exercise2 = {
            "name": "jumps",
            "instructions": "do it"
        }
        exercise3 = {
            "name": "squats",
            "instructions": "do it"
        }
        self.app.post('/exercises', json=exercise1,
                           headers=set_auth_header('trainer'))
        self.app.post('/exercises', json=exercise2,
                           headers=set_auth_header('trainer'))
        self.app.post('/exercises', json=exercise3,
                           headers=set_auth_header('trainer'))
        data = {
            "theme": "new workout test",
            "description": "new description test",
            "exerciseOne": "burpees",
            "exerciseTwo": "squats",
            "exerciseThree": "jumps"
        }
        self.app.post('/workouts', json=data,
                        headers=set_auth_header('trainer'))
        workout_id = Workout.query.first().id
        response = self.app.delete(
                f'/workouts/{workout_id}', json=data,
                headers=set_auth_header('trainer'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['success'], True)

    # DELETE WORKOUT FAILED
    def test_delete_workout_unauthorized(self):
        workout_id = 10
        response = self.app.delete(
                f'/workouts/{workout_id}', headers=set_auth_header(''))
        self.assertEqual(response.status_code, 401)


if __name__ == "__main__":
    unittest.main()
