import math
import time
import tkinter as tk
from tkinter import Canvas
import numpy as np
import copy

class TKWindow:
    def __init__(self) -> None:
        self.window = tk.Tk()
        self.width = 1000 
        self.height = 1000
        self.window.geometry(f'{self.width}x{self.height}')
        self.canv = Canvas(self.window, width=self.width, height=self.height)
        self.canv.bind("<Button 1>", self.addPoint)
        self.canv.place(x=0,y=0)
        self.part = True
        self.dots = []
        self.update()

    def sw(self):
        if self.part:
            self.part = False
        else:
            self.part = True    

    def drawBezier(self):
        if len(self.dots) >=3:
            points = []
            delta = 0.01
            controlPoints = copy.deepcopy(self.dots)
            if self.part:
                newContrPoints = []
                cntrllen = len(controlPoints)
                for i in range (cntrllen):
                    newContrPoints.append(controlPoints[i])
                    if i < cntrllen - 1:
                        point_1 = controlPoints[i]
                        point_2 = controlPoints[i+1]
                        sum = point_1 + point_2
                        sum *= 0.5
                        newContrPoints.append(sum)

                controlPoints = newContrPoints[:]
            for i in range(len(controlPoints)):
                 self.placeDot(controlPoints[i][0],controlPoints[i][1])

            degree = 2
            degreeFac = math.factorial(degree)
            for j in range(1,len(controlPoints)-degree,degree):
                for t in np.arange(0.01,1+delta,delta):
                    point = np.array([0,0],dtype=np.float64)
                    for i in range(degree+1):
                        vec = np.array([controlPoints[j+i][0],controlPoints[j+i][1]])
                        factor = degreeFac / (math.factorial(i) * math.factorial(degree-i))
                        pw = (1.0 - t)**(degree-i)
                        pw_t = t**i
                        appsum = factor * pw * pw_t
                        vec = vec * appsum
                        point+=vec 
                    points.append(point)

            for i in range(len(points)-1):
                v1 = points[i]
                self.placeDot(v1[0],v1[1])
                v2 = points[i+1]
                self.drawLine(v1[0],v1[1],v2[0],v2[1])
                
    def addPoint(self,event):
        self.placeDot(event.x,event.y)
        self.dots.append(np.array([event.x,event.y],dtype=np.float64))

    def showDots(self):
        for i in self.dots:
            self.placeDot(i[0],i[1])
    
    def drawLine(self, x1, y1, x2, y2, clr="black", wd=1):
        self.canv.create_line(x1, y1, x2, y2, fill=clr, width=wd)

    def placeDot(self, x, y, size=0, color="black"):
        self.canv.create_rectangle((x, y), (x+size, y+size), fill = color, outline=color)

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
