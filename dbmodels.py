from app import db
from werkzeug.security import generate_password_hash, check_password_hash


class Users(db.Model):
    __tablename__ = 'userreg'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=False, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(256), unique=False, nullable=False)

    def __repr__(self):
        return "<Register{}>".format(self.id)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    post = db.Column(db.Text, unique=False, nullable=False)

    def __repr__(self):
        return "<Post {}>".format(self.id)
