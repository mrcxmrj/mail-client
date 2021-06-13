import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from bs4 import BeautifulSoup as bs

def sendEmail(email, password, to, subject, body_html, attachments=[]):
    msg = MIMEMultipart("alternative")
    msg["From"] = email
    msg["To"] = to
    msg["Subject"] = subject

    body_text = bs(body_html, "html.parser").text

    text_part = MIMEText(body_text, "plain")
    html_part = MIMEText(body_html, "html")

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

    # initialize the SMTP server
    server = smtplib.SMTP("smtp.gmail.com", 587)
    # connect to the SMTP server as TLS mode (secure) and send EHLO
    server.starttls()
    # login to the account using the credentials
    server.login(email, password)
    # send the email
    server.sendmail(msg["From"], msg["To"], msg.as_string())
    # terminate the SMTP session
    server.quit()
    print("Message sent!")

#sendEmail("mock60288@gmail.com", "mailclient123", "nokehec532@moxkid.com", "New messageasdfasdfasdfdsa", "New message <b>test</b>", ["attachments/text.txt", "attachments/image.jpg"])