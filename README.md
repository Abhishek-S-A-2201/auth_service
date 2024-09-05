# Auth Service

This project is an authentication service built with FastAPI, providing user management, organization handling, and email notifications.

## Features

- User authentication (sign up, sign in)
- Organization management
- Role-based access control
- Member invitation and management
- Password reset functionality
- Email notifications (using Brevo/SendinBlue and Resend)
- Statistics for user and organization data

## Tech Stack

- FastAPI
- SQLAlchemy
- Alembic (for database migrations)
- PostgreSQL
- Pydantic
- JWT for authentication
- SendGrid, Brevo, and Resend for email services

## Project Structure

The main components of the project are:

- `app/main.py`: Entry point of the application
- `app/models.py`: SQLAlchemy models
- `app/schemas.py`: Pydantic schemas for request/response validation
- `app/crud.py`: CRUD operations
- `app/auth_utils.py`: Authentication utilities
- `app/dependencies.py`: Dependency injection
- `app/routers/`: API routes
- `alembic/`: Database migration files

## Setup

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set up environment variables in a `.env` file (see `.env.example` for required variables)
4. Run database migrations:
   ```
   alembic upgrade head
   ```
5. Start the server:
   ```
   uvicorn app.main:app --reload
   ```

## API Endpoints

- `/auth/signup`: User registration
- `/auth/signin`: User login
- `/auth/reset_password`: Password reset
- `/member/invite`: Invite a member to an organization
- `/member/delete`: Remove a member from an organization
- `/member/update_role`: Update a member's role
- `/stats/`: Various statistics endpoints
- `/email/`: Email notification endpoints

For detailed API documentation, visit `/docs` after starting the server.

## Testing

The project includes a Postman collection for API testing.

## Database

The project uses PostgreSQL. The database schema is defined in models.py
