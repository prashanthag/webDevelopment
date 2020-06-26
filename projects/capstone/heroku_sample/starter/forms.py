from datetime import datetime

from flask_wtf import Form
from wtforms import IntegerField,StringField, SelectField, SelectMultipleField, DateTimeField,DateField
from wtforms.validators import DataRequired, AnyOf, URL



class MovieForm(Form):
    title = StringField(
        'title', validators=[DataRequired()]
    )
    release_date = DateField(
        'release_date', validators=[DataRequired()],
         default = datetime.today()
    )
    actor_id =IntegerField(
        'actor_id', validators=[DataRequired()]
    )
 

class ActorForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    age = IntegerField(
        'age', validators=[DataRequired()]
    )
    gender = StringField(
        'gender', validators=[DataRequired()]
    )
 
# TODO IMPLEMENT NEW ACTOR FORM AND NEW MOVIE FORM
