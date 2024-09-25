from agent.email_integration import send_email

def test_sendgrid_email():
    send_email(
        service="sendgrid",
        from_email="test@example.com",
        to_email="recipient@example.com",
        subject="Test Subject",
        content="Test Content"
    )

def test_ses_email():
    send_email(
        service="ses",
        from_email="test@example.com",
        to_email="recipient@example.com",
        subject="Test Subject",
        content="Test Content"
    )

if __name__ == "__main__":
    test_sendgrid_email()
    test_ses_email()
