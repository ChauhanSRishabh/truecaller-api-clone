from flask import Flask, jsonify, request, session
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'the random string'    
db = SQLAlchemy(app)

from api import views

if __name__=='__main__':
    app.run(debug=True)