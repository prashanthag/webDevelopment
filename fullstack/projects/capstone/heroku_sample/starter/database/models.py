import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
import json
from flask_migrate import Migrate


db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app):
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)
    db_drop_and_create_all()
    # db.create_all()


'''
db_drop_and_create_all()
    drops the database tables and starts fresh
    can be used to initialize a clean database
    !!NOTE you can change the database_filename variable to have multiple
    verisons of a database
'''


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()


'''
Movies
a persistent Movies entity, extends the base SQLAlchemy Model
'''


class Movies(db.Model):
    __tablename__ = 'Movies'
    # Autoincrementing, unique primary key
    id = db.Column(db.Integer, primary_key=True)
    # String Title
    title = Column(String(120), unique=True)
    release_date = Column(db.DateTime(), nullable=False)
    actor_id = db.Column(db.Integer, db.ForeignKey(
        'Actors.id'), nullable=False)

    '''
    insert()
        inserts a new model into a database
        the model must have a unique name
        the model must have a unique id or null id
        EXAMPLE
            movie = Movie(title=req_title, recipe=req_recipe)
            movie.insert()
    '''

    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    delete()
        deletes a new model into a database
        the model must exist in the database
        EXAMPLE
            movie = Movie(title=req_title, recipe=req_recipe)
            movie.delete()
    '''

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    '''
    update()
        updates a new model into a database
        the model must exist in the database
        EXAMPLE
            movie = Movie.query.filter(Movie.id == id).one_or_none()
            movie.title = 'Black Coffee'
            movie.update()
    '''

    def update(self):
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.short())


class Actors(db.Model):
    __tablename__ = 'Actors'
    # Autoincrementing, unique primary key
    id = db.Column(db.Integer, primary_key=True)
    # String Name

    name = Column(String(120), unique=True)

    age = Column(db.Integer)
    gender = Column(String(120), nullable=False)
    movies = db.relationship('Movies', backref='Actors', lazy=True)
    '''
    insert()
        inserts a new model into a database
        the model must have a unique name
        the model must have a unique id or null id
        EXAMPLE
            movie = Movie(title=req_title, recipe=req_recipe)
            movie.insert()
    '''

    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    delete()
        deletes a new model into a database
        the model must exist in the database
        EXAMPLE
            movie = Movie(title=req_title, recipe=req_recipe)
            movie.delete()
    '''

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    '''
    update()
        updates a new model into a database
        the model must exist in the database
        EXAMPLE
            movie = Movie.query.filter(Movie.id == id).one_or_none()
            movie.title = 'Black Coffee'
            movie.update()
    '''

    def update(self):
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.short())
