from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
#'postgresql://myusername:mypassword@localhost:5432/mydatabase'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres@localhost:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
class Person(db.Model):
    __tablename__='ftable'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String,nullable=False)

    def __repr__(self):
        return f'<Person ID:{self.id}, name:{self.name}'

db.create_all()
person = Person(name='bull')
db.session.add(person)
db.session.commit()

@app.route('/')
def index():
        p = Person.query.first()
        return "hello " + p.name
if __name__ == '__main__':
  app.run()
