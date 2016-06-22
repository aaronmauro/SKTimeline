#This is a web app built with the Flask framework based on Jinja templating: http://flask.pocoo.org
import os
import gc

from wtforms import Form, BooleanField, TextField, IntegerField, StringField, SubmitField, TextAreaField, PasswordField, DateField, validators
from functools import wraps
from flask import Flask, render_template, flash, request, url_for, redirect, session

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile( os.path.join( os.path.dirname(__file__) , '../instance/config.py') )

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

from flask_mail import Mail, Message
mail = Mail(app)

from sktimeline.models import User
import sktimeline.views





if __name__ == "__main__":
    app.run()
