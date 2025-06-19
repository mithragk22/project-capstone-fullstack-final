import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Movie, Actor

from dotenv import load_dotenv

load_dotenv()
database_url=os.getenv("DATABASE_URL")
database = os.getenv("DATABASE")
assistant = os.getenv("CASTINGASSISTANT")
director = os.getenv("CASTINGDIRECTOR")
producer = os.getenv("EXECUTIVEPRODUCER")

database_name = database

print(database_url)

class CastingTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = database_name
        self.database_path = database_url
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

            self.movie = {
            'title': 'The Blacklist',
            'release_date': 'Sun, 24 May 2020 13:04:03 GMT'
        }

        self.actor = {
            'name': 'John Wick',
            'age': 44,
            'gender': 'Male'
        }
    
    def tearDown(self):
        """Executed after reach test"""
        pass



    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_retrieve_movies(self):
        res = self.client().get(
            "/movies",
            headers={
                'Authorization': 'Bearer '+producer
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["movies"])

    def test_retrieve_actors(self):
        res = self.client().get(
            "/actors",
            headers={
                'Authorization': 'Bearer '+producer
            })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["actors"])

    def test_delete_movies(self):
        res = self.client().delete(
            "/movies/1",
            headers={
                'Authorization': 'Bearer '+producer
            })
        data = json.loads(res.data)

        movies = Movie.query.filter(Movie.id == 1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 1)

    def test_delete_actors(self):
        res = self.client().delete(
            "/actors/1",
            headers={
                'Authorization': 'Bearer '+producer
            })
        data = json.loads(res.data)

        actors = Actor.query.filter(Actor.id == 1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 1)
    
    def test_post_movies(self):
        new_movie = {
            'title': 'Movie1',
            'release_date': 'Jan'
        }
        res = self.client().post(
            "/movies",
            headers={
                'Authorization': 'Bearer '+producer
            },json=new_movie)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])  

    def test_update_actor(self):
        res = self.client().patch('/actors/1', json=self.actor, headers={
                'Authorization': 'Bearer '+producer
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actor']))

    def test_update_movie(self):
        res = self.client().patch('/movies/1', json=self.movie, headers={
                'Authorization': 'Bearer '+producer
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movie']))  

    def test_delete_movies(self):
        res = self.client().delete(
            "/movies/2",
            headers={
                'Authorization': 'Bearer '+producer
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Data not found!!')

    def test_delete_actors(self):
        res = self.client().delete(
            "/actors/100",
            headers={
                'Authorization': 'Bearer '+producer
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Data not found!!')

    def test_delete_movies_assistant(self):
        res = self.client().delete(
            "/movies/1",
            headers={
                'Authorization': 'Bearer '+assistant
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
    
    def test_retrieve_movies_assistant(self):
        res = self.client().get(
            "/movies",
            headers={
                'Authorization': 'Bearer '+assistant
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["movies"])

    def test_401_create_movie_unauthorized(self):
        res = self.client().post('/movies', json=self.movie, headers='')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_401_update_movie_unauthorized(self):
        res = self.client().patch('movies/1', json=self.movie, headers='')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_401_delete_movie_unauthorized(self):
        res = self.client().delete('/movies/1', headers='')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_401_create_actor_unauthorized(self):
        res = self.client().post('/actors', json=self.actor, headers='')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
    
    def test_401_update_actor_unauthorized(self):
        res = self.client().patch('actors/1', json=self.actor, headers='')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_401_delete_actors_unauthorized(self):
        res = self.client().delete('/actors/1', headers='')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
