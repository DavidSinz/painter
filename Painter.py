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
	rowIdx = 1
	
	def __init__(self, painter, root, width, height, padx, pady, color):
		Button.__init__(self, painter, root, width, height, padx, pady)
		self.color = color
		self.TkBut = Tkinter.Button(root, command=self.button_event, width=width, height=height, bg=color, cursor="hand2")
		self.TkBut.grid(column=ColorButton.rowIdx, row=13)
		ColorButton.rowIdx += 1
	
	def button_event(self):
		self.painter.pencil_color = self.color

class ToolButton(Button):
	rowIdx = 1
	colIdx = 18
	saveIndex = 1
	
	def __init__(self, painter, drawing_area, root, width, height, padx, pady, tool, img):
		Button.__init__(self, painter, root, width, height, padx, pady)
		self.drawing_area = drawing_area
		self.tool = tool
		self.TkBut = Tkinter.Button(root, command=self.button_event, width=width, height=height, bg="white", cursor="hand2")
		self.TkBut.config(image=img)
		self.TkBut.image = img
		self.TkBut.grid(column=ToolButton.colIdx, row=ToolButton.rowIdx)
		if ToolButton.colIdx == 20:
			ToolButton.colIdx = 18
			ToolButton.rowIdx += 1
		else:
			ToolButton.colIdx += 2
	
	def button_event(self):
		if self.tool == "delete":
			self.drawing_area.delete("all")
		elif self.tool == "save":
			x=self.root.winfo_rootx()+self.drawing_area.winfo_x()
			y=self.root.winfo_rooty()+self.drawing_area.winfo_y()
			x1=x+self.drawing_area.winfo_width()
			y1=y+self.drawing_area.winfo_height()
			ImageGrab.grab().crop((x,y,x1,y1)).save("save" + str(self.saveIndex) + ".jpg")
			self.saveIndex = self.saveIndex + 1
		elif self.tool == "undo":
			if len(self.painter.cv_elements) > 0:
				if type(self.painter.cv_elements[len(self.painter.cv_elements) - 1]) is list:
					el_list = self.painter.cv_elements[len(self.painter.cv_elements) - 1]
					for i in range(len(el_list)):
						self.drawing_area.delete(el_list[i])
				else:
					self.drawing_area.delete(self.painter.cv_elements[len(self.painter.cv_elements) - 1])
				del self.painter.cv_elements[-1]
		else:
			self.painter.drawing_tool = self.tool

class LineWidthController(object):
	scale = None
	painter = None
	
	def __init__(self, painter, root):
		self.painter = painter
		self.scale = Scale(root, command=self.scale_event, width=40, fr=1, to=20, label="Strichstaerke:", cursor="hand2", orient="horizontal", length=120)
		self.scale.grid(column=18,row=5,columnspan=3)

	def scale_event(self, size):
		self.painter.pencil_line_width = size

class Painter:
    drawing_tool = "pencil"
    pencil_color = "black"
    pencil_line_width = 1
    but_pressed = False
    x_pos, y_pos = None, None

    x1, y1, x2, y2 = None, None, None, None

    tool_names = ["pencil", "line", "circle", "rect", "eraser", "undo", "save", "delete"]
    color_codes = ["#000000", "#808080", "#C0C0C0", "#FFFFFF", "#800000", "#FF0000", "#808000", "#FFFF00", "#008000", "#00FF00", "#008080", "#00FFFF", "#000080", "#0000FF", "#800080", "#FF00FF"]
    cv_elements = []
    cv_el_list = []
	
    def maintain_list_size(self):
        if len(self.cv_elements) >= 6:
            self.cv_elements.pop(0)

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
        self.maintain_list_size()

    def line_draw(self,event=None):
        if (self.x1,self.y1,self.x2,self.y2) != None:
            self.cv_elements.append(event.widget.create_line(self.x1,self.y1,self.x2,self.y2,width=self.pencil_line_width, smooth = True, fill=self.pencil_color))
        self.maintain_list_size()

    def circle_draw(self, event=None):
        if (self.x1, self.y1, self.x2, self.y2) != None:
            self.cv_elements.append(event.widget.create_oval(self.x1, self.y1, self.x2, self.y2, width=30, fill=self.pencil_color, outline=self.pencil_color))
        self.maintain_list_size()

    def rectangle_draw(self, event=None):
        if (self.x1, self.y1, self.x2, self.y2) != None:
            self.cv_elements.append(event.widget.create_rectangle(self.x1, self.y1, self.x2, self.y2, width = 30, fill=self.pencil_color, outline=self.pencil_color))
        self.maintain_list_size()

    def eraser_draw(self, event=None):
        if self.but_pressed:
            if (self.x_pos and self.y_pos) != None:
                self.cv_el_list.append(event.widget.create_line(self.x_pos, self.y_pos, event.x, event.y,width = 30,smooth=True,fill="white"))
            self.x_pos, self.y_pos = event.x, event.y
        if not self.but_pressed and self.cv_el_list != []:
            self.cv_elements.append(self.cv_el_list)
            self.cv_el_list = []
        self.maintain_list_size()

    def init_drawing_area(self):
        drawing_area = Canvas(root,height=600,width=600,bg="white",cursor="crosshair")
        drawing_area.grid(column=1, row=1, rowspan=11, columnspan=16)
        return drawing_area

    def init_controller(self, drawing_area):
        for i in range(len(self.tool_names)):
            ToolButton(self, drawing_area, root, 50, 50, 2, 2, self.tool_names[i], ImageTk.PhotoImage(file="img/"+self.tool_names[i]+".png"))
        for i in range(len(self.color_codes)):
            ColorButton(self, root, 3, 1, 2, 2, self.color_codes[i])
        LineWidthController(self, root)

    def init_grid_placeholders(self):
        Frame(root, height=20, width=40).grid(column=0, row=0)
        Frame(root, height=20, width=20).grid(column=17, row=0)
        Frame(root, height=20, width=20).grid(column=0, row=12)
        Frame(root, height=10, width=20).grid(column=19, row=0)

    def __init__(self,root):
        drawing_area = self.init_drawing_area()
        self.init_controller(drawing_area)
        self.init_grid_placeholders()
        drawing_area.bind("<Motion>",self.move)
        drawing_area.bind("<ButtonPress-1>", self.button_pressed)
        drawing_area.bind("<ButtonRelease-1>", self.button_released)

root = Tk()
root.geometry('900x900+5+5')
root.title('Painter')
root.iconbitmap("img/icon.ico")
painter = Painter(root)
root.mainloop()