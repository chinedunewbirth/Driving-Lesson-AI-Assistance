from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Student, Instructor, Lesson, Payment
from datetime import datetime
import stripe

student_bp = Blueprint('student', __name__, url_prefix='/student')

@student_bp.before_request
@login_required
def require_student():
    if current_user.role != 'student':
        flash('Access denied')
        return redirect(url_for('main.index'))

@student_bp.route('/profile')
def profile():
    student = Student.query.filter_by(user_id=current_user.id).first()
    if not student:
        return redirect(url_for('student.create_profile'))
    return render_template('student/profile.html', student=student)

@student_bp.route('/create_profile', methods=['GET', 'POST'])
def create_profile():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        phone = request.form.get('phone')
        address = request.form.get('address')
        
        student = Student(user_id=current_user.id, first_name=first_name, last_name=last_name, phone=phone, address=address)
        db.session.add(student)
        db.session.commit()
        flash('Profile created')
        return redirect(url_for('student.profile'))
    
    return render_template('student/create_profile.html')

@student_bp.route('/book_lesson', methods=['GET', 'POST'])
def book_lesson():
    student = Student.query.filter_by(user_id=current_user.id).first()
    if not student:
        flash('Please create your profile first')
        return redirect(url_for('student.create_profile'))
    
    instructors = Instructor.query.all()
    
    if request.method == 'POST':
        instructor_id = request.form.get('instructor_id')
        date_str = request.form.get('date')
        time_str = request.form.get('time')
        
        date_time_str = f"{date_str} {time_str}"
        date_time = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M')
        
        # Check for conflicts
        conflict = Lesson.query.filter_by(instructor_id=instructor_id, date=date_time).first()
        if conflict:
            flash('Instructor is not available at this time')
            return redirect(url_for('student.book_lesson'))
        
        lesson = Lesson(student_id=student.id, instructor_id=instructor_id, date=date_time)
        db.session.add(lesson)
        db.session.commit()
        flash('Lesson booked successfully')
        return redirect(url_for('student.lessons'))
    
    return render_template('student/book_lesson.html', instructors=instructors)

@student_bp.route('/pay/<int:lesson_id>', methods=['GET', 'POST'])
def pay_lesson(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    if lesson.student_id != current_user.id:
        flash('Access denied')
        return redirect(url_for('student.lessons'))
    
    if request.method == 'POST':
        # Create Stripe payment intent
        stripe.api_key = 'sk_test_...'  # From config
        intent = stripe.PaymentIntent.create(
            amount=5000,  # $50.00
            currency='usd',
            metadata={'lesson_id': lesson_id}
        )
        return render_template('student/pay.html', client_secret=intent.client_secret, lesson=lesson)
    
    return render_template('student/pay.html', lesson=lesson)