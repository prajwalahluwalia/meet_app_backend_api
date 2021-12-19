from datetime import datetime
from flask import Flask, render_template, flash, redirect, url_for, session
from flask_restful import Api
from flask_jwt import JWT
from resources.users import UserRegister, UserMeetCount, UserMeeting, UserMeetTime
from resources.meetings import Meeting, MeetingsList
from forms import LoginForm, MeetigForm, RegisterForm
from models.users import UserModel
from models.meetings import MeetingModel
from resources.meetings import Meeting
from flask_bootstrap import Bootstrap
from flask_datepicker import datepicker


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'secret_key@321'

api = Api(app)
Bootstrap(app)
datepicker(app)

@app.route("/")
def index():
    return render_template("welcome.html")

@app.route("/login", methods=['GET','POST'])
def login():
    if session.get('username'):
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = UserModel.find_by_username(username=username).first()
        if user and user.get_password(password):
            flash(f"{user.first_name}, you are successfully logged in!", "success")
            session['username'] = user.username
            return redirect("/index")
        else:
            flash("Sorry, something went wrong.","danger")
    return render_template("login.html", title="Login", form=form, login=True )

@app.route("/logout")
def logout():
    session['user_id']=False
    session.pop('username',None)
    return redirect(url_for('index'))

@app.route("/register", methods=['GET','POST'])
def register():
    if session.get('username'):
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        
        first_name = form.first_name.data
        last_name = form.last_name.data
        username = form.username.data
        email = form.email.data
        password = form.password.data


        user = UserModel(first_name=first_name, last_name=last_name, username = username, email = email)
        user.set_password(password)
        user.save_to_db()
        flash("You are successfully registered!","success")
        return redirect(url_for('index'))
    return render_template("register.html", title="Register", form=form, register=True)

@app.route("/create_meet", methods=["GET","POST"])
def create_meet():
    form = MeetigForm()
    if form.validate_on_submit():
        
        y, m, d = form.scheduled_on.data.split('/')
        h1, m1, s1 = form.start_time.data.split(":")
        h2, m2, s2 = form.end_time.data.split(":")
        subject = form.subject.data
        attendes = form.attendes.data

        scheduled_on = datetime.date(int(y), int(m), int(d))
        start_time = datetime.time(int(h1), int(m1), int(s1))
        end_time = datetime.timr(int(h2), int(m2), int(s2))

        meet = MeetingModel(scheduled_on = scheduled_on, start_time = start_time, end_time = end_time, total_time = (datetime.strptime(end_time)-datetime.strptime(end_time)).total_seconds()//60, subject = subject, attendes = attendes)
        meet.save_to_db()
        flash("Meeting successfully scheduled!","success")
        return redirect(url_for('index'))
    return render_template("create_meet.html", title="Create Meet", form=form, register=True)    

@app.route("/meetings<int:id>/delete")
def delete():
    MeetingModel.delete_from_db()
    return render_template("meetings_created.html")

@app.route("/meetings/<int:id>/edit")
def edit(scheduled_on, start_time, end_time, subject):
    Meeting.put(scheduled_on = scheduled_on, start_time = start_time, end_time = end_time, subject = subject)
    return render_template("meetings_created.html")


##########################################################

api.add_resource(UserRegister, '/register')
api.add_resource(UserMeetTime,'/users/<int:id>/time')
api.add_resource(UserMeetCount,'/users/<int:id>/count')
api.add_resource(UserMeeting, '/users/<int:id>/meets')
api.add_resource(Meeting, '/meetings/<int:id>')
api.add_resource(MeetingsList, '/meetings')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)