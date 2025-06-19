### Casting Agency - Udacity FullStack WebDevelopment Project

## Project Motivation
The Casting Agency is a project designed to assist producers and directors in managing movie and actor information. It allows users to add new movies, maintain actor data, and assign actors to specific movies.

The project provides a set of APIs that support full CRUD (Create, Read, Update, Delete) operations for both movies and actors. It also implements role-based access control, where users have different permissions based on their assigned roles. Authentication is handled using JWT tokens through Auth0, ensuring secure access to the system.

## https://project-capstone-fullstack-final.onrender.com/health

## Getting Started

### Installing Dependencies

#### Python

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## Running the App Locally
# You should have setup.sh and requirements.txt available
```bash
chmod +x setup.sh
source setup.sh
```
- The setup.sh will run the following:
- export DATABASE_URL="postgresql://postgres@localhost:5432/postgres"
- export EXCITED="true"
- Change the DATABASE_URL, as applicable to you.
```bash
echo $DATABASE_URL
```
- postgresql://postgres@localhost:5432/postgres
```bash
echo $EXCITED
```
- true
```bash
python3 app.py
```
## Running the server

From within the root directory first ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:

```bash
export FLASK_APP=app.py;
```

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## Tasks

### Setup Auth0

1. Create a new Auth0 Account
2. Select a unique tenant domain
3. Create a new, single page web application
4. Create a new API
   - in API Settings:
     - Enable RBAC
     - Enable Add Permissions in the Access Token
5. Create new API permissions:
   - `get:actors`
   - `get:movies`
   - `post:actors`
   - `post:movies`
   - `patch:actors`
   - `patch:movies`
   - `delete:actors`
   - `delete:movies`
6. Create new roles for:
   - CastingAssistant
     - can `get:actors`
     - can `get:movies`
   - CastingDirector
     - can add actors/movies
   - ExecutiveProducer
     - can perform all actions (view/update/delete)
7. Test your endpoints with [Postman](https://getpostman.com).
   - Register 3 users - assign the CastingAssistant role to one and CastingDirector role to the other.
   - Sign into each account and make note of the JWT.
   - Import the postman collection, if you have
   - Right-clicking the collection folder for barista and manager, navigate to the authorization tab, and including the JWT in the token field (you should have noted these JWTs).
   - Run the collection and correct any errors.
   - Export the collection overwriting the one we've included so that we have your proper JWTs during review!

### Implement The Server

1. `auth.py`
2. `app.py`
3. `models.py`

## Documenting Endpoints

You will need to provide detailed documentation of your API endpoints including the URL, request parameters, and the response body. Use the example below as a reference.


`GET /movies'`
Example: curl http://127.0.0.1:5000/movies

curl --request GET \
  --url http://127.0.0.1:5000/movies \
  --header 'Authorization: Bearer YOUR_JWT_TOKEN'
  

* This requires permission `get:movies`
* Fetches a dictionary of movies in which the keys are the ids and the value is the corresponding string of the movies
* Request Arguments: None
* Returns: An object with a single key, `movies`, that contains an object of list of actors of that movie, id and release date.

```json
{
    "movies": [
        {
            "actors": [],
            "id": 1,
            "release_date": "4-APR",
            "title": "title7"
        }
    ],
    "success": true
}
```
`GET /actors'`
Example: curl http://127.0.0.1:5000/actors
* This requires permissions `get:actors`
* Fetches a dictionary of actors along with the movie id they are part of
* Request Argguments: None
* Returns: A Json Object which contains name,age,gender and movie_id key value pairs.

```json
{
    "actors": [
        {
            "age": 24,
            "gender": "f",
            "id": 1,
            "movie_id": 1,
            "name": "actor2"
        }
    ],
    "success": true
}
```
`POST /movies'`
* This requires permissions `post:movies`
* This endpoint helps user to create a new movies.
* Fields: movie title, release date.
* Returns: Success values
Example: curl http://127.0.0.1:5000/movies -X POST -H "Content-Type: application/json" -d '{"title":"new movie","release_date":"24-APR"}'

```json
{
    "success": true
}
```
Response if permission is not found:
```json
{
    "error": 403,
    "message": "Permission not found.",
    "success": false
}
```

`POST /actors'`
* This requires permissions `post:actors`
* This endpoint helps user to create a new actors.
* Fields: actors name, age, gender, movie_id.
* Returns: Success values
Example: curl http://127.0.0.1:5000/actors -X POST -H "Content-Type: application/json" -d '{"name":"new actor","age":24,"gender":"f","movie_id":1}'

```json
{
    "success": true
}
```
Response if permission is not found:
```json
{
    "error": 403,
    "message": "Permission not found.",
    "success": false
}
```

`DELETE '/movies/<movie_id>'`
* This endpoint helps user to delete movies based on the movie id.
* Fields: movie_id
* Returns success on deletion of the record.
* Returns 200 as request code if successful, else 404 if the id is not found
Example: curl -X DELETE http://127.0.0.1:5000/movies/2

```json
{
    "deleted": 2,
    "success": true
}
```
* Response body for not found record
```json
{
  "error":404,
  "message":"Data not found",
  "success":false
  }
```
Response if permission is not found:
```json
{
    "error": 403,
    "message": "Permission not found.",
    "success": false
}
```

`DELETE '/actors/<actor_id>'`
* This endpoint helps user to delete actors based on the actor id.
* Fields: actor_id
* Returns success on deletion of the record.
* Returns 200 as request code if successful, else 404 if the id is not found
Example: curl -X DELETE http://127.0.0.1:5000/actor/2

```json
{
    "deleted": 2,
    "success": true
}
```
* Response body for not found record
```json
{
  "error":404,
  "message":"Data not found",
  "success":false
  }
```
Response if permission is not found:
```json
{
    "error": 403,
    "message": "Permission not found.",
    "success": false
}
```

Error Handlers:

* Erros are handeled and gives a exact response to the user 
200: On successful operation
422: When operation is not proccesseble
404: When the resouce is not found

```json
{
  "error":422,
  "message":"Unprocessable entity!!",
  "success":false
}
```

```json
{
  "error":404,
  "message":"Data not found!!",
  "success":false
}
```
RBAC failures:
Response if permission is not found:
```json
{
    "error": 403,
    "message": "Permission not found.",
    "success": false
}
```


## Run unit cases
# You should have setup.sh and requirements.txt available
```bash
chmod +x setup.sh
source setup.sh
```
```bash
    python -m unittest -v
```
