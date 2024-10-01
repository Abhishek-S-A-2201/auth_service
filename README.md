# Auth Service

This project is an authentication service built with FastAPI, providing user management, organization handling, email notifications, and job queue management for background tasks.

## Features

- User authentication (sign up, sign in)
- Organization management
- Role-based access control
- Member invitation and management
- Password reset functionality
- Email notifications (using Brevo/SendinBlue and Resend)
- **Job queue for background email tasks (using Redis and RQ)**
- Statistics for user and organization data

## Tech Stack

- FastAPI
- SQLAlchemy
- Alembic (for database migrations)
- PostgreSQL
- Pydantic
- JWT for authentication
- SendGrid, Brevo, and Resend for email services
- **Redis and RQ for job queuing and background tasks**

## Project Structure

The main components of the project are:

- `app/main.py`: Entry point of the application
- `app/models.py`: SQLAlchemy models
- `app/schemas.py`: Pydantic schemas for request/response validation
- `app/crud.py`: CRUD operations
- `app/auth_utils.py`: Authentication utilities
- `app/dependencies.py`: Dependency injection
- **`app/queues.py`: Job queuing utilities and background task management**
- `app/routers/`: API routes
- `alembic/`: Database migration files

## Setup

### Prerequisites

- PostgreSQL installed and running
- Redis installed and running for job queuing
  - Install Redis:
    ```
    sudo apt-get install redis-server
    ```
  - Start Redis:
    ```
    redis-server
    ```

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
5. **Run the Redis worker to process background jobs**:
   ```
   rq worker --with-scheduler
   ```
6. Start the server:
   ```
   uvicorn app.main:app --reload
   ```

## API Endpoints

- `/auth/signup`: User registration
- `/auth/signin`: User login
- `/auth/reset_password`: Password reset
- `/member/invite`: Invite a member to an organization (queued email job)
- `/member/delete`: Remove a member from an organization
- `/member/update_role`: Update a member's role
- `/stats/`: Various statistics endpoints
- **`/email/`: Email notification and queue-related endpoints**
  - `/email/send-invite`: Send an invitation email via a queued job
  - `/email/send-password-update`: Send password update notification
  - `/email/send-login-alert`: Send a login alert notification
  - `/email/queue`: View current queue and job statuses

For detailed API documentation, visit `/docs` after starting the server.

## Testing

The project includes a Postman collection for API testing.

## Database

The project uses PostgreSQL. The database schema is defined in `models.py`.
