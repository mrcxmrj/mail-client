import imaplib, email, os
from email.header import decode_header


# creates folder in received directory, returns path to the new folder
def create_folder(folder_name):
    # clean text for creating a folder
    folder_name = ''.join(c if c.isalnum() else '_' for c in folder_name)
    owd = os.getcwd()
    os.chdir('received')
    if not os.path.isdir(folder_name):
        # make a folder for this email (named after the subject)
        os.mkdir(folder_name)
    foler_path = os.path.join('received', folder_name)
    os.chdir(owd)
    return foler_path


def download_emails(imap_server, messages_owned):
    status, messages = imap_server.select('INBOX')
    # total number of emails
    messages = int(messages[0])
    mails = ''

    for i in range(messages_owned+1, messages+1):
        # fetch the email message by ID
        res, msg = imap_server.fetch(str(i), '(RFC822)')
        if res == 'OK':
            raw = email.message_from_bytes(msg[0][1])
            mails = '#####<EMAIL>##### ' + str(i) + '\n' + str(raw) + mails

    return mails, messages