# from fastapi import HTTPException
# from app.models import EmailTemplate
# from app.schemas import EmailModel
# from app.settings import SMTP_SERVER, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD
# import smtplib
# from email.mime.text import MIMEText

# def send_email_via_smtp(email: str, subject: str, message: str):
#     msg = MIMEText(message, 'html')
#     msg['Subject'] = subject
#     msg['From'] = SMTP_USERNAME
#     msg['To'] = email

#     try:
#         with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
#             server.login(SMTP_USERNAME, SMTP_PASSWORD)
#             server.sendmail(SMTP_USERNAME, [email], msg.as_string())
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# def send_custom_notification(email: str, subject: str, message: str):
#     send_email_via_smtp(email, subject, message)

# def send_notification_via_template(email_details: EmailModel, notification_func_map: dict):
#     notification_func = notification_func_map.get(email_details.notification_type)
#     if notification_func:
#         notification_func(email_details.email)
#     else:
#         raise HTTPException(status_code=404, detail="Invalid notification type")


# from fastapi import HTTPException
# from app.models import EmailTemplate
# from app.schemas import EmailModel
# from app.settings import SMTP_SERVER, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD
# import smtplib
# from email.mime.text import MIMEText

# def send_email_via_smtp(email: str, subject: str, message: str):
#     msg = MIMEText(message, 'html')
#     msg['Subject'] = subject
#     msg['From'] = SMTP_USERNAME
#     msg['To'] = email

#     try:
#         with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
#             server.login(SMTP_USERNAME, SMTP_PASSWORD)
#             server.sendmail(SMTP_USERNAME, [email], msg.as_string())
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# def send_custom_notification(email: str, subject: str, message: str):
#     send_email_via_smtp(email, subject, message)

# def send_notification_via_template(email_details: EmailModel, notification_func_map: dict):
#     notification_func = notification_func_map.get(email_details.notification_type)
#     if notification_func:
#         notification_func(email_details.email)
#     else:
#         raise HTTPException(status_code=404, detail="Invalid notification type")

# # Define notification_func_map
# notification_func_map = {
#     "custom": send_custom_notification,
#     # Add other notification types and their corresponding functions here
# }



from fastapi import HTTPException
from app.models import EmailTemplate
from app.schemas import EmailModel
from app.settings import SMTP_SERVER, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD
import smtplib
from email.mime.text import MIMEText
import logging

logger = logging.getLogger(__name__)

def send_email_via_smtp(email: str, subject: str, message: str):
    msg = MIMEText(message, 'html')
    msg['Subject'] = subject
    msg['From'] = SMTP_USERNAME
    msg['To'] = email

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(SMTP_USERNAME, [email], msg.as_string())
    except smtplib.SMTPException as e:
        logger.error(f"SMTPException: {e}")
        raise HTTPException(status_code=500, detail="SMTP error occurred")
    except Exception as e:
        logger.error(f"Exception: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

def send_custom_notification(email: str, subject: str, message: str):
    send_email_via_smtp(email, subject, message)

def send_notification_via_template(email_details: EmailModel, notification_func_map: dict):
    notification_func = notification_func_map.get(email_details.notification_type)
    if notification_func:
        notification_func(email_details.email)
    else:
        raise HTTPException(status_code=404, detail="Invalid notification type")

# Define notification_func_map
notification_func_map = {
    "custom": send_custom_notification,
    # Add other notification types and their corresponding functions here
}