from sqlalchemy import Column, Integer, String, Boolean, JSON, ForeignKey, BigInteger
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from .database import Base


# Organization model representing a company or group
class Organization(Base):
    __tablename__ = 'organization'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    status = Column(Integer, default=0, nullable=False)  # e.g., 0: active, 1: inactive
    personal = Column(Boolean, default=False, nullable=True)  # Whether it's a personal organization
    settings = Column(JSON, default={}, nullable=True)  # Custom settings for the organization
    created_at = Column(BigInteger, nullable=True)  # Timestamp of creation
    updated_at = Column(BigInteger, nullable=True)  # Timestamp of last update


# User model representing individual users of the system
class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)  # Hashed password
    profile = Column(JSON, default={}, nullable=False)  # User profile information
    status = Column(Integer, default=0, nullable=False)  # e.g., 0: active, 1: inactive
    settings = Column(JSON, default={}, nullable=True)  # User-specific settings
    created_at = Column(BigInteger, nullable=True)  # Timestamp of account creation
    updated_at = Column(BigInteger, nullable=True)  # Timestamp of last update


# Role model defining different roles within an organization
class Role(Base):
    __tablename__ = 'role'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)  # Name of the role (e.g., "Admin", "Member")
    description = Column(String, nullable=True)  # Description of the role's responsibilities
    org_id = Column(Integer, ForeignKey('organization.id',
                    ondelete='CASCADE'), nullable=False)  # Organization this role belongs to


# Member model representing the association between users, organizations, and roles
class Member(Base):
    __tablename__ = 'member'
    id = Column(Integer, primary_key=True, index=True)
    org_id = Column(Integer, ForeignKey('organization.id',
                    ondelete='CASCADE'), nullable=False)  # Organization the member belongs to
    user_id = Column(Integer, ForeignKey(
        'user.id', ondelete='CASCADE'), nullable=False)  # User associated with this membership
    role_id = Column(Integer, ForeignKey(
        'role.id', ondelete='CASCADE'), nullable=False)  # Role of the user in this organization
    status = Column(Integer, default=0, nullable=False)  # e.g., 0: active, 1: inactive
    settings = Column(JSON, default={}, nullable=True)  # Member-specific settings
    created_at = Column(BigInteger, nullable=True)  # Timestamp of membership creation
    updated_at = Column(BigInteger, nullable=True)  # Timestamp of last update
