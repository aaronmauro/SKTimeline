from sktimeline import *
from sktimeline.views import login_required, page_not_found
from wtforms import validators, SelectField
import urllib
from slackclient import SlackClient


@app.route('/dashboard/slack/start_auth',methods=['POST'])
@login_required
def dashboard_slack_start_auth(id=None):
    if 'slack_auth_info' in session:
        del session['slack_auth_info']

    # this kicks off the authorization flow between the app and flasks
    params = urllib.urlencode({
        'client_id': app.config['SLACK_CLIENT_ID'],
        'scope': 'channels:read,channels:history,users:read',
        'redirect_uri': url_for('slack_auth_callback', _external=True),
    })
    auth_url = "https://slack.com/oauth/authorize?%s" % params
    return redirect( auth_url )


@app.route('/slack_auth/callback',methods=['GET','POST'])
# this is the route that must be configured on the slack app dashboard at https://api.slack.com/
# where one must also input the SLACK_CLIENT_ID and SLACK_CLIENT_SECRET in the instance/config.py
@login_required
def slack_auth_callback():
    code = request.args.get('code')
    if code:
        sc = SlackClient('')
        auth_info = sc.api_call('oauth.access',client_id = app.config['SLACK_CLIENT_ID'], client_secret= app.config['SLACK_CLIENT_SECRET'], code=code, redirect_uri=url_for('slack_auth_callback', _external=True))
        if ( auth_info['ok'] ):
            session['slack_auth_info'] = auth_info
            # store the token, forward to page to get which channel/channels to use
            return redirect(url_for("dashboard_slack_add"))
        else:
            raise Exception('Something went wrong! Error from Slack API:' + auth_info['error'])
    else:
        raise Exception('Something went wrong! Slack code not present.')
    return ''

class SlackChannelSelectForm(Form):
    channel = SelectField(u'Channel',[ validators.required() ] )

@app.route('/dashboard/slack/add',methods=['GET','POST'])
@login_required
def dashboard_slack_add():
    if not('slack_auth_info' in session):
        flash("There was an error authorizing Slack.")
        return redirect(url_for("dashboard"))
    #
    form = SlackChannelSelectForm(request.form)
    sc = SlackClient( session['slack_auth_info']['access_token'] )

    if request.method == 'GET' or (request.method == 'POST' and not(form.channel.data) ):
        channel_response = sc.api_call('channels.list', exclude_archived=1)
        channels = channel_response['channels']
        # todo: this should throw an error here if no channels available
        form.channel.choices = [ (c['id'], c['name']) for c in channel_response['channels']]
        return render_template("dashboard/slack.html", form = form )

    elif request.method == 'POST':
        model = SlackFeedSetting()

        model.status = 'new'
        model.user_id = session['user_id']
        model.slack_auth_info = session['slack_auth_info']


        channel_id = form.channel.data
        channel_info = sc.api_call('channels.info', channel=channel_id)
        if channel_info['ok']:
            channel_info = channel_info['channel']

        model.channel_id = channel_id
        model.channel_info = channel_info

        db.session.add(model)
        db.session.commit()
        db.session.close()
        del session['slack_auth_info']

        flash('Slack channel added!')
        return redirect(url_for("dashboard") + '#slack')


@app.route('/dashboard/slack/delete/<id>',methods=['POST'])
@login_required
def dashboard_slack_delete(id):
    model = SlackFeedSetting.query.get(id)
    if not(model) or model.user_id != session['user_id']:
        return page_not_found()

    db.session.delete(model)
    db.session.commit()
    db.session.close()

    flash('Slack channel deleted!')
    return redirect(url_for("dashboard") + '#slack')
