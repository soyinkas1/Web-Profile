from flask import render_template, session, redirect, url_for, current_app
from . import main_blueprint
# from .forms import WebForm
# from .. import db
# from ..db_models import HeartPredictions
# from app.main.pipeline.stage_05_prediction_pipeline import CustomData, PredictPipeline
# from app.main.config.configuration import ConfigurationManager
# from .. import email
from .logging import logging
from app import flatpages
from dotenv import load_dotenv
import os

load_dotenv()

FLATPAGES_AUTO_RELOAD = os.getenv("FLATPAGES_AUTO_RELOAD")
FLATPAGES_EXTENSION = os.getenv("FLATPAGES_EXTENSION")
FLATPAGES_ROOT = os.getenv("FLATPAGES_ROOT")
DIR_PROJECTS = os.getenv("DIR_PROJECTS")
TWITTER_URL = os.getenv("TWITTER_URL")
GITHUB_URL = os.getenv("GITHUB_URL")
MEDIUM_URL = os.getenv("MEDIUM_URL")
LINKEDIN_URL = os.getenv("LINKEDIN_URL")

print(FLATPAGES_ROOT)

@main_blueprint.route('/', methods=['GET', 'POST'])
def index():
    projects = [p for p in flatpages if p.path.startswith(DIR_PROJECTS)]
    
    # Sort the filtered posts by date
    latest = sorted(projects, reverse=True, key=lambda p: getattr(p, "meta").get('date'))
    return render_template('index.html', twitter_url=TWITTER_URL, 
                            github_url=GITHUB_URL, medium_url=MEDIUM_URL, linkedin_url=LINKEDIN_URL,
                            projects=latest)

      

# @main.route('/predictdata', methods=['GET', 'POST'])
# def predict_datapoint():
#     form = WebForm()
#     if form.validate_on_submit():
#         # Collect data imput from webform      
#         data = CustomData(
#             email=form.email.data,
#             age=form.age.data,
#             sex=form.sex.data,
#             cp=form.cp.data,
#             trestbps=form.trestbps.data,
#             chol=form.chol.data,
#             fbs=form.fbs.data,
#             restecg=form.restecg.data,
#             thalach=form.thalach.data,
#             exang=form.exang.data,
#             oldpeak=form.oldpeak.data,
#             slope=form.slope.data,
#             ca=form.ca.data,
#             thal=form.thal.data,
#             target=1
#         )

#         # Create DataFrame for prediction 
#         pred_df=data.get_data_as_data_frame()
#         print(pred_df)
   
#         # Make prediction using data supplied 
#         obj = PredictPipeline(config=predict_config)
#         predict = obj.predict(pred_df)

#         # Update the results to database
#         database_df = data.get_data_for_database()
#         database_df['target'] = predict
#         data.add_to_database(database_df)

#         logging.info('Database updated')
#         # Email results 
#         email.send_email(database_df['email'].iloc[0], 'results',
# 'mail/results', predict=predict)
#         logging.info('Email sent')

#         return render_template('results.html', predict=predict)

#     else:

#         return render_template('prediction.html', form=form)
    
# @main.route('/datadict', methods=['GET', 'POST'])
# def datadict():

#     return render_template('datadict.html')

# @main.route('/privacy', methods=['GET', 'POST'])
# def privacy():

#     return render_template('privacy.html')