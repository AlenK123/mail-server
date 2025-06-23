### Usage

The `aman_mail` package provides a CLI tool to run in either `server` or `client` mode. Below are the details for each mode:

---

### Server Mode

Use the `server` mode to start the SMTP proxy server.

```bash
python -m aman_mail.cli server <host> <port> \
    --routing-path <path_to_routing_config>
```

**Arguments:**
- `<host>`: The IPv4 address to bind the server to.
- `<port>`: The port number to bind the server to.
- `--routing-path`: The path to the routing configuration file (required). The file must be in JSON format.

**Example:**

```bash
python -m aman_mail.cli server 127.0.0.1 2525 \
    --routing-path "./routing_config.json"
```

**Routing Configuration Example:**

The routing configuration file should be in JSON format and define how emails are routed. Below is an example:

```json
{
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
            "username": "test@example.com",
            "password": "example_password",
        },
    }
}
```

---

### Client Mode

Use the `client` mode to send emails through the SMTP proxy server.

```bash
python -m aman_mail.cli client <host> <port> \
    --from-address <sender_email> \
    --to-address <recipient_emails> \
    --subject "<email_subject>" \
    --content "<email_body>" \
    [--secret <auth_secret>] \
    [--tls <true_or_false>]
```

**Arguments:**
- `<host>`: The hostname of the SMTP proxy server.
- `<port>`: The port of the SMTP proxy server.
- `--from-address`: The sender's email address (required).
- `--to-address`: One or more recipient email addresses (required).
- `--subject`: The subject of the email (required).
- `--content`: The body of the email (required).
- `--secret`: The authentication secret for the SMTP server (optional).
- `--tls`: Whether to use TLS for the connection (default: `False`).

**Example:**

```bash
python -m aman_mail.cli client 127.0.0.1 2525 \
    --from-address "sender@example.com" \
    --to-address "recipient1@example.com" "recipient2@example.com" \
    --subject "Test Email" \
    --content "This is a test email sent via the SMTP proxy." \
    --tls True
```

---

### Notes

- Ensure the routing configuration file exists and is in valid JSON format when using `server` mode.
- Ensure the SMTP proxy server is running before using the `client` mode.
- The `client` mode requires valid email addresses and an accessible SMTP proxy server.