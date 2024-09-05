
from fastapi import FastAPI
from .routers import auth, member, brevo_email, stats
from .database import engine, Base

# Initialize FastAPI app
app = FastAPI()

# Include routers
app.include_router(auth.router)
app.include_router(member.router)
app.include_router(stats.router)
app.include_router(brevo_email.router)

# Create database tables
Base.metadata.create_all(bind=engine)
