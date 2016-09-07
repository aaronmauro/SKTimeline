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

# OS X Development Setup Instructions

If not yet done so, install python verion 2.7 & virtualenv.  

```
brew install python
pip install virtualenv
```
_Note: If you receive an error that the command `brew` is not found, you must install [Homebrew](http://brew.sh/) first._


Clone this repository, change directories to project working directory, then setup and activate the virtual enviroment:

```
git clone REPOSITORY_URL_GOES_HERE
cd SKTimeline
virtualenv --no-site-packages .
source bin/activate
```

Downgrade to pip v8.1.1 and install pip-tools:
_(note: this is currently needed for pip-tools as used to manage packages)_

```
bin/pip install --upgrade pip==8.1.1
bin/pip install pip-tools
```
Install needed project packages from requirements.txt in the virtualenv via pip-sync:

```
bin/pip-sync
```

## Configuration Setup for Development

Install MySQL Server if not already on your machine.

```
brew install mysql
```

Confirm the MySQL server started by running:

```
brew services start mysql
```

Connect to MySQL server to setup a new database for the application.

```
mysql --user=root 
```
_Note: MySQL installs without a root password by default, if using another development setup, you may need to enter a password here or find a way to setup_

Create the sktimeline database on my MySQL shell with the command `CREATE DATABASE sktimeline;`

```
mysql> CREATE DATABASE sktimeline;
Query OK, 1 row affected (0.01 sec)
```

At this point the application can create the needed database schema via SQLAlchemy.  First we must tell the local instance how to connect to the database in the local config.

Copy the `config.py` file into `instance/config.py`. The `instance/config.py` file is ignored by version control, so all local application instance which shouldn't be made public (database settings, API keys, etc) should be placed in this file.

```
cp config.py instance/config.py
```

Modify the line `SQLALCHEMY_DATABASE_URI = 'mysql://user:password@localhost/dbname'` with your database settings.  For instance, if using the database name `sktimeline` with user  `root` and no password like database we created above it should read as following:

```
SQLALCHEMY_DATABASE_URI = 'mysql://root@localhost/sktimeline'
```

If you instance is using a different username, password, server address, or database, you must modify this database URI reflect this.  For more information see the [SQLAlchemy documentation](http://docs.sqlalchemy.org/en/latest/core/engines.html#database-urls)

Finally, we can create the database schema by running the following command.

```
bin/python migration.py setup_db
```

At this point the application server is ready to run!  

### Running the Instance


Now you should be able to retup the Flask application server

```
bin/python run.py
```

## Generating and Entering API Credentials 

In order to download the activity from GitHub, Twitter, & Slack, you must enter API credentials into `instance/config.py`.

### Twitter API Credentials

1. Go to [https://apps.twitter.com](https://apps.twitter.com) and login to your Twitter account
2. Press **Create New App**, enter a name, description, and website.  It is fine to use a placeholder value for the website URL like `http://127.0.0.1:5000/`.
3. Click on the tab **Keys and Access Tokens**
4. Click **Access Level** and change to "read only" _(this is so that if these credentials were ever stolen that they cannot make changes to your account and act on your behalf)_
5. Copy the **Consumer Key (API Key)** value and place in the `TWEEPY_CONSUMER_KEY` value of `instance/config.py`
6. Copy **Consumer Secret (API Secret)** and place in `TWEEPY_CONSUMER_SECRET` 
7. Press **Generate Access Token and Token Secret**
8. Copy **Access Token** and place in `TWEEPY_ACCESS_TOKEN_KEY`
9. Copy **Access Token Secret** and place in `TWEEPY_ACCESS_TOKEN_SECRET`

### GitHub API Credentials

These GitHub access tokens are used to use the [GitHub API over Basic Authentication](https://developer.github.com/v3/auth/#basic-authentication) in the PyGithub module.

1. Go login to your GitHub account, go to [https://github.com/settings/developers](https://github.com/settings/developers) and click **Register New Application**
2. Enter an Application Name and Homepage URL and press save.  _Note: It is fine to use a placeholder homepage URL like `http://127.0.0.1:5000/` since this will just be visible to you._
3. Copy the **Access Token** value and place in the `GITHUB_CLIENT_ID` value of `instance/config.py`
4. Copy **Client Secret** and place in `GITHUB_CLIENT_SECRET`


### Slack API Credentials
1. Go to [https://api.slack.com/apps](https://api.slack.com/apps), login to any Slack team with an account, and press "Create New App".
2. Fill in a app name, short & long description, select a team.
3. In the **Redirect URI(s)** field you must enter the OAuth callback URIs for where this app will be hosted.

 For local development this will likely be `http://127.0.0.1:5000/slack_auth/callback`
  
 For development on a remote web server you will need to enter `http://yourserveraddress/slack_auth/callback`
 
 _Note: this can be changed and added to in the future, so if you do not know all the places this will be hosted; it is fine to leave blank for now_
4. After submitting form, click the **OAuth and Permissions** menu item.
5. Copy the **Client ID** value and place in the `SLACK_CLIENT_ID` value of `instance/config.py`
6. Click **Show** under **Client Secret** then copy the value into `SLACK_CLIENT_SECRET`


Once these API credentials are present, you may need to restart the web server for these configuration values take effect.

## Development Notes

### About [`pip-tools`](https://github.com/nvie/pip-tools#readme) for package management ##
I've setup this project to use the `requirements.in` file to manage all python packages that are needed in the code.  

If a new package is needed, add it to the `requirements.in` file then run `bin/pip-compile`.  This generates the `requirements.txt` file which locks the package to a version.  

When upgrading a code change from the repo that requires a new package to be d, run `bin/pip-sync` which will install/upgrade/uninstall everything so that the virtualenv exactly matches what's in `requirements.txt` file.


###  Note about the styles custom styles in `assets/css/styles.css`
I've setup this file to be compiled using SASS and the the grunt task runner, so
these should not be edited directly and instead use the SCSS files in `assets/scss/`.

#### To use gulp for SCSS compilation

Install node/npm if not on your system if not already available `brew install node`

Install gulp and gulp-sass `npm install gulp && npm install gulp-sass --save-dev`

While developing, tell gulp to watch and compile the SCSS whenever it is changed
by running `gulp sass:watch`

Note: I recommend sending it into a background process by running `gulp sass:watch &`
