from sender import sendEmail
from viewer import downloadEmails

class User:
    def __init__(self, email, password):
        self.email = email
        self.password = password

    def send(self, to, subject, body_html, attachments=[]):
        sendEmail(self.email, self.password, to, subject, body_html, attachments)

    def view(self, quantity):
        # emails can be viewed by parsing received folder
        downloadEmails(self.email, self.password, quantity)
