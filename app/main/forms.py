
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, FloatField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, InputRequired, Email, NumberRange
from app.main.exception import CustomException
import sys
from flask_bootstrap import Bootstrap

class WebForm(FlaskForm): 
    name =StringField(validators=[DataRequired() ], 
                                          render_kw={"placeholder": "Your Name"})
    email = StringField(validators=[DataRequired(), Email()], 
                                          render_kw={"placeholder": "Your email"})
    subject = StringField(validators=[DataRequired()], 
                                          render_kw={"placeholder": "Subject"})
    message = TextAreaField(validators=[DataRequired()], 
                                          render_kw={"rows": 7, "placeholder": "Message"})   
    submit = SubmitField('Send Message', validators=[DataRequired()])


    