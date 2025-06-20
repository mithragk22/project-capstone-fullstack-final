import os
from flask import Flask, request, jsonify, abort
from models import setup_db
from flask_cors import CORS
from auth import AuthError, requires_auth
from models import db_drop_and_create_all, setup_db, Movie, Actor
from sqlalchemy.exc import SQLAlchemyError

def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    db_drop_and_create_all()

    @app.route('/')
    def get_greeting():
        excited = os.environ['EXCITED']
        greeting = "Hello" 
        if excited == 'true': 
            greeting = greeting + "!!!!! You are doing great in this Udacity project."
        return greeting

    @app.route('/health')
    def be_cool():
        return "Health!! OK"
    
    '''
    GET /movies
    - Fetches all the movies from the database
    - Request arguments: None
    - Returns: A list of movies contain key:value pairs of id, title and
    release_date
    Response:
        {
            "success": true,
            "movies":
            [
                {
                    "id": 1,
                    "title": "Movie1",
                    "release_date": "June"
                },
                {
                    "id": 2,
                    "title": "Movie2",
                    "release_date": "July"
                }
            ]
        }
    '''
    
    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies(payload):
        try:
            select_movies = Movie.query.order_by(Movie.id).all()   
            format_movies = [movies.format() for movies in select_movies]
            print("Select movies:",select_movies)
            print("format movies:",format_movies)
            if len(select_movies) ==0:
                abort(404)
            else:    
                return jsonify({
                'success':True,
                'movies':format_movies
            })
        except Exception as e:
            print("get movies exception",e)

    '''
    GET /actors
    - Fetches all the actors from the database
    - Request arguments: None
    - Returns: A list of actors contain key:value pairs of id, name, age and
    gender

    Response:
        {
            "success": true,
            "actors":
            [
                {
                    "id": 1,
                    "name": "John",
                    "age": 35,
                    "gender": "Male"
                },
                {
                    "id": 2,
                    "name": "Julia",
                    "age": 34,
                    "gender": "Women"
                }
            ]
        }
    '''

    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors(payload):
        try:
            select_actors = Actor.query.order_by(Actor.id).all()   
            format_actors = [actors.format() for actors in select_actors]

            if len(select_actors) ==0:
                abort(404)
            else:    
                return jsonify({
                'success':True,
                'actors':format_actors
            })
        except Exception as e:
            print("get actors exception",e)

    '''
    POST /movies
    - Creates a movie from the request's body
    - Request arguments: None
    - Returns: the created movie contains key:value pairs of id, title and
    release_date
    Body:
        {
            "title": "Movie1",
            "release_date": "July"
        }
    Response:
        {
            "success": true,
            "movie":
                {
                    "id": 1,
                    "title": "Movie1",
                    "release_date": "July"
                }
        }
    '''
    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def create_movie(payload):
        body = request.get_json()
        print(body)

        if body is None:
            abort(400)

        new_title = body.get('title', None)
        new_release_date = body.get('release_date', None)

        if new_title is None or new_release_date is None:
            abort(400, "Missing field for Movie")

        movie = Movie(title=new_title,
                      release_date=new_release_date)

        movie.insert()

        return jsonify({
            "success": True
        })
    
    '''
    POST /actors

    - Creates an actor from the request's body
    - Request arguments: None
    - Returns: the created actor contains key:value pairs of id, name, age and
    gender

    Body:
         {
             "name": "John",
             "age": 20,
             "gender": "Women"
         }

    Response:
        {
            "success": true,
            "actor":
                {
                    "id": 1
                    "name": "John",
                    "age": 20,
                    "gender": "Women"
                }
        }
    '''

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def create_actor(payload):
        body = request.get_json()

        if body is None:
            abort(400)

        new_name = body.get('name', None)
        new_age = body.get('age', None)
        new_gender = body.get('gender', None)
        new_movie_id = body.get('movie_id', None)

        if new_name is None or new_age is None or new_gender is None or new_movie_id is None:
            abort(400)

        actor = Actor(name=new_name, age=new_age, gender=new_gender, movie_id=new_movie_id)

        actor.insert()

        return jsonify({
            "success": True
        })

    '''
    PATCH /actors/<int:id>

    - Updates a actor using the information provided by request's body
    - Request arguments: Actor id
    - Returns: the updated actor contains key:value pairs of id, name, age and
    gender

    Body:
        {
            "name": "John",
            "age": 20,
            "gender": "Women"
        }

    Response:
        {
            "success": true,
            "actor":
                {
                    "id": 1,
                    "name": "John",
                    "age": 20,
                    "gender": "Women"
                }
        }
    '''
    
    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actor(payload, actor_id):
        # Query for the actor by ID
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        
        if actor is None:
            abort(404)  # Actor not found

        body = request.get_json()
        new_name = body.get('name')
        new_age = body.get('age')
        new_gender = body.get('gender')
        new_movie = body.get('movie_id')

        # Update only if new values are provided
        if new_name is not None:
            actor.name = new_name
        if new_age is not None:
            actor.age = new_age
        if new_gender is not None:
            actor.gender = new_gender
        if new_movie is not None:
            actor.movie_id = new_movie

        try:
            actor.update() 
            return jsonify({
                'success': True,
                'actor': actor.format()
            })
        except Exception as e:
            print("Update exception:", e)
            abort(500)  # Return a 500 error for any unexpected exceptions
        

    '''
    PATCH /movies/<int:id>
    - Updates a movie using the information provided by request's body
    - Request arguments: Movie id
    - Returns: the updated movie contains key:value pairs of id, title and
     release_date
    Body:
        {
            "title": "Movie2",
            "release_date": "July"
        }
    Response:
        {
            "success": true,
            "movie":
                {
                    "id": 1,
                    "title": "Movie2",
                    "release_date": "July"
                }
        }
    '''
    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movie(payload, movie_id):
        # Query for the movie by ID
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        
        if movie is None:
            abort(404)  # Movie not found
        

        body = request.get_json()
        new_title = body.get('title', None)
        new_release_date = body.get('release_date', None)

        if new_title is None or new_release_date is None:
            abort(422, "Title or release date are required.")  # Return a 422 error if required fields are missing

        # Update only if new values are provided
        if new_title is not None:
            movie.title = new_title
        if new_release_date is not None:
            movie.release_date = new_release_date        

        try:
            movie.update()  # Ensure this method is defined in your Movie model
            return jsonify({
                'success': True,
                'movie': movie.format() 
            }), 200  # Return a 200 OK status     

        except Exception as e:
            print("Update exception:", e)
            abort(500)  # Return a 500 error for any unexpected exceptions
    '''
    DELETE /actors/<int:id>

    - Updates a movie using the information provided by request's body
    - Request arguments: Actor id
    - Returns: the deleted actor id

    Response:
        {
            "success": true,
            "deleted": 1
        }
    '''

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(payload, actor_id):
        try:
            # Retrieves the actor from the database
            actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
            # If there's no such actor, abort 404
            if not actor:
                abort(404)

            actor.delete()

            return jsonify({
                'success': True,
                'deleted': actor_id
            }), 200  # Return a 200 OK status
        except SQLAlchemyError:
            abort(422)

    '''
    DELETE /movies/<int:id>
    - Updates a movie using the information provided by request's body
    - Request arguments: Movie id
    - Returns: the deleted movie id
    Response:
        {
            "success": true,
            "deleted": 1
        }
    '''
    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(payload, movie_id):
        try:
            # Retrieves the movie from the database
            movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

            # If there's no such movie, abort 404
            if not movie:
                abort(404)

            movie.delete()

            return jsonify({
                'success': True,
                'deleted': movie.id
            }), 200

        except SQLAlchemyError:
            abort(422)  

    # Error Handling

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": getattr(error, 'description', "Data not found!!")
        }),422

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Data not found!!"
        }),404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": 'The request can not be processed'
        }), 400

    @app.errorhandler(AuthError)
    def auth_error(auth_error):
        return jsonify({
            "success": False,
            "error": auth_error.status_code,
            "message": auth_error.error['description']
        }), auth_error.status_code
    
    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'Internal server error. Please try again later.'
        }), 500
    
    return app   
    

app = create_app()

if __name__ == '__main__':
    app.run()
