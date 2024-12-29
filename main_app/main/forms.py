
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email 
from main_app.main.exception import CustomException
import sys


class WebForm(FlaskForm): 
    try:
        name =StringField(validators=[DataRequired() ], 
                                            render_kw={"placeholder": "Your Name"})
        email = StringField(validators=[DataRequired(), Email()], 
                                            render_kw={"placeholder": "Your email"})
        subject = StringField(validators=[DataRequired()], 
                                            render_kw={"placeholder": "Subject"})
        message = TextAreaField(validators=[DataRequired()], 
                                            render_kw={"rows": 7, "placeholder": "Message"})   
        submit = SubmitField('Send Message', validators=[DataRequired()])

    except Exception as e:
        raise CustomException(sys, e)


    