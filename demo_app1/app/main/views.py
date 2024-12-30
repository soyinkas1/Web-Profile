from flask import render_template, session, redirect, url_for
from . import demo1_app
from .forms import WebForm
# from .. import db
# from ..db_models import HeartPredictions
from demo_app1.app.main.pipeline.stage_05_prediction_pipeline import CustomData, PredictPipeline
from demo_app1.app.main.config.configuration import ConfigurationManager
from .. import email
from .logging import logging


config = ConfigurationManager()
predict_config = config.get_prediction_pipeline_config()

@demo1_app.route('/', methods=['GET', 'POST'])
def demo1_app_home():

    return render_template('demo1_app_home.html')

      

@demo1_app.route('/predictdata', methods=['GET', 'POST'])
def predict_datapoint():
    form = WebForm()
    if form.validate_on_submit():
        # Collect data imput from webform      
        data = CustomData(
            email=form.email.data,
            age=form.age.data,
            sex=form.sex.data,
            cp=form.cp.data,
            trestbps=form.trestbps.data,
            chol=form.chol.data,
            fbs=form.fbs.data,
            restecg=form.restecg.data,
            thalach=form.thalach.data,
            exang=form.exang.data,
            oldpeak=form.oldpeak.data,
            slope=form.slope.data,
            ca=form.ca.data,
            thal=form.thal.data,
            target=1
        )

        # Create DataFrame for prediction 
        pred_df=data.get_data_as_data_frame()
        print(pred_df)
   
        # Make prediction using data supplied 
        obj = PredictPipeline(config=predict_config)
        predict = obj.predict(pred_df)

        # Update the results to database
        database_df = data.get_data_for_database()
        database_df['target'] = predict
        data.add_to_database(database_df)

        logging.info('Database updated')
        # Email results 
        email.send_email(database_df['email'].iloc[0], 'results',
'mail/results', predict=predict)
        logging.info('Email sent')

        return render_template('results.html', predict=predict)

    else:

        return render_template('prediction.html', form=form)
    
@demo1_app.route('/datadict', methods=['GET', 'POST'])
def datadict():

    return render_template('datadict.html')

@demo1_app.route('/privacy', methods=['GET', 'POST'])
def privacy():

    return render_template('privacy.html')