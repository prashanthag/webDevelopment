# Full Stack Casting Agency  

## Getting Started

### Installing Dependencies

#### Python 3.8.2

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)


#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the project directory  projects/capstone/heroku_sample/starter and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

### Postman
Install [postman](https://www.postman.com/downloads/) to test for unit testing

### Environment set up
please source `setup.sh`. to define variables used in the project 

```bash
source setup.sh
    or
. setup.sh
```

## Database Setup
Postgres already running in heroku cloud, so no need of setting up this locally to test this project 

## Running the server

From root directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `app.py` file to find the application. 



# Casting Agency Specifications
- The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process.

- Models:

    - Movies with attributes title and release date
    - Actors with attributes name, age and gender
- Endpoints:
    - GET /actors and /movies
    - DELETE /actors/ and /movies/
    - POST /actors and /movies and
    - PATCH /actors/ and /movies/
- Roles:
    - Casting Assistant
        - Can view actors and movies
    - Casting Director
        - All permissions a Casting Assistant has and…
        - Add or delete an actor from the database
        - Modify actors or movies
    - Executive Producer
        - All permissions a Casting Director has and…
        - Add or delete a movie from the database

## Example API endpoints and expected behavior
Since Front end is implemented, any end point request will not return any data as endpoint redirects to other path or render html . We can test this by visiting and running url  https://intense-earth-93621.herokuapp.com/. It only returns success 200 or error messages 4xx. In front end, login for casting producer and casting director and casting assistance is not implemented which is out of scope for this project



### GET `/actors`  

Returns a 200 OK if is success. If you added any actors , you can see that in heroku url as in below pic

Example:

![/actors](/projects/capstone/heroku_sample/starter/static/img/get_actors.png)

### POST `/movies`
 returns 401 for casting director and casting assistant and returns 200 for casting producer which you can see that in postman test case and also unittest 
### More examples 
in test_app.py 

## Testing
- ### Heroku url 
    Project is running in cloud         
        https://intense-earth-93621.herokuapp.com/

- Import enviroments by running
    ```
    source setup.sh
    ```
- To run the tests, there are two ways of running this project. Before this you need to clear database and run the test case otherwise you get some test cases getting failed
    - By python unittest
    
        ```bash
        python3 test_app.py
        ```

    - import file ```udacity-fsnd-capstone.postman_collection.json``` in postman and run test cases
       
