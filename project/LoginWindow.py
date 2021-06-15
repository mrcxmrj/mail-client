import getpass, os, re, json, Encryotor, smtplib, imaplib
from tkinter import *
from tkinter.messagebox import *
from PIL import Image, ImageTk
from ClientWindow import ClientWindow


imap_server_endpoints = {'gmail': ('imap.gmail.com', 993),
                         'wp': ('imap.wp.pl', 993),
                         'onet': ('imap.poczta.onet.pl', 993),
                         'o2': ('poczta.o2.pl', 993),
                         'interia': ('poczta.interia.pl', 143),
                         'gazeta': ('imap.gazeta.pl', 993),
                         'yahoo': ('imap.mail.yahoo.com', 993),
                         'student': ('poczta.agh.edu.pl', 993)}

smtp_server_endpoints = {'gmail': ('smtp.gmail.com', 465),
                         'wp': ('smtp.wp.pl', 465),
                         'onet': ('smtp.poczta.onet.pl', 465),
                         'o2': ('poczta.o2.pl', 465),
                         'interia': ('poczta.interia.pl', 465),
                         'gazeta': ('smtp.gazeta.pl', 465),
                         'yahoo': ('smtp.mail.yahoo.com', 465),
                         'student': ('poczta.agh.edu.pl', 465)}


def is_valid_email(email):
    return re.match(r'\S+@\w+\.\w{2,}', email)


def get_imap_server_endpoint(email):
    domain = email.split('@')[1].split('.')[0]
    return imap_server_endpoints[domain] if domain in imap_server_endpoints else None

def get_smtp_server_endpoint(email):
    domain = email.split('@')[1].split('.')[0]
    return smtp_server_endpoints[domain] if domain in smtp_server_endpoints else None


def try_to_login_imap(email, password):
    endpoint = get_imap_server_endpoint(email)
    if not endpoint:
        showerror('error', 'unknown domain.')
        return None
    try:
        server = imaplib.IMAP4_SSL(endpoint[0], endpoint[1])
    except imaplib.IMAP4_SSL.error:
        showerror('error', 'error.')
        return None
    except imaplib.IMAP4_SSL.abort:
        showerror('abort', 'abort.')
        return None
    except imaplib.IMAP4_SSL.readonly:
        showerror('readonly', 'readonly.')
        return None
    except:
        showerror('Unexpected error:', sys.exc_info()[0])
        return None

    try:
        server.login(email, password)
        return server
    except imaplib.IMAP4_SSL.error:
        showerror('error', 'error.')
    except imaplib.IMAP4_SSL.abort:
        showerror('abort', 'abort.')
    except imaplib.IMAP4_SSL.readonly:
        showerror('readonly', 'readonly.')
    except:
        showerror('Unexpected error:', sys.exc_info()[0])
    return None


def try_to_login_smtp(email, password):
    endpoint = get_smtp_server_endpoint(email)
    if not endpoint:
        showerror('error', 'unknown domain.')
        return None
    try:
        server = smtplib.SMTP_SSL(endpoint[0], endpoint[1], timeout=2)
    except smtplib.SMTPConnectError:
        showerror('SMTPConnectError', 'Error.')
        return None
    except smtplib.SMTPServerDisconnected:
        showerror('SMTPServerDisconnected', 'server disconnected.')
        return None
    except:
        showerror('Unexpected error:', sys.exc_info()[0])
        return None

    server.ehlo()
    try:
        server.login(email, password)
        return server
    except smtplib.SMTPHeloError:
        showerror('SMTPHeloError', 'The server didn’t reply properly to the HELO greeting.')
    except smtplib.SMTPAuthenticationError:
        showerror('SMTPAuthenticationError', 'The server didn’t accept the username/password combination.')
    except smtplib.SMTPNotSupportedError:
        showerror('SMTPNotSupportedError', 'The AUTH command is not supported by the server.')
    except smtplib.SMTPException:
        showerror('SMTPException', 'No suitable authentication method was found.')
    except:
        showerror('Unexpected error:', sys.exc_info()[0])
    return None


class LoginWindow:
    def __init__(self):
        self.frame = Tk()
        self.frame.title('Logging window')
        self.icon = ImageTk.PhotoImage(Image.open('icons/icon.ico'))
        self.frame.iconphoto(False, self.icon)
        self.frame.geometry('647x661')
        self.frame.resizable(0, 0)
        self.create_widgets()
        self.frame.mainloop()

    def create_widgets(self):
        # continue
        self.continue_button = Button(self.frame, text='Continue', state=DISABLED, command=lambda: self.go_on())
        self.continue_button.place(x=517, y=600)
        # name
        self.name_label = Label(self.frame, text='Your name:')
        self.name_label.place(x=30, y=110)
        name_sv = StringVar()
        name_sv.trace('w', lambda name, index, mode, sv=name_sv: self.check())
        self.name_entry = Entry(self.frame, width=50, bd=2)
        # email
        self.email_label = Label(self.frame, text='Email address:')
        self.email_label.place(x=30, y=155)
        email_sv = StringVar()
        email_sv.trace('w', lambda name, index, mode, sv=email_sv: self.check())
        self.email_entry = Entry(self.frame, width=50, bd=2, textvariable=email_sv,
                                 highlightthickness=0, highlightbackground='red', highlightcolor='red')
        self.email_entry.bind('<FocusOut>', lambda entry: self.email_entry_on_focus_out())
        self.email_entry.place(x=195, y=155)
        self.name_entry.config(textvariable=name_sv)
        self.name_entry.insert(0, getpass.getuser())
        self.name_entry.place(x=195, y=110)
        # password
        self.password_label = Label(self.frame, text='Password:')
        self.password_label.place(x=30, y=200)
        self.password_entry = Entry(self.frame, width=50, bd=2, show='*')
        self.password_entry.place(x=195, y=200)
        self.show_password_image = ImageTk.PhotoImage(Image.open('icons/show_password_icon.bmp'))
        self.hide_password_image = ImageTk.PhotoImage(Image.open('icons/hide_password_icon.bmp'))
        self.show_password_var = IntVar()
        self.show_password_check_box = Checkbutton(self.frame, bd=0, image=self.hide_password_image,
                                                   selectimage=self.show_password_image, indicatoron=False,
                                                   variable=self.show_password_var, onvalue=1, offvalue=0,
                                                   command=lambda: self.show_password_change())
        self.show_password_check_box.place(x=610, y=200)
        # cancle
        self.cancle_button = Button(self.frame, text='Cancel', command=self.frame.destroy)
        self.cancle_button.place(x=30, y=600)
        # return handle
        self.frame.bind('<Return>', lambda event: self.return_pressed())
        # escape handle
        self.frame.bind('<Escape>', lambda event: self.frame.destroy())

    def check(self):
        name = self.name_entry.get()
        email = self.email_entry.get()
        if name and email and is_valid_email(email):
            self.continue_button.config(state=NORMAL)
        else:
            self.continue_button.config(state=DISABLED)

    def email_entry_on_focus_out(self):
        self.check_email()

    def check_email(self):
        email = self.email_entry.get()
        if not email or is_valid_email(email):
            self.email_entry.config(highlightthickness=0)
        else:
            self.email_entry.config(highlightthickness=2)

    def show_password_change(self):
        if self.show_password_var.get():
            self.password_entry.config(show='')
        else:
            self.password_entry.config(show='*')

    def go_on(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        imap_server = try_to_login_imap(email, password)
        if imap_server:
            smtp_server = try_to_login_smtp(email, password)
            if smtp_server:
                name = self.name_entry.get()
                self.save_profile()
                self.frame.destroy()
                ClientWindow(name, email, imap_server, smtp_server)
            else:
                imap_server.logout()

    def save_profile(self):
        profile = {'name': self.name_entry.get(),
                   'email': self.email_entry.get(),
                   'password': Encryotor.encrypt(self.password_entry.get())}

        home = os.path.expanduser('~')
        path = home+'/.mailclient/'
        if not os.path.exists(path):
            os.mkdir(path)
        path += 'profile.json'
        with open(path, 'w') as outfile:
            json.dump(profile, outfile)

    def return_pressed(self):
        name = self.name_entry.get()
        email = self.email_entry.get()
        if name and email and is_valid_email(email):
            self.go_on()
