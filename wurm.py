import sys
import random
from tkinter import *

salat       = None
wurm        = None
dimension   = 50
dicke       = 10
text1       = None
text2       = None


class Wurm():
    def __init__(self, canvas, dimension, dicke):
        self.canvas    = canvas
        self.dimension = dimension
        self.dicke     = dicke
        self.gsegments = []
        self.reset()

    def reset(self):
        while self.gsegments:
            self.deltail()
            
        self.segments = [(dimension/2, dimension/2)]
        self.gsegments = []
        self.drawhead()
        self.richtung  = "N"
        self.pause     = 1
        self.gameover  = 0
        self.speed     = 401


        

    def drawhead(self):
        x = self.segments[0][0]
        y = self.segments[0][1]
        d = self.dicke

        g = self.canvas.create_rectangle(x*d + 2, y*d + 2, (x+1)*d + 2, (y+1)*d + 2, fill="orange")
        self.gsegments.insert(0, g)

    def deltail(self):
        g = self.gsegments.pop()
        self.canvas.delete(g)

    def taste(self, ev):
        if ev.keysym == "Left":
            if self.richtung == "N":
                self.richtung = "W"
            elif self.richtung == "O":
                self.richtung = "N"
            elif self.richtung == "S":
                self.richtung = "O"
            elif self.richtung == "W":
                self.richtung = "S"
        elif ev.keysym == "Right":
            if self.richtung == "N":
                self.richtung = "O"
            elif self.richtung == "O":
                self.richtung = "S"
            elif self.richtung == "S":
                self.richtung = "W"
            elif self.richtung == "W":
                self.richtung = "N"
        elif ev.keysym == "plus":
            self.speed -= 50
            if self.speed < 1:
                self.speed = 1
        elif ev.keysym == "minus":
            self.speed += 50
        elif ev.keysym == "space":
            if self.gameover:
                # delete text, wurm & salat
                global text1, text2
                self.canvas.delete(text1)
                self.canvas.delete(text2)
                self.reset()
            else:
                self.pause = 1-self.pause
            
    def schritt(self):
        if self.pause == 0 and self.gameover==0:
            x = self.segments[0][0]
            y = self.segments[0][1]
            
            if self.richtung == "N":
                xn = x
                yn = y -1
            elif self.richtung == "O":
                xn = x + 1
                yn = y
            elif self.richtung == "S":
                xn = x
                yn = y + 1
            elif self.richtung == "W":
                xn = x - 1
                yn = y

            if xn < 0 or yn < 0 or xn >= self.dimension or yn >= self.dimension or (xn, yn) in self.segments:
                gameover(self.canvas)
                self.gameover = 1
            else:
                self.segments.insert(0, (xn, yn))
                self.drawhead()
                
                if (xn, yn) != salat.position:
                    self.segments.pop()
                    self.deltail()
                else:
                    salat.werfen()

        self.canvas.after(self.speed, self.schritt)

class Salat():
    def __init__(self, canvas, dimension, dicke):
        self.canvas    = canvas
        self.dimension = dimension
        self.dicke     = dicke
        self.g         = None
        self.werfen()

    def werfen(self):
        if self.g != None:
            self.canvas.delete(self.g)
        while (1):
            x=random.randint(0, self.dimension-1)
            y=random.randint(0, self.dimension-1)
            if not (x,y) in wurm.segments:
                break
                
        self.position = (x,y)
        d=self.dicke
        self.g = self.canvas.create_rectangle(x*d + 2, y*d + 2, (x+1)*d + 2, (y+1)*d + 2, fill="red")


def gameover(canvas):
    global dimension, dicke, text1, text2
    x = dimension * dicke / 2 + 2
    y = dimension * dicke / 2 + 2
    text1 = canvas.create_text(x, y-30, text="Game Over", font="Helvetica 36", fill="yellow" )
    text2 = canvas.create_text(x, y+30, text="%d Punkte" % len(wurm.segments), font="Helvetica 24", fill="yellow" )

def tastendruck(ev):
    global wurm
    wurm.taste(ev)

def __main__():
    global salat
    global wurm
    
    pix = dimension*dicke
    top = Tk()
    
    canvas = Canvas(top, width=pix + 4, height=pix + 4, bg="darkgreen")
    canvas.pack()

    top.bind("<Key>", tastendruck)
    

    wurm=Wurm(canvas, dimension, dicke)
    salat=Salat(canvas, dimension, dicke)

    wurm.schritt()

    top.mainloop()

__main__()
