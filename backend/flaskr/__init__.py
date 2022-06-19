import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

# define var to represent questions per page
QUESTIONS_PER_PAGE = 10

# function to implement pagination


def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE  # begin at 0
    end = start + QUESTIONS_PER_PAGE  # grab 10

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={"/": {"origins": "*"}})

    # utilize the after_request decorator to set Access-Control-Allow
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, PATCH, PUT, POST, DELETE, OPTIONS')
        return response

    # endpoint to handle GET requests for all available categories
    @app.route('/categories')
    def get_categories():
        # obtain all the categories
        data = Category.query.all()
        categories = {}
        for category in data:
            categories[category.id] = category.type

        if len(data) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'categories': categories
        })

    # endpoint to handle GET requests for questions
    @app.route('/questions')  # components/QuestionView.js
    def get_questions():
        # get all questions
        selection = Question.query.all()
        # obtain a count of the total number of questions
        total_questions = len(selection)
        # paginate by every (10) questions, return list
        current_questions = paginate_questions(request, selection)

        # get all categories
        categories = Category.query.all()
        categories_dict = {}
        for category in categories:
            categories_dict[category.id] = category.type

        # abort 404 if no questions
        if (len(current_questions) == 0):
            abort(404)

        # return data to view
        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': total_questions,
            'categories': categories_dict
        })

    # endpoint to DELETE question using a question ID.
    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()

            if question is None:
                abort(404)
            # delete selected question
            question.delete()
            # get all questions
            selection = Question.query.order_by(Question.id).all()
            # paginate by every (10) questions, return list
            current_questions = paginate_questions(request, selection)
            # obtain a count of the total number of questions
            total_questions = len(selection)

            return jsonify(
                {
                    "success": True,
                    "deleted": question_id,
                    "questions": current_questions,
                    "total_questions": total_questions,
                }
            )

        except:
            abort(422)
    '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

    '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

    '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''

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

    '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''

    return app
