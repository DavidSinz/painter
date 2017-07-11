import Tkinter

from PIL import ImageTk
from tkinter import *

class Painter:
    drawing_tool = "pencil"
    pencil_color = "black"
    pencil_line_width = 1
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

    def change_duenn(self):
        self.pencil_line_width = 1

    def change_mittel(self):
        self.pencil_line_width = 10

    def change_dick(self):
        self.pencil_line_width = 20

    def change_circle(self):
        self.drawing_tool = "circle"

    def change_rect(self):
        self.drawing_tool = "rect"

    def change_eraser(self):
        self.drawing_tool = "eraser"

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
        if self.drawing_tool == "eraser":
            self.eraser_draw(event)

    def pencil_draw(self, event= None):
        if self.but_pressed:
            if (self.x_pos and self.y_pos) != None:
                event.widget.create_line(self.x_pos, self.y_pos, event.x, event.y,width=self.pencil_line_width,smooth=True,fill=self.pencil_color)

            self.x_pos, self.y_pos = event.x, event.y

    def line_draw(self,event=None):
        if (self.x1,self.y1,self.x2,self.y2) != None:
            event.widget.create_line(self.x1,self.y1,self.x2,self.y2,width=self.pencil_line_width, smooth = True, fill=self.pencil_color)

    def circle_draw(self, event=None):
        if (self.x1, self.y1, self.x2, self.y2) != None:
            event.widget.create_oval(self.x1, self.y1, self.x2, self.y2, width=30, fill=self.pencil_color, outline=self.pencil_color)

    def rectangle_draw(self, event=None):
        if (self.x1, self.y1, self.x2, self.y2) != None:
            event.widget.create_rectangle(self.x1, self.y1, self.x2, self.y2, width = 30, fill=self.pencil_color, outline=self.pencil_color)

    def eraser_draw(self, event=None):
        if self.but_pressed:
            if (self.x_pos and self.y_pos) != None:
                event.widget.create_line(self.x_pos, self.y_pos, event.x, event.y,width = 30,smooth=True,fill="white")

            self.x_pos, self.y_pos = event.x, event.y


    def __init__(self,root):
        drawing_area = Canvas(root,height=600,width=600,bg="white")
        drawing_area.pack()

        def delete_canvas():
            drawing_area.delete("all")

        img_rect = ImageTk.PhotoImage(file="rect.png")
        img_circle = ImageTk.PhotoImage(file="circle.png")
        img_line = ImageTk.PhotoImage(file="line.png")
        img_pencil = ImageTk.PhotoImage(file="pencil.png")
        img_eraser = ImageTk.PhotoImage(file="eraser.png")
        img_delete = ImageTk.PhotoImage(file="delete.png")

        pencil = Tkinter.Button(root, command=self.change_pen, width=50, height=50, bg="white")
        pencil.config(image=img_pencil)
        pencil.image = img_pencil
        pencil.pack(padx=20, pady=20, side=LEFT)
        line = Tkinter.Button(root, command=self.change_line, width=50, height=50, bg="white")
        line.config(image=img_line)
        line.image = img_line
        line.pack(padx=20, pady=20, side=LEFT)

        delete_all = Tkinter.Button(root, command=delete_canvas, width=50, height=50, bg="white")
        delete_all.config(image=img_delete)
        delete_all.image = img_delete
        delete_all.pack(padx=20, pady=20, side=LEFT)

        duenn = Tkinter.Button(root,text="duenn", command=self.change_duenn, width=5, height=2, bg="white")
        duenn.pack(padx=20, pady=20, side=LEFT)
        mittel = Tkinter.Button(root, text="mittel", command=self.change_mittel, width=5, height=2, bg="white")
        mittel.pack(padx=20, pady=20, side=LEFT)
        dick = Tkinter.Button(root, text="dick", command=self.change_dick, width=5, height=2, bg="white")
        dick.pack(padx=20, pady=20, side=LEFT)

        eraser = Tkinter.Button(root, command=self.change_eraser,width=50,height=50, bg="white")
        eraser.config(image=img_eraser)
        eraser.image = img_eraser
        eraser.pack(padx=20, pady=20, side=LEFT)
        circle = Tkinter.Button(root, command=self.change_circle, width=50, height=50, bg="white")
        circle.config(image=img_circle)
        circle.image = img_circle
        circle.pack(padx=20, pady=20, side=LEFT)
        rect = Tkinter.Button(root, command=self.change_rect, width=50, height=50, bg="white")
        rect.config(image=img_rect)
        rect.image = img_rect
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
root.iconbitmap("icon.ico")
painter = Painter(root)
root.mainloop()