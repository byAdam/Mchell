import tkinter as tk
from world import main_world

class Camera(tk.Frame):
    def __init__(self,root,name):
        tk.Frame.__init__(self, master=root)
        self.root = root
        self.name = name

        self.root.title(self.name)
        self.set_size(5,5)
        self.pack()

    def set_camera_info(coordinates_a,coordinates_b,width,height,facing):
        self.coordinates_a = coordinates_a
        self.coordinates_b = coordinates_b
        self.width = width
        self.height = height
        self.facing = facing
        self.set_size()

    def update_camera(self):
        blocks = main_world.get_blocks(self.coordinates_a,self.coordinates_b,True)

        w = 0
        while w < self.width:
            h = 0
            while h < self.height:
                if facing == "+x":
                    k = (0,h,w)
                elif facing == "-x":
                    k = (0,h,-w)
                elif facing == "+z":
                    k = (-w,h,0)
                elif facing == "-z":
                    k = (w,h,0)

                self.draw_block(blocks[k],w,h)
                h += 1
            w += 1

    def set_size(self,width,height):
        self.root.geometry("{}x{}".format(self.width*64,self.height*64))
        self.init_canvas()

    def init_canvas(self):
        self.canvas = tk.Canvas(self,width=self.width,height=self.height)
        self.canvas.pack()

    def draw_block(self,block,x,y):
        start_x = x*64
        start_y = self.height*64 - y*64
        if block["block"] == "air":
            self.canvas.create_rectangle(start_x,start_y,start_x+64,start_y-64,fill="#fff")
        else:
            self.canvas.create_rectangle(start_x,start_y,start_x+64,start_y-64,fill="#000")

def create_camera():
    global camera
    root = tk.Tk()
    camera = Camera(root,"mcscreen")