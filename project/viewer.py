import imaplib
import email
from email.header import decode_header
import os

# creates folder in received directory, returns path to the new folder
def createFolder(foldername):
    # clean text for creating a folder
    foldername = "".join(c if c.isalnum() else "_" for c in foldername)
    owd = os.getcwd()
    os.chdir("received")
    if not os.path.isdir(foldername):
        # make a folder for this email (named after the subject)
        os.mkdir(foldername)
    folderpath = os.path.join("received", foldername)
    os.chdir(owd)
    return folderpath

def downloadEmails(username, password, quantity):
    # create an IMAP4 class with SSL 
    imap = imaplib.IMAP4_SSL("imap.gmail.com")
    # authenticate
    imap.login(username, password)

    status, messages = imap.select("INBOX")
    # total number of emails
    messages = int(messages[0])

    for i in range(messages, messages-quantity, -1):
        # fetch the email message by ID
        res, msg = imap.fetch(str(i), "(RFC822)")
        for response in msg:
            if isinstance(response, tuple):
                # parse a bytes email into a message object
                msg = email.message_from_bytes(response[1])
                # decode the email subject
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    # if it's a bytes, decode to str
                    subject = subject.decode(encoding)
                # decode email sender
                From, encoding = decode_header(msg.get("From"))[0]
                if isinstance(From, bytes):
                    From = From.decode(encoding)
                print("Subject:", subject)
                print("From:", From)
                # if the email message is multipart
                if msg.is_multipart():
                    # iterate over email parts
                    for part in msg.walk():
                        # extract content type of email
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))
                        try:
                            # get the email body
                            body = part.get_payload(decode=True).decode()
                        except:
                            pass
                        if "attachment" in content_disposition:
                            # download attachment
                            filename = part.get_filename()
                            if filename:
                                folderpath = createFolder(subject)
                                filepath = os.path.join(folderpath, filename)
                                # download attachment and save it
                                open(filepath, "wb").write(part.get_payload(decode=True))
                if content_type == "text/html":
                    folderpath = createFolder(subject)
                    filename = "index.html"
                    filepath = os.path.join(folderpath, filename)
                    # write the file
                    open(filepath, "w").write(body)
    # close the connection and logout
    imap.close()
    imap.logout()

downloadEmails("mock60288@gmail.com", "mailclient123", 4)