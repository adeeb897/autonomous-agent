import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content
import os

class SendGridEmailSender:
    def __init__(self):
        self.sg = sendgrid.SendGridAPIClient(api_key=os.getenv('SENDGRID_API_KEY'))

    def send_email(self, from_email, to_email, subject, content):
        from_email = Email(from_email)
        to_email = To(to_email)
        content = Content("text/plain", content)
        mail = Mail(from_email, to_email, subject, content)
        
        try:
            response = self.sg.send(mail)
            print(f"Email sent, status code: {response.status_code}")
        except Exception as e:
            print(f"Error sending email: {e}")

# Usage example
# email_sender = SendGridEmailSender()
# email_sender.send_email("from@example.com", "to@example.com", "Subject", "Email content")
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

class SESEmailSender:
    def __init__(self):
        self.client = boto3.client('ses', region_name='us-west-2')

    def send_email(self, from_email, to_email, subject, body):
        try:
            response = self.client.send_email(
                Source=from_email,
                Destination={'ToAddresses': [to_email]},
                Message={
                    'Subject': {'Data': subject},
                    'Body': {'Text': {'Data': body}}
                }
            )
            print(f"Email sent, Message ID: {response['MessageId']}")
        except (NoCredentialsError, PartialCredentialsError) as e:
            print(f"Credential error: {e}")
        except Exception as e:
            print(f"Error sending email: {e}")

# Usage example
# ses_email_sender = SESEmailSender()
# ses_email_sender.send_email("from@example.com", "to@example.com", "Subject", "Email content")
