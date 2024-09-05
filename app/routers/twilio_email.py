from fastapi import APIRouter, HTTPException
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from pydantic import EmailStr
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()
sg = SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))

@router.post("/email/send-invite")
async def send_invite_email(email: EmailStr, invite_link: str):
    try:
        message = Mail(
            from_email=os.environ.get('FROM_EMAIL'),
            to_emails=email,
            subject='Welcome! Activate your account',
            html_content=f"<p>Welcome! Click <a href='{invite_link}'>here</a> to activate your account.</p>"
        )
        response = sg.send(message)
        return {"message": "Invite email sent successfully", "status_code": response.status_code}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/email/send-password-update")
async def send_password_update_email(email: EmailStr):
    try:
        message = Mail(
            from_email=os.environ.get('FROM_EMAIL'),
            to_emails=email,
            subject='Password Update Alert',
            html_content="<p>Your password has been updated. If you didn't make this change, please contact support immediately.</p>"
        )
        response = sg.send(message)
        return {"message": "Password update email sent successfully", "status_code": response.status_code}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/email/send-login-alert")
async def send_login_alert_email(email: EmailStr, login_details: str):
    try:
        message = Mail(
            from_email=os.environ.get('FROM_EMAIL'),
            to_emails=email,
            subject='New Login Detected',
            html_content=f"<p>A new login was detected for your account. Details: {login_details}</p>"
        )
        response = sg.send(message)
        return {"message": "Login alert email sent successfully", "status_code": response.status_code}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))