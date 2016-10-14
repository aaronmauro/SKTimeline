#This is a web app built with the Flask framework based on Jinja templating: http://flask.pocoo.org

import os
import gc

from pprint import pprint



from flask_wtf import Form
from wtforms import BooleanField, TextField, IntegerField, StringField, SubmitField, TextAreaField, PasswordField, DateField, validators
from wtforms.ext.sqlalchemy.orm import model_form
from functools import wraps
from flask import Flask, render_template, flash, request, url_for, redirect, session

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile( os.path.join( os.path.dirname(__file__) , '../instance/config.py') )

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

from flask_mail import Mail, Message
mail = Mail(app)

from flask_bootstrap import Bootstrap
Bootstrap(app)

import tweepy
tweepy_auth = tweepy.OAuthHandler( app.config['TWEEPY_CONSUMER_KEY'], app.config['TWEEPY_CONSUMER_SECRET'])
tweepy_auth.set_access_token( app.config['TWEEPY_ACCESS_TOKEN_KEY'], app.config['TWEEPY_ACCESS_TOKEN_SECRET'] )
tweepy_API = tweepy.API(tweepy_auth)


import github as pyGithub
if app.config['PYGITHUB_DEBUG']:
    pyGithub.enable_console_debug_logging()
GithubAPI = pyGithub.Github(per_page=100, client_id=app.config['GITHUB_CLIENT_ID'], client_secret=app.config['GITHUB_CLIENT_SECRET'] )

from sktimeline.models import *
from sktimeline.views import *
