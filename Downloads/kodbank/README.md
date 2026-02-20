# Kodbank Application

Kodbank is a simple banking application that allows users to register, login, and check their account balance.

## Features

- User registration with default role "Customer"
- User authentication with JWT tokens
- Secure password storage using hashing
- Token storage in database
- Balance checking with JWT verification
- Beautiful UI with confetti animation when checking balance

## Database Schema

The application uses two main tables:

1. **KodUser**
   - uid (Primary Key)
   - username
   - email
   - password (hashed)
   - balance (default: 100000)
   - phone
   - role (default: "Customer")

2. **UserToken**
   - tid (Primary Key)
   - token
   - uid (Foreign Key)
   - expiry

## Installation and Setup

1. Clone the repository or download the files
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the application:
   ```
   python app.py
   ```
4. Open your browser and navigate to `http://127.0.0.1:5000`

## How to Use

1. **Register**: Create a new account by providing username, email, password, and phone number
2. **Login**: Use your credentials to log in
3. **Dashboard**: After successful login, you'll be redirected to your dashboard
4. **Check Balance**: Click the "Check Balance" button to view your account balance with a fun animation

## Security Features

- Passwords are hashed using PBKDF2 with SHA-256
- JWT tokens are used for authentication
- Tokens are stored in the database with expiry time
- Role-based access control is implemented
