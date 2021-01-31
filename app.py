import dbmodels
from flask import Flask, render_template, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5435/viewdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = b'g\x0b\xaa\xaf0\xd6\n\x88\x1aI9o\x7f\xa5\n\xa4%Ek\xc5\x93\xa6\xa6\n'

db = SQLAlchemy(app)


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/signin/")
def signin():
    session['next_url'] = request.args.get('next', '/')
    return render_template('signin.html', information="Please complete the form", css="normal")


@app.route("/process-signin/", methods=['POST'])
def process_signin():
    username = request.form['username']
    password = request.form['password']

    if authentication(username, password):

        session["username"] = username

        if username == "seyiodediran":
            session["userroles"] = ['admin']
        else:
            session['userroles'] = ['user']

        return redirect(session['next_url'])
    else:

        error = "Invalid user or password"
        return render_template("signin.html", information=error, css="is-danger")


def authentication(username, password):

    user = dbmodels.Users.query.filter_by(username=username).first()

    if user and user.check_password(password):
        return True
    else:
        return False


@app.route("/signup/")
def signup():
    return render_template('signup.html', information='Please complete the form')


@app.route("/process-signup/", methods=['POST'])
def process_signup():

        name = request.form['name']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # write to database
        try:

            user = dbmodels.Users(name=name, username=username, email=email, password=password)
            user.set_password(password)

            db.session.add(user)
            db.session.commit()

        except Exception as e:
            error = "There was an error in the sign up process. The error is {}".format(e.__cause__)
            return render_template('signup.html', information=error, css="is-danger")

        return render_template('signup.html', information="Sign up was successful", css="is-success")


def signed_in():
    if 'username' not in session:
        return False
    else:
        return True


@app.route("/logout/")
def logout():
    # pop out the username and the roles
    session.pop("username")
    session.pop("userroles")

    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run()