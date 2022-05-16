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
        pass

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
