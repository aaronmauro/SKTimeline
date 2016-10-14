from sktimeline import tweepy_API, app
from . import login_required
import json


@app.route('/admin/twitter_api_status')
@login_required
def admin_twitter_api_status():
    rate_limit_status = tweepy_API.rate_limit_status()
    return render_template("admin/twitter_api_status.html", rate_limit_status = rate_limit_status)
