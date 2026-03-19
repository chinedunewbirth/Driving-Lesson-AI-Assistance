from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import User, Student, Instructor, Lesson

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.before_request
@login_required
def require_admin():
    if current_user.role != 'admin':
        flash('Access denied')
        return redirect(url_for('main.index'))

@admin_bp.route('/users')
def users():
    users = User.query.all()
    return render_template('admin/users.html', users=users)

@admin_bp.route('/students')
def students():
    students = Student.query.all()
    return render_template('admin/students.html', students=students)

@admin_bp.route('/instructors')
def instructors():
    instructors = Instructor.query.all()
    return render_template('admin/instructors.html', instructors=instructors)

@admin_bp.route('/lessons')
def lessons():
    lessons = Lesson.query.all()
    return render_template('admin/lessons.html', lessons=lessons)