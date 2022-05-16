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
        self.knots =[]
        self.degree = 2
        self.precision = 1/100
        self.update()

    def drawLine(self, x1, y1, x2, y2, clr="black", wd=1):
        self.canv.create_line(x1, y1, x2, y2, fill=clr, width=wd)

    def placeDot(self, x, y):
        self.canv.create_rectangle((x,y)*2)

    def addPoint(self,event):
        self.placeDot(event.x,event.y)
        self.dots.append(np.array([event.x,event.y],dtype=np.float64))

    def showDots(self):
        for i in self.dots:
            self.placeDot(i[0],i[1])

    def clearScreen(self):
        self.canv.delete("all")

    def drawSpline(self):
        _precision = self.precision
        points = []
        controlPoints =[]
        for i in range(len(self.dots)):
            controlPoints.append(np.array([self.dots[i][0],self.dots[i][1]]))
        _degree = self.degree
        mknots = []
        n = len(self.dots)
        flen = n + _degree + 1
        for i in range(flen):
            if i<=_degree:
                mknots.append(0)
            elif i < flen - _degree - 1:
                mknots.append(i/flen)
            else:
                mknots.append(1)        
        self.knots = mknots
        
        pointsAmount = len(self.dots)
        for u in np.arange(0,pointsAmount,_precision):
            x = 0
            y = 0
            for i in range(pointsAmount):
                pass
                ##101

    def N(self,i, m, u):
        if m == 0:
            if self.knots[i] <= u and u <= self.knots[i+1]:
                return 1 
            return 0        
        part1 = 0
        ##163
    def update(self):
        while(True):
            self.window.update()
            self.clearScreen()
            self.showDots()
            if(len(self.dots) > 2):
                self.drawSpline()
            time.sleep(0.01)      