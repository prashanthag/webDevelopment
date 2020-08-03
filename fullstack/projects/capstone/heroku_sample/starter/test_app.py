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
        self.token_ca = os.environ['CA_JWT_TOKEN']
        self.cp_headers = {
            "Authorization": f"Bearer {self.token_cp}"
        }
        self.cd_headers = {
            "Authorization": f"Bearer {self.token_cd}"
        }
        self.ca_headers = {
            "Authorization": f"Bearer {self.token_ca}"
        }
        self.actor1 = dict(
            name='Ina Gowda',
            age='9',
            gender='female'
        )
        self.patch_actor = dict(
            age='41'
        )
        self.movie1 = dict(
            title='corona',
            release_date='2020/09/01',
            actor_id='1'
        )
        self.patch_movie = dict(
            release_date='2020/12/01'
        )
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

        tokenn  = json.loads(data.decode("utf-8"))['access_token']
        print(tokenn)
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

    def get_item(self, url, headers):
        res = self.client().get(url, headers=headers)
        return res

    def add_item(self, url, data, headers):
        res = self.client().post(url,
                                 data=data,
                                 headers=headers,
                                 follow_redirects=True
                                 )
        return res

    def patch_item(self, url, data, headers):
        res = self.client().patch(url,
                                  data=data,
                                  headers=headers,
                                  follow_redirects=True
                                  )
        return res

    def delete_item(self, url, headers):
        res = self.client().delete(url,
                                   headers=headers,
                                   follow_redirects=True
                                   )
        return res
    # Producer

    def test_get_producer_all_movies(self):
        res = self.get_item('/movies', self.cp_headers)
        self.assertEqual(res.status_code, 200)

    def test_get_producer_all_actors(self):
        res = self.get_item('/actors', self.cp_headers)
        self.assertEqual(res.status_code, 200)

    def test_casting_prod_create_actor(self):
        res = self.add_item('/actors/create', self.actor1, self.cp_headers)
        self.assertEqual(res.status_code, 200)

    def test_casting_prod_create_movie(self):
        res = self.add_item('/movies/create', self.movie1, self.cp_headers)
        self.assertEqual(res.status_code, 200)

    def test_casting_prod_patch_actor(self):
        res = self.patch_item(
            '/actors/1/edit', self.patch_actor, self.cp_headers)
        self.assertEqual(res.status_code, 200)

    def test_casting_prod_patch_movie(self):
        res = self.patch_item(
            '/movies/1/edit', self.patch_movie, self.cp_headers)
        self.assertEqual(res.status_code, 200)

    def test_casting_producer_delete_movie(self):
        res = self.delete_item('/movies/1', self.cp_headers)
        self.assertEqual(res.status_code, 200)

    def test_casting_producer_delete_actor(self):
        res = self.delete_item('/actors/1', self.cp_headers)
        self.assertEqual(res.status_code, 200)

    # Director
    def test_get_director_all_movies(self):
        res = self.get_item('/movies', self.cd_headers)
        self.assertEqual(res.status_code, 200)

    def test_get_director_all_actors(self):
        res = self.get_item('/actors', self.cd_headers)
        self.assertEqual(res.status_code, 200)

    def test_casting_director_create_actor(self):
        res = self.add_item('/actors/create', self.actor1, self.cd_headers)
        self.assertEqual(res.status_code, 200)

    def test_casting_director_create_movie(self):
        res = self.add_item('/movies/create', self.movie1, self.cd_headers)
        self.assertEqual(res.status_code, 401)

    def test_casting_director_patch_movie(self):
        res = self.patch_item(
            '/movies/1/edit', self.patch_movie, self.cd_headers)
        self.assertEqual(res.status_code, 422)

    def test_casting_director_patch_actor(self):
        res = self.patch_item(
            '/actors/1/edit', self.patch_actor, self.cd_headers)
        self.assertEqual(res.status_code, 200)

    def test_casting_direct_delete_actor(self):
        res = self.delete_item('/actors/1', self.cp_headers)
        self.assertEqual(res.status_code, 200)

    # Assistant

    def test_get_assistant_all_movies(self):
        res = self.get_item('/movies', self.ca_headers)
        self.assertEqual(res.status_code, 200)

    def test_get_assistant_all_actors(self):
        res = self.get_item('/actors', self.ca_headers)
        self.assertEqual(res.status_code, 200)

    def test_casting_assistant_create(self):
        res = self.add_item('/actors/create', self.actor1, self.ca_headers)
        self.assertEqual(res.status_code, 401)

    def test_casting_assistant_create_actor(self):
        res = self.add_item('/actors/create', self.actor1, self.ca_headers)
        self.assertEqual(res.status_code, 401)

    def test_casting_assistant_create_movie(self):
        res = self.add_item('/movies/create', self.movie1, self.ca_headers)
        self.assertEqual(res.status_code, 401)

    def test_casting_assistant_patch_actor(self):
        res = self.patch_item(
            '/actors/1/edit', self.patch_actor, self.ca_headers)
        self.assertEqual(res.status_code, 401)

    def test_casting_assistant_patch_movie(self):
        res = self.patch_item(
            '/movies/1/edit', self.patch_movie, self.ca_headers)
        self.assertEqual(res.status_code, 401)

    def test_casting_assistant_delete_movie(self):
        res = self.delete_item('/movies/1', self.ca_headers)
        self.assertEqual(res.status_code, 401)

    def test_casting_assistant_delete_actor(self):
        res = self.delete_item('/actors/1', self.ca_headers)
        self.assertEqual(res.status_code, 401)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
