from .route import RouteController
from .auth import Authenticator
from .handler import ProxyWatermarkHandler
from aiosmtpd.controller import Controller

ROUTING = {
    "gmail.com": {
        "host": "smtp.gmail.com",
        "port": 587,
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
        "host": "smtp.example.com",
        "port": 587,
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


def run_mail_proxy(
    hostname: str = "127.0.0.1", port: int = 1025, routing: dict = ROUTING
):
    """Starts the SMTP proxy server with the specified routing configuration."""
    route_controller = RouteController(routing=routing)
    handler = ProxyWatermarkHandler(route_controller)
    authenticator = Authenticator(route_controller)

    controller = Controller(
        handler=handler,
        hostname=hostname,
        port=port,
        auth_require_tls=False,
        authenticator=authenticator,
    )
    controller.start()
    print(f"SMTP proxy running on {hostname}:{port}")
    try:
        while True:
            pass
    except KeyboardInterrupt:
        controller.stop()


if __name__ == "__main__":
    run_mail_proxy()
