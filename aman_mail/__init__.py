"""Top-level package for aman_mail."""

from .handler import ProxySMTPHandler, ProxyWatermarkHandler
from .auth import Authenticator
from .route import RouteController
from .server import run_mail_proxy

__all__ = [
    "ProxySMTPHandler",
    "ProxyWatermarkHandler",
    "Authenticator",
    "RouteController",
    "run_mail_proxy",
]

__author__ = """Segel"""
__email__ = "segel@segel.com"
__version__ = "0.1.0"
