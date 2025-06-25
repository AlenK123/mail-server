#!/usr/bin/env python

"""Tests for `aman_mail` package."""

from email.message import EmailMessage
import smtplib
import pytest

from aman_mail.auth import Authenticator
from aman_mail.handler import ProxyWatermarkHandler
from aman_mail.route import RouteController
from aiosmtpd.controller import Controller

from aiosmtpd.handlers import AsyncMessage


@pytest.fixture()
def routing_data():
    return {
        "gmail.com": {
            "host": "127.0.0.1",
            "port": 1026,
            "inbound_auth": {
                "username": "test@gmail.com",
                "password": "secret",
            },
            "outbound_auth": {
                "username": "test@gmail.com",
                "password": "example_password",
            },
        },
        "example.com": {
            "host": "127.0.0.1",
            "port": 1027,
            "inbound_auth": {
                "username": "test@example.com",
                "password": "secret",
            },
            "outbound_auth": {
                "username": "proxy@example.com",
                "password": "example_password",
            },
        },
    }


@pytest.fixture()
def route_controller(routing_data):
    return RouteController(routing=routing_data)


@pytest.fixture()
def authenticator(route_controller):
    return Authenticator(route_controller=route_controller)


@pytest.fixture()
def watermark():
    return "This email was send from the intelligence coprs"


@pytest.fixture()
def handler(route_controller, watermark):
    return ProxyWatermarkHandler(route_controller=route_controller, watermark=watermark)


@pytest.fixture()
def hostname():
    return "127.0.0.1"


@pytest.fixture()
def port():
    return 1025


@pytest.fixture()
def server(handler, authenticator, hostname, port):
    controller = Controller(
        handler=handler,
        hostname=hostname,
        port=port,
        authenticator=authenticator,
        auth_require_tls=False,
    )
    controller.start()

    yield controller

    controller.stop()


@pytest.mark.parametrize(
    "routing_data",
    [
        {
            "inbound.com": {
                "inbound_auth": {
                    "username": "test@inbound.com",
                    "password": "secret",
                },
            }
        }
    ],
)
def test__inbound_authentication_incorrect_credentials(server):
    with pytest.raises(smtplib.SMTPAuthenticationError) as e:
        with smtplib.SMTP(server.hostname, server.port) as client:
            client.login("asd@inbound.com", "aasdd")
        assert isinstance(e, Exception)


@pytest.mark.parametrize(
    "routing_data",
    [
        {
            "inbound.com": {
                "inbound_auth": {
                    "username": "test@inbound.com",
                    "password": "secret",
                },
            }
        }
    ],
)
def test__inbound_authentication_correct_credentials(server):

    with smtplib.SMTP(server.hostname, server.port) as client:
        code, resp = client.login("test@inbound.com", "secret")

        assert code == 235  # SMTP authentication success code


@pytest.mark.parametrize(
    "routing_data",
    [
        {
            "e2e.com": {
                "host": "127.0.0.1",
                "port": 1028,
            }
        }
    ],
)
def test__email_proxy(server, hostname, mocker):
    class Handler(AsyncMessage):
        def handle_message(self, message):
            return super().handle_message(message)

    handler = Handler()
    spy = mocker.spy(handler, "handle_message")

    controller = Controller(
        handler=handler,
        hostname=hostname,
        port=1028,
        authenticator=authenticator,
        auth_require_tls=False,
    )
    controller.start()

    with smtplib.SMTP(server.hostname, server.port) as client:
        msg = EmailMessage()
        msg["Subject"] = "Some Subject"
        msg["From"] = "some@e2e.com"
        msg["To"] = "other@e2e.com"
        msg.set_content("Some Content")

        client.ehlo()  # Identify ourselves to
        client.send_message(msg)

    controller.stop()

    assert spy.call_count == 1


@pytest.mark.skip(reason="TODO: Implement")
def test__email_proxy_inbound_auth():
    pass


@pytest.mark.skip(reason="TODO: Implement")
def test__email_proxy_inbound_auth_outbound_auth():
    pass


@pytest.mark.skip(reason="TODO: Implement")
def test__email_proxy_with_watermark():
    pass


@pytest.mark.skip(reason="TODO: Implement")
def test__email_proxy_to_multipule_recipients():
    pass


@pytest.mark.skip(
    reason="TODO: Find authentication vulnrability, fix it and test for it."
)
def test__inbound_auth_is_secure():
    pass
