from LoginWindow import *
from ClientWindow import ClientWindow
import os
import json
import encryption

if __name__ == "__main__":
    home = os.path.expanduser("~")
    profile_path = home + "/.mailclient/profile.json"
    if not os.path.isfile(profile_path):
        LoginWindow()
    else:
        with open(profile_path, 'r') as infile:
            profile = json.load(infile)

        name = profile['name']
        email = profile['email']
        password = encryption.decrypt(profile['password'])

        imap_server = try_to_login_imap(email, password)
        if imap_server:
            smtp_server = try_to_login_smtp(email, password)
            if smtp_server:
                ClientWindow(name, email, imap_server, smtp_server)
            else:
                imap_server.logout()
                LoginWindow()