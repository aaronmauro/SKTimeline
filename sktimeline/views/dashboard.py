from sktimeline import *
from . import login_required


#Dashboard
@app.route('/dashboard/')
@login_required
def dashboard():
    twitter_settings = TwitterFeedSetting.belonging_to_user(session['user_id'])
    slack_settings = SlackFeedSetting.belonging_to_user(session['user_id'])
    github_settings = GithubFeedSetting.belonging_to_user(session['user_id'])
    #TODO: maybe user object and ORM methods - depends on where other settings going
    return render_template("dashboard.html", twitter_settings = twitter_settings,
                                             slack_settings = slack_settings,
                                             github_settings = github_settings)




TwitterForm = model_form(TwitterFeedSetting, Form, exclude=['user'], field_args = {
 #todo add basic validation
})

@app.route('/dashboard/twitter/new',methods=['GET','POST'])
@login_required
def dashboard_twitter_new(id=None):
    model = TwitterFeedSetting()
    #todo: if id present check user is allowed to edit this item
    form = TwitterForm(request.form, model)


    if request.method == 'POST' and form.validate():
        form.populate_obj(model)
        model.user = User.query.get(session['user_id'])
        db.session.add(model)
        db.session.commit()
        db.session.close()

        flash("Twitter entry added.")
        return redirect(url_for("dashboard"))

    return render_template("dashboard/twitter.html", form = form)


@app.route('/dashboard/twitter/edit/<id>',methods=['GET','POST'])
@login_required
def dashboard_twitter_edit(id):
    model = TwitterFeedSetting.query.get(id)
    if not(model) or model.user_id != session['user_id']:
        return page_not_found()

    form = TwitterForm(request.form, model)

    if request.method == 'POST' and request.form.has_key('delete'):
        db.session.delete(model)
        db.session.commit()
        db.session.close()
        flash("Twitter entry deleted.")
        return redirect(url_for("dashboard"))

    elif request.method == 'POST' and form.validate():
        form.populate_obj(model)
        db.session.commit()
        db.session.close()
        flash("Twitter entry updated.")
        return redirect(url_for("dashboard"))

    return render_template("dashboard/twitter.html", form = form, edit = True)


SlackForm = model_form(SlackFeedSetting, Form, exclude=['user'], field_args = {
 #todo add basic validation
})

@app.route('/dashboard/slack/new',methods=['GET','POST'])
@login_required
def dashboard_slack_new(id=None):
    model = SlackFeedSetting()
    #todo: if id present check user is allowed to edit this item
    form = SlackForm(request.form, model)


    if request.method == 'POST' and form.validate():
        form.populate_obj(model)
        model.user = User.query.get(session['user_id'])
        db.session.add(model)
        db.session.commit()
        db.session.close()

        flash("Slack entry added.")
        return redirect(url_for("dashboard"))

    return render_template("dashboard/slack.html", form = form)


@app.route('/dashboard/slack/edit/<id>',methods=['GET','POST'])
@login_required
def dashboard_slack_edit(id):
    model = SlackFeedSetting.query.get(id)
    if not(model) or model.user_id != session['user_id']:
        return page_not_found()

    form = SlackForm(request.form, model)

    if request.method == 'POST' and request.form.has_key('delete'):
        db.session.delete(model)
        db.session.commit()
        db.session.close()
        flash("Slack entry deleted.")
        return redirect(url_for("dashboard"))

    elif request.method == 'POST' and form.validate():
        form.populate_obj(model)
        db.session.commit()
        db.session.close()
        flash("Slack entry updated.")
        return redirect(url_for("dashboard"))

    return render_template("dashboard/slack.html", form = form, edit = True)



GithubForm = model_form(GithubFeedSetting, Form, exclude=['user'], field_args = {
 #todo add basic validation
})

@app.route('/dashboard/github/new',methods=['GET','POST'])
@login_required
def dashboard_github_new(id=None):
    model = GithubFeedSetting()
    #todo: if id present check user is allowed to edit this item
    form = GithubForm(request.form, model)


    if request.method == 'POST' and form.validate():
        form.populate_obj(model)
        model.user = User.query.get(session['user_id'])
        db.session.add(model)
        db.session.commit()
        db.session.close()

        flash("GitHub entry added.")
        return redirect(url_for("dashboard"))

    return render_template("dashboard/github.html", form = form)


@app.route('/dashboard/github/edit/<id>',methods=['GET','POST'])
@login_required
def dashboard_github_edit(id):
    model = GithubFeedSetting.query.get(id)
    if not(model) or model.user_id != session['user_id']:
        return page_not_found()

    form = GithubForm(request.form, model)

    if request.method == 'POST' and request.form.has_key('delete'):
        db.session.delete(model)
        db.session.commit()
        db.session.close()
        flash("Github entry deleted.")
        return redirect(url_for("dashboard"))

    elif request.method == 'POST' and form.validate():
        form.populate_obj(model)
        db.session.commit()
        db.session.close()
        flash("GitHub entry updated.")
        return redirect(url_for("dashboard"))

    return render_template("dashboard/github.html", form = form, edit = True)
