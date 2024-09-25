import sendgrid
from sendgrid.helpers.mail import Mail
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmailAPI:
    def __init__(self, sendgrid_api_key, aws_access_key, aws_secret_key):
        self.sg = sendgrid.SendGridAPIClient(api_key=sendgrid_api_key)
        self.ses_client = boto3.client(
            'ses',
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            region_name='us-east-1'
        )

    def send_email_sendgrid(self, from_email, to_emails, subject, content):
        message = Mail(
            from_email=from_email,
            to_emails=to_emails,
            subject=subject,
            plain_text_content=content
        )
        try:
            response = self.sg.send(message)
            logger.info(f"SendGrid Email sent: {response.status_code}")
        except Exception as e:
            logger.error(f"SendGrid Email failed: {e}")

    def send_email_ses(self, from_email, to_emails, subject, content):
        try:
            response = self.ses_client.send_email(
                Source=from_email,
                Destination={
                    'ToAddresses': to_emails
                },
                Message={
                    'Subject': {
                        'Data': subject
                    },
                    'Body': {
                        'Text': {
                            'Data': content
                        }
                    }
                }
            )
            logger.info(f"SES Email sent: {response['MessageId']}")
        except (NoCredentialsError, PartialCredentialsError) as e:
            logger.error(f"SES Email failed due to credential error: {e}")
        except Exception as e:
            logger.error(f"SES Email failed: {e}")
