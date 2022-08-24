from api import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(10), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True)
    auth_token = db.Column(db.String(10), unique=True)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    name = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(10), nullable=False) # phone number taken as a string as it helps with implementation of 're' module inside isValidNumber() function
    is_spam = db.Column(db.String(10))