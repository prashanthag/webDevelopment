import os
import http
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

# from flaskr import create_app

from database.models import setup_db, db_drop_and_create_all
# from models import setup_db, Question, Category
from app import app


class CapstoneTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app
        self.client = self.app.test_client
        self.token_cp = os.environ['CP_JWT_TOKEN']
        self.token_cd = os.environ['CD_JWT_TOKEN']
        self.cp_headers = {
            "Authorization": f"Bearer {self.token_cp}"
        }
        self.cd_headers = {
            "Authorization": f"Bearer {self.token_cd}"
        }
        self.ca_headers = {

        }
        self.actor1 = dict(
            name='Ina Gowda',
            age='9',
            gender='female'
        )
        self.actor2 = dict(
            age='41',
        )
        self.movie1 = dict(
            title='corona',
            release_date='2020/09/01'
        )
        self.movie2 = dict(
            release_date='2020/12/01'
        ),
        '''
        conn = http.client.HTTPSConnection(os.environ['AUTH0_DOMAIN'])
        payload = {
            "client_id": os.environ['CLIENT_ID'],
            "client_secret": os.environ['CLIENT_SECRET'],
            "audience": os.environ['API_AUDIENCE'],
            "grant_type": "client_credentials"
        }

        headers = {'content-type': "application/json"}

        conn.request("POST", "/oauth/token", json.dumps(payload), headers)

        res = conn.getresponse()
        data = res.read()

        # self.token  = json.loads(data.decode("utf-8"))['access_token']
        # print(self.token )
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.drop_all()
            self.db.create_all()

self.new_missing_data = {
            'question': 'What is my cat name',
            'difficulty': 4,
            'category': 1
        }
    '''

    def tearDown(self):
        """Executed after reach test"""
        pass

    def add_item(self, url, token, data, headers):
        res = self.client().post(url,
                                 data=data,
                                 headers=headers,
                                 follow_redirects=True
                                 )
        return res

    def delete_item(self, token, data, headers):
        res = self.client().delete(url,
                                   data=data,
                                   headers=headers,
                                   follow_redirects=True
                                   )
        return res

    def test_get_all_movies(self):
        res = self.client().get('/movies')
        self.assertEqual(res.status_code, 200)

    def test_get_all_actors(self):
        res = self.client().get('/actors')
        self.assertEqual(res.status_code, 200)

    def test_casting_producer_create(self):
        res = self.add_item('/actors/create', self.token_cp,
                            self.actor1, self.cp_headers)
        self.assertEqual(res.status_code, 200)

    def test_casting_director_create(self):
        res = self.add_item('/actors/create', self.token_cd,
                            self.actor1, self.cd_headers)
        self.assertEqual(res.status_code, 200)

    def test_casting_assistant_create(self):
        res = self.add_item('/actors/create', '', self.actor2, self.ca_headers)
        self.assertEqual(res.status_code, 401)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
