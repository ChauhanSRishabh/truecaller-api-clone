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
    s =  (request.headers.get('Authorization'))
    user = User.query.filter(User.auth_token==s).first()
    if not user:
        return False
    else:
        return True


@app.route('/')
def home():
    if validateUser():
        return jsonify({'message' : 'You are already logged in'})
    else:
        return jsonify({'message' : 'Unauthorized User. Go /login, /register'})

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
        return jsonify({'status': 400, 'message': 'Bad Request'})

    if isValidNumber(phone) and not isValidEmail(email):
        return jsonify({'message': 'Please enter a valid E-mail Id'})
    elif isValidEmail(email) and not isValidNumber(phone):
        return jsonify({'message': 'Please enter a valid Phone Number'})
    elif not isValidEmail(email) and not isValidNumber(phone):
        return jsonify({'message': 'Email Id and Phone number entered are wrong'})
    else:
        user = User(username=username, password=password, name=name, phone=phone, email=email)
        try:
            db.session.add(user)
            db.session.commit()
            return jsonify({'status': 200, 'message': 'User details successfully added', 'Now' : 'go to /login'})
        except :
            return jsonify({"status": 400,
                        "message": "Failed to register User.This may occur due to duplicate entry of username or phone number"})


# Endpoint for Login
@app.route('/login', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']
    contact_info = request.json['contactInfo']

    if username and password and contact_info:
        #check user exists          
        user = User.query.filter_by(username=username).first()
        if user.username == username and user.password == password:
            user.auth_token = ''.join((random.choice(user.username)) for x in range(10))  # Generate authorization token for the user. It is random and unique for each login
            db.session.add(user) 
            db.session.commit() # add token to the table
            
            for key, value in contact_info.items():
                name = value['name']
                phone_number = value['phone_number']
                is_spam = value['is_spam']
                contact_id = str(user.id) + '_' + key 
                contact = Contact(id=contact_id,
                          name=name,
                          phone_number=phone_number,
                          is_spam = is_spam)
                db.session.add(contact)
                db.session.commit()

            return jsonify({'Message' : 'You are logged in successfully', 'Authorization Token' : user.auth_token, 'Success' : "Contact Details were synced" }) # show auth_token to the user so that he can remember/save it. This token needs to be passed for each Request method(be it GET, PUT, POST) for all the endpoints defined below
        else:
            return jsonify({'Error' : 'Invalid username or password'})

    else:
        return jsonify({'Error' : 'Bad Request'})

    
# Endpoint to Search by name
@app.route('/contacts/search/<contact_name>', methods=['GET'])
def search_by_name(contact_name):
    if validateUser():
        if not contact_name:
            return jsonify({"message": "Bad request", "status": 400})
        contact = Contact.query.filter_by(name=contact_name).first()
        return jsonify({"ID": contact.id, "name" : contact.name, "Phone Number" : contact.phone_number, "Spam Status" : contact.is_spam})
    else:
        return jsonify({'Message' : 'You are not logged in'})

'''
This end-point will have two functions depending on the parameters we send with it. 

(1) Search by contact number
Request Method = GET
Request URL would be : 'http://127.0.0.1:5000/contacts/<contact_number>'

(2) Update the spam status for a given contact number
Request Method = PUT
Request URL would be : 'http://127.0.0.1:5000/contacts/<contact_number>?status=yes'
'''
@app.route('/contacts/<contact_number>', methods=['GET', 'PUT'])
def search(contact_number):
    if validateUser():
        if not contact_number:
            return jsonify({"message": "Bad request", "status": 400})
        if request.method == 'GET':
            contact = Contact.query.filter_by(phone_number=contact_number).first()
            user = User.query.filter_by(phone=contact_number).first()

            if user:
                return jsonify({"Message" : "User with this contact number is registered with us", "name" : user.name, "Phone Number" : user.phone, "Spam Status" : contact.is_spam, "Email Id" : user.email})
            else :
                contacts = Contact.query.filter_by(phone_number=contact_number).all()
                output = []
                for contact in contacts:
                    contact_data  = {"id" : contact.id, "name" : contact.name, "Number" : contact.phone_number, "Spam Status" : contact.is_spam}
                    output.append(contact_data)
                return jsonify({"Message":"Not a Registered User", "contacts" : output})

        elif request.method == 'PUT':
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
                new_contact_data  = {"id" : contact.id, "name" : contact.name, "Number" : contact.phone_number, "Spam" : contact.is_spam}
                output.append(new_contact_data)
            return jsonify({"Spam Status" : "Spam status was changed for the mentioned number", "contacts affected" : output})
        else:
            return jsonify({"Msg" : "Bad Request"})
    else:
        return jsonify({'Message' : 'You are not logged in'})

@app.route('/logout')
def logout():
    s =  (request.headers.get('Authorization'))
    user = User.query.filter(User.auth_token==s).first()
    user.auth_token = None # we set auth_token as None when we logout. So now if we pass the same auth_token that we had earlier, our validateUser() function returns false and we know user isn't logged in
    db.session.add(user)
    db.session.commit()
    return jsonify({'message' : 'You successfully logged out'})