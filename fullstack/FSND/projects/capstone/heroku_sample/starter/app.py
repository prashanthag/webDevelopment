
import os
import sys
from flask import Flask,abort
from flask_cors import CORS
from models import setup_db

def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.route('/')
    def get_greeting():
        try:
            excited = os.environ['EXCITED']
            greeting = "Hello" 
            if excited == 'true': greeting = greeting + "!!!!!"
            return greeting
        except:
             print(sys.exc_info())
             abort(422)

    @app.route('/coolkids')
    def be_cool():
        return "Be cool, man, be coooool! You're almost a FSND grad!"

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)