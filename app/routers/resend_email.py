from fastapi import APIRouter, HTTPException
import resend
from pydantic import EmailStr
from .. import schemas
from dotenv import load_dotenv
import os

load_dotenv()


router = APIRouter()
resend.api_key = os.environ["RESEND_API_KEY"]


@router.post("/email/send-invite")
async def send_invite_email(send_invite_email: schemas.SendInviteEmail):
    try:
        response = resend.Emails.send({
            "from": os.getenv("EMAIL_FROM"),
            "to": send_invite_email.email,
            "subject": "Welcome! Activate your account",
            "html": f"<p>Welcome! Click <a href='{send_invite_email.invite_link}'>here</a> to activate your account.</p>"
        })
        return {"message": "Invite email sent successfully", "email_id": response["id"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/email/send-password-update")
async def send_password_update_email(email: EmailStr):
    try:
        response = resend.Emails.send({
            "from": os.getenv("EMAIL_FROM"),
            "to": email,
            "subject": "Password Update Alert",
            "html": "<p>Your password has been updated. If you didn't make this change, please contact support immediately.</p>"
        })
        return {"message": "Password update email sent successfully", "email_id": response["id"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/email/send-login-alert")
async def send_login_alert_email(login_alert: schemas.LoginAlert):
    try:
        response = resend.Emails.send({
            "from": os.getenv("EMAIL_FROM"),
            "to": login_alert.email,
            "subject": "New Login Detected",
            "html": f"<p>A new login was detected for your account. Details: {login_alert.login_details}</p>"
        })
        return {"message": "Login alert email sent successfully", "email_id": response["id"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
