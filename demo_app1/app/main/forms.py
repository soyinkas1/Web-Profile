from flask import Flask, redirect, render_template, url_for, session
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, FloatField, IntegerField, SelectField
from wtforms.validators import DataRequired, InputRequired, Email, NumberRange
from .exception import CustomException
import sys

# from src.pipeline.stage_07_prediction_pipeline import CustomData, PredictPipeline
from .config.configuration import ConfigurationManager

def validate_float_range(form, field):
    if not (-2.6 <= field.data <= 6.2):
        raise CustomException(sys)


class WebForm(FlaskForm):

    config = ConfigurationManager()
    webform_config = config.get_webform_config
     
        
    email = StringField("Email address", validators=[DataRequired(), Email()], 
                                          render_kw={"placeholder": "Provide the email address that the prediction will be sent to"})
    age = IntegerField('Age in years', default=18 , validators=[DataRequired(), InputRequired(), NumberRange(min=18, max=120, message="Age must be between 18 and 120")])
    sex = SelectField('Sex', choices=[(1, 'male'), (0, 'female')], coerce=int, validate_choice=True)
    cp = SelectField('Chest Pain Type', choices=[(1, 'typical angina'),(2, 'atypical angina'),(3, 'non-anginal pain'), (4, 'asymptomatic')], coerce=int, validate_choice=True)
    trestbps = IntegerField("Resting blood pressure (in mm Hg on admission to the hospital)", default=94 ,validators=[DataRequired(), InputRequired(), NumberRange(min=94, max=200, message="Value must be between 94 and 200")])
    chol = IntegerField("Serum cholestoral in mg/dl", default=126 ,validators=[DataRequired(), InputRequired(), NumberRange(min=126, max=564, message="Value must be between 126 and 564")])
    fbs = SelectField('(Fasting blood sugar &gt; 120 mg/dl)', choices=[(1, 'True'), (0, 'False')], coerce=int, validate_choice=True)
    restecg = SelectField('Resting electrocardiographic results', choices=[(0, '0-Normal'), (1, '1-Having ST-T wave abnormality'), (2, '2-Showing probable or definite left ventricular hypertrophy')], coerce=int, validate_choice=True)
    thalach = IntegerField('Maximum heart rate achieved', default=71 ,validators=[DataRequired(), InputRequired(), NumberRange(min=71, max=202, message="Value must be between 18 and 120")])
    exang = SelectField('Exercise induced angina', choices=[(1, 'Yes'), (0, 'No')], coerce=int, validate_choice=True)
    oldpeak = FloatField('ST depression induced by exercise relative to rest', default=-2.6 ,validators=[DataRequired(), InputRequired(), validate_float_range])
    slope = SelectField('The slope of the peak exercise ST segment', choices=[(0, '0-Upsloping'), (1, '1-Flat'), (2, '2-Downsloping')], coerce=int, validate_choice=True)
    ca = SelectField('Number of major vessels (0-3) colored by flourosopy', choices=[(0, '0'),(1, '1'),(2, '2'), (3, '3')], coerce=int, validate_choice=True)
    thal = SelectField('Thalassemia (a type of anemia)', choices=[(1, '1-Normal'), (2, '2-Fixed defect'), (3, '3-Reversable defect')], coerce=int, validate_choice=True)
    submit = SubmitField('Submit', validators=[DataRequired()])


    