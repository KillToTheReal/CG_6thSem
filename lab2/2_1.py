import math
import time
import tkinter as tk
from tkinter import Canvas
import numpy as np
import copy

class TKWindow:
    def __init__(self) -> None:
        self.window = tk.Tk()
        self.window.geometry('800x600')
        self.canv = Canvas(self.window, width=800, height=600)
        self.canv.bind("<Button 1>", self.addPoint)
        self.canv.place(x=0,y=0)
        self.dots = []
        self.update()

    def drawLine(self, x1, y1, x2, y2, clr="black", wd=1):
        self.canv.create_line(x1, y1, x2, y2, fill=clr, width=wd)

    def placeDot(self, x, y):
        self.canv.create_rectangle((x,y)*2)

    def addPoint(self,event):
        self.placeDot(event.x,event.y)
        self.dots.append(np.array([event.x,event.y]))
        self.drawBezier()

    def showDots(self):
        for i in self.dots:
            self.placeDot(i[0],i[1])

    def drawBezier(self):
        if(len(self.dots) >= 3):
            pts = []
            step = 0.01
            deg = len(self.dots) - 1
            degFac = math.factorial(deg)
            cpy = copy.deepcopy(self.dots)
            i = step
            for i in np.arange(0.01,1,step):
                point = np.array([0,0],dtype=np.float64)
                for j in range(0,deg+1):
                    vec = np.array([cpy[j][0],cpy[j][1]], dtype=np.float64)
                    fact = degFac / (math.factorial(j) * math.factorial(deg - j))
                    pow = (1-i)**(deg-j)
                    pow_t = i**j
                    vec = vec * (fact * pow * pow_t)
                    point+=vec

                pts.append(point)

            for i in range (len(pts)-1):
                v1 = pts[i]
                v2 = pts[i+1]
                self.drawLine(v1[0],v1[1],v2[0],v2[1],clr='red',wd = 2)
                
            for i in range (len(cpy)-1):
                v1 = cpy[i]
                v2 = cpy[i+1]
                self.drawLine(v1[0],v1[1],v2[0],v2[1])

    def clearScreen(self):
        self.canv.delete("all")

    def update(self):
        while(True):
            self.window.update()
            self.clearScreen()
            self.showDots()
            self.drawBezier()
            time.sleep(0.01)


TKWindow()