import time
from flask import render_template, redirect, url_for, flash, request

from . import main_blueprint
from .forms import WebForm
from .data import CustomData
from . import email
from .logging import logging
from main_app import flatpages, limiter
from dotenv import load_dotenv
import os

load_dotenv()

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
MAIL_USERNAME = os.getenv("MAIN_MAIL_USERNAME")


def _real_client_ip():
    """Return the visitor's real IP, trusting PA's proxy headers."""
    return (
        request.headers.get("X-Real-IP")
        or request.headers.get("X-Forwarded-For", request.remote_addr or "0.0.0.0")
                  .split(",")[0]
                  .strip()
    )


@main_blueprint.route("/", methods=["GET", "POST"])
@limiter.limit(
    "3 per hour; 10 per day",
    methods=["POST"],
    key_func=_real_client_ip,
    error_message="Too many submissions. Please try again later.",
)
def index():
    
    projects = [p for p in flatpages if p.path.startswith(DIR_PROJECTS)]
    latest_projects = sorted(
        projects, reverse=True, key=lambda p: getattr(p, "meta").get("date")
    )

    posts = [p for p in flatpages if p.path.startswith(DIR_BLOG_POSTS)]
    filtered_posts = [
        p for p in posts if getattr(p, "meta").get("published") is True
    ]
    latest_posts = sorted(
        filtered_posts, reverse=True, key=lambda p: getattr(p, "meta").get("date")
    )

    trainings = [t for t in flatpages if t.path.startswith(DIR_TRAININGS)]
    latest_trainings = sorted(
        trainings, reverse=True, key=lambda p: getattr(p, "meta").get("date")
    )

    testimonials = [t for t in flatpages if t.path.startswith(DIR_TESTIMONIALS)]
    latest_testimonials = sorted(
        testimonials, reverse=True, key=lambda p: getattr(p, "meta").get("date")
    )

    logging.info("index page hit, method=%s ip=%s", request.method, _real_client_ip())

    # --- Contact form ---
    form = WebForm()

    # On GET, stamp the render time so the form's timing validator can
    # check how long the user took to fill it in.
    if request.method == "GET":
        form.form_loaded_at.data = str(time.time())

    if form.validate_on_submit():
        # Validation has already passed: honeypots empty, timing within
        # bounds, no header injection, no gibberish, valid email domain.
        # The narrow try/except below covers ONLY real I/O (DB + mail).
        try:
            data = CustomData(
                name=form.name.data,
                email=form.email.data,
                subject=form.subject.data,
                message=form.message.data,
            )
            data_df = data.get_data_as_data_frame()
            data.add_to_database(data_df)
            logging.info("Contact stored from ip=%s", _real_client_ip())

            email.send_contact_notification(
                sender_name=form.name.data,
                sender_email=form.email.data,
                subject=form.subject.data,
                message_body=form.message.data,
            )

            flash("Message sent", "success")
            return redirect(url_for("main.index", _anchor="contact"))

        except Exception:
            # Real failure (DB error, mail server down, etc.).
            # Log full traceback, show generic message — never leak
            # internals to the requester.
            logging.exception("Contact form processing failed")
            flash("Something went wrong. Please try again later.", "error")
            return redirect(url_for("main.index", _anchor="contact"))

    # POST that failed validation: log what was rejected so we can
    # tune the filters by watching the logs.
    if request.method == "POST" and form.errors:
        logging.warning(
            "Contact form rejected ip=%s errors=%s",
            _real_client_ip(),
            form.errors,
        )

    return render_template(
        "index.html",
        twitter_url=TWITTER_URL,
        github_url=GITHUB_URL,
        medium_url=MEDIUM_URL,
        linkedin_url=LINKEDIN_URL,
        projects=latest_projects,
        posts=latest_posts,
        trainings=latest_trainings,
        testimonials=latest_testimonials,
        form=form,
    )


@main_blueprint.errorhandler(429)
def ratelimit_handler(e):
    """Friendly UX for rate-limited submissions instead of a hard 429 page."""
    flash(
        "Too many submissions from your network. Please try again in an hour.",
        "error",
    )
    return redirect(url_for("main.index", _anchor="contact"))


@main_blueprint.route("/post/<name>/")
def post(name):
    path = "{}/{}".format(DIR_BLOG_POSTS, name)
    post = flatpages.get_or_404(path)
    return render_template("blog-post.html", post=post)


@main_blueprint.route("/miniblog", methods=["GET", "POST"])
def miniblog():
    posts = [p for p in flatpages if p.path.startswith(DIR_BLOG_POSTS)]
    filtered_posts = [
        p for p in posts if getattr(p, "meta").get("published") is True
    ]
    latest_posts = sorted(
        filtered_posts, reverse=True, key=lambda p: getattr(p, "meta").get("date")
    )

    return render_template(
        "miniblog.html",
        twitter_url=TWITTER_URL,
        github_url=GITHUB_URL,
        medium_url=MEDIUM_URL,
        linkedin_url=LINKEDIN_URL,
        posts=latest_posts,
    )


@main_blueprint.route("/portfolio", methods=["GET", "POST"])
def portfolio():
    projects = [p for p in flatpages if p.path.startswith(DIR_PROJECTS)]
    latest_projects = sorted(
        projects, reverse=True, key=lambda p: getattr(p, "meta").get("date")
    )

    return render_template(
        "portfolio.html",
        twitter_url=TWITTER_URL,
        github_url=GITHUB_URL,
        medium_url=MEDIUM_URL,
        linkedin_url=LINKEDIN_URL,
        projects=latest_projects,
    )


@main_blueprint.route("/trainings", methods=["GET", "POST"])
def trainings():
    trainings = [t for t in flatpages if t.path.startswith(DIR_TRAININGS)]
    latest_trainings = sorted(
        trainings, reverse=True, key=lambda p: getattr(p, "meta").get("date")
    )

    return render_template(
        "trainings.html",
        twitter_url=TWITTER_URL,
        github_url=GITHUB_URL,
        medium_url=MEDIUM_URL,
        linkedin_url=LINKEDIN_URL,
        trainings=latest_trainings,
    )