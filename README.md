# Full Stack API Project

## Full Stack Trivia Game

This project is a web application where users can play trivia quiz game and test their knowledge in various categories (Science, Art, Geography, History, Entertainment and Sports).

The task for this project was to create the APIs and the test cases for the APIs to implement the follwoing functionalities:

1) Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer. 
2) Delete questions.
3) Add questions and require that they include question and answer text.
4) Search for questions based on a text query string.
5) Play the quiz game, randomizing either all questions or within a specific category. 

## Getting Started

### Pre-requisites and Local Development 
Developers using this project should already have Postgres, Python3, pip and node installed.

#### Setup the Backend
To start and run the local development server, navigate to the `/backend` directory.

##### Backend Dependencies

First you need to have your virtual enviroment setup and running using the following commands:
```
$ virtualenv --no-site-packages env
$ source env/bin/activate
```
Then run `$ pip install requirements.txt`. The requirements file includes all the required packages for the backend. 

##### Database Setup

With Postgres running, restore a database using the `trivia.psql` using the following command:
```
psql trivia < trivia.psql
```

##### Running the backend server

Run the following commands: 
```
$ export FLASK_APP=flaskr
$ export FLASK_ENV=development
$ flask run
```
The first command directs our application to use the `__init__.py` file in our flaskr folder. The second command enables development mode.

The application is run on `http://127.0.0.1:5000/` by default and is a proxy in the frontend configuration. 

#### Setup the Frontend
To start and run the frontend client, navigate to the `/frontend` directory.

##### Frotend Dependencies

This project uses NPM to manage software dependencies. NPM relies on the `paccakge.json` file. Run the following command to download the dependencies located in this file: 
```
$ npm install
```

##### Running the frontend

In order to run the app in development mode use `$ npm start`.

The frontend is run on localhost:3000 by default.

### Testing
In order to run the tests located in `test_flaskr.py`, you will first need to create a test database called trivia_test. 
Navigate to the `/backend` directory and run the following commands:
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

## API Reference

### Getting Started
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration. 
- Authentication: This version of the application does not require authentication or API keys. 

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return three error types when requests fail:
- 400: Bad Request
- 404: Resource Not Found
- 405: Method Not Allowed
- 422: Not Processable 

### Endpoints

#### GET /categories
- General: Returns a list of all available categories and a success value
- Sample: `curl http://127.0.0.1:5000/categories`
```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true
}
```

#### GET /questions
- General: Returns a list of questions (paginated in groups of 10), number of total questions, a list of all categories, current category and a success value 
- Sample: `curl http://127.0.0.1:5000/questions`
```
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category ": null,
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ],
  "success": true,
  "total_questions": 21
}
```

#### DELETE /questions/<int:id>
- General: 
    - Deletes the book of the given ID in the url parameters if it exists
    - Returns the id of the deleted book and a success value
- Sample: `curl -X DELETE http://127.0.0.1:5000/questions/27`
```
{
  "deleted": 27,
  "success": true
}
```

#### POST /questions
This endpoint either cerates a new question or returns search results.

1. Question Creation (no search term is included in the request):
- General: 
    - Creates a new question with the specified attribute values given in the json request parameters
    - Returns the id of the created book and a success value
- Sample: `curl -X POST -H "Content-Type: application/json" -d '{"question": "What is the capital of Egypt?","answer": "Cairo","category": "3","difficulty": 2}' http://127.0.0.1:5000/questions`
```
{
  "created": 28,
  "success": true
}
```

2. Serach Questions (search term is included in the request):
- General:
    - Searches for questions that match the search term given in the json request parameters
    - Returns a list of questions matching the search term (paginated in groups of 10), number of total questions, current category and a success value
- Sample: `curl -X POST -H "Content-Type: application/json" -d '{"searchTerm": "title"}' http://127.0.0.1:5000/questions`
```
{
  "current_category ": null,
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }
  ],
  "success": true,
  "total_questions": 2
}
```

#### GET /categories/<int:id>/questions
- General: 
    - Retreives questions by category id given in the url parameters
    - Returns a list of the retreived questions (paginated in groups of 10), number of total questions, current category and a success value
- Sample: `curl http://127.0.0.1:5000/categories/2/questions`
```
{
"current_category": 2,
  "questions": [
    {
      "answer": "Escher",
      "category": 2,
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    },
    {
      "answer": "Mona Lisa",
      "category": 2,
      "difficulty": 3,
      "id": 17,
      "question": "La Giaconda is better known as what?"
    },
    {
      "answer": "One",
      "category": 2,
      "difficulty": 4,
      "id": 18,
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    },
    {
      "answer": "Jackson Pollock",
      "category": 2,
      "difficulty": 2,
      "id": 19,
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    }
  ],
  "success": true,
  "total_questions": 4
}
```

#### POST /quizzes
- General: 
    - Allows the user to play the game
    - Uses the chosen category and a list of previous questions given in the json request parameters to return a random question that is within that category and not included in the previous questions
- Sample: `curl -X POST -H "Content-Type: application/json" -d '{"previous_questions":[], "quiz_category":{"type":"Science","id":1}}' http://127.0.0.1:5000/quizzes`
```
{
  "question": {
    "answer": "The Liver",
    "category": 1,
    "difficulty": 4,
    "id": 20,
    "question": "What is the heaviest organ in the human body?"
  },
  "success": true
}
```

## Authors
Noha Salama has written the APIs in `__init__.py`, the test cases in `test_flaskr.py` and this README.
The rest of the project files, including the models and the frontend, were created by [Udacity](https://www.udacity.com/) as a project base code for project 2 for the [Full Stack Web Developer Nanodegree](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd0044).

## Acknowledgements 
The awesome team at Udacity# trivia_project
