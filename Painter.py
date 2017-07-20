import Tkinter

from PIL import ImageTk
from Tkinter import *
from PIL import ImageGrab

class Button(object):
	width, height, padx, pady = 0, 0, 0, 0

	def __init__(self, root, width, height, padx, pady):
		self.width = width
		self.height = height
		self.padx = padx
		self.pady = pady

class ColorButton(Button):
	def __init__(self, painter, root, width, height, padx, pady, color):
		Button.__init__(self, root, width, height, padx, pady)
		self.painter = painter
		self.color = color
		self.TkBut = Tkinter.Button(root, command=self.button_event, width=width, height=height, bg=color)
		self.TkBut.pack(padx=padx, pady=pady, side=LEFT)
	
	def button_event(self):
		self.painter.pencil_color = self.color

class ToolButton(Button):
	def __init__(self, painter, drawing_area, root, width, height, padx, pady, tool, img):
		Button.__init__(self, root, width, height, padx, pady)
		self.painter = painter
		self.drawing_area = drawing_area
		self.tool = tool
		self.TkBut = Tkinter.Button(root, command=self.button_event, width=width, height=height, bg="white")
		self.TkBut.config(image=img)
		self.TkBut.image = img
		self.TkBut.pack(padx=padx, pady=pady, side=LEFT)
	
	def button_event(self):
		if self.tool == "delete":
			self.drawing_area.delete("all")
		else:
			self.painter.drawing_tool = self.tool

class LineWidthButton(Button):
	def __init__(self, painter, root, width, height, padx, pady, lineWidth):
		Button.__init__(self, root, width, height, padx, pady)
		self.painter = painter
		self.lineWidth = lineWidth
		self.TkBut = Tkinter.Button(root, text=lineWidth, command=self.button_event, width=width, height=height, bg="white")
		self.TkBut.pack(padx=padx, pady=pady, side=LEFT)
	
	def button_event(self):
		if self.lineWidth == "duenn":
			self.painter.pencil_line_width = 1
		if self.lineWidth == "mittel":
			self.painter.pencil_line_width = 10
		if self.lineWidth == "dick":
			self.painter.pencil_line_width = 20

class SaveButton(Button):
	i = 1
	
	def __init__(self, drawing_area, root, width, height, padx, pady):
		Button.__init__(self, root, width, height, padx, pady)
		self.drawing_area = drawing_area
		self.root = root
		self.TkBut = Tkinter.Button(root, text="speichern", command=self.button_event, width=width, height=height, bg="white")
		self.TkBut.pack(padx=padx, pady=pady, side=LEFT)
	
	def button_event(self):
		x=self.root.winfo_rootx()+self.drawing_area.winfo_x()
		y=self.root.winfo_rooty()+self.drawing_area.winfo_y()
		x1=x+self.drawing_area.winfo_width()
		y1=y+self.drawing_area.winfo_height()
		ImageGrab.grab().crop((x,y,x1,y1)).save("save" + str(self.i) + ".jpg")
		self.i = self.i + 1

class Painter:
    drawing_tool = "pencil"
    pencil_color = "black"
    pencil_line_width = 1
    but_pressed = False
    x_pos, y_pos = None, None
    d = []

    x1, y1, x2, y2 = None, None, None, None

    tool_names = ["pencil", "line", "circle", "rect", "eraser", "delete"]
    color_codes = ["#000000", "#808080", "#C0C0C0", "#FFFFFF", "#800000", "#FF0000", "#808000", "#FFFF00", "#008000", "#00FF00", "#008080", "#00FFFF", "#000080", "#0000FF", "#800080", "#FF00FF"]
    line_widths = ["duenn", "mittel", "dick"]

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
            self.d.append(event.widget.create_line(self.x1,self.y1,self.x2,self.y2,width=self.pencil_line_width, smooth = True, fill=self.pencil_color))

    def circle_draw(self, event=None):
        if (self.x1, self.y1, self.x2, self.y2) != None:
            self.d.append(event.widget.create_oval(self.x1, self.y1, self.x2, self.y2, width=30, fill=self.pencil_color, outline=self.pencil_color))

    def rectangle_draw(self, event=None):
        if (self.x1, self.y1, self.x2, self.y2) != None:
            self.d.append(event.widget.create_rectangle(self.x1, self.y1, self.x2, self.y2, width = 30, fill=self.pencil_color, outline=self.pencil_color))

    def eraser_draw(self, event=None):
        if self.but_pressed:
            if (self.x_pos and self.y_pos) != None:
                event.widget.create_line(self.x_pos, self.y_pos, event.x, event.y,width = 30,smooth=True,fill="white")

            self.x_pos, self.y_pos = event.x, event.y

    x = 1

    def init_buttons(self, drawing_area):
        for i in range(6):
            ToolButton(self, drawing_area, root, 50, 50, 2, 2, self.tool_names[i], ImageTk.PhotoImage(file=self.tool_names[i]+".png"))
        for i in range(3):
            LineWidthButton(self, root, 5, 3, 2, 2, self.line_widths[i])
        SaveButton(drawing_area, root, 5, 3, 2, 2)
        def func_undo():
            drawing_area.delete(self.d[len(self.d) - self.x])
            self.x = self.x +1
        def func_redo():
            print str(self.d[len(self.d) - 1])
        undo = Tkinter.Button(root, text="undo", command=func_undo, width=5, height=3, bg="white")
        undo.pack(padx=2, pady=2, side=LEFT)
        redo = Tkinter.Button(root, text="redo", command=func_redo, width=5, height=3, bg="white")
        redo.pack(padx=2, pady=2, side=LEFT)
        for i in range(16):
            ColorButton(self, root, 2, 1, 2, 2, self.color_codes[i])

    def __init__(self,root):
        drawing_area = Canvas(root,height=600,width=600,bg="white")
        drawing_area.pack()
        self.init_buttons(drawing_area)
        drawing_area.bind("<Motion>",self.move)
        drawing_area.bind("<ButtonPress-1>", self.button_pressed)
        drawing_area.bind("<ButtonRelease-1>", self.button_released)

root = Tk()
root.geometry('900x900+5+5')
root.title('Painter')
root.iconbitmap("icon.ico")
painter = Painter(root)
root.mainloop()