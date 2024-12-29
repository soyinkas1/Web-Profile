from flask import render_template, session, redirect, url_for, current_app, flash
from . import main_blueprint
from .forms import WebForm
from .. import db
from main_app.db_models import ContactTable
from .data import CustomData
from .exception import CustomException
from . import email
from .logging import logging
from main_app import flatpages
from dotenv import load_dotenv
import os
import sys

load_dotenv()

<<<<<<< HEAD:main_app/main/views.py
FLATPAGES_AUTO_RELOAD = os.getenv("MAIN_FLATPAGES_AUTO_RELOAD")
FLATPAGES_EXTENSION = os.getenv("MAIN_FLATPAGES_EXTENSION")
FLATPAGES_ROOT = os.getenv("MAIN_FLATPAGES_ROOT")
DIR_BLOG_POSTS = os.getenv("MAIN_DIR_BLOG_POSTS")
DIR_PROJECTS = os.getenv("MAIN_DIR_PROJECTS")
DIR_TESTIMONIALS = os.getenv("MAIN_DIR_TESTIMONIALS")
DIR_TRAININGS = os.getenv("MAIN_DIR_TRAININGS")
TWITTER_URL = os.getenv("MAIN_TWITTER_URL")
GITHUB_URL = os.getenv("MAIN_GITHUB_URL")
MEDIUM_URL = os.getenv("MAIN_MEDIUM_URL")
LINKEDIN_URL = os.getenv("MAIN_LINKEDIN_URL")
=======
FLATPAGES_AUTO_RELOAD = os.getenv("FLATPAGES_AUTO_RELOAD")
FLATPAGES_EXTENSION = os.getenv("FLATPAGES_EXTENSION")
FLATPAGES_ROOT = os.getenv("FLATPAGES_ROOT")
DIR_PROJECTS = os.getenv("DIR_PROJECTS")
DIR_BLOG_POSTS = os.getenv("DIR_BLOG_POSTS")
DIR_TESTIMONIALS = os.getenv("DIR_TESTIMONIALS")
DIR_TRAININGS = os.getenv("DIR_TRAININGS")
TWITTER_URL = os.getenv("TWITTER_URL")
GITHUB_URL = os.getenv("GITHUB_URL")
MEDIUM_URL = os.getenv("MEDIUM_URL")
LINKEDIN_URL = os.getenv("LINKEDIN_URL")
MAIL_USERNAME = os.getenv("MAIL_USERNAME")
>>>>>>> main:app/main/views.py


@main_blueprint.route('/', methods=['GET', 'POST'])
def index():
    
    # Get the projects 
    projects = [p for p in flatpages if p.path.startswith(DIR_PROJECTS)]

    
    # Sort the filtered projects by date
    latest_projects = sorted(projects, reverse=True, key=lambda p: getattr(p, "meta").get('date'))

    # Get the posts
    posts = [p for p in flatpages if p.path.startswith(DIR_BLOG_POSTS)]
    
    # Filter for posts for publish
    filtered_posts = []
    for post in posts:
        published_status = getattr(post, "meta").get('published')
        # print(f"Check2 - Published status for {post.path}: {published_status}")
        if published_status == True:
            filtered_posts.append(post)

    # Sort the filtered posts by date
    latest_posts = sorted(filtered_posts, reverse=True, key=lambda p: getattr(p, "meta").get('date'))
    
     # Get the trainings
    trainings = [t for t in flatpages if t.path.startswith(DIR_TRAININGS)]
    
    # Sort the filtered projects by date
    latest_trainings = sorted(trainings, reverse=True, key=lambda p: getattr(p, "meta").get('date'))

    # Get the testimonials
    testimonials = [t for t in flatpages if t.path.startswith(DIR_TESTIMONIALS)]
    
    # Sort the filtered projects by date
    latest_testimonials = sorted(testimonials, reverse=True, key=lambda p: getattr(p, "meta").get('date'))
    
    logging.info('test')
    # Contact form data collection
    try:
        form = WebForm()
        if form.validate_on_submit():
            # Collect data input from webform      
            data = CustomData(
                name=form.name.data,
                email=form.email.data,
                subject=form.subject.data,
                message=form.message.data,
                
            )

            # Create DataFrame for prediction 
            data_df=data.get_data_as_data_frame()
            
    
            # Update the data to database
            
            data.add_to_database(data_df)

            logging.info('Database updated')
            # Email results 
            email.send_email([MAIL_USERNAME, data_df['email'].iloc[0]], data_df['subject'].iloc[0],
    'mail', message=data_df['message'].iloc[0], name=data_df['name'].iloc[0])
            confirm = 'Message sent'
            flash(confirm, 'success')

            return redirect(url_for('main.index', _anchor='contact'))

            # Render the template with the sorted projects and posts 
            # return render_template('index.html', twitter_url=TWITTER_URL, 
            #                         github_url=GITHUB_URL, medium_url=MEDIUM_URL, linkedin_url=LINKEDIN_URL,
            #                         projects=latest_projects, posts=latest_posts, testimonials=latest_testimonials, form=form, confirm=confirm)
    except Exception as e:
            raise CustomException(sys, e)
    
    return render_template('index.html', twitter_url=TWITTER_URL, 
                                        github_url=GITHUB_URL, medium_url=MEDIUM_URL, linkedin_url=LINKEDIN_URL,
                                        projects=latest_projects, posts=latest_posts, trainings=latest_trainings, testimonials=latest_testimonials, form=form)

    
        
      
@main_blueprint.route('/post/<name>/')
def post(name):
    path = '{}/{}'.format(DIR_BLOG_POSTS, name)
    post = flatpages.get_or_404(path)
    return render_template('blog-post.html', post=post)
  


@main_blueprint.route('/miniblog', methods=['GET', 'POST'])
def miniblog():

# Get the posts
    posts = [p for p in flatpages if p.path.startswith(DIR_BLOG_POSTS)]
    
    # Filter for posts for publish
    filtered_posts = []
    for post in posts:
        published_status = getattr(post, "meta").get('published')
        # print(f"Check2 - Published status for {post.path}: {published_status}")
        if published_status == True:
            filtered_posts.append(post)
# Sort the filtered posts by date
    latest_posts = sorted(filtered_posts, reverse=True, key=lambda p: getattr(p, "meta").get('date'))
    

    return render_template('miniblog.html', twitter_url=TWITTER_URL, 
                                        github_url=GITHUB_URL, medium_url=MEDIUM_URL, linkedin_url=LINKEDIN_URL, posts=latest_posts)


@main_blueprint.route('/portfolio', methods=['GET', 'POST'])
def portfolio():
    # Get the projects 
    projects = [p for p in flatpages if p.path.startswith(DIR_PROJECTS)]
    
    # Sort the filtered projects by date
    latest_projects = sorted(projects, reverse=True, key=lambda p: getattr(p, "meta").get('date'))

    return render_template('portfolio.html', twitter_url=TWITTER_URL, 
                                        github_url=GITHUB_URL, medium_url=MEDIUM_URL, linkedin_url=LINKEDIN_URL, projects=latest_projects)


@main_blueprint.route('/trainings', methods=['GET', 'POST'])
def trainings():
    # Get the trainings
    trainings = [t for t in flatpages if t.path.startswith(DIR_TRAININGS)]
    
    # Sort the filtered projects by date
    latest_trainings = sorted(trainings, reverse=True, key=lambda p: getattr(p, "meta").get('date'))

    return render_template('trainings.html', twitter_url=TWITTER_URL, 
                                        github_url=GITHUB_URL, medium_url=MEDIUM_URL, linkedin_url=LINKEDIN_URL, trainings=latest_trainings)