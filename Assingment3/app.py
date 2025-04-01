import os
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_bcrypt import Bcrypt
from datetime import timedelta, datetime
from sqlalchemy import or_

# Determine the absolute path of the current directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Set the instance folder path (inside your Assignment3 folder)
INSTANCE_PATH = os.path.join(BASE_DIR, 'instance')

# Create the instance folder if it doesn't exist
if not os.path.exists(INSTANCE_PATH):
    os.makedirs(INSTANCE_PATH)

app = Flask(
    __name__,
    template_folder='Template',  # Points to your "Template" folder
    static_folder='Static',       # Points to your "Static" folder
    instance_path=INSTANCE_PATH,  # Set the instance folder path
    instance_relative_config=True  # Treat instance_path as relative
)

# Configure the database URI using an absolute path.
app.config['SECRET_KEY'] = 'YOUR_SECRET_KEY'  # Change this to a secure secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'assignment3.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Define the User model with a user_type field (Student or Instructor)
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
    regrade = db.relationship('Regrade', backref='user', lazy=True)

# Grade model with a property to return remark status
class Grade(db.Model):
    __tablename__ = 'Grade'
    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    work = db.Column(db.String(50), nullable=False)
    grade = db.Column(db.Integer, nullable=False)

    @property
    def remark_status(self):
        # Query the Regrade table for a request matching this grade (by user and work)
        regrade_req = Regrade.query.filter_by(userID=self.userID, work=self.work).first()
        return regrade_req.status if regrade_req else "Not Requested"

# Regrade model (still using work as the foreign key)
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
@app.route('/')
def index():
    return redirect(url_for('login'))

# Home route.
@app.route('/home')
def home():
    name = session.get('name')
    if 'username' not in session:
        flash('Please login first.', 'error')
        return redirect(url_for('login'))
    return render_template('index.html', name=name)

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
        user_type  = request.form.get('user_type')  # "Student" or "Instructor"

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
        new_user = User(first_name=first_name,
                        last_name=last_name,
                        username=username,
                        email=email,
                        password=hashed_password,
                        user_type=user_type)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    return render_template('Register.html')

# Grades route.
@app.route('/grades', methods=['GET'])
def view_grades():
    if 'username' not in session:
        return redirect(url_for('login'))

    user = User.query.filter_by(username=session['username']).first()
    if not user:
        return "User not found", 404

    if user.user_type == 'Student':
        # Only fetch the grades of the logged-in student.
        grades = Grade.query.filter_by(userID=user.id).all()
        return render_template('grades_student.html', grades=grades)
    elif user.user_type == 'Instructor':
        # Instructors can see all students' grades.
        grades = Grade.query.all()
        return render_template('grades_instructor.html', grades=grades)
    else:
        return "Unauthorized", 403

# Student grades route (using session-based authentication).
@app.route('/student_grades')
def student_grades():
    if 'username' not in session:
        flash("Please login first.", "error")
        return redirect(url_for('login'))
    user = User.query.filter_by(username=session['username']).first()
    if not user or user.user_type != 'Student':
        flash("Unauthorized access.", "error")
        return redirect(url_for('home'))
    student_grades = Grade.query.filter_by(userID=user.id).all()
    return render_template('StudentGrade.html', query_grade_result=student_grades)

# Login route.
@app.route('/Login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username').strip()
        password = request.form.get('password')
        form_user_type = request.form.get('accountType')  # "Student" or "Instructor"
        user = User.query.filter_by(username=username).first()
        if user and user.user_type == form_user_type and bcrypt.check_password_hash(user.password, password):
            session['username'] = user.username
            session['user_type'] = user.user_type
            session['name'] = user.first_name
            session.permanent = True
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username, password, or user type.', 'error')
            return render_template('Login.html')
    return render_template('Login.html')

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

# Unified Feedback route.
@app.route('/Feedback', methods=['GET', 'POST'])
def feedback():
    if 'username' not in session:
        flash("Please log in to access feedback.", "error")
        return redirect(url_for('login'))
    
    user_type = session.get('user_type')
    
    if user_type == 'Instructor':
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
            new_feedback = Feedback(instructor_id=instructor_id,
                                    feedback_instructor_like=instructor_like,
                                    feedback_instructor_improve=instructor_improve,
                                    feedback_labs_like=labs_like,
                                    feedback_labs_improve=labs_improve)
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

# Submit remark route.
@app.route('/submit_remark/<int:grade_id>', methods=['POST'])
def submit_remark(grade_id):
    if 'username' not in session:
        return jsonify({"success": False, "error": "Unauthorized"}), 403

    data = request.get_json()
    reason = data.get('reason', '').strip()
    if not reason:
        return jsonify({"success": False, "error": "Reason is required"}), 400

    user = User.query.filter_by(username=session['username']).first()
    if not user:
        return jsonify({"success": False, "error": "User not found"}), 404

    grade = Grade.query.get(grade_id)
    if not grade:
        return jsonify({"success": False, "error": "Grade not found"}), 404

    # Ensure the user owns this grade.
    if grade.userID != user.id:
        return jsonify({"success": False, "error": "You cannot request a remark for another student's grade"}), 403

    # Check if a remark request already exists for this grade.
    existing_regrade = Regrade.query.filter_by(userID=user.id, work=grade.work).first()
    if existing_regrade:
        return jsonify({"success": False, "error": "Remark request already exists"}), 400

    # Create a new regrade request.
    new_regrade = Regrade(userID=user.id, work=grade.work, question=None, reason=reason, status="pending")
    db.session.add(new_regrade)
    db.session.commit()
    return jsonify({"success": True, "message": "Remark request submitted successfully"})

# Update remark status route.
@app.route('/update_remark_status/<int:regrade_id>', methods=['POST'])
def update_remark_status(regrade_id):
    if 'username' not in session or session.get('user_type') != 'Instructor':
        return jsonify({"success": False, "message": "Unauthorized"}), 403

    data = request.get_json()
    status = data.get('status', '').lower()
    if status not in ['approved', 'rejected']:
        return jsonify({"success": False, "message": "Invalid status"}), 400

    regrade = Regrade.query.get(regrade_id)
    if regrade:
        regrade.status = status
        db.session.commit()
        return jsonify({"success": True, "message": f"Regrade {status}"}), 200
    return jsonify({"success": False, "message": "Regrade not found"}), 404

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
        grade_val = request.form['grade']
        new_grade = Grade(userID=student_id, work=work, grade=grade_val)
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

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("Database tables created successfully.")
        # Test accounts and sample data.
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
