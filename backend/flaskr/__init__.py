import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
	page = request.args.get('page', 1, type=int)
	start = (page-1) * QUESTIONS_PER_PAGE
	end = start + QUESTIONS_PER_PAGE

	questions = [question.format() for question in selection]
	current_questions = questions[start:end]

	return current_questions

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  CORS(app, resources={'/':{'origins':'*'}})

  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

  @app.route('/categories')
  def retrieve_categories():
    query_categories = Category.query.order_by(Category.type).all()
  
    if len(query_categories) == 0:
 		  abort(404)
     
    categories = {}
    for category in query_categories:
 		  categories[category.id] = category.type
     
    return jsonify({
 		  'success': True,
 		  'categories': categories
 		  })

  @app.route('/questions')
  def retrieve_questions():
    query_questions = Question.query.order_by(Question.id).all()
    current_questions = paginate_questions(request, query_questions)
     
    if len(current_questions) == 0:
 		  abort(404)
       
    query_categories = Category.query.all()
    categories = {}
    for category in query_categories:
 		  categories[category.id] = category.type
       
    return jsonify({
 		  'success': True,
 		  'questions': current_questions,
 		  'total_questions': len(query_questions),
 		  'categories': categories,
 		  'current_category ': None
 		  })

  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    try:
      question = Question.query.filter(Question.id==question_id).one_or_none()

      if question is None:
        abort(404)

      question.delete()

      return jsonify({
        'success': True,
        'deleted': question_id
        })

    except:
      abort(422)

  @app.route('/questions', methods=['POST'])
  def create_question():
    body = request.get_json()

    if body is None:
      abort(400)

    new_question = body.get('question', None)
    new_answer = body.get('answer', None)
    new_category = body.get('category', None)
    new_difficulty = body.get('difficulty', None)
    search_term = body.get('searchTerm', None)

    try:
      if search_term:
        search = '%{}%'.format(search_term)
        query_questions = Question.query.order_by(Question.id).filter(Question.question.ilike(search)).all()

        return jsonify({
				  'success': True,
				  'questions': paginate_questions(request, query_questions),
				  'total_questions': len(query_questions),
				  'current_category ': None
				  })

      else:
        if ((new_question is None) or (new_answer is None) or (new_difficulty is None) or (new_category is None)):
          abort(422)

        question = Question(question = new_question, answer = new_answer, difficulty = new_difficulty, category = new_category)
        question.insert()

        return jsonify({
				  'success': True,
				  'created': question.id
				  })

    except:
      abort(422)


  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:category_id>/questions', methods=['GET'])
  def retrieve_questions_by_category(category_id):
    category = Category.query.filter(Category.id==category_id).one_or_none()
    
    if category is None:
      abort(404)
      
    query_questions = Question.query.filter(Question.category==str(category_id)).all()
    
    return jsonify({
      'success': True,
		  'questions': paginate_questions(request, query_questions),
		  'total_questions': len(query_questions),
		  'current_category': category.id
		  })


  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes', methods=['POST'])
  def play_game():
    body = request.get_json()

    if body is None:
      abort(400)

    previous_questions = body.get('previous_questions', None)
    quiz_category = body.get('quiz_category', None)

    if previous_questions is None or quiz_category is None:
      abort(422)

    if quiz_category['id'] == 0:
      query_questions = Question.query.all()

    else:
      query_questions = Question.query.filter(Question.category==quiz_category['id']).all()

    if len(query_questions) == 0:
      abort(404)

    if len(query_questions) == len(previous_questions):
      return jsonify({
        'success': True
        })

    questions = [question.format() for question in query_questions]

    try:
      while True:
        random_question = random.choice(questions)
        if random_question['id'] not in previous_questions:
          return jsonify({
            'success': True,
            'question': random_question
            })
    
    except:
      abort(422)

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(400)
  def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'bad request'
        }), 400

  @app.errorhandler(404)
  def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'resource not found'
        }), 404

  @app.errorhandler(405)
  def not_found(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'method not allowed'
        }), 405

  @app.errorhandler(422)
  def uprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'unprocessable'
        }), 422

  return app    