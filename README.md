# SKTimeline
### The missing link for teams working with collaboration platforms, social media, and version control.

##### A development version of this tool is available at the <a href="http://162.243.121.195">SKTimeline</a> site. Feel free to register an account and see a sample system in action. 

## Features

<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/2/2b/Slack_CMYK.svg/1000px-Slack_CMYK.svg.png" width="200"> 
##### Using Slack to organize teams is great! Wouldn't it be great to have a way to integrate these organic conversations into the history of your project? Use your team chatter to understand the chemistry responsible for your insights and innovations!

<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/2/29/GitHub_logo_2013.svg/2000px-GitHub_logo_2013.svg.png" width="200">
##### Github is one of the most common ways to maintain version control in large fast moving teams. Git commit tags can become more than just a quick note. Commits become part of your development narrative. It's a story told each and every step of the way!

<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/51/Twitter_logo.svg/2000px-Twitter_logo.svg.png" width="200">
##### Twitter does a lot of things. It can tell the world what you had for lunch, or it can inform your teams of trends and issues happening right now! Link hashtags and user handles directly into your development timeline.

## OS X Development Setup Instructions 

Install MySQL Server

`brew install mysql`

Install python verions 2.7

`brew install python`

Install virtualenv

`pip install virtualenv` 

Go to project application folder 

`cd FlaskApp/FlaskApp`

Activate the virtual enviroment

`virtualenv --no-site-packages .`

Activate the virtual enviroment:

`source bin/activate`

Install needed packages

`bin/pip install Flask MySQL-python wtforms flask_mail passlib`

Setup Flask enviroment

`export FLASK_APP=__init__.py`

Start development server

`bin/flask run` 

or alternatively run the Flask interactive console

`bin/flask  shell`


