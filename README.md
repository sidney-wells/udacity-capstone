# YOORS APP
This exercise and workout app tracker helps trainers create exercises for workouts that they can provide to their clients.

Yoors is all about enabling personal trainers to create optimal workouts that can be provided to clients who can try those workouts. First, the trainer needs to create at least three exercises. Then, they will be able to add three exercises to their workout for clients. 

This Application is hosted on Heroku: https://yoors-app.herokuapp.com

# Motivation
Yoors App is my final project for the Udacity Full Stack Nanodegree.

# Dependencies
These are listed in requirements.txt It can be installed with pip install -r requirments.txt

# Authentication
Yoors App has 2 types of users:

Client: Can view workouts

Trainer: All permissions including getting workouts and exercises, adding workouts and exercises, updating exercises, and deleting workouts.

The Authentication is carried out by third-party authentication tool which is Auth0 The Auth0 domain and api audience can be found in setup.sh.

# End-Points

## GET /workouts
* General
    * This end point will fetch all workouts. 
* Sample
Response:
{
    "success": true,
    "total_workouts": 1,
    "workouts": [
        {
            "workout_description": "new description1",
            "workout_exercises": [
                {
                    "exercise_id": 1,
                    "exercise_instructions": "instructions1",
                    "exercise_name": "jumps"
                },
                {
                    "exercise_id": 3,
                    "exercise_instructions": "instructions1",
                    "exercise_name": "burpees"
                },
                {
                    "exercise_id": 4,
                    "exercise_instructions": "instructions1",
                    "exercise_name": "squats"
                }
            ],
            "workout_id": 1,
            "workout_theme": "new workout1"
        }
    ]
}

## POST /workouts
* General
    * This end point is used to post a new workout. However, the trainer must create three exercises in order to post a workout. 
* Sample
Data: json={ "theme": "new workout1", "description": "new description1", "exerciseOne": "burpees" "exerciseTwo": "squats", "exerciseThree": "jumps" }
Response: {
    "created": 1,
    "created_workout_theme": "new workout1",
    "new_workout": {
        "workout_description": "new description1",
        "workout_exercises": [
            {
                "exercise_id": 1,
                "exercise_instructions": "instructions1",
                "exercise_name": "jumps"
            },
            {
                "exercise_id": 3,
                "exercise_instructions": "instructions1",
                "exercise_name": "burpees"
            },
            {
                "exercise_id": 4,
                "exercise_instructions": "instructions1",
                "exercise_name": "squats"
            }
        ],
        "workout_id": 1,
        "workout_theme": "new workout1"
    },
    "success": true,
    "total_workouts": 1
}

## DELETE /workouts/<int:id>
* General
    * This end point deletes an existing workout: 
* Sample
Resposne:
{
    "deleted": 1,
    "success": true,
    "total_workouts": 0
}

## GET /exercises
* General
    * This end point will get all exercises 
* Sample
Response: 
{
    "exercises": [
        {
            "exercise_id": 1,
            "exercise_instructions": "instructions1",
            "exercise_name": "jumps"
        },
        {
            "exercise_id": 3,
            "exercise_instructions": "instructions1",
            "exercise_name": "burpees"
        },
        {
            "exercise_id": 4,
            "exercise_instructions": "instructions1",
            "exercise_name": "squats"
        }
    ],
    "success": true,
    "total_exercises": 3
}

## POST /exercises
* General
    * This end point will post a new exercise: 
* Sample
Data: json= {"name": "jumps", "instructions": "instructions1"} 
Response: {"created": 1, "exercise": { "exercise_id": 1, "exercise_instructions": "instructions1", "exercise_name": "jumps" }, "success": true, "total_exercises": 1 }

## PATCH /exercises/<int:id>
* General
    * This end point updates the details of an existing exercise: 
* Sample
Data: Json={"name":"Tiedmann", "gender":"Female"} 
Response: 
{
    "edited": 1,
    "exercise": {
        "exercise_id": 1,
        "exercise_instructions": "updated instructions",
        "exercise_name": "new jumps"
    },
    "success": true,
    "total_exercises": 3
}

# Tests
To run the tests, use test_app.py with below command: python test_app.py

# Author
Sidney Wells authored this API with only backend features present in flaskr, test_app.py and database folders. Authentication can be found in auth folder.

