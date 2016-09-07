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



### About [`pip-tools`](https://github.com/nvie/pip-tools#readme) for package management ##
I've setup this project to use the `requirements.in` file to manage all packages that is needed for development.  

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
