# Trivia Game API
A trivia game with the intent to create bonding experiences. The application is composed of a react-based frontend and flask-based backend. The application performs the following:

1. Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.

## Screenshots
<img src="screenshots/list.png" width = "700"> 

<img src="screenshots/add.png" width = "350"> <img src="screenshots/play.png" width = "350">

## About the Stack
### Backend Dependencies
1. **Python 3.7**
2. **PIP and Virtual Env**
3. **PIP Dependencies** - navigate to `/backend` directory and run: ```pip install -r requirements.txt``` via terminal. 
4. **Key Dependencies**
 - [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

 - [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. 

 - [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.
5. **Database Setup** - With Postgres running, restore a database using the trivia.psql file provided. 
``` bash
dropdb trivia
createdb trivia
psql trivia < trivia.psql 
```
6. **Running the Server** - From within the `./src` directory, ensure you are working using your created virtual environment. To run the server, execute:
```bash
export FLASK_APP=flaskr
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

### Frontend Dependencies
The ./frontend directory contains a complete React frontend to display our data from the Flask server. 

1. Install Node and NPM from [https://nodejs.com/en/download](https://nodejs.org/en/download/).
2. Navigate to `/frontend` directory and run ```npm install``` via terminal.
3. Confirm successful install by running ```node -v``` via terminal.
4. Run the application in development mode using ```npm start```
5. Open [http://localhost:3000](http://localhost:3000) to view it in the browser. The page will reload if you make edits.

## Unit Testing
1. Navigate to `/backend/test_flaskr.py`
2. Change `database_name` and `database_path` accordingly. 
3. Run the following commands:
```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
## API Reference
### Getting Started
- **Base URL:** http://127.0.0.1:5000/ <br>  
>_NOTE_: Application is meant to run locally.
- **API Keys:** Not applicable. 
- **Authentication:** Not applicable.

### Error Handling
#### Response Codes
- **404** - resource not found
- **422** - unprocessable
- **400** - bad request

#### Error Messages
Error messages are returned as JSON objects. <br>
**Example:** `curl http://127.0.0.1:5000/secretpage`

**Response:**
```bash
{
  "error": 404, 
  "message": "resource not found", 
  "success": false
}
```
### Resource Endpoint Library 
#### GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a two keys, categories, that contains an object of id: category_string key:value pairs and success. 

**Example of Usage:** `curl http://127.0.0.1:5000/categories`

**Response:**
```bash
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

#### GET '/questions?page=${integer}'
- Fetches a paginated set of questions, a total number of questions, all categories and current category string. 
- Request Arguments: page - integer
- Returns: An object with 10 paginated questions, total questions, object including all categories, and current category string

**Example of Usage:** `curl http://127.0.0.1:5000/questions?page=2`

**Response:**
```bash
{
    'questions': [
        {
            'id': 1,
            'question': 'This is a question',
            'answer': 'This is an answer', 
            'difficulty': 5,
            'category': 2
        },
    ],
    'totalQuestions': 100,
    'categories': { '1' : "Science",
    '2' : "Art",
    '3' : "Geography",
    '4' : "History",
    '5' : "Entertainment",
    '6' : "Sports" },
    'currentCategory': 'History'
}
```

#### GET '/categories/${id}/questions'
- Fetches questions for a cateogry specified by id request argument 
- Request Arguments: id - integer
- Returns: An object with questions for the specified category, total questions, and current category string

**Example of Usage:** `curl http://127.0.0.1:5000/categories/2/questions`

**Response:**
```bash
{
    'questions': [
        {
            'id': 1,
            'question': 'This is a question',
            'answer': 'This is an answer', 
            'difficulty': 5,
            'category': 4
        },
    ],
    'totalQuestions': 100,
    'currentCategory': 'History'
}
```

#### DELETE '/questions/${id}'
- Deletes a specified question using the id of the question
- Request Arguments: id - integer
- Returns: Does not need to return anything besides the appropriate HTTP status code. Optionally can return the id of the question. If you are able to modify the frontend, you can have it remove the question using the id instead of refetching the questions. 

**Example of Usage:** `curl -X DELETE http://127.0.0.1:5000/questions/5`

**Response:**

```bash
{
  "deleted": 5, 
  "questions": [
    {
      "answer": "Tom Cruise", 
      "category": "5", 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }, 
    {
      "answer": "Edward Scissorhands", 
      "category": "5", 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }
  ], 
  "success": true, 
  "total_questions": 16
}
```

#### POST '/quizzes'
- Sends a post request in order to get the next question 
- Request Body: 
{'previous_questions':  an array of question id's such as [1, 4, 20, 15]
'quiz_category': a string of the current category }
- Returns: a single new question object

**Example of Usage:** `curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions": [10], "quiz_category": {"type": "Science", "id": "1"}}'`

**Response:**

```bash
{
  "question": {
    "answer": "The Liver", 
    "category": "1", 
    "difficulty": 4, 
    "id": 20, 
    "question": "What is the heaviest organ in the human body?"
  }, 
  "success": true
}
```

#### POST '/questions'
- Sends a post request in order to add a new question
- Request Body: 
```bash
{
    'question':  'Heres a new question string',
    'answer':  'Heres a new answer string',
    'difficulty': 1,
    'category': 3,
}
```
- Returns: Does not return any new data

#### POST '/questions/search'
- Sends a post request in order to search for a specific question by search term 

**Example of Usage:** `curl http://127.0.0.1:5000/questions/search -X POST -H "Content-Type: application/json" -d '{"searchTerm":"boxer"}'`

**Response:** 
```bash
{
  "questions": [
    {
      "answer": "Muhammad Ali", 
      "category": "4", 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }
  ], 
  "success": true, 
  "total_questions": 1
}
```

## Acknowledgements 
- **SVG Icons:** [SVG Repo](https://www.svgrepo.com/)
- **Starter Code:** [Udacity](https://github.com/udacity/FSND)
