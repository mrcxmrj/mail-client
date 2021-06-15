import tkinter.ttk as ttk, re, email.parser, email
from tkinter import *
from datetime import datetime

class Header:
    def __init__(self, id, author, subject, date):
        self.id = id
        self.author = author
        self.subject = subject
        self.date = date



def get_headers(mails, mail_address):
    out = []
    for mail in mails.split('#####<EMAIL>#####')[1:]:
        i = mail.find('\n')
        id = int(mail[:i])
        mail = mail[i+1:]
        data = email.parser.Parser().parsestr(mail)
        out.append(Header(id, data['from'], data['subject'], data['date']))
    return out


def get_date(string):
    ind = re.search(r'\d+ [a-zA-z]{3} \d{4} \d\d:\d\d:\d\d', string).regs[0]
    string = string[ind[0]:ind[1]]
    return datetime.strptime(string, '%d %b %Y %H:%M:%S')


class MailHeaders:
    def __init__(self, client_window, page_size):
        self.client_window = client_window
        self.headers_tree = ttk.Treeview(client_window.frame, show="headings")
        self.headers_tree.config(columns=('author', 'subject', 'date'))
        self.headers_tree.heading('#1', text='author')
        self.headers_tree.heading('#2', text='subject')
        self.headers_tree.heading('#3', text='date')
        self.headers_tree.bind("<Button-1>", lambda event: self.on_single_click(event))
        self.headers_tree.bind("<Double-1>", lambda event: self.on_double_click(event))
        self.headers = []
        self.sorting = 'date'
        self.sort_descending = True
        self.page_size = page_size
        self.pages = 0
        self.page = 1
        self.selected_row = -1

    def add_headers(self, mails, mail_address):
        new_headers = get_headers(mails, mail_address)
        self.headers.extend(new_headers)
        self.pages = (len(self.headers)-1)//self.page_size+1 if self.headers else 1
        self.sort()
        self.set_page(self.page)

    def sort_by(self, key):
        if self.sorting == key:
            self.sort_descending = not self.sort_descending
        else:
            self.sorting = key
            self.sort_descending = True

        self.sort()
        self.set_page(self.page)

    def sort(self):
        if self.sorting == 'date':
            self.headers.sort(key=lambda x: x.id, reverse=self.sort_descending)
        elif self.sorting == 'author':
            self.headers.sort(key=lambda x: x.author, reverse=self.sort_descending)
        else:
            self.headers.sort(key=lambda x: x.subject, reverse=self.sort_descending)

    def set_page(self, n):
        self.clear()
        self.page = n
        start_ind = (n-1)*self.page_size
        end_ind = min(len(self.headers), n*self.page_size)
        headers = self.headers[start_ind:end_ind]
        for i in range(len(headers)):
            header = headers[i]
            self.headers_tree.insert("", i, values=(header.author, header.subject, header.date),
                                     tag=('white' if i%2 == 0 else 'blue', i))
        self.headers_tree.tag_configure('white', background='#FFFFFF')
        self.headers_tree.tag_configure('blue', background='#1C9EEF')
        self.client_window.open_button.config(state=DISABLED)

    def place(self, *args, **kwargs):
        self.headers_tree.place(args, **kwargs)

    def place_forget(self):
        self.headers_tree.place_forget()

    def get_page_count(self):
        return self.pages

    def clear(self):
        self.headers_tree.delete(*self.headers_tree.get_children())

    def on_single_click(self, event):
        region = self.headers_tree.identify("region", event.x, event.y)
        if region == "cell":
            self.client_window.open_button.config(state=NORMAL)

    def on_double_click(self, event):
        region = self.headers_tree.identify("region", event.x, event.y)
        if region == "heading":
            identifier = self.headers_tree.identify_column(event.x)
            self.sort_by(self.get_column_name(identifier))

    def get_column_name(self, identifier):
        if identifier == '#1':
            return 'author'
        if identifier == '#1':
            return 'subject'
        return 'date'

    def clear_selction(self):
        if len(self.headers_tree.selection()) > 0:
            self.headers_tree.selection_remove(self.headers_tree.selection()[0])

    def get_selected(self):
        cur = self.headers_tree.focus()
        item = self.headers_tree.item(cur)
        ind = item['tags'][1]
        return self.headers[self.page_size*(self.page-1)+ind].id

    def get_page(self):
        return self.page