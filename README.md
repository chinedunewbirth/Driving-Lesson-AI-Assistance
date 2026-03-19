# AI Driving School System

A complete, production-ready driving lesson management system built with Flask, PostgreSQL, Docker, and AI-powered features.

## Features

- **User Authentication**: Secure login/registration with role-based access (Admin, Instructor, Student)
- **Lesson Booking**: Students can book lessons with instructors, with conflict prevention
- **AI-Powered Feedback**: Generate personalized driving improvement suggestions using OpenAI
- **Skill Scoring**: Automatic scoring of driving skills (steering, mirrors, parking, etc.)
- **Payments**: Stripe integration for secure payments
- **Email Notifications**: Automated emails for bookings and updates
- **Analytics**: Dashboards for progress tracking and revenue
- **Docker Support**: Containerized deployment with multi-service setup
- **CI/CD**: GitHub Actions for automated testing and deployment

## Quick Start

### Local Development

1. Clone the repository
2. Create virtual environment: `python -m venv venv`
3. Activate: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Linux/Mac)
4. Install dependencies: `pip install -r requirements.txt`
5. Set environment variables in `.env` (copy from `.env.example`)
6. Run the app: `python run.py`
7. Open http://localhost:5000

### Docker

1. `docker-compose up --build`
2. App runs on http://localhost:5000

## Project Structure

```
app/
├── __init__.py          # Flask app factory
├── models.py            # SQLAlchemy models
├── ai.py                # AI functions (OpenAI integration)
├── routes/              # Blueprints for different user roles
│   ├── auth.py
│   ├── main.py
│   ├── admin.py
│   ├── instructor.py
│   └── student.py
└── templates/           # Jinja2 templates
    ├── base.html
    ├── auth/
    ├── admin/
    ├── instructor/
    └── student/

config.py                # Configuration
run.py                   # App entry point
celery_worker.py         # Background tasks
requirements.txt         # Python dependencies
Dockerfile
docker-compose.yml
.github/workflows/ci.yml # CI/CD pipeline
```

## Environment Variables

Create a `.env` file with:

```
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://user:password@localhost/driving_school
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-email-password
STRIPE_PUBLIC_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
OPENAI_API_KEY=your-openai-key
```

## API Endpoints

- `/` - Home page
- `/login` - User login
- `/register` - User registration
- `/dashboard` - Role-based dashboard
- `/admin/*` - Admin management
- `/instructor/*` - Instructor functions
- `/student/*` - Student functions

## Testing

Run tests: `pytest`

## Deployment

The app is production-ready with Docker and can be deployed to any cloud platform supporting containers.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes and add tests
4. Submit a pull request

## License

MIT License
