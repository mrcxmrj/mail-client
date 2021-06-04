import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from bs4 import BeautifulSoup as bs

class Sender:
    def __init__(self, email, password):
        self.email = email
        self.password = password

    def new_mail(self, to, subject, body_html, attachments=[]):
        self.msg = MIMEMultipart("alternative")
        self.msg["From"] = self.email
        self.msg["To"] = to
        self.msg["Subject"] = subject

        body_text = bs(body_html, "html.parser").text

        text_part = MIMEText(body_text, "plain")
        html_part = MIMEText(body_html, "html")
        
        self.msg.attach(text_part)
        self.msg.attach(html_part)

        for file in attachments:
            with open(file, "rb") as f:
                    attach_part = MIMEBase("application", "octet-stream")
                    attach_part.set_payload(f.read())
                    
            encoders.encode_base64(attach_part)
        
            attach_part.add_header("Content-Disposition", f"attachment; filename= {file}")
            self.msg.attach(attach_part)

    def send_mail(self):
        if not hasattr(self, 'msg'):
            print("Message hasn't been defined")
            return

        # initialize the SMTP server
        server = smtplib.SMTP("smtp.gmail.com", 587)
        # connect to the SMTP server as TLS mode (secure) and send EHLO
        server.starttls()
        # login to the account using the credentials
        server.login(self.email, self.password)
        # send the email
        server.sendmail(self.msg["From"], self.msg["To"], self.msg.as_string())
        # terminate the SMTP session
        server.quit()
        print("Message sent!")


sender = Sender("mock60288@gmail.com", "mailclient123")
sender.new_mail("xojicej620@revutap.com", "New message", "New message <b>test</b>", ["attachments/text.txt", "attachments/image.jpg"])
sender.send_mail()
