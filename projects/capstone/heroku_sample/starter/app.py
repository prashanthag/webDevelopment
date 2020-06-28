import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, \
    Response, flash, redirect, url_for, jsonify, abort
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
# import FlaskForm as Form
from forms import *
from flask_migrate import Migrate
import sys
from sqlalchemy import func
import datetime

from database.models import setup_db, db_drop_and_create_all, \
    Movies, Actors, db
from auth.auth import AuthError, requires_auth

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
setup_db(app)

CORS(app, resources={r'/api/*': {'origins': '*'}})

# @TODO: Use the after_request decorator to set Access-Control-Allow


@app.after_request
def app_after_request(response):
    response.headers.add('Access-Control-Allow-Header',
                         'Content-Type,Authorization,true')
    response.headers.add('Access-Control_Allow-Methods',
                         'GET,POST,PATCH,DELETE,PUT,OPTIONS')
    return response


def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)


app.jinja_env.filters['datetime'] = format_datetime


@app.route('/')
def index():
    return render_template('pages/home.html')


@app.route('/movies', methods=['GET'])
def movies():
    areas = db.session.query(Movies.title, Movies.release_date).distinct()
    data = []
    # print("areas: \n",areas)
    # movie = {}
    for area in areas:
        movie = dict(zip(('title', 'release_date'), area))
        movie['movies'] = []
        for movie_data in Movies.query.filter_by(
            title=movie['title'],
            release_date=movie['release_date']
        ).all():
            movies_data = {
                'id': movie_data.id,
                'title': movie_data.title,
            }
        movie['movies'].append(movies_data)
        data.append(movie)
    print("\n data: ", data)
    return render_template('pages/movies.html', areas=data)


@app.route('/movies/search', methods=['POST'])
def search_movies():
    search_term = request.form.get('search_term', None)

    movies = Movies.query.filter(
        Movies.title.ilike('%{}%'.format(search_term))).all()

    count_movies = len(movies)

    response = {
        'cout': count_movies,
        'data': movies
    }

    return render_template(
        'pages/search_movies.html',
        results=response,
        search_term=request.form.get('search_term', '')
    )


@app.route('/movies/<int:movie_id>')
def show_movie(movie_id):

    movie = Movies.query.filter_by(id=movie_id).first()
    try:

        data = {
            'id': movie.id,
            'title': movie.title,
            'release_date': movie.release_date
        }
        # data['image_link']='/static/img/uda1.png'
    except Exception:
        print("\n\n\n\n\n")
        print(sys.exc_info())

        abort(422)

    return render_template('pages/show_movie.html', movie=data)


#  Create Movies
#  ----------------------------------------------------------------


@app.route('/movies/create', methods=['GET'])
@requires_auth('post:movies')
def create_movie_form():
    form = MovieForm()
    return render_template('forms/new_movie.html', form=form)


@app.route('/movies/create', methods=['POST'])
@requires_auth('post:movies')
def create_movie_submission():
    try:
        new_movie = Movies(
            title=request.form['title'],
            release_date=request.form['release_date'],
            actor_id=request.form['actor_id'],
        )
        db.session.add(new_movie)
        db.session.commit()
        flash('Movies ' + request.form['title'] + ' was successfully listed!')
    except Exception:
        print(sys.exc_info())
        db.session.rollback()
        flash(
            'An error occurred. Movies '
            + request.form['title']
            + ' could not be listed.'

        )
        print("abort 422")
        abort(422)
    finally:
        db.session.close()

    return render_template('pages/home.html')


@app.route('/movies/<movie_id>', methods=['DELETE'])
@requires_auth('delete:movies')
def delete_movie(movie_id):
    try:
        print("movie to deleted: ", movie_id)
        movie = Movies.query.filter_by(id=movie_id).first_or_404()
        db.session.delete(movie)
        db.session.commit()
        flash('Movies  was successfully deleted!')
    except Exception:
        print(sys.exc_info())
        db.session.rollback()
        abort(404)
    finally:
        db.session.close()
    return render_template('pages/home.html')


@app.route('/movies/<int:movie_id>/edit', methods=['GET'])
@requires_auth('patch:movies')
def edit_movie(movie_id):
    movie = Movies.query.get(movie_id)
    form = MovieForm(obj=movie)
    print("Edit movie: ", movie_id)

    return render_template('forms/edit_movie.html', form=form, movie=movie)


@app.route('/movies/<int:movie_id>/edit', methods=['PATCH'])
@requires_auth('patch:movies')
def edit_movie_submission(movie_id):
    try:
        movie = Movies.query.get(movie_id)
        form = MovieForm(obj=movie)

        if(request.form.get('title')):
            movie.title = request.form['title']
        if(request.form.get('release_date')):
            movie.release_date = request.form['release_date']

        db.session.commit()
        flash('Actor ' + movie.title + ' was successfully edited!')

    except Exception:
        print(sys.exc_info())
        db.session.rollback()
        abort(422)
    finally:
        db.session.close()

    return redirect(url_for('show_movie', movie_id=movie_id))

# ---------------------------------------------------------------
#  Actors
#  ----------------------------------------------------------------


@app.route('/actors')
def actors():
    actors = Actors.query.all()
    return render_template('pages/actors.html', actors=actors)


@app.route('/actors/search', methods=['POST'])
def search_actors():
    search_term = request.form.get('search_term', None)

    actors = Actors.query.filter(
        Actors.name.ilike(
            '%{}%'.format(search_term)
        )
    )

    if actors:
        count_actors = func.len(actors)

    response = {
        'cout': count_actors,
        'data': actors
    }

    return render_template(
        'pages/search_actors.html',
        results=response,
        search_term=request.form.get('search_term', '')
    )


@app.route('/actors/<int:actor_id>')
def show_actor(actor_id):

    actor = Actors.query.get(actor_id)

    data = {
        'id': actor.id,
        'name': actor.name,
        'age': actor.age,
        'gender': actor.gender
    }
    return render_template('pages/show_actor.html', actor=data)


# Update /edit actors

@ app.route('/actors/<int:actor_id>/edit', methods=['GET'])
@requires_auth('patch:actors')
def edit_actor(actor_id):
    actor = Actors.query.get(actor_id)
    form = ActorForm(obj=actor)
    return render_template('forms/edit_actor.html', form=form, actor=actor)


@ app.route('/actors/<int:actor_id>/edit', methods=['PATCH'])
@requires_auth('patch:actors')
def edit_actor_submission(actor_id):
    try:
        actor = Actors.query.get(actor_id)
        form = ActorForm(obj=actor)
        if(request.form.get('name')):
            actor.name = request.form['name']
            if(request.form.get('age')):
                actor.age = request.form['age']
        if(request.form.get('gender')):
            actor.gender = request.form['gender']
        db.session.commit()
        flash('Actor ' + actor.name + ' was successfully edited!')

    except Exception:
        print(sys.exc_info())
        actor = Actors.query.get(actor_id)
        if actor is not None:
            flash(
                'An error occurred. Actor '
                + actor.name
                + ' could not be edited.'
            )
        abort(422)
        db.session.rollback()
    finally:
        db.session.close()

    return redirect(url_for('show_actor', actor_id=actor_id))


#  Create Actor
@ app.route('/actors/create', methods=['GET'])
@requires_auth('post:actors')
def create_actor_form():
    form = ActorForm()
    return render_template('forms/new_actor.html', form=form)


@ app.route('/actors/create', methods=['POST'])
@requires_auth('post:actors')
def create_actor_submission():
    try:
        # print("request form post: ", request.form)
        new_actor = Actors(
            name=request.form['name'],
            age=request.form['age'],
            gender=request.form['gender'],
        )
        db.session.add(new_actor)
        db.session.commit()
        flash('Actor ' + request.form['name'] + ' was successfully listed!')
    except Exception:
        print(sys.exc_info())
        db.session.rollback()
        flash(
            'An error occurred. Actor '
            + request.form['name']
            + ' could not be listed.'
        )

    finally:
        db.session.close()

    return render_template('pages/home.html')
# delete actors


@app.route('/actors/<actor_id>', methods=['DELETE'])
@requires_auth('delete:actors')
def delete_actor(actor_id):
    try:
        actor = Actors.query.filter_by(id=actor_id).first_or_404()
        db.session.delete(actor)
        db.session.commit()
    except Exception:
        db.session.rollback()
    finally:
        db.session.close()
    return render_template('pages/home.html')


if __name__ == '__main__':
    app.run(debug=True)
