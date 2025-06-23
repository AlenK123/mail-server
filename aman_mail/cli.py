"""
Use argparse to create a command line interface for the aman_mail package.
This CLI will allow users to start the SMTP proxy server with custom parameters.
"""

import argparse
from enum import Enum
import json
import os
from .server import run_mail_proxy
from .client import send_via_proxy


class Mode(str, Enum):
    CLIENT = "client"
    SERVER = "server"

    def __str__(self):
        return self.value


def main():

    # First parser: only get mode
    initial_parser = argparse.ArgumentParser(
        description="Client/Server App", add_help=False
    )
    initial_parser.add_argument(
        "mode", type=Mode, choices=list(Mode), help="Mode to run: client or server"
    )
    args_partial, remaining_argv = initial_parser.parse_known_args()

    # Full parser
    parser = argparse.ArgumentParser(parents=[initial_parser])

    # Shared args
    parser.add_argument("host", type=str, help="IPv4 address")
    parser.add_argument("port", type=int, help="Port number")

    # Mode-specific args
    if args_partial.mode == Mode.CLIENT:
        parser.add_argument(
            "--from-address", type=str, required=True, help="Sender email address"
        )
        parser.add_argument(
            "--to-address", nargs="+", required=True, help="Recipient email addresses"
        )
        parser.add_argument("--subject", type=str, required=True, help="Email subject")
        parser.add_argument("--content", type=str, required=True, help="Email content")
        parser.add_argument(
            "--secret", type=str, required=False, help="Authentication secret"
        )
        parser.add_argument(
            "--tls",
            type=bool,
            required=False,
            default=False,
            help="Use TLS for the connection (default: False)",
        )

    elif args_partial.mode == Mode.SERVER:
        parser.add_argument(
            "--routing-path",
            type=str,
            required=True,
            help="Path to routing config file",
        )

    # Parse all args
    args = parser.parse_args()

    # Example logic
    if args.mode == Mode.CLIENT:

        print(f"[CLIENT] From: {args.from_address} → To: {args.to_address}")
        send_via_proxy(
            host=args.host,
            port=args.port,
            from_address=args.from_address,
            to_address=args.to_address,
            subject=args.subject,
            content=args.content,
            secret=args.secret,
            tls=args.tls,
        )
    elif args.mode == Mode.SERVER:
        if not os.path.exists(args.routing_path):
            parser.error(f"Routing path '{args.routing_path}' does not exist")

        with open(args.routing_path, "r") as f:

            routing_config = json.loads(
                f.read()
            )  # Assuming the routing config is in JSON format
            run_mail_proxy(hostname=args.host, port=args.port, routing=routing_config)
        print(f"[SERVER] Routing from: {args.routing_path}")


if __name__ == "__main__":
    main()
