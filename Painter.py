import Tkinter


from PIL import ImageTk
from Tkinter import *
from PIL import ImageGrab

class Button(object):
    root, painter = None, None
    width, height, padx, pady = 0, 0, 0, 0

    def __init__(self, painter, root, width, height, padx, pady):
        self.root = root
        self.painter = painter
        self.width = width
        self.height = height
        self.padx = padx
        self.pady = pady

class ColorButton(Button):
    def __init__(self, painter, root, width, height, padx, pady, color):
        Button.__init__(self, painter, root, width, height, padx, pady)
        self.color = color
        self.TkBut = Tkinter.Button(root, command=self.button_event, width=width, height=height, bg=color)
        self.TkBut.pack(padx=padx, pady=pady, side=LEFT)

    def button_event(self):
        self.painter.pencil_color = self.color

class ToolButton(Button):
    saveIndex = 1

    def __init__(self, painter, drawing_area, root, width, height, padx, pady, tool, img):
        Button.__init__(self, painter, root, width, height, padx, pady)
        self.drawing_area = drawing_area
        self.tool = tool
        self.TkBut = Tkinter.Button(root, command=self.button_event, width=width, height=height, bg="white")
        self.TkBut.config(image=img)
        self.TkBut.image = img
        self.TkBut.pack(padx=padx, pady=pady, side=LEFT)

    def button_event(self):
        if self.tool == "delete":
            self.drawing_area.delete("all")

        elif self.tool == "duenn":
            self.painter.pencil_line_width = 1

        elif self.tool == "mittel":
            self.painter.pencil_line_width = 10

        elif self.tool == "dick":
            self.painter.pencil_line_width = 20

        elif self.tool == "undo":
            if len(self.painter.cv_elements) > 0:
                if type(self.painter.cv_elements[len(self.painter.cv_elements) - 1]) is list:
                    el_list = self.painter.cv_elements[len(self.painter.cv_elements) - 1]
                    for i in range(len(el_list)):
                        self.drawing_area.delete(el_list[i])
                else:
                    self.drawing_area.delete(self.painter.cv_elements[len(self.painter.cv_elements) - 1])
                del self.painter.cv_elements[-1]

        elif self.tool == "save":
            x = self.root.winfo_rootx() + self.drawing_area.winfo_x()
            y = self.root.winfo_rooty() + self.drawing_area.winfo_y()
            x1 = x + self.drawing_area.winfo_width()
            y1 = y + self.drawing_area.winfo_height()
            ImageGrab.grab().crop((x, y, x1, y1)).save("save" + str(self.saveIndex) + ".jpg")
            self.saveIndex = self.saveIndex + 1

        else:
            self.painter.drawing_tool = self.tool

class Painter:
    drawing_tool = "pencil"
    pencil_color = "black"
    pencil_line_width = 1
    but_pressed = False
    x_pos, y_pos = None, None

    x1, y1, x2, y2 = None, None, None, None

    tool_names = ["pencil", "line", "circle", "rect", "eraser", "delete", "undo", "save", "duenn", "mittel", "dick"]
    color_codes = ["#000000", "#808080", "#C0C0C0", "#FFFFFF", "#800000", "#FF0000", "#808000", "#FFFF00", "#008000", "#00FF00", "#008080", "#00FFFF", "#000080", "#0000FF", "#800080", "#FF00FF"]
    cv_elements = []
    cv_el_list = []

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
                self.cv_el_list.append(event.widget.create_line(self.x_pos, self.y_pos, event.x, event.y,width=self.pencil_line_width,smooth=True,fill=self.pencil_color))
            self.x_pos, self.y_pos = event.x, event.y
        if not self.but_pressed and self.cv_el_list != []:
            self.cv_elements.append(self.cv_el_list)
            self.cv_el_list = []

    def line_draw(self,event=None):
        if (self.x1,self.y1,self.x2,self.y2) != None:
            self.cv_elements.append(event.widget.create_line(self.x1,self.y1,self.x2,self.y2,width=self.pencil_line_width, smooth = True, fill=self.pencil_color))

    def circle_draw(self, event=None):
        if (self.x1, self.y1, self.x2, self.y2) != None:
            self.cv_elements.append(event.widget.create_oval(self.x1, self.y1, self.x2, self.y2, width=30, fill=self.pencil_color, outline=self.pencil_color))

    def rectangle_draw(self, event=None):
        if (self.x1, self.y1, self.x2, self.y2) != None:
            self.cv_elements.append(event.widget.create_rectangle(self.x1, self.y1, self.x2, self.y2, width = 30, fill=self.pencil_color, outline=self.pencil_color))

    def eraser_draw(self, event=None):
        if self.but_pressed:
            if (self.x_pos and self.y_pos) != None:
                self.cv_el_list.append(event.widget.create_line(self.x_pos, self.y_pos, event.x, event.y,width = 30,smooth=True,fill="white"))
            self.x_pos, self.y_pos = event.x, event.y
        if not self.but_pressed and self.cv_el_list != []:
            self.cv_elements.append(self.cv_el_list)
            self.cv_el_list = []

    def init_buttons(self, drawing_area):
        for i in range(11):
            ToolButton(self, drawing_area, root, 50, 50, 2, 2, self.tool_names[i], ImageTk.PhotoImage(file=self.tool_names[i]+".png"))
        for i in range(16):
            ColorButton(self, root, 3, 1, 2, 2, self.color_codes[i])

    def __init__(self,root):
        drawing_area = Canvas(root,height=600,width=600,bg="white")
        drawing_area.pack()
        self.init_buttons(drawing_area)
        drawing_area.bind("<Motion>",self.move)
        drawing_area.bind("<ButtonPress-1>", self.button_pressed)
        drawing_area.bind("<ButtonRelease-1>", self.button_released)

root = Tk()
root.geometry('1300x800+5+5')
root.configure(background='grey')
root.title('Painter')
root.iconbitmap("icon.ico")
painter = Painter(root)
root.mainloop()