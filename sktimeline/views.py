
from sktimeline import *

#Content() is defined in content_management.py
from content_management import Content


#Homepage
@app.route('/')
def homepage():
    return render_template("main.html")

#Terms of Service Page
@app.route('/tos/')
def tos():
    return render_template("tos.html")


#Login Required Flash Warning
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("Please login")
            return redirect(url_for('login_page'))
    return wrap

#Dashboard
@app.route('/dashboard/')
@login_required
def dashboard():
    twitter_settings = TwitterFeedSetting.belonging_to_user(session['user_id'])
    #TODO: maybe user object and ORM methods - depends on where other settings going
    return render_template("dashboard.html", TOPIC_DICT = Content(), twitter_settings = twitter_settings  )



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
    #todo: if id present check user is allowed to edit this item
    form = TwitterForm(request.form, model)

    if request.method == 'POST' and form.validate():
        form.populate_obj(model)
        db.session.commit()
        db.session.close()
        flash("Twitter entry updated.")
        return redirect(url_for("dashboard"))

    return render_template("dashboard/twitter.html", form = form)


#Error Handling
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")


@app.errorhandler(500)
def page_not_found(e):
    return ("Internal Server Error"), 500

#Sitemap for SEO
@app.route('/sitemap.xml', methods=['GET'])
def sitemap():
    try:
#Generate sitemap.xml. Makes a list of urls and date modified.
        pages=[]
        ten_days_ago=(datetime.now() - timedelta(days=7)).date().isoformat()
#static pages
        for rule in app.url_map.iter_rules():
            if "GET" in rule.methods and len(rule.arguments)==0:
                pages.append(["http://162.243.121.195/"+str(rule.rule),ten_days_ago])
        sitemap_xml = render_template('sitemap_template.xml', pages=pages)
        response= make_response(sitemap_xml)
        response.headers["Content-Type"] = "application/xml"

        return response
    except Exception as e:
        return(str(e))

#Logout Notice Flash Warning
@app.route("/logout/")
@login_required
def logout():
    session.clear()
    flash("You are logged out!")
    gc.collect()
    return redirect(url_for('homepage'))

#Login Page
@app.route('/login/', methods=["GET","POST"])
def login_page():

    error = ''
    try:
        if request.method == "POST":
            user = User.load_by_username(request.form['username'])
            if user and user.password_is_correct(request.form['password']):
                session['logged_in'] = True
                session['username'] = user.username
                session['user_id'] = user.uid

                flash("You are now logged in!")
                return redirect(url_for("dashboard"))
            else:
                error = "Invalid creditials, try again."

            gc.collect()
            return render_template(login.html, error=error)

        return render_template("login.html", error = error)

    except Exception as e:
        #flash(e)
        error = "Invalid credentials, try again."
        return render_template("login.html", error = error)


#Registration Form Class
class RegistrationForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=20)])
    email = TextField('Email Address', [validators.Length(min=6, max=50)])
    password = PasswordField('New Password', [validators.Required(), validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the <a href="/tos/" target="_blank">Terms of Service and Privacy Notice</a>', [validators.Required()])

#Registration Page
@app.route('/register/', methods=["GET","POST"])
def register_page():
    try:
        form = RegistrationForm(request.form)

        if request.method == "POST" and form.validate():
            username = form.username.data
            email = form.email.data
            password = form.password.data

            new_user = User(username, password, email)

            if User.username_exists(username):
                flash("Username already in use. Please choose another.")
                return render_template('register.html', form=form)
            else:
                # insert user here
                #todo: readd the tracking
                db.session.add(new_user)
                db.session.commit()
                db.session.close()
# /homepage/ is where the user will be sent after a failed registration. You could forward to an intro to site functionality too.
                flash("Thanks for registering! Confirmation email sent.")


                gc.collect() #garbage collection to reduce memory use.

                session['logged_in'] = True
                session['username'] = username
                msg = Message("Thanks for Registering!", sender="baaronmauro@gmail.com", recipients=[email])
                msg.body = "Hi there, "+username+"!\nThis system is still in active development. By registering, you'll recieve notifications about availability and new functionality!\n Thanks for your interest in SKTimeline,\nAaron"
                mail.send(msg)
                return redirect(url_for('dashboard'))
                #this will redirect to dashboard page to begin use.

        return render_template("register.html", form=form)

    except Exception as e:
        return(str(e))
        #Error is here for debugging process. Remove once project is completed.

#Contact Form Class ..Not in Use.. The main page uses a mailto in HTML.
class ContactForm(Form):
	firstName = TextField('First Name', [validators.DataRequired("Enter your first name")])
	lastName = TextField('Last Name', [validators.DataRequired("Enter your last name")])
	email = TextField('E-mail', [validators.DataRequired("Enter a valid email address")])
	subject = TextField('Subject', [validators.DataRequired("What's the nature of your message?")])
	message = TextAreaField('Message', [validators.DataRequired("Didn't you want to say something?")])
	submit = SubmitField('Send')

@app.route('/contact/', methods=('GET', 'POST'))
def contact():
	form = ContactForm()
	if request.method == 'POST':
		if form.validate() == False:
			flash('You must enter something into all of the fields')
			return render_template('contact.html', form = form)
		else:
			msg = Message(form.subject.data, sender='[SENDER EMAIL]', recipients=['[RECIPIENT EMAIL]'])
			msg.body = """
			From: %s %s <%s>
			%s
			""" % (form.firstName.data, form.lastName.data, form.email.data, form.message.data)
			mail.send(msg)
			return render_template('contact.html', success=True)
	elif request.method == 'GET':
		return render_template('contact.html',
			title = 'Contact Us',
			form = form)
