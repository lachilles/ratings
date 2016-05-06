"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie,connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")

@app.route("/users")
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template("user_list.html", users=users)

@app.route("/user-profile/<int:user_id>")
def user_profile(user_id):
    """Shows user profile"""

    user = db.session.query(User).filter(User.user_id==user_id).first()    

    print user
    return render_template("profile.html", display_profile=user)

@app.route("/login-form", methods=["GET"])
def login_form():
    """User login"""
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login_process():
    """Process login"""

    email = request.form.get("email")
    pw = request.form.get("password")
    # error = None

    # Returns a single User object querying by email.
    user = db.session.query(User).filter(User.email==email).first()

    # input_email_pw = (request.args.get("inputEmail"), request.args.get("inputPassword"))

    # if user_email: 
    #     user_pw = db.session.query(User).filter(User.email==email, User.password==pw).one()
    #     flash('You were successfully logged in')
    #     return redirect("/")
    # else:
    #     error = 'Invalid credentials'
            
    # return render_template('login.html', error=error)

##Ask why rows 62-73 didn't work...
    # session["user_id"] = user.user_id

    # if user: 
    #     if pw == user.password:
    #         flash("Successfully logged in!")
    #         return redirect("/users/%s" % user.user_id)
    #     else:
    #         flash("Invalid login/password.")
    #         return  render_template("login.html")
    # elif user is None:
    #     flash("Please sign up for an account")
    #     return render_template("registration.html")

    if not user:
        flash("No such user")
        return redirect("/register")

    if user.password != pw:
        flash("Incorrect password")
        return redirect("/login")

    session["user_id"] = user.user_id

    flash("Logged in")
    return redirect("/users/%s" % user.user_id)

@app.route('/logout')
def logout():
    """Log out."""

    del session["user_id"]
    flash("Logged Out.")
    return redirect("/")


@app.route("/register", methods=["GET"])
def registration_form():
    """Register new user"""

    return render_template("registration.html")


@app.route('/register', methods=['POST'])
def register_process():
    """Process registration."""

    # Get form variables
    email = request.form["email"]
    password = request.form["password"]
    age = int(request.form["age"])
    zipcode = request.form["zipcode"]

    new_user = User(email=email, password=password, age=age, zipcode=zipcode)

    db.session.add(new_user)
    db.session.commit()

    flash("User %s added." % email)
    return redirect("/")


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
