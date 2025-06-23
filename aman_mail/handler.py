import asyncio
from itertools import chain
import smtplib
from email.message import EmailMessage, Message
from email import message_from_bytes
from aiosmtpd.handlers import AsyncMessage
from .util import recreate_email_message
from .route import RouteController


class ProxySMTPHandler(AsyncMessage):
    route_controller: RouteController

    def __init__(self, route_controller: RouteController):
        """
        Initializes the ProxySMTPHandler with a RouteController instance.
        :param route_controller: An instance of RouteController to manage routing.
        """
        super().__init__()
        self.route_controller = route_controller

    async def handle_message(self, message: Message):
        # Get recipient addresses
        recipients = message.get_all("To", [])
        if isinstance(recipients, str):
            recipients = [recipients]

        elif isinstance(recipients, list):
            recipients = list(chain.from_iterable([x.split(", ") for x in recipients]))

        for recipient in recipients:
            host, port = self.route_controller.get_route_endpoint(recipient)
            outbound_auth = self.route_controller.get_route_outbound_auth(recipient)
            print(f"Forwarding to: {host} for {recipient}")
            await self.send_mail(host, port, outbound_auth, message, recipient)

    async def send_mail(self, host, port, outbound_auth, message, recipient):
        loop = asyncio.get_event_loop()

        def send():
            with smtplib.SMTP(host, port) as smtp:
                smtp.ehlo()
                if outbound_auth:
                    outbound_user = outbound_auth.get("username")
                    outbound_pass = outbound_auth.get("password")
                    if outbound_user and outbound_pass:
                        smtp.starttls()
                        smtp.login(user=outbound_user, password=outbound_pass)

                smtp.send_message(
                    message, from_addr=message.get("From"), to_addrs=[recipient]
                )

        await loop.run_in_executor(None, send)


class ProxyWatermarkHandler(ProxySMTPHandler):
    def __init__(self, route_controller, watermark: str):
        super().__init__(route_controller)
        self.watermark = watermark

    async def handle_DATA(self, server, session, envelope):
        msg = recreate_email_message(message_from_bytes(envelope.content))

        assert isinstance(msg, EmailMessage)

        # Modify the body (example: replace body with custom text)
        if msg.is_multipart():
            # For multipart, replace the payload of the first part (simplified)
            content = ""
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    content += part.get_content()

        else:
            content = msg.get_content()

        if msg.get_content_type() == "text/plain":
            msg.set_content(f"{content}\n\n{self.watermark}")
            envelope.content = msg.as_bytes()

        return await super().handle_DATA(server, session, envelope)
