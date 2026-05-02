"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

from app import app, bcrypt, db
from app.models import User, Profile, Interest, Like, Match, Message, Favorite
from flask import render_template, request, jsonify, send_file
import os


###
# Routing for your application.
###

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")


@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()

    email = data.get("email")
    username = data.get("username")
    password = data.get("password")

    first_name = data.get("firstName")
    last_name = data.get("lastName")
    dob = data.get("dob")
    
    age = None
    if dob:
        from datetime import datetime
        try:
            dob_date = datetime.strptime(dob, "%Y-%m-%d")
            today = datetime.today()
            age = today.year - dob_date.year - ((today.month, today.day) < (dob_date.month, dob_date.day))
        except ValueError:
            return jsonify({"error": "Invalid date format for dob. Use YYYY-MM-DD."}), 400

    gender = data.get("gender")
    looking_for = data.get("lookingFor")
    bio = data.get("bio")
    location = data.get("location")
    interests = data.get("interests", [])

    if not all([email, username, password, first_name, last_name, age, gender, looking_for, bio, location]):
        return jsonify({"error": "Missing required fields"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already exists"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists"}), 400

    # create user
    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

    user = User(
        email=email,
        username=username,
        password_hash=hashed_password
    )

    db.session.add(user)
    db.session.flush()

    # create profile linked to user
    profile = Profile(
        user_id=user.id,
        first_name=first_name,
        last_name=last_name,
        age=age,
        gender=gender,
        looking_for=looking_for,
        bio=bio,
        location=location
    )

    db.session.add(profile)

    for name in interests:
        interest = Interest.query.filter_by(name=name.lower()).first()

        if not interest:
            interest = Interest(name=name.lower())

        profile.interests.append(interest)

    db.session.commit()

    return jsonify({
        "message": "User and profile created successfully"
    }), 201


@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    user = User.query.filter_by(email=email).first()

    if user and bcrypt.check_password_hash(user.password_hash, password):
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"error": "Invalid email or password"}), 401
    

    
###
# The functions below should be applicable to all Flask apps.
###

# Here we define a function to collect form errors from Flask-WTF
# which we can later use
def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)

    return error_messages

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404
