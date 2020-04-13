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
        self.database_path = "postgres://{}:{}@{}/{}".format('postgres','postgres','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # sample question to use in some test cases
        self.new_question = {
            'question': 'What is the capital of Egypt?',
            'answer': 'Cairo',
            'category': '3',
            'difficulty': 2
	        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_retrieve_categories(self):
        #test categories retrieval success
	    res = self.client().get('/categories')
	    data = json.loads(res.data)

	    self.assertEqual(res.status_code, 200)
	    self.assertEqual(data['success'], True)
	    self.assertTrue(len(data['categories']))

    def test_405_create_category(self):
        #test category creation failure
	    res = self.client().post('/categories', json={'type':'IT'})
	    data = json.loads(res.data)

	    self.assertEqual(res.status_code, 405)
	    self.assertEqual(data['success'], False)
	    self.assertEqual(data['message'], 'method not allowed')

    def test_get_paginated_questions(self):
        #test questions pagination success
	    res = self.client().get('/questions')
	    data = json.loads(res.data)

	    self.assertEqual(res.status_code, 200)
	    self.assertEqual(data['success'], True)
	    self.assertEqual(len(data['questions']), 10)
	    self.assertTrue(data['total_questions'])
	    self.assertTrue(len(data['categories']))

    def test_404_questions_page_beyond_valid_page(self):
        #test questions pagination failure
	    res = self.client().get('/questions?page=100')
	    data = json.loads(res.data)

	    self.assertEqual(res.status_code, 404)
	    self.assertEqual(data['success'], False)
	    self.assertEqual(data['message'], 'resource not found')

    def test_delete_question(self):
        #test question deletion success

	    #create a new question to delete it
	    question = Question(question=self.new_question['question'], answer=self.new_question['answer'], category=self.new_question['category'], difficulty=self.new_question['difficulty'])
	    question.insert()
	    question_id = question.id

	    #delete the question
	    res = self.client().delete('/questions/{}'.format(question_id))
	    data = json.loads(res.data)

	    question_after_deletion = Question.query.filter(Question.id==question_id).one_or_none()

	    self.assertEqual(res.status_code, 200)
	    self.assertEqual(data['success'], True)
	    self.assertEqual(data['deleted'], question_id)
	    self.assertEqual(question_after_deletion, None)

    def test_404_delete_non_existing_question(self):
        #test question deletion failure
	    res = self.client().delete('/questions/1000')
	    data = json.loads(res.data)

	    self.assertEqual(res.status_code, 422)
	    self.assertEqual(data['success'], False)
	    self.assertEqual(data['message'], 'unprocessable')

    def test_create_new_question(self):
        #test question creation success
	    res = self.client().post('/questions', json=self.new_question)
	    data = json.loads(res.data)

	    #test if question has been successfully created
	    question_after_insertion = Question.query.filter(Question.id==data['created']).one_or_none()

	    self.assertEqual(res.status_code, 200)
	    self.assertEqual(data['success'], True)
	    self.assertIsNotNone(question_after_insertion)

    def test_422_create_new_question_without_sending_data(self):
        #test question creation failure
	    res = self.client().post('/questions')
	    data = json.loads(res.data)

	    self.assertEqual(res.status_code, 400)
	    self.assertEqual(data['success'], False)
	    self.assertEqual(data['message'], 'bad request')

    def test_get_question_serach_with_results(self):
        #test question search with results
	    res = self.client().post('/questions', json={'searchTerm': 'title'})
	    data = json.loads(res.data) 

	    self.assertEqual(res.status_code, 200)
	    self.assertEqual(data['success'], True)
	    self.assertEqual(len(data['questions']), 2)
	    self.assertTrue(data['total_questions'])

    def test_get_question_serach_without_results(self):
        #test questions search without results
	    res = self.client().post('/questions', json={'searchTerm': 'continent'})
	    data = json.loads(res.data) 

	    self.assertEqual(res.status_code, 200)
	    self.assertEqual(data['success'], True)
	    self.assertEqual(len(data['questions']), 0)
	    self.assertEqual(data['total_questions'], 0)

    def test_retrieve_question_by_category(self):
        #test questions retrieval  by category success
	    res = self.client().get('categories/2/questions')
	    data = json.loads(res.data)

	    self.assertEqual(res.status_code, 200)
	    self.assertEqual(data['success'], True)
	    self.assertTrue(len(data['questions']))
	    self.assertTrue(data['total_questions'])
	    self.assertEqual(data['current_category'], 2)

    def test_404_retrieve_question_by_non_existing_category(self):
        #test questions retrieval  by category failure
	    res = self.client().get('categories/100/questions')
	    data = json.loads(res.data)

	    self.assertEqual(res.status_code, 404)
	    self.assertEqual(data['success'], False)
	    self.assertEqual(data['message'], 'resource not found')

    def test_play_game(self):
        #test play game success
        res = self.client().post('/quizzes', json={'previous_questions':[], 'quiz_category':{'type':'Science','id':1}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(data['question'])

    def test_422_play_game_sending_empty_data(self):
        #test play game failure
        res = self.client().post('/quizzes', json={})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()