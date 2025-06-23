from email.message import Message, EmailMessage


def recreate_email_message(old_msg: Message) -> EmailMessage:
    new_msg = EmailMessage()

    # Copy headers (except some internal ones if needed)
    for key, value in old_msg.items():
        new_msg[key] = value

    # Copy content/payload
    if old_msg.is_multipart():
        # For multipart, recursively copy each part
        for part in old_msg.iter_parts():
            new_part = recreate_email_message(part)  # recursive copy
            new_msg.attach(new_part)
    else:
        # For simple payloads

        content = old_msg.get_payload()
        maintype = old_msg.get_content_maintype()
        subtype = old_msg.get_content_subtype()
        charset = old_msg.get_content_charset()

        if maintype == "text":
            # Preserve charset if possible
            if charset:
                new_msg.set_content(content, subtype=subtype, charset=charset)
            else:
                new_msg.set_content(content, subtype=subtype)
        else:
            # For non-text payloads (e.g., attachments)
            payload = old_msg.get_payload(decode=True)
            content_type = old_msg.get_content_type()
            new_msg.add_attachment(
                payload,
                maintype=old_msg.get_content_maintype(),
                subtype=old_msg.get_content_subtype(),
                filename=old_msg.get_filename(),
            )

    # Copy other headers or flags if necessary here

    return new_msg
