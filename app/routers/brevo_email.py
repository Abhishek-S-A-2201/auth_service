from fastapi import APIRouter, HTTPException
from sib_api_v3_sdk import Configuration, ApiClient, TransactionalEmailsApi, SendSmtpEmail
from pydantic import EmailStr
import os
from dotenv import load_dotenv
from .. import schemas

load_dotenv()

router = APIRouter()

# Configure Brevo API client
configuration = Configuration()
configuration.api_key['api-key'] = os.environ.get('BREVO_API_KEY')
api_instance = TransactionalEmailsApi(ApiClient(configuration))


@router.post("/email/send-invite")
async def send_invite_email(send_invite_email: schemas.SendInviteEmail):
    try:
        subject = "Welcome! Activate your account"
        html_content = f"<p>Welcome! Click <a href='{send_invite_email.invite_link}'>here</a> to activate your account.</p>"
        sender = {
            "name": "Abhishek S A",
            "email": os.getenv('FROM_EMAIL')
        }
        if not sender["email"]:
            raise ValueError("FROM_EMAIL environment variable is not set")

        to = [{"email": send_invite_email.email}]

        send_smtp_email = SendSmtpEmail(
            to=to,
            html_content=html_content,
            sender=sender,
            subject=subject
        )
        response = api_instance.send_transac_email(send_smtp_email)

        return {"message": "Invite email sent successfully", "message_id": response.message_id}
    except ValueError as ve:
        raise HTTPException(status_code=500, detail=str(ve))
    except Exception as e:
        if e.status == 400:
            raise HTTPException(
                status_code=400, detail=f"Bad Request: {e.body}")
        elif e.status == 401:
            raise HTTPException(
                status_code=401, detail="Unauthorized: Invalid API key")
        raise HTTPException(status_code=500, detail=f"API error: {str(e)}")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Unexpected error: {str(e)}")


@router.post("/email/send-password-update")
async def send_password_update_email(send_password_update_email: schemas.SendPasswordUpdateEmail):
    try:
        subject = "Password Update Alert"
        html_content = "<p>Your password has been updated. If you didn't make this change, please contact support immediately.</p>"
        sender = {"name": "Abhishek S A",
                  "email": os.environ.get('FROM_EMAIL')}
        to = [{"email": send_password_update_email.email}]

        send_smtp_email = SendSmtpEmail(
            to=to, html_content=html_content, sender=sender, subject=subject)
        response = api_instance.send_transac_email(send_smtp_email)

        return {"message": "Password update email sent successfully", "message_id": response.message_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/email/send-login-alert")
async def send_login_alert_email(login_alert: schemas.LoginAlert):
    try:
        subject = "New Login Detected"
        html_content = f"<p>A new login was detected for your account. Details: {login_alert.login_details}</p>"
        sender = {"name": "Abhishek S A",
                  "email": os.environ.get('FROM_EMAIL')}
        to = [{"email": login_alert.email}]

        send_smtp_email = SendSmtpEmail(
            to=to, html_content=html_content, sender=sender, subject=subject)
        response = api_instance.send_transac_email(send_smtp_email)

        return {"message": "Login alert email sent successfully", "message_id": response.message_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
