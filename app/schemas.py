from pydantic import BaseModel, EmailStr
from typing import Optional


# User creation schema
class UserCreate(BaseModel):
    email: EmailStr
    password: str


# User login schema
class UserLogin(BaseModel):
    email: str
    password: str


# Authentication token schema
class Token(BaseModel):
    access_token: str
    token_type: str


# Organization creation schema
class OrganizationCreate(BaseModel):
    name: str
    personal: Optional[bool] = False
    settings: Optional[dict] = {}


# Schema for inviting a member to an organization
class InviteMember(BaseModel):
    email: EmailStr
    org_name: str


# Schema for user password reset
class UserResetPassword(BaseModel):
    email: EmailStr
    new_password: str


# Schema for deleting a member from an organization
class DeleteMember(BaseModel):
    org_name: str
    user_email: EmailStr


# Schema for updating a member's role in an organization
class UpdateMemberRole(BaseModel):
    org_name: str
    user_email: EmailStr
    new_role: str


# Generic email data schema
class EmailData(BaseModel):
    to: EmailStr
    subject: str
    body: str


# Schema for sending an invite email
class SendInviteEmail(BaseModel):
    email: EmailStr
    invite_link: str


# Schema for login alert email
class LoginAlert(BaseModel):
    email: EmailStr
    login_details: str


# Schema for sending a password update email
class SendPasswordUpdateEmail(BaseModel):
    email: EmailStr