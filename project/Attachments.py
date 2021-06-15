from tkinter import *


class Attachemnts:
    def __init__(self, root, width, height):
        self.canvas = Canvas(root, width=width, height=height, bg='white')
        self.ybar = Scrollbar(self.canvas, orient=VERTICAL)
        self.ybar.place(x=width-13, y=0, height=height)
        self.ybar.config(command=self.canvas.yview)
        self.canvas.config(yscrollcommand=self.ybar.set)
        self.width = width
        self.height = height
        self.attachments = []
        self.buttons = []
        self.names = []
        self.calculate_sizes_and_positions()

    def calculate_sizes_and_positions(self):
        self.button_x = [15, self.width/2+15]
        self.button_w = 20
        self.name_x = [30, self.width/2+30]
        self.name_w = self.width/2-55
        self.y = 12
        self.h = 20
        self.padding_h = 3

    def add(self, path):
        n = len(self.attachments)
        self.attachments.append(path)
        self.buttons.append(Button(self.canvas, text='x', command=lambda: self.remove(n)))
        self.canvas.create_window(self.button_x[n%2], self.y+n//2*self.h+(self.padding_h)*(n//2),
                                  width=self.button_w, height=self.h, window=self.buttons[-1])
        name = path.split('/')[-1]
        if len(name) > 30:
            name = name[:30] + '..'
        self.names.append(Label(self.canvas, text=name, bg='white'))
        self.canvas.create_window(self.name_x[n%2], self.y+n//2*self.h+(self.padding_h)*(n//2),
                                  window=self.names[-1], anchor=W)
        self.height = 2*self.y+n//2*self.h+(self.padding_h)*(n//2)
        self.canvas.config(scrollregion=[0, 0, self.width, self.height])

    def remove(self, i):
        paths = self.attachments[i+1:]
        for k in range(i, len(self.attachments)):
            self.buttons[i].destroy()
            self.buttons.pop(i)
            self.names[i].destroy()
            self.names.pop(i)
            self.attachments.pop(i)

        for path in paths:
            self.add(path)

    def place(self, *args, **kwargs):
        self.canvas.place(*args, **kwargs)

    def place_forget(self):
        self.canvas.place_forget()

    def get(self):
        return self.attachments

    def clear(self):
        for i in range(len(self.attachments)):
            self.buttons[i].destroy()
            self.names[i].destroy()

        self.attachments = []
        self.buttons = []
        self.names = []


