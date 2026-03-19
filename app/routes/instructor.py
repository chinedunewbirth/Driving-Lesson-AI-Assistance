from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db, mail
from app.models import Lesson, Student
from app.ai import generate_ai_feedback, score_driving_skills, generate_learning_recommendations
from flask_mail import Message

instructor_bp = Blueprint('instructor', __name__, url_prefix='/instructor')

@instructor_bp.before_request
@login_required
def require_instructor():
    if current_user.role != 'instructor':
        flash('Access denied')
        return redirect(url_for('main.index'))

@instructor_bp.route('/lessons')
def lessons():
    instructor = Instructor.query.filter_by(user_id=current_user.id).first()
    if not instructor:
        flash('Instructor profile not found')
        return redirect(url_for('main.index'))
    lessons = Lesson.query.filter_by(instructor_id=instructor.id).all()
    return render_template('instructor/lessons.html', lessons=lessons)

@instructor_bp.route('/lesson/<int:lesson_id>', methods=['GET', 'POST'])
def lesson_detail(lesson_id):
    instructor = Instructor.query.filter_by(user_id=current_user.id).first()
    if not instructor:
        flash('Instructor profile not found')
        return redirect(url_for('main.index'))
    lesson = Lesson.query.get_or_404(lesson_id)
    if lesson.instructor_id != instructor.id:
        flash('Access denied')
        return redirect(url_for('instructor.lessons'))
    
    if request.method == 'POST':
        lesson.notes = request.form.get('notes')
        lesson.status = 'completed'
        
        # Send email to student
        msg = Message('Lesson Completed', sender='noreply@drivingschool.com', recipients=[lesson.student.user.email])
        msg.body = f'Your lesson on {lesson.date} has been completed. Notes: {lesson.notes}'
        mail.send(msg)
        
        # Trigger AI tasks (simplified)
        # In real app, handle async results
        db.session.commit()
        flash('Lesson updated and notification sent')
        return redirect(url_for('instructor.lessons'))
    
    return render_template('instructor/lesson_detail.html', lesson=lesson)