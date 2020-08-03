import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={r'/api/*': {'origins': '*'}})

    #@TODO: Use the after_request decorator to set Access-Control-Allow
    
    @app.after_request
    def app_after_request(response):
      response.headers.add('Access-Control-Allow-Header','Content-Type,Authorization,true')
      response.headers.add('Access-Control_Allow-Methods','GET,POST,PATCH,DELETE,PUT,OPTIONS')
      return response 

    '''
    Get all available categories.
    '''
    @app.route('/categories')
    def get_categories():
        categories = Category.query.all()

        # serilise categories 
        categories_dict = {}
        for category in categories:
            categories_dict[category.id] = category.type

        if len(categories) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'categories': categories_dict,
            'total_categories': len(categories)
        })
    '''
    Create an endpoint to handle GET requests for questions, 
    including pagination (every 10 questions). 
    This endpoint should return a list of questions, 
    number of total questions, current category, categories. 

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions. 
    '''

    @app.route('/questions')
    def get_questions():

        # Get questions then paginate
        questions = Question.query.order_by(Question.id).all()

        current_questions = paginate_questions(request, questions)

        # Create categories dict
        categories = Category.query.order_by(Category.id).all()
        categories_dict = {}
        for category in categories:
            categories_dict[category.id] = category.type

        if len(current_questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(questions),
            'categories': categories_dict
        })

    '''
    Delete a question.
    '''
    @app.route('/questions/<int:id>', methods=['DELETE'])
    def delete_question(id):
        try:
            select_question = Question.query.filter_by(id=id).one_or_none()

            if select_question is None:
                abort(404)
            else:
                select_question.delete()

            return jsonify(
                {
                    'success': True,
                    'deleted': id
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

    and also find ot serch term 
    '''
    
    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()

        if body.get('searchTerm'):
            search_Term = body.get('searchTerm')
            selection = Question.query.filter(
                Question.question.ilike(
                    f'%{search_Term}%'
                )
            ).all()

            if len(selection) == 0:
                abort(404)

            current_questions = paginate_questions(request, selection)

            return jsonify({
                'success': True,
                'questions': current_questions,
                'total_questions': len(Question.query.all())
            })

        # Post a new question.
        else:
            new_question = body.get('question')
            new_answer = body.get('answer')
            new_category = body.get('category')
            new_difficulty = body.get('difficulty')

            if (
                (new_question is None) or
                (new_answer is None) or
                (new_category is None) or
                (new_difficulty is None)
            ):
                abort(422)

            try:
                question = Question(
                    question=new_question,
                    answer=new_answer,
                    category=new_category,
                    difficulty=new_difficulty
                )
                question.insert()

                selection = Question.query.order_by(Question.id).all()
                current_questions = paginate_questions(request, selection)

                return jsonify(
                    {
                        'success': True,
                        'created': question.id,
                        'questions': current_questions,
                        'question_created': question.question,
                        'total_questions': len(Question.query.all())
                    })
            except:
                abort(422)

    '''
    Get questions based on category.
    '''

    @app.route('/categories/<int:id>/questions')
    def get_questions_by_category(id):
        category = Category.query.filter_by(id=id).one_or_none()

        if category is None:
            abort(400)

        selection = Question.query.filter_by(category=category.id).all()
        paginated_questions = paginate_questions(request, selection)

        return jsonify({
            'success': True,
            'questions': paginated_questions,
            'total_questions': len(Question.query.all()),
            'current_category': category.type
        })

    '''
    Get questions to play the quiz.
    '''
    @app.route('/quizzes', methods=['POST'])
    def get_random_questions():

        body = request.get_json()
        previous = body.get('previous_questions')
        category = body.get('quiz_category')

        if (category is None) or (previous is None):
            abort(400)

        if category['id'] == 0:
            questions = Question.query.all()
        else:
            questions = Question.query.filter_by(category=category['id']).all()

            total = len(questions)

        def get_random_question():
            return questions[random.randrange(0, len(questions), 1)]

        # function to check played quizzes
        def check_if_used(question):
            used = False
            for quiz in previous:
                if quiz == question.id:
                    used = True

            return used

        question = get_random_question()

        while check_if_used(question):
            question = get_random_question()

            if len(previous) == total:
                return jsonify(
                    {
                        'success': True
                    }
                )

        return jsonify({
            'success': True,
            'question': question.format()
        })

    '''
    Error handlers.
    '''
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'bad request'
        }), 400

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'unprocessable'
        }), 422

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'resource not found'
        }), 404

    return app