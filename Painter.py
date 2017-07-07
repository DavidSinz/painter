import Tkinter

from tkinter import *

class Painter:
    drawing_tool = "pencil"
    pencil_color = "black"
    but_pressed = False
    x_pos, y_pos = None, None

    x1, y1, x2, y2 = None, None, None, None

    def change_pencil_black(self):
        self.pencil_color = "black"

    def change_pencil_white(self):
        self.pencil_color = "white"

    def change_pencil_red(self):
        self.pencil_color = "red"

    def change_pencil_blue(self):
        self.pencil_color = "blue"

    def change_pencil_green(self):
        self.pencil_color = "green"

    def change_pencil_yellow(self):
        self.pencil_color = "yellow"

    def change_pen(self):
        self.drawing_tool = "pencil"

    def change_line(self):
        self.drawing_tool = "line"

    def change_circle(self):
        self.drawing_tool = "circle"

    def change_rect(self):
        self.drawing_tool = "rect"


    def button_pressed(self, event=None):
        self.but_pressed = True

        self.x1, self.y1 = event.x, event.y

    def button_released(self, event=None):
        self.but_pressed = False
        self.x_pos, self.y_pos = None, None
        self.x2, self.y2 = event.x, event.y
        if self.drawing_tool == "line":
            self.line_draw(event)
        if self.drawing_tool == "rect":
            self.rectangle_draw(event)
        if self.drawing_tool == "circle":
            self.circle_draw(event)

    def move(self,event=None,):
        if self.drawing_tool == "pencil":
            self.pencil_draw(event)

    def pencil_draw(self, event= None):
        if self.but_pressed:
            if (self.x_pos and self.y_pos) != None:
                event.widget.create_line(self.x_pos, self.y_pos, event.x, event.y,smooth=True,fill=self.pencil_color)

            self.x_pos, self.y_pos = event.x, event.y

    def line_draw(self,event=None):
        if (self.x1,self.y1,self.x2,self.y2) != None:
            event.widget.create_line(self.x1,self.y1,self.x2,self.y2,smooth = True,fill=self.pencil_color)

    def circle_draw(self, event=None):
        if (self.x1, self.y1, self.x2, self.y2) != None:
            event.widget.create_oval(self.x1, self.y1, self.x2, self.y2, width=30, fill=self.pencil_color, outline=self.pencil_color)

    def rectangle_draw(self, event=None):
        if (self.x1, self.y1, self.x2, self.y2) != None:
            event.widget.create_rectangle(self.x1, self.y1, self.x2, self.y2, width = 30, fill=self.pencil_color, outline=self.pencil_color)

    def __init__(self,root):
        drawing_area = Canvas(root,height=600,width=600,bg="white")
        drawing_area.pack()

        pencil = Tkinter.Button(root, text="pencil", command=self.change_pen, width=5, height=2, bg="white")
        pencil.pack(padx=20, pady=20, side=LEFT)
        line = Tkinter.Button(root, text="line", command=self.change_line, width=5, height=2, bg="white")
        line.pack(padx=20, pady=20, side=LEFT)
        circle = Tkinter.Button(root, text="circle", command=self.change_circle, width=5, height=2, bg="white")
        circle.pack(padx=20, pady=20, side=LEFT)
        rect = Tkinter.Button(root, text="rect", command=self.change_rect, width=5, height=2, bg="white")
        rect.pack(padx=20, pady=20, side=LEFT)
        black = Tkinter.Button(root, command=self.change_pencil_black, width=5, height=2, bg="black")
        black.pack(padx=20, pady=20, side=LEFT)
        white = Tkinter.Button(root, command=self.change_pencil_white, width=5, height=2, bg="white")
        white.pack(padx=20, pady=40, side=LEFT)
        red = Tkinter.Button(root, command=self.change_pencil_red, width=5, height=2, bg="red")
        red.pack(padx=20, pady=40, side=LEFT)
        blue = Tkinter.Button(root, command=self.change_pencil_blue, width=5, height=2, bg="blue")
        blue.pack(padx=20, pady=20, side=LEFT)
        green = Tkinter.Button(root, command=self.change_pencil_green, width=5, height=2, bg="green")
        green.pack(padx=20, pady=20, side=LEFT)
        yellow = Tkinter.Button(root, command=self.change_pencil_yellow, width=5, height=2, bg="yellow")
        yellow.pack(padx=20, pady=20, side=LEFT)

        drawing_area.bind("<Motion>",self.move)
        drawing_area.bind("<ButtonPress-1>", self.button_pressed)
        drawing_area.bind("<ButtonRelease-1>", self.button_released)

root = Tk()
root.geometry('900x900+5+5')
root.title('Painter')
painter = Painter(root)
root.mainloop()