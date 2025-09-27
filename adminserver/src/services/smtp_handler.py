import json
import datetime
import smtplib
import email
import logging
from string import Template
from quart import render_template
import config as cfg

logger = logging.getLogger(__name__)

text_content = json.load(open("./src/templates/emails/text_content.json", "r"))


async def ship_email(message, recipient):
    logging.debug("Shipping Email...")
    with smtplib.SMTP_SSL(cfg.SMTP_SERVER, cfg.SMTP_PORT) as server:
        logging.debug("\tSSL Connection Created")
        server.login(cfg.EMAIL_ADDRESS, cfg.EMAIL_PASSWORD)
        logging.debug("\tLogin Successful")
        server.sendmail(cfg.EMAIL_ADDRESS, recipient, message.as_string())
        logging.debug("\tMessage Sent")
        return True
    return False


async def send_email(to_email, template, **context):
    logging.debug(f"Building email for template: {template}")
    if template not in text_content.keys():
        raise ValueError("The template is not defined.")
    
    html_message = await render_template(f'emails/{template}.html', **context)
    plain_message = Template(text_content[template]["text"]).substitute(**context)

    msg = email.message.EmailMessage()
    msg['From'] = cfg.EMAIL_ADDRESS
    msg['To'] = to_email
    msg["Subject"] = text_content[template]["subject"]
    msg.set_content(plain_message)
    msg.add_alternative(html_message, subtype='html')
    
    if await ship_email(msg, to_email):
        return True
    else:
        return False
    