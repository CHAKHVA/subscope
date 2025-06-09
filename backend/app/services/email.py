import logging

import boto3
from botocore.exceptions import ClientError

from app.core.config import settings

logger = logging.getLogger(__name__)


class EmailService:
    def __init__(self):
        self.ses_client = boto3.client(
            "ses",
            region_name=settings.AWS_REGION,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )

    def send_email(
        self,
        to_email: str,
        subject: str,
        body_text: str,
        body_html: str | None = None,
    ) -> bool:
        """Send email using AWS SES."""
        try:
            message = {
                "Subject": {"Data": subject},
                "Body": {"Text": {"Data": body_text}},
            }

            if body_html:
                message["Body"]["Html"] = {"Data": body_html}

            response = self.ses_client.send_email(
                Source=settings.SES_FROM_EMAIL,
                Destination={"ToAddresses": [to_email]},
                Message=message,
            )

            logger.info(
                f"Email sent successfully to {to_email}. Message ID: {response['MessageId']}"
            )
            return True

        except ClientError as e:
            logger.error(
                f"Failed to send email to {to_email}: {e.response['Error']['Message']}"
            )
            return False
        except Exception as e:
            logger.error(f"Unexpected error sending email to {to_email}: {e!s}")
            return False


email_service = EmailService()


def send_welcome_email(email: str, full_name: str) -> bool:
    """Send welcome email to new user."""
    subject = f"Welcome to {settings.PROJECT_NAME}!"

    body_text = f"""
    Hi {full_name},

    Welcome to {settings.PROJECT_NAME}! We're excited to have you on board.

    {settings.PROJECT_NAME} helps you manage your subscriptions and never miss a payment again.

    Get started by adding your first subscription in the app.

    Best regards,
    The {settings.PROJECT_NAME} Team
    """

    body_html = f"""
    <html>
    <head></head>
    <body>
        <h2>Welcome to {settings.PROJECT_NAME}!</h2>
        <p>Hi {full_name},</p>
        <p>Welcome to <strong>{settings.PROJECT_NAME}</strong>! We're excited to have you on board.</p>
        <p>{settings.PROJECT_NAME} helps you manage your subscriptions and never miss a payment again.</p>
        <p>Get started by adding your first subscription in the app.</p>
        <br>
        <p>Best regards,<br>The {settings.PROJECT_NAME} Team</p>
    </body>
    </html>
    """

    return email_service.send_email(email, subject, body_text, body_html)
