from sktimeline import *
from sktimeline.views import login_required, page_not_found




def hashtag_validator(form, field):
    if field.data[0] != '#':
        raise validators.ValidationError('Must start with #')
    if len(field.data.split()) > 1:
        raise validators.ValidationError('Enter only one hashtag')

TwitterForm = model_form(TwitterFeedSetting, Form, exclude=['user','status','last_updated','feed_items'], field_args = {
   'hashtag' : {
        'validators' : [validators.Required(), hashtag_validator]
    }
})

@app.route('/dashboard/twitter/new',methods=['GET','POST'])
@login_required
def dashboard_twitter_new(id=None):
    model = TwitterFeedSetting()
    #todo: if id present check user is allowed to edit this item
    form = TwitterForm(request.form, model)
    model.user = User.query.get(session['user_id'])

    if request.method == 'POST' and form.validate():
        form.populate_obj(model)
        model.status = 'new'
        db.session.add(model)
        db.session.commit()
        db.session.close()

        flash("Twitter entry added.")
        return redirect(url_for("dashboard"))

    return render_template("dashboard/twitter.html", form = form)

@app.route('/dashboard/twitter/delete/<id>',methods=['POST'])
@login_required
def dashboard_twitter_delete(id):
    model = TwitterFeedSetting.query.get(id)
    if not(model) or model.user_id != session['user_id']:
        return page_not_found()

    db.session.delete(model)
    db.session.commit()
    db.session.close()

    flash('Twitter hashtag deleted!')
    return redirect( url_for("dashboard") + '#twitter')
