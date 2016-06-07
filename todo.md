# To Do List
----
<p>This todo list is intended for the development team at Penn State's TLT Brad Kozlek, Nick Rossi, and Jared Wenerd. We'll be using this page to monitor and assess tasks in the development of the SKTimeline. For anyone observing the development of the project, this page might serve as a guide to our development and future directions. So, without further ado...</p>

- [X] Make todo list. 


## Overview

##### The goal of the next few months of development will be to use the Python API wrappers to draw data from Twitter, Slack, and Github into a unified JSON file. The JSON file must be compatible with the [TimelineJS](https://timeline.knightlab.com) format available [here](https://timeline.knightlab.com/docs/json-format.html). Once we are drawing data down in real time and updating each users JSON file, we will need to build an <iframe> generator that will render the timeline for each user outside the platform.  The [Github page for TimelineJS](https://github.com/NUKnightLab/TimelineJS3) provides all the code and examples needed for this.

##### As you can already tell, this is a Python3 project. We are using Python for a couple of reasons. It allows for a seamless linking between these services and it makes handling JSON much easier. [Python's JSON module](https://docs.python.org/3.5/library/json.html) makes JSON into Python lists and dictionaries, making the transition pretty simple.

##### If you haven't done so, go back to the development server and log into the system. You'll see some of the functionality of the site and a sample timeline on the Dashboard.

##### Our first task will be to draw data from these services:

## Twitter 

##### [Tweepy](http://tweepy.readthedocs.io/en/v3.5.0/) currently offers the best support for the Twitter APIs. It supports OAuth and streaming, which is something we'll need. The Hello World for Tweepy goes something like this:

''' 
import tweepy

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

public_tweets = api.home_timeline()
for tweet in public_tweets:
    print tweet.text
'''

##### We'll need to add support for hashtags and user handles as well. 

##### Then we'll need to package this up into TimelineJS JSON format. TimelineJS does a nice job formatting Tweets, so we'll want to preserve this functionality in our version. 

## Slack

##### Slack should be similarly straight forward. The goal is to draw down Slack messages by channel and group. We will then reformat Slack messages to be included in the timeline. We may have to develop some basic logic for how to split or shorten messages here. There are two API modules for Slack: [Slacker](https://github.com/os/slacker) and [Slackclient](https://github.com/slackhq/python-slackclient). I'm frankly not sure which one is the best choice here, but I think Slacker is slightly more popular and will likely have more support and examples. 

## Github

##### Github has several wrappers for the its API. The [GitPython](https://github.com/gitpython-developers/GitPython) module seems to be the best, but there are [PyGithub](https://github.com/PyGithub/PyGithub) or [PyGithub3](http://pygithub3.readthedocs.io/en/latest/). There may even be a simpler way to do this with [urllib](https://docs.python.org/3/howto/urllib2.html).

##### We are interested in collecting Commit Messages, Usernames, Dates, and Times. These will be formatted much like the Slack messages, but we'll have explicit links to a moment in the project's development through version control. 

## Merging

##### We'll need to have a mechanism for merging these sources as they come in. The Crontab function in Flask will allow us to handle some of this, but there might be a better solution. 
