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
    if not signed_in():
        return redirect(url_for('signin', next='/'))

    posts = dbmodels.Post.query.all()


    return render_template('index.html', posts=posts)


@app.route("/process-post/", methods=['POST', 'GET'])
def post():
    if not signed_in():
        return redirect(url_for('signin', next='/'))

    post = request.form['post']

    try:

        post = dbmodels.Post(post=post)

        dbmodels.db.session.add(post)
        dbmodels.db.session.commit()

    except Exception as e:

        error = "Failed to post {}".format(e.__cause__)
        return render_template('index.html', information=error, css="is-danger")

    information = "Post successful"
    return redirect(url_for('home', information=information, css="is-success"))


@app.route("/edit/<int:id>/")
def edit(id):

    # check db for the post

    posts = dbmodels.Post.query.filter_by(id=id).first()

    # send post to edit form
    return render_template('index.html', post=post)


@app.route("/process-edit/<int:id>/", methods=['POST', 'GET'])
def process_edit(id):
    if not signed_in():
        return redirect(url_for('signin', next='/'))

    posts = request.form['posts']

    # update db

    try:
        # get the existing data from db object

        Post = dbmodels.Post.query.filter_by(id=id).first()

        # update fields
        Post.post = posts

        dbmodels.db.session.commit()

    except Exception as e:
        error = "Failed to update"

        return redirect(url_for('home', information=error, css="is-danger"))

    return redirect(url_for('home', information="Success", css="is-success"))


@app.route("/delete/<int:id>/", methods=['POST', 'GET'])
def delete(id):
    if not signed_in():
        return redirect(url_for('signin', next='/'))

    # update database
    if session['username'] == 'seyiodediran':
        try:

            # get data from the database object
            post = dbmodels.Post.query.filter_by(id=id).first()

            # delete the record
            dbmodels.db.session.delete(post)

            dbmodels.db.session.commit()

        except Exception as e:
            error = "Failed to delete"
            return render_template("index.html", information=error, css="is-danger")

        return redirect(url_for("home", information="Successfully deleted", css="is-success"))
    else:
        return redirect(url_for('home'))


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
    app.run(port=3459)