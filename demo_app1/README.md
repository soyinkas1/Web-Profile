# PP0002_Heart-Diesease-Project
This project is a binary classification project which predicts if a person has a heart disease based on health data provided. 

    
**Problem Statement:** 
The In a statement,
> Given clinical parameters about a patient, can we predict whether or not they have heart disease?


## Table of Contents
1. [Project Overview](#project-overview)
2. [Project Structure](#project-structure)
3. [Technology Stack](#tech-stack)
4. [Data Preparation](#data-preparation)
5. [Model Training](#model-training)
6. [Model Evaluation](#evaluating-multiple-models)
7. [Deployment](#deployment)
    - [Flask Web App](#Flask-web-app)
    - [Azure Deployment](#azure-deployment)
    - [AWS Elastic Beanstalk Deployment](#aws-elastic-beanstalk-deployment)
9.  [Update Workflows](#update-workflows)
10. [Usage](#usage)
11. [Contributing](#contributing)
12. [License](#license)
13. [Acknowledgments](#acknowledgments)
14. [Future Planned Updates](#future-work/advancements)


## Project Overview
The first attempt at this project was part of the ZTM ML Data Science bootcamp. The notebook- Heart Disease Classification Project_ZTM Walkalong 08_22.ipynb in the notebook directory is the work along file from the bootcamp. 

This version is an upgrade to an end-to-end ML project to extend the work done in the bootcamp by carrying out the following additional steps and capabilities such as:

* Experiment with additional classification models and hyperparameters
* Convert project structure to modular programming using OOP
* Deploy as a Flask Web App
* Prediction results sent to email
* Prediction data and results saved to a Cloud database
* Deploy the web application to the Cloud.

**Current Objectives**
* Enhance the approach used in the initial project from ZTM ML bootcamp
* Improve on the experiments carried out
* Implement as a modular programmed application using best practices such as Object-Oriented Programming etc.
* Deploying the application to both Azure and AWS. The goal is to create a robust, scalable solution that can be accessed and used via web services on both cloud platforms.
* Ultimately deploy the app in a custom domain 
  
## Project Structure
```
├── app
│   ├── data
│   │   ├── heart-diesease.csv
│   ├── main
│   │   ├── components
│   │   │   ├── __initi__.py
│   │   │   ├── data_cleaning.py
│   │   │   ├── data_ingestion.py
│   │   │   ├── data_transformation.py
│   │   │   ├── model_training.py
│   │   ├── config
│   │   │   ├── __init__.py
│   │   │   ├── config_entity.py
│   │   │   ├── config.yaml
│   │   │   ├── configuration.py
│   │   │   ├── params.yaml
│   │   ├── constants
│   │   │   ├── __init__.py
│   │   ├── pipeline
│   │   │   ├── __init__.py
│   │   │   ├── stage_01_data_ingestion.py
│   │   │   ├── stage_02_data_cleaning.py
│   │   │   ├── stage_03_data_transformation.py
│   │   │   ├── stage_04_model_training.py
│   │   │   ├── stage_05_prediction_pipeline.py
│   │   ├── __init__.py
│   │   ├── errors.py
│   │   ├── exception.py
│   │   ├── forms.py
│   │   ├── logging.py
│   │   ├── views.py
│   ├── notebooks
│   │   ├── Heart Disease Classification Project_Latest Research.ipynb
│   │   ├── Heart Disease Classification Project_ZTM Walkalong 08_22.ipynb
│   ├── static
│   │   ├──bootstrap.min.css
│   │   ├──style.css    
│   ├── templates
│   │   ├──mail
│   │   │   ├──results.html
│   │   ├──404.html
│   │   ├──500.html
│   │   ├──base.html
│   │   ├──index.html
│   │   ├──prediction.html
│   │   ├──results.html
│   ├──utils
│   │   ├── __init__.py
│   │   ├── common.py
│   ├── __init__.py
│   ├── db_models.py 
│   ├── email.py 
├── artifacts
│   ├── data_cleaning 
│   │   ├── clean_heart-disease.csv    
│   ├── data_ingestion
│   │   ├── loaded_heart-disease.csv  
│   ├── data_transformation
│   │   ├── X_test.csv
│   │   ├── X_train.csv
│   │   ├── y_test.csv
│   │   ├── y_train.csv
│   ├── best_model.pkl
│   ├── preprocessor.pkl
├── logs
├── migrations
├── tests
├── venv
├── __init__.py
├── .env
├── .gitignore
├── application.py
├── config.py
├── Dockerfile
├──  README.md
├── requirements.txt


```
## Tech Stack
### Dependencies
```
- python 3.12
- pandas
- numpy
- scikit-learn
- plotly
- matplotlib
- seaborn
- lightgbm
- xgboost
- dill
- flask
- flask-wtf
- flask-bootstrap
- flask-mail
- flask-moment
- flask_sqlalchemy
- psycopg2
- flask_fontawesome
- Flask-Migrate
- ensure
- python-box
- pyYAML
- python-dotenv
- jupyter
- gunicorn
- email_validator
- Github (action)
- Azure Web App
- Azure MySQL Flexible Server
- HTML & CSS

```
### Step-by-Step Implementation
 **Install the required packages:**
    ```
    pip install -r requirements.txt
    ```

## Data Preparation
### Data Sources
- The original data if from the Cleveland data from the UCI machine Learning Repository. https://archive.ics.uci.edu/ml/datasets/heart+disease

- There is also a version on Kaggle. https://www.kaggle.com/datasets/johnsmith88/heart-disease-dataset 

### Data Cleaning, Preprocessing and Transformation
The following steps were carried out of this dataset to clean and transform it for use:
- Missing Values:
    * There is no missing values in the dataset
- There was no requirement for transformation as well as there dataset were already encoded for its categorical features
        
## Final Data Dictionary 

<table border="1">
        <thead>
            <tr>
                <th>S/N</th>
                <th>Feature</th>
                <th>Description</th>
                <th>Data Class</th>
                <th>Data Type</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>1</td>
                <td>Age</td>
                <td>The Age of patient in years</td>
                <td>numeric</td>
                <td>int</td>
            </tr>
            <tr>          
                <td>2</td>
                <td>Sex</td>
                <td>1-Male or 2-Female.</td>
                <td>categorical</td>
                <td>int</td>
            </tr>
            <tr>
                <td>3</td>
                <td>cp</td>
                <td>Chest Pain Type</td>
                <td>categorical</td>
                <td>int</td>
            </tr>
            <tr>
                <td>4</td>
                <td>tresbps</td>
                <td>Resting Blood Pressure (in mm Hg on admissions to the hospital).</td>
                <td>numeric</td>
                <td>int</td>
            </tr>
            <tr>
                <td>5</td>
                <td>chol</td>
                <td>Serum Cholestoral in mg/dl.</td>
                <td>numeric</td>
                <td>int</td>
            </tr>
            <tr>
                <td>6</td>
                <td>fbs</td>
                <td>Fasting Blood Sugar > 120mg (1-True, 0-False).</td>
                <td>categorical</td>
                <td>int</td>
            </tr>
            <tr>
                <td>7</td>
                <td>restecg</td>
                <td>Resting electocadiographic (ECG)  results</td>
                <td>numeric</td>
                <td>int</td>
            </tr>
            <tr>
                <td>8</td>
                <td>oldpeak</td>
                <td>ST depression induced by exercise relative to rest</td>
                <td>numeric</td>
                <td>float</td>
            </tr>
            <tr>
                <td>9</td>
                <td>slope</td>
                <td>The slope of the peak exercise ST segment.</td>
                <td>numeric</td>
                <td>int</td>
            </tr>
            <tr>
                <td>10</td>
                <td>ca</td>
                <td>Number of major vessels (0-3) coloured by flourosopy</td>
                <td>numeric</td>
                <td>int</td>
            </tr>
            <tr>
                <td>11</td>
                <td>thal</td>
                <td>1-Normal, 2-Fixed defect, 3-Reversible defect</td>
                <td>numeric</td>
                <td>int</td>
            </tr>
             <tr>
                <td>12</td>
                <td>Target</td>
                <td>(1) for has heart disease and (0) for do not have heart disease</td>
                <<td>label</td>
                <td>int</td>
            </tr>           
        </tbody>
    </table>
				

## Model Training
### Model Selection
The following models were selected after using recommendations from researching classification models and subsequent experimenting:

- Logistic regression
- Support Vector Machine Classifier (SVC)
- Random Forest Classifier
- XGBoost
- LightGBM

### Training the Model
- Loading the Configuration
First, load the  model training configuration. This configuration includes settings which are the paths to the training, validation, and test data, as well as the machine learning models and their parameters.
- Loading the Data
Next, load the datasets:
    * Training Data: Used to train the models.
    * Validation Data: Used to tune and validate the models during the training process.
    * Test Data: Used to evaluate the final model's performance.
- Splitting the Data
Split each dataset into:
    * Input Features (X): The data that our model will learn from.
    * Target Labels (y): The actual outcomes we want to predict (whether the patient has heart diesease or not).

### Evaluating Multiple Models
Evaluated several machine learning models to see which one performs the best. 

Each model is tested using the training and validation data. Used a helper function based on ‘GridSearchCV’ called evaluate_models using hyperparameters values set in the `params.yaml` file to check how well each model performs and store the results. 
- Selecting the Best Model
Looked at the performance scores of all the models and choose the one with the highest score. If no model achieves a score of at least 0.6 (out of 1.0), the application raises an error indicating that no suitable model was found.
- Saving the Best Model
Once the best model is identified, it is saved to a file to be used later to make predictions.

This process will be updated in the next version to incorporate a complete MLOps pipeline with automated model training and model Registry 

## Deployment
### Flask Web App
- The Flask web framework was used to share the web application for use. A simple web app with a form to collect data points and return the prediction was developed. CSS was used to perform minimal customasation of the Bootstrap template used for the web page. This web app has the capability to email the prediction results to the email address provided and also store the prediction data and result in a database.
### Azure Deployment
Deployment to `Azure Web App Service` was done using Github action with `Docker` for CI/CD of the application. The `Azure MySQL Flexible Server` was used to store the prediction results and data. The database was connect to MySQL Workbench for easy analysis of the prediction data in the database.

Use the link below to access the web app deployed to `Azure Cloud`:

https://hdpredictor.azurewebsites.net/

## Update Workflow

1. Update the config_entity in config
2. Update config.yaml in config
3. Update params.yaml in config
4. Update the configuration manager in config
5. Update the components scripts
6. Update the pipeline scripts
7. Update the main files (forms.py, views.py, errors.py, exception.py)
8. Update db_models.py and email.py
8. Update the application.py

## Usage
### Accessing the Deployed Model
- Upon launching the application, the default page is the `About` page.
- Use the `Predict`tab to access the prediction page and provide values for all the data endpoints for the patient using the input boxes, dropdowns etc.
- Click the submit button for prediction by the model. The result is displayed in the web page and also emailed to the email address provided.
  
## Contributing
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a pull request.

## License
This project is licensed under the MIT License 

## Acknowledgments
The project code, structure, best practices etc. were inspired and learnt from a myriad of open sources such as :
- Coursework from Zero to Mastery Data Science ML Bootcamp 
- Youtube videos of Kris Naik such as the End to End Machine Learning Project Video 
- Books and literature such as Flask Web Development, Data Science from Scratch etc.
- Udemy trainings
- Github repositories and resources
- Medium.com articles etc.
- Lastly and not the least -ChatGPT!

## Future Work/Advancements

1. Update with an automated training pipeline with model registry using tools such as MLFlow, DVC, CometML.

