from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_bcrypt import Bcrypt
from datetime import timedelta
from sqlalchemy import or_

app = Flask(
    __name__,
    template_folder='Template',  # Points to your "Template" folder
    static_folder='Static'       # Points to your "Static" folder
)

app.config['SECRET_KEY'] = 'YOUR_SECRET_KEY'  # Change this to a secure secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///assignment3.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Define the User model with a user_type field (Student or Instructor)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name  = db.Column(db.String(50), nullable=False)
    username   = db.Column(db.String(50), unique=True, nullable=False)
    email      = db.Column(db.String(100), unique=True, nullable=False)
    password   = db.Column(db.String(200), nullable=False)
    user_type  = db.Column(db.String(20), nullable=False)  # 'Student' or 'Instructor'

# Root route: Always start at the login page.
@app.route('/')
def index():
    return redirect(url_for('login'))

# Home route: Renders index.html after successful login.
@app.route('/home')
def home():
    # Optionally, check that the user is logged in:
    if 'username' not in session:
        flash('Please login first.', 'error')
        return redirect(url_for('login'))
    return render_template('index.html')

# Registration route: Collects user details and creates an account.
@app.route('/Register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form.get('first_name').strip()
        last_name  = request.form.get('last_name').strip()
        username   = request.form.get('username').strip()
        email      = request.form.get('email').strip()
        password   = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        user_type  = request.form.get('user_type')  # Should be "Student" or "Instructor"

        # Check that password and confirm_password match.
        if password != confirm_password:
            flash('Passwords do not match. Please try again.', 'error')
            return render_template('Register.html')

        # Check if the username already exists.
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose another.', 'error')
            return render_template('Register.html')

        # (Optional) You could also check for email uniqueness if needed:
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            flash('An account with this email already exists.', 'error')
            return render_template('Register.html')

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password=hashed_password,
            user_type=user_type
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    return render_template('Register.html')


# Login route: Authenticates a user based on username, password, and account type.
@app.route('/Login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username').strip()
        password = request.form.get('password')
        form_user_type = request.form.get('accountType')  # "Student" or "Instructor" from the radio button

        user = User.query.filter_by(username=username).first()
        if user and user.user_type == form_user_type and bcrypt.check_password_hash(user.password, password):
            session['username'] = user.username
            session['user_type'] = user.user_type
            session.permanent = True
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username, password, or user type.', 'error')
            # Re-render the login template with the error message displayed.
            return render_template('Login.html')
    return render_template('Login.html')

# Dashboard route (optional if needed)
@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        flash('Please login to access the dashboard.', 'error')
        return redirect(url_for('login'))
    user_type = session.get('user_type')
    username = session.get('username')
    return render_template('dashboard.html', user_type=user_type, username=username)

# Additional routes for static pages (Assignments, Lab, Lecture Notes, Feedback, Course Team)
@app.route('/Assignment1')
def assignment1():
    return render_template('Assignment1.html')

@app.route('/Assignment2')
def assignment2():
    return render_template('Assignment2.html')

@app.route('/Assignment3')
def assignment3():
    return render_template('Assignment3.html')

@app.route('/Lab')
def lab():
    return render_template('Lab.html')

@app.route('/LectureNote')
def lecture_note():
    return render_template('LectureNote.html')

@app.route('/Feedback')
def feedback():
    return render_template('Feedback.html')

@app.route('/CourseTeam')
def course_team():
    return render_template('CourseTeam.html')

# Logout route: Clears the session data.
@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
