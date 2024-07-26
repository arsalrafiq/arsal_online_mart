# from fastapi import APIRouter, Depends, HTTPException
# from app.schemas import EmailModel
# from app.service import send_custom_notification, send_notification_via_template, notification_func_map
# from app.models import EmailTemplate

# router = APIRouter()

# @router.post("/send_custom_notification")
# def send_custom_notification(email: str, subject: str, message: str):
#     send_custom_notification(email, subject, message)
#     return {"detail": "Email sent successfully"}

# @router.post("/send_notification_via_template")
# def send_notification_via_template(email_details: EmailModel):
#     try:
#         send_notification_via_template(email_details, notification_func_map)
#         return {"detail": "Email sent successfully"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

from fastapi import APIRouter
from app.service import send_custom_notification as send_custom_notification_service, send_notification_via_template, notification_func_map
from app.schemas import EmailModel

router = APIRouter()

@router.post("/send_custom_notification")
def send_custom_notification(email: str, subject: str, message: str):
    send_custom_notification_service(email, subject, message)
    return {"message": "Notification sent"}

@router.post("/send_notification_via_template")
def send_notification_via_template_route(email_details: EmailModel):
    send_notification_via_template(email_details, notification_func_map)
    return {"message": "Notification sent"}

