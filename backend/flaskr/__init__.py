import os
from unicodedata import category
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from sqlalchemy import func

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
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(
                Question.id == question_id).one_or_none()

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
            abort(404)

    # endpoint to POST a new question, which will require the question and answer text, category, and difficulty score.
    @app.route('/questions', methods=['POST'])
    def add_question():
        # obtain data from form
        body = request.get_json()
        new_question = body.get("question", None)
        new_answer = body.get("answer", None)
        new_difficulty = body.get("difficulty", None)
        new_category = body.get("category", None)

        # ensure data isn't empty
        if not new_question:
            abort(422)

        if not new_answer:
            abort(422)

        if not new_difficulty:
            abort(422)

        if not new_category:
            abort(422)

        try:
            question = Question(question=new_question, answer=new_answer,
                                difficulty=new_difficulty, category=new_category)
            question.insert()

            # get all questions
            selection = Question.query.order_by(Question.id).all()
            # paginate by every (10) questions, return list
            current_questions = paginate_questions(request, selection)
            # obtain a count of the total number of questions
            total_questions = len(selection)

            return jsonify(
                {
                    "success": True,
                    "created": question.id,
                    "questions": current_questions,
                    "total_questions": total_questions
                }
            )

        except:
            abort(422)

    # a POST endpoint to get questions based on a given search term
    @app.route('/questions/search', methods=['POST'])
    def get_by_search_term():
      # obtain search term
      body = request.get_json()
      search_term = body.get("searchTerm", None)

      try: 
        if search_term:
          # return any questions for whom the search term is a substring of the question
          selection = Question.query.filter(
                Question.question.ilike(f'%{search_term}%')).all()
          # paginate by every (10) questions, return list
          current_questions = paginate_questions(request, selection)
          # obtain a count of the total number of questions
          total_questions = len(selection)

          return jsonify(
                  {
                      "success": True,
                      "questions": current_questions,
                      "total_questions": total_questions
                  }
              )
      except:
        abort(422)
      

    # a GET endpoint to get questions based on category
    @app.route('/categories/<int:category_id>/questions')
    def get_by_category(category_id):
        try:
            # query based on category id
            selection = Question.query.filter(
                Question.category == str(category_id)).all()

            # paginate by every (10) questions, return list
            current_questions = paginate_questions(request, selection)

            # obtain a count of the total number of questions
            total_questions = len(selection)

            if total_questions == 0:
              abort(404)
            else:
              return jsonify(
                  {
                      "success": True,
                      "questions": current_questions,
                      "total_questions": total_questions,
                      "current_category": category_id
                  }
              )
        except:
            abort(404)

    # a POST endpoint to get questions to play the quiz
    @app.route('/quizzes', methods=['POST'])
    def quizzes():
      try:
        # obtain category and previous questions via json
        body = request.get_json()
        quiz_category = body.get('quiz_category')
        previous_questions = body.get('previous_questions')

        # return a random question within the given category that is not one of the previous questions
        if quiz_category['id'] == 0:
          # if category is 0, it means ALL
          print(quiz_category['id']) # testing
          set_of_questions = Question.query.filter(Question.id.notin_((previous_questions))).all()
        else: 
          # if category is not 0, take the category id
          print(quiz_category['id']) # testing
          set_of_questions = Question.query.filter_by(category = quiz_category['id']).filter(Question.id.notin_((previous_questions))).all()

        if len(set_of_questions) == 0:
          # if the quiz is over b/c we ran out of questions, return none to end the quiz
          return jsonify({
            "success": True,
            "question": None
          })
        else:
          # if the quiz is not over, return a random question from the set
          next_question = random.choice(set_of_questions).format()
          return jsonify({
            "success": True,
            "question": next_question
          })

      except:
        abort(422)
      
    # error handlers for all expected errors
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    return app
