import smtplib
from email.message import EmailMessage
from typing import List, Optional, Union


def send_via_proxy(
    host: str,
    port: int,
    from_address: str,
    to_address: Union[str, List[str]],
    subject: str = "Test Email",
    content: str = "This is a test email sent through the aiosmtpd proxy",
    secret: Optional[str] = None,
    tls: bool = False,
):
    with smtplib.SMTP(host, port) as server:
        server.set_debuglevel(1)  # Shows full SMTP dialog
        if tls:
            server.starttls()
        if secret:
            server.login(from_address, secret)

        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = from_address
        msg["To"] = to_address
        msg.set_content(content)

        server.ehlo()  # Identify ourselves to
        server.send_message(msg)
        print("Email sent successfully via proxy.")


if __name__ == "__main__":
    send_via_proxy(
        "127.0.0,1",
        1025,
        "test@test.com",
        "test@test.com",
        "Some Subject",
        "Some Content",
    )
