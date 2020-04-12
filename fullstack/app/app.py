import sys 
from flask import Flask ,render_template ,request,redirect,url_for,abort,jsonify
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres@localhost:5432/app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)

class Todo(db.Model):
    __tablename__='Todo'
    id = db.Column(db.Integer,primary_key=True)
    description = db.Column(db.String(),nullable=False)

    def __repr__(self):
        return f'Todo {self.id}, {self.description}'

#db.session.add(Data(des))
db.create_all()
#person = Data(description='bull')
#db.session.add(person)
#db.session.commit()
@app.route('/todos/create', methods=['POST'])
def create_todo():
    error = False
    body = {}
    try:
        #description = request.form.get('description','')
        description = request.get_json()['description']
        todo = Todo(description=description)
        db.session.add(todo)
        db.session.commit()
        #return redirect(url_for('index'))
        body ['description'] = todo.description
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if not error:
        return  jsonify(body)
@app.route('/')
def index():
   """
   return render_template('index.html',data=[{
        'description':"Todo 1"
    },
    {
        'description':"Todo 2"
    },
    {
        'description':"Todo 3"
    }
    ])
    """


   return render_template('index.html',data=Todo.query.all())


if __name__ == '__main__':
  app.run()