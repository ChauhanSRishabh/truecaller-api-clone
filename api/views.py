from ast import Return
from api import app, db
from flask import request, jsonify
from api.models import User, Contact
import random
import re


# creates tables in our database
@app.before_first_request
def create_tables():
    db.create_all()

"""
VERY IMPORTANT

When we login after register, we are shown an authorization token.
We need to pass this token for all our requests while we are logged in.

How to pass:
We give the auth_token through the Headers in Postman before sending any request for any Endpoint
Choose request method -> enter URL -> choose Headers
Inside Headers, choose Key:"Authorization" and Value:"auth_token" that was displayed when you logged in
Hit Send
"""
# Function to check for valid email
regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
def isValidEmail(email):
    if re.fullmatch(regex, email):
      return True
    else:
      return False

# Function to check for valid phone number
def isValidNumber(ph_no):
    if re.fullmatch('[6-9][0-9]{9}',ph_no):
      return True
    else:
      return False


# this function validates whether user is logged in or not
# all our endpoints use this function to verify if user is logged in or not
def validateUser():
    s = request.headers.get('Authorization')
    user = User.query.filter(User.auth_token==s).first()
    if not user or s is None:
        return False
    else:
        return True


@app.route('/')
def home():
    if validateUser():
        return jsonify({'Message' : 'You are already logged in'})
    else:
        return jsonify({'Message' : 'Unauthorized User. Go /login, /register'})

# Endpoint for Registering new user
@app.route('/register', methods=['POST'])
def register():
    try:
        username=request.json['username']
        password=request.json['password']
        name=request.json['name']
        phone=request.json['phone']
        email=request.json['email']
    except:
        return jsonify({'Status': 400, 'Message': 'Bad Request'})

    if isValidNumber(phone) and not isValidEmail(email):
        return jsonify({'Message': 'Please enter a valid E-mail Id'})
    elif isValidEmail(email) and not isValidNumber(phone):
        return jsonify({'Message': 'Please enter a valid Phone Number'})
    elif not isValidEmail(email) and not isValidNumber(phone):
        return jsonify({'Message': 'Both Email Id and Phone number entered are wrong'})
    else:
        user = User(username=username, password=password, name=name, phone=phone, email=email)
        try:
            db.session.add(user)
            db.session.commit()
            return jsonify({'Status': 200, 'Message': 'User details successfully added', 'Now' : 'go to /login'})
        except :
            return jsonify({"Status": 400,
                        "Message": "Failed to register User.This may occur due to duplicate entry of username or phone number"})


# Endpoint for Login
@app.route('/login', methods=['POST'])
def login():
    try:
        username = request.json['username']
        password = request.json['password']
    except:
        return jsonify({'Status': 400, 'Message': 'Bad Request'})

    if username and password:
        #check if user exists 
        user = User.query.filter_by(username=username).first()
        user.auth_token = ''.join((random.choice(user.username)) for x in range(10))  # Generate authorization token for the user. It is random and unique for each login
        db.session.add(user) 
        db.session.commit()
        return jsonify({'Message' : 'You are logged in successfully', 'Authorization Token' : user.auth_token, 'Go to /addcontacts' : "To add/sync your contacts" }) # show auth_token to the user so that he can remember/save it. This token needs to be passed for each Request method(be it GET, PATCH, POST) for all the endpoints defined below
    else:
        return jsonify({'Error' : 'Invalid username or password'})

# Endpoint to Add Contacts
@app.route('/addcontacts', methods=['POST'])
def addContacts():  
    if validateUser():
        s =  request.headers.get('Authorization')
        user = User.query.filter(User.auth_token==s).first()
        
        # contactInfo is a dictionary of contact(s) passed by the user 
        contact_info = request.json['contactInfo']
    
        if contact_info:
            for value in contact_info.values(): # We are only interested in the value field of our dictionary
                name = value['name']
                phone_number = value['phone_number']
                is_spam = value['is_spam']
                user_id = user.id
                contact = Contact(user_id=user_id,
                            name=name,
                            phone_number=phone_number,
                            is_spam = is_spam)
                db.session.add(contact)
                db.session.commit()
            return jsonify({'Message' : 'Contact details added successfully'})
        else:
            return jsonify({'Error' : 'Bad Request', "Status": 400})
    else:
        return jsonify({'Message' : 'You need to be logged in to add contacts', "Status": 401})

    
# Endpoint to Search by name
@app.route('/contacts/searchbyname/<contact_name>', methods=['GET'])
def search_by_name(contact_name):
    if validateUser():
        if not contact_name:
            return jsonify({"Message": "Bad request", "Status": 400})
        contact = Contact.query.filter_by(name=contact_name).first()
        return jsonify({"Name" : contact.name, "Phone Number" : contact.phone_number, "Spam Status" : contact.is_spam})
    else:
        return jsonify({'Message' : 'You are not logged in'})

'''
This end-point will have two functions depending on the parameters we send with it. 

(1) Search by contact number
Request Method = GET
Request URL would be : 'http://127.0.0.1:5000/contacts/<contact_number>'

(2) Update the spam Status for a given contact number
Request Method = PATCH
Request URL would be : 'http://127.0.0.1:5000/contacts/<contact_number>?Status=yes'
'''
@app.route('/contacts/<contact_number>', methods=['GET', 'PATCH'])
def search(contact_number):
    if validateUser():
        if isValidNumber(contact_number):
            if request.method == 'GET':
                user = User.query.filter_by(phone=contact_number).first()

                if user:
                    contact = Contact.query.filter_by(phone_number=contact_number).first()
                    return jsonify({"Message" : "User with this contact number is registered with us", "Name" : user.name,  "Phone Number" : user.phone, "Spam Status" : contact.is_spam, "Email Id" : user.email})
                else:
                    contacts = Contact.query.filter_by(phone_number=contact_number).all()
                    output = []
                    for contact in contacts:
                        contact_data  = {"id" : contact.id, "Name" : contact.name, "Phone Number" : contact.phone_number,   "Spam Status" : contact.is_spam}
                        output.append(contact_data)
                    return jsonify({"Message":"Not a Registered User", "Contacts" : output})

            elif request.method == 'PATCH':
                status = None
                try:
                    status = request.args.get('status')
                except:
                    return jsonify({"Message":"Wrong Parameters"})
                contacts = Contact.query.filter_by(phone_number=contact_number).all()
                output = []
                for contact in contacts:
                    contact.is_spam = status
                    db.session.add(contact)
                    db.session.commit()
                    new_contact_data  = {"id" : contact.id, "Name" : contact.name, "Number" : contact.phone_number, "Spam" : contact.is_spam}
                    output.append(new_contact_data)
                return jsonify({"Spam Status" : "Spam Status was changed for the mentioned number", "contacts affected" :   output})

            else:
                return jsonify({"Message" : "Bad Request"})
        else:
            return jsonify({"Error": "You entered the wrong number"})
    else:
        return jsonify({'Message' : 'You are not logged in', "Status": 401})

@app.route('/logout')
def logout():
    if validateUser():
        s =  (request.headers.get('Authorization'))
        user = User.query.filter(User.auth_token==s).first()
        user.auth_token = None # we set auth_token as None when we logout. So now if we pass the same auth_token that we had earlier, our validateUser() function returns false and we know user isn't logged in
        db.session.add(user)
        db.session.commit()
        return jsonify({'Message' : 'You successfully logged out'})
    else:
        return jsonify({'Message' : 'You are not logged in', "Status": 401})