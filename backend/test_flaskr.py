from cgi import test
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
        
        self.new_question = {"question": "What is the name of the fruit that resembles Spongebob's home?",
        "answer": "pineapple", "difficulty": 1, "category": 5}
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    # Test ability to obtain paginated questions
    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['categories']))
    
    # Test and ensure application throws 404 in event page beyond what exists is requested
    def test_get_questions_404(self):
        res = self.client().get('/questions?page=99999')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    
    # Test ability to obtain categories
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
    
    # Test and ensure application throws 404 in event specific category is requested
    def test_get_categories_404(self):
        res = self.client().get('/categories/99999') # route not configured to func this way
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # Test ability to DELETE a question given the question ID
    def test_delete_question(self):
        
        # create test question
        new_test_question = Question(question='How fast can a cheetah run?', answer= '60 mph', difficulty=1, category=1)
        # insert into the database
        new_test_question.insert() # ensures we have a question meant just for testing

        # obtain the question ID of the newly created question
        question_id = new_test_question.id
       
        # DELETE the question given the ID
        res = self.client().delete('/questions/{}'.format(question_id))
        data = json.loads(res.data)

        # perform query
        question = Question.query.filter(Question.id == question_id).one_or_none()

        # check status code
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], question_id)

        # ensure that our question does not exist
        self.assertEqual(question, None)
    
    # Test and ensure application throws 404 in event question ID requested is not valid for deletion
    def test_delete_question_404(self):
        res = self.client().delete('/questions/99999')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # Test ability to create new questions
    def test_add_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["created"])
    
    # Test and ensure application throws 422 error in invalid creation of question
    def test_add_question_422(self):
        res = self.client().post('/questions', json={}) # empty json data
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    # Test ability to search
    def test_get_by_search_term(self):
        res = self.client().post('/questions/search', json={"searchTerm": "boxer"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # Test ability to search w/o results
    def test_get_by_search_term_no_results(self):
        res = self.client().post('/questions/search', json={"searchTerm": "9999999"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # Test ability to get questions based on category
    def test_get_by_category(self):
        res = self.client().get('/categories/2/questions?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsInstance(data['questions'], list)
        self.assertEqual(data['total_questions'], 4)
        self.assertEqual(data['current_category'], 2)

    # Test and ensure application throws 404 for invalid category search
    def test_get_by_category_404(self):
        res = self.client().get('/categories/99999/questions?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()