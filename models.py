from dataclasses import dataclass
import os
from sqlalchemy import Column, String, Integer, create_engine, ForeignKey
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
import json

database_path = os.environ['DATABASE_URL']
if database_path.startswith("postgres://"):
  database_path = database_path.replace("postgres://", "postgresql://", 1)

# print(f"Database URL test: {database_path}") 
db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)

'''
    db_drop_and_create_all()
    drops the database tables and starts fresh
    can be used to initialize a clean database
    !!NOTE you can change the database_filename variable to have multiple verisons of a database
'''

def db_drop_and_create_all():
    db.drop_all()
    db.create_all()

    # add one demo row which is helping in POSTMAN test
    movie = Movie(title='Movie1', release_date="jan")
    movie.insert()
    print(movie)

    actor = Actor(name='actor1', age=25, gender='Female', movie_id=1)
    actor.insert()


'''
Extend the base model class to add common methods
insert/update/delete records of the table

'''
class dbCrudOperations(db.Model):
    __abstract__ = True

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
  
"""
Creating Movie Table

"""
@dataclass
class Movie(dbCrudOperations):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    release_date = Column(String)
    actors = relationship('Actor', backref="movie", lazy=True)

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    #def __repr__(self):
    #    return f'<movies: id: {self.id.data}'

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date,
            'actors': list(map(lambda actor: actor.format(), self.actors))
        }

"""
Creating Actor table

"""
@dataclass
class Actor(dbCrudOperations):
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    gender = Column(String)
    movie_id = Column(Integer, ForeignKey('movies.id'), nullable=True)

    def __init__(self, name,age,gender,movie_id):
        self.name = name
        self.age = age
        self.gender = gender
        self.movie_id = movie_id

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender':self.gender,
            'movie_id':self.movie_id
          }  

