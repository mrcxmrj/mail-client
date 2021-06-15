import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from bs4 import BeautifulSoup as bs


def send_email(smtp_server, email, to, subject, text, attachments):
    msg = MIMEMultipart("alternative")
    msg["From"] = email
    msg["To"] = to
    msg["Subject"] = subject

    body_text = bs(text, "html.parser").text

    text_part = MIMEText(body_text, "plain")
    html_part = MIMEText(text, "html")

    msg.attach(text_part)
    msg.attach(html_part)

    # process attachments
    for file in attachments:
        with open(file, "rb") as f:
                attach_part = MIMEBase("application", "octet-stream")
                attach_part.set_payload(f.read())
                
        encoders.encode_base64(attach_part)
    
        attach_part.add_header("Content-Disposition", f"attachment; filename= {file}")
        msg.attach(attach_part)

    # send the email
    smtp_server.sendmail(msg["From"], msg["To"], msg.as_string())