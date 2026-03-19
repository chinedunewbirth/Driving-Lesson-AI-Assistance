import pytest
from app import create_app, db
from app.models import User, Student, Instructor, Lesson

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'AI Driving School' in response.data

def test_register_user(client):
    response = client.post('/register', data={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password',
        'role': 'student'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Registration successful' in response.data