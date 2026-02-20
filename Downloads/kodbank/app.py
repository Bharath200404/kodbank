from flask import Flask, request, jsonify, render_template, redirect, url_for, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os
import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'kodbank_secret_key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///kodbank.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'jwt_secret_string')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

db = SQLAlchemy(app)
jwt = JWTManager(app)
CORS(app)

# Database Models
class KodUser(db.Model):
    __tablename__ = 'KodUser'
    uid = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    balance = db.Column(db.Float, default=100000.0)
    phone = db.Column(db.String(20), nullable=False)
    role = db.Column(db.String(20), default='Customer')

class UserToken(db.Model):
    __tablename__ = 'UserToken'
    tid = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    token = db.Column(db.String(500), nullable=False)
    uid = db.Column(db.String(36), db.ForeignKey('KodUser.uid'), nullable=False)
    expiry = db.Column(db.DateTime, nullable=False)
    user = db.relationship('KodUser', backref=db.backref('tokens', lazy=True))

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.form
        hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')

        # Check if username already exists
        if KodUser.query.filter_by(username=data['username']).first():
            return render_template('register.html', error='Username already exists')

        # Check if email already exists
        if KodUser.query.filter_by(email=data['email']).first():
            return render_template('register.html', error='Email already registered')

        # Create new user
        new_user = KodUser(
            username=data['username'],
            email=data['email'],
            password=hashed_password,
            phone=data['phone'],
            role='Customer'  # Fixed role as Customer
        )

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = KodUser.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            # Create JWT token
            additional_claims = {"role": user.role}
            access_token = create_access_token(identity=username, additional_claims=additional_claims)

            # Store token in UserToken table
            expiry_time = datetime.utcnow() + timedelta(hours=1)
            new_token = UserToken(
                token=access_token,
                uid=user.uid,
                expiry=expiry_time
            )

            db.session.add(new_token)
            db.session.commit()

            # Create response and set cookie
            response = make_response(redirect(url_for('dashboard')))
            response.set_cookie('jwt_token', access_token, httponly=True, secure=False)

            return response
        else:
            return render_template('login.html', error='Invalid username or password')

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    # Check if user is logged in by checking for the token
    token = request.cookies.get('jwt_token')
    if not token:
        return redirect(url_for('login'))

    return render_template('dashboard.html')

@app.route('/check_balance', methods=['GET'])
@jwt_required()
def check_balance():
    current_user = get_jwt_identity()
    user = KodUser.query.filter_by(username=current_user).first()

    if user:
        return jsonify({"balance": user.balance})
    else:
        return jsonify({"error": "User not found"}), 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
