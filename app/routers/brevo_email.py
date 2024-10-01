from fastapi import APIRouter, HTTPException
from sib_api_v3_sdk import Configuration, ApiClient, TransactionalEmailsApi, SendSmtpEmail
from rq.registry import StartedJobRegistry, FinishedJobRegistry, FailedJobRegistry
import os
from dotenv import load_dotenv
from .. import schemas
from redis import Redis
from rq import Queue, Retry
from rq.job import Job
import time

load_dotenv()

router = APIRouter()

# Configure Brevo API client
configuration = Configuration()
configuration.api_key['api-key'] = os.environ.get('BREVO_API_KEY')
api_instance = TransactionalEmailsApi(ApiClient(configuration))

try:
    redis_conn = Redis(host='localhost', port=6379, db=0)
    redis_conn.ping()
    print("Connected to Redis successfully!")
except Exception as e:
    print(f"Redis connection error: {e}")

queue = Queue(connection=redis_conn)


def send_email(send_invite_email: schemas.SendInviteEmail):
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


@router.post("/email/send-invite")
async def send_invite_email(send_invite_email: schemas.SendInviteEmail):
    try:
        job = queue.enqueue(
            send_email,
            send_invite_email,
            description="Send email invite using Brevo",
            retry=Retry(max=3, interval=[10, 30, 60]),
        )
        return {"message": "Email send job added to the queue", "job_id": job.get_id()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Queue error: {str(e)}")


@router.get("/email/queue")
def get_all_jobs():
    jobs = []

    # Fetch jobs that are currently queued (waiting to be executed)
    queued_jobs = queue.jobs
    for job in queued_jobs:
        jobs.append({
            'id': job.get_id(),
            'description': job.description,
            'status': job.get_status(),
            'function': job.func_name,
            'args': job.args
        })

    # Fetch running jobs from the StartedJobRegistry
    running_jobs = StartedJobRegistry(queue=queue).get_job_ids()
    for job_id in running_jobs:
        job = Job.fetch(job_id, connection=queue.connection)
        jobs.append({
            'id': job.get_id(),
            'description': job.description,
            'status': job.get_status(),
            'function': job.func_name,
            'args': job.args
        })

    # Fetch finished jobs from the FinishedJobRegistry
    finished_jobs = FinishedJobRegistry(queue=queue).get_job_ids()
    for job_id in finished_jobs:
        job = Job.fetch(job_id, connection=queue.connection)
        jobs.append({
            'id': job.get_id(),
            'description': job.description,
            'status': job.get_status(),
            'function': job.func_name,
            'args': job.args
        })

    # Fetch failed jobs from the FailedJobRegistry
    failed_jobs = FailedJobRegistry(queue=queue).get_job_ids()
    for job_id in failed_jobs:
        job = Job.fetch(job_id, connection=queue.connection)
        jobs.append({
            'id': job.get_id(),
            'description': job.description,
            'status': job.get_status(),
            'function': job.func_name,
            'args': job.args
        })

    return {"jobs": jobs}


@router.post("/email/send-password-update")
async def send_password_update_email(send_password_update_email: schemas.SendPasswordUpdateEmail):
    try:
        job = queue.enqueue(
            send_password_update_email_task,
            send_password_update_email,
            description="Send password update email",
            retry=Retry(max=3, interval=[10, 30, 60]),
        )
        return {"message": "Password update email job added to the queue", "job_id": job.get_id()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Queue error: {str(e)}")


def send_password_update_email_task(send_password_update_email: schemas.SendPasswordUpdateEmail):
    try:
        subject = "Password Update Alert"
        html_content = "<p>Your password has been updated. If you didn't make this change, please contact support immediately.</p>"
        sender = {"name": "Abhishek S A",
                  "email": os.environ.get('FROM_EMAIL')}
        if not sender["email"]:
            raise ValueError("FROM_EMAIL environment variable is not set")

        to = [{"email": send_password_update_email.email}]

        send_smtp_email = SendSmtpEmail(
            to=to, html_content=html_content, sender=sender, subject=subject)
        response = api_instance.send_transac_email(send_smtp_email)

        return {"message": "Password update email sent successfully", "message_id": response.message_id}
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


@router.post("/email/send-login-alert")
async def send_login_alert_email(login_alert: schemas.LoginAlert):
    try:
        job = queue.enqueue(
            send_login_alert_email_task,
            login_alert,
            description="Send login alert email",
            retry=Retry(max=3, interval=[10, 30, 60]),
        )
        return {"message": "Login alert email job added to the queue", "job_id": job.get_id()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Queue error: {str(e)}")


def send_login_alert_email_task(login_alert: schemas.LoginAlert):
    try:
        subject = "New Login Detected"
        html_content = f"<p>A new login was detected for your account. Details: {login_alert.login_details}</p>"
        sender = {"name": "Abhishek S A",
                  "email": os.environ.get('FROM_EMAIL')}
        if not sender["email"]:
            raise ValueError("FROM_EMAIL environment variable is not set")

        to = [{"email": login_alert.email}]

        send_smtp_email = SendSmtpEmail(
            to=to, html_content=html_content, sender=sender, subject=subject)
        response = api_instance.send_transac_email(send_smtp_email)

        return {"message": "Login alert email sent successfully", "message_id": response.message_id}
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
