<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
import os
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_bcrypt import Bcrypt
from datetime import timedelta, datetime
from sqlalchemy import or_
=======
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import timedelta
>>>>>>> Stashed changes

# Determine the absolute path of the current directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Set the instance folder path (inside your Assignment3 folder)
INSTANCE_PATH = os.path.join(BASE_DIR, 'instance')

# Create the instance folder if it doesn't exist
if not os.path.exists(INSTANCE_PATH):
    os.makedirs(INSTANCE_PATH)

app = Flask(
    __name__,
<<<<<<< Updated upstream
    template_folder='Template',  # Points to your "Template" folder
    static_folder='Static',       # Points to your "Static" folder
    instance_path=INSTANCE_PATH,  # Set the instance folder path
    instance_relative_config=True  # Treat instance_path as relative
)

# Configure the database URI using an absolute path.
app.config['SECRET_KEY'] = 'YOUR_SECRET_KEY'  # Change this to a secure secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'assignment3.db')
=======
    template_folder='Template',
    static_folder='Static'
)

=======
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import timedelta

app = Flask(
    __name__,
    template_folder='Template',
    static_folder='Static'
)

>>>>>>> Stashed changes
=======
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import timedelta

app = Flask(
    __name__,
    template_folder='Template',
    static_folder='Static'
)

>>>>>>> Stashed changes
app.config['SECRET_KEY'] = 'YOUR_SECRET_KEY'  
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///assignment3.db'
>>>>>>> Stashed changes
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Define User model
class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name  = db.Column(db.String(50), nullable=False)
    username   = db.Column(db.String(50), unique=True, nullable=False)
    email      = db.Column(db.String(100), unique=True, nullable=False)
    password   = db.Column(db.String(200), nullable=False)
    user_type  = db.Column(db.String(20), nullable=False)  # 'Student' or 'Instructor'
    grades = db.relationship('Grade', backref='user', lazy=True)
    regrade=db.relationship('Regrade', backref='user', lazy=True)

<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
# Additional models...
class Grade(db.Model):
    __tablename__ = 'Grade'
    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    work = db.Column(db.String(50), nullable=False)
    grade = db.Column(db.Integer, nullable=False)

class Regrade(db.Model):
    __tablename__ = 'Remark'
    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    work = db.Column(db.String(50), db.ForeignKey('Grade.work'), nullable=False)
    question = db.Column(db.Integer)
    reason = db.Column(db.String(1000), nullable=False)
    status = db.Column(db.String(50), nullable=False)

# Updated Feedback model with a status column.
class Feedback(db.Model):
    __tablename__ = 'Feedback'
    id = db.Column(db.Integer, primary_key=True)
    instructor_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    feedback_instructor_like = db.Column(db.String(1000), nullable=False)
    feedback_instructor_improve = db.Column(db.String(1000), nullable=False)
    feedback_labs_like = db.Column(db.String(1000), nullable=False)
    feedback_labs_improve = db.Column(db.String(1000), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default="open")  # "open" or "reviewed"

# Root route.
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
# Define Marks model
class Marks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    assignment1 = db.Column(db.Float, nullable=True)
    assignment2 = db.Column(db.Float, nullable=True)
    assignment3 = db.Column(db.Float, nullable=True)
    midterm = db.Column(db.Float, nullable=True)
    lab_tutorials = db.Column(db.Float, nullable=True)
    final_exam = db.Column(db.Float, nullable=True)

    user = db.relationship('User', backref=db.backref('marks', lazy=True))

# Define Remark Request model
class RemarkRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    assignment = db.Column(db.String(50), nullable=False)
    reason = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default="Pending")
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

    user = db.relationship('User', backref=db.backref('remark_requests', lazy=True))

<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html', first_name=session.get('first_name', 'Guest'))
    return redirect(url_for('login'))

<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
# Home route.
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
@app.route('/home')
def home():
    if 'username' not in session:
        flash('Please login first.', 'error')
        return redirect(url_for('login'))
    return render_template('index.html', first_name=session.get('first_name', 'Guest'))

<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
# Registration route.
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

        if password != confirm_password:
            flash('Passwords do not match. Please try again.', 'error')
            return render_template('Register.html')

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose another.', 'error')
            return render_template('Register.html')

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

# Login route.
@app.route('/Login', methods=['GET', 'POST'])
=======
@app.route('/login', methods=['GET', 'POST'])
>>>>>>> Stashed changes
=======
@app.route('/login', methods=['GET', 'POST'])
>>>>>>> Stashed changes
=======
@app.route('/login', methods=['GET', 'POST'])
>>>>>>> Stashed changes
def login():
    if request.method == 'POST':
        username = request.form.get('username').strip()
        password = request.form.get('password')
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
        form_user_type = request.form.get('accountType')  # "Student" or "Instructor"
=======
        form_user_type = request.form.get('accountType')
>>>>>>> Stashed changes
=======
        form_user_type = request.form.get('accountType')
>>>>>>> Stashed changes
=======
        form_user_type = request.form.get('accountType')
>>>>>>> Stashed changes

        user = User.query.filter_by(username=username).first()

        if user and user.user_type == form_user_type and bcrypt.check_password_hash(user.password, password):
            session['username'] = user.username
            session['user_type'] = user.user_type
            session['first_name'] = user.first_name
            session.permanent = True
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username, password, or user type.', 'error')
            return render_template('Login.html')
    return render_template('Login.html')

<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
# Dashboard route.
@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        flash('Please login to access the dashboard.', 'error')
        return redirect(url_for('login'))
    user_type = session.get('user_type')
    username = session.get('username')
    return render_template('dashboard.html', user_type=user_type, username=username)

# Additional static pages.
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

# Unified Feedback route: renders different views based on user type.
@app.route('/Feedback', methods=['GET', 'POST'])
def feedback():
    if 'username' not in session:
        flash("Please log in to access feedback.", "error")
        return redirect(url_for('login'))
    
    user_type = session.get('user_type')
    
    if user_type == 'Instructor':
        # Retrieve feedback for the logged-in instructor.
        instructor = User.query.filter_by(username=session.get('username')).first()
        feedbacks = Feedback.query.filter_by(instructor_id=instructor.id).all()
        return render_template('InstructorFeedback.html', feedbacks=feedbacks)
    
    elif user_type == 'Student':
        if request.method == 'POST':
            instructor_id = request.form.get('instructor_id')
            instructor_like = request.form.get('instructor_like')
            instructor_improve = request.form.get('instructor_improve')
            labs_like = request.form.get('labs_like')
            labs_improve = request.form.get('labs_improve')
            
            new_feedback = Feedback(
                instructor_id=instructor_id,
                feedback_instructor_like=instructor_like,
                feedback_instructor_improve=instructor_improve,
                feedback_labs_like=labs_like,
                feedback_labs_improve=labs_improve
            )
            db.session.add(new_feedback)
            db.session.commit()
            
            flash("Your feedback has been submitted successfully!", "success")
            return render_template('feedback_confirmation.html')
        else:
            instructors = User.query.filter_by(user_type='Instructor').all()
            return render_template('StudentFeedback.html', instructors=instructors)
    
    else:
        flash("Unauthorized access.", "error")
        return redirect(url_for('home'))

# Route for instructors to mark feedback as reviewed.
@app.route('/mark_feedback_reviewed', methods=['POST'])
def mark_feedback_reviewed():
    if 'username' not in session or session.get('user_type') != 'Instructor':
        flash("Only instructors can mark feedback as reviewed.", "error")
        return redirect(url_for('login'))
    
    feedback_id = request.form.get('feedback_id')
    feedback_item = Feedback.query.get(feedback_id)
    instructor = User.query.filter_by(username=session.get('username')).first()
    
    if feedback_item and feedback_item.instructor_id == instructor.id:
        feedback_item.status = "reviewed"
        db.session.commit()
        flash("Feedback marked as reviewed.", "success")
    else:
        flash("Feedback not found or you are not authorized.", "error")
    
    return redirect(url_for('feedback'))

@app.route('/CourseTeam')
def course_team():
    return render_template('CourseTeam.html')

@app.route('/Grade')
def grade():
    query_grade_result = query_grades()
    user_type = session.get('user_type')
    if user_type == 'Instructor':
        return render_template('InstructorGrade.html', query_grade_result=query_grade_result)
    else:
        return render_template('StudentGrade.html', query_grade_result=query_grade_result)

@app.route('/Regrade')
def regrade():
    regrades_list = query_regrades()
    user_type = session.get('user_type')
    if user_type == 'Instructor':
        return render_template('InstructorRegrade.html', regrades_list=regrades_list)
    else:
        return render_template('StudentRegrade.html', regrades_list=regrades_list)

@app.route('/update_regrade_status', methods=['POST'])
def update_regrade_status():
    regrade_id = request.form.get('regrade_id')
    new_status = request.form.get('new_status')
    regrade = Regrade.query.get(regrade_id)
    if regrade:
        regrade.status = new_status
        db.session.commit()
        flash(f"Regrade request {regrade_id} has been {new_status}.", 'success')
    else:
        flash("Regrade request not found.", 'error')
    return redirect(url_for('regrade'))

@app.route('/addGrades', methods=['GET', 'POST'])
def addGrades():
    if request.method == 'POST':
        student_id = request.form['student_id']
        work = request.form['work']
        grade = request.form['grade']
        new_grade = Grade(userID=student_id, work=work, grade=grade)
        db.session.add(new_grade)
        db.session.commit()
        flash('Marks updated successfully!', 'success')
        return redirect(url_for('addGrades'))
    else:
        return render_template("AddGrades.html")

def query_grades():
    return Grade.query.all()

def query_regrades():
    return Regrade.query.all()
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('login'))
>>>>>>> Stashed changes

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        username = request.form.get('username')
        email = request.form.get('email')
        password = bcrypt.generate_password_hash(request.form.get('password')).decode('utf-8')
        user_type = request.form.get('user_type')

        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'error')
            return redirect(url_for('register'))
        if User.query.filter_by(email=email).first():
            flash('Email already exists.', 'error')
            return redirect(url_for('register'))

        new_user = User(first_name=first_name, last_name=last_name, username=username, email=email, password=password, user_type=user_type)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('login'))

    return render_template('Register.html')

@app.route('/marks')
def view_marks():
    if 'username' not in session:
        flash('Please log in to view your marks.', 'error')
        return redirect(url_for('login'))

    user = User.query.filter_by(username=session['username']).first()
    marks = Marks.query.filter_by(user_id=user.id).first()
    remark_requests = {req.assignment: req for req in RemarkRequest.query.filter_by(user_id=user.id).all()}

    return render_template('marks.html', user=user, marks=marks, remark_requests=remark_requests)

@app.route('/remark_request', methods=['POST'])
def remark_request():
    if 'username' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('login'))

    user = User.query.filter_by(username=session['username']).first()
    if not user:
        flash('User not found.', 'error')
        return redirect(url_for('login'))

    assignment = request.form.get('assignment')
    reason = request.form.get('reason').strip()

    if not reason:
        flash('Please provide a reason for the remark request.', 'error')
        return redirect(url_for('view_marks'))

    existing_request = RemarkRequest.query.filter_by(user_id=user.id, assignment=assignment).first()
    if existing_request:
        flash(f'Remark request for {assignment.replace("_", " ").title()} already submitted!', 'error')
        return redirect(url_for('view_marks'))

    new_request = RemarkRequest(user_id=user.id, assignment=assignment, reason=reason, status="Pending")
    db.session.add(new_request)
    db.session.commit()

    flash(f'Remark request for {assignment.replace("_", " ").title()} submitted successfully!', 'success')
    
    return redirect(url_for('view_marks'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        username = request.form.get('username')
        email = request.form.get('email')
        password = bcrypt.generate_password_hash(request.form.get('password')).decode('utf-8')
        user_type = request.form.get('user_type')

        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'error')
            return redirect(url_for('register'))
        if User.query.filter_by(email=email).first():
            flash('Email already exists.', 'error')
            return redirect(url_for('register'))

        new_user = User(first_name=first_name, last_name=last_name, username=username, email=email, password=password, user_type=user_type)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('login'))

    return render_template('Register.html')

@app.route('/marks')
def view_marks():
    if 'username' not in session:
        flash('Please log in to view your marks.', 'error')
        return redirect(url_for('login'))

    user = User.query.filter_by(username=session['username']).first()
    marks = Marks.query.filter_by(user_id=user.id).first()
    remark_requests = {req.assignment: req for req in RemarkRequest.query.filter_by(user_id=user.id).all()}

    return render_template('marks.html', user=user, marks=marks, remark_requests=remark_requests)

@app.route('/remark_request', methods=['POST'])
def remark_request():
    if 'username' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('login'))

    user = User.query.filter_by(username=session['username']).first()
    if not user:
        flash('User not found.', 'error')
        return redirect(url_for('login'))

    assignment = request.form.get('assignment')
    reason = request.form.get('reason').strip()

    if not reason:
        flash('Please provide a reason for the remark request.', 'error')
        return redirect(url_for('view_marks'))

    existing_request = RemarkRequest.query.filter_by(user_id=user.id, assignment=assignment).first()
    if existing_request:
        flash(f'Remark request for {assignment.replace("_", " ").title()} already submitted!', 'error')
        return redirect(url_for('view_marks'))

    new_request = RemarkRequest(user_id=user.id, assignment=assignment, reason=reason, status="Pending")
    db.session.add(new_request)
    db.session.commit()

    flash(f'Remark request for {assignment.replace("_", " ").title()} submitted successfully!', 'success')
    
    return redirect(url_for('view_marks'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        username = request.form.get('username')
        email = request.form.get('email')
        password = bcrypt.generate_password_hash(request.form.get('password')).decode('utf-8')
        user_type = request.form.get('user_type')

        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'error')
            return redirect(url_for('register'))
        if User.query.filter_by(email=email).first():
            flash('Email already exists.', 'error')
            return redirect(url_for('register'))

        new_user = User(first_name=first_name, last_name=last_name, username=username, email=email, password=password, user_type=user_type)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('login'))

    return render_template('Register.html')

@app.route('/marks')
def view_marks():
    if 'username' not in session:
        flash('Please log in to view your marks.', 'error')
        return redirect(url_for('login'))

    user = User.query.filter_by(username=session['username']).first()
    marks = Marks.query.filter_by(user_id=user.id).first()
    remark_requests = {req.assignment: req for req in RemarkRequest.query.filter_by(user_id=user.id).all()}

    return render_template('marks.html', user=user, marks=marks, remark_requests=remark_requests)

@app.route('/remark_request', methods=['POST'])
def remark_request():
    if 'username' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('login'))

    user = User.query.filter_by(username=session['username']).first()
    if not user:
        flash('User not found.', 'error')
        return redirect(url_for('login'))

    assignment = request.form.get('assignment')
    reason = request.form.get('reason').strip()

    if not reason:
        flash('Please provide a reason for the remark request.', 'error')
        return redirect(url_for('view_marks'))

    existing_request = RemarkRequest.query.filter_by(user_id=user.id, assignment=assignment).first()
    if existing_request:
        flash(f'Remark request for {assignment.replace("_", " ").title()} already submitted!', 'error')
        return redirect(url_for('view_marks'))

    new_request = RemarkRequest(user_id=user.id, assignment=assignment, reason=reason, status="Pending")
    db.session.add(new_request)
    db.session.commit()

    flash(f'Remark request for {assignment.replace("_", " ").title()} submitted successfully!', 'success')
    
    return redirect(url_for('view_marks'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("Database tables created successfully.")
        # Test accounts
        user1 = User(first_name='Purva', last_name='Gawde', username='1234qwer', 
                     email='purva@example.com', password=bcrypt.generate_password_hash('password123').decode('utf-8'), 
                     user_type='Instructor')
        user2 = User(first_name='student', last_name='A', username='4321qwer', 
                     email='student-a@example.com', password=bcrypt.generate_password_hash('password321').decode('utf-8'), 
                     user_type='Student')
        grade1 = Grade(userID=2, work='Assignment', grade=97, user=user2)
        grade2 = Grade(userID=2, work='Midterm Test', grade=82, user=user2)
        grade3 = Grade(userID=2, work='Final Test', grade=95, user=user2)
        regrade1 = Regrade(userID=2, work='Midterm Test', question=4, reason='blablabla', status='rejected', user=user2)
        regrade2 = Regrade(userID=2, work='Midterm Test', question=6, reason='blablabla', status='pending', user=user2)
        regrade3 = Regrade(userID=2, work='Assignment', question=2, reason='blablabla', status='approved', user=user2)

        if not User.query.first():
            db.session.add_all([user1, user2])
            db.session.commit()
        if not Grade.query.first():
            db.session.add_all([grade1, grade2, grade3])
            db.session.commit()
        if not Regrade.query.first():
            db.session.add_all([regrade1, regrade2, regrade3])
            db.session.commit()

        db.session.close()
    app.run(debug=True)