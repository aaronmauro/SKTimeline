Instructions for supervisor configuration.

On the test server, we use supervisord to run the background task that does the downloading of feed items.

To install supervisor run `apt-get install supervisor`.

Then copy or symlink this configuration to the systems supervisor configuration 

`ln -s supervisor/sktimeline_scheduler.conf /etc/supervisor/conf.d/sktimeline_scheduler.conf`

OR 

`cp supervisor/sktimeline_scheduler.conf  /etc/supervisor/conf.d/sktimeline_scheduler.conf`

Then restart the supervisor daemon by running `service supervisor restart`


