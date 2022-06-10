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
        self.canv.place(x=0, y=0)
        self.dots = []
        self.update()

    def duplicate(self, queue):
        coords = queue[:]
        new_queue = []
        new_queue.append(coords[0])
        for i in range(1, len(coords)-1):
            item = coords[i]
            new_queue.append(item)
            new_queue.append(item)

        new_queue.append(coords[-1])
        return new_queue

    def lerp(self, v1, v2, t):
        difference = (v2 - v1) * t + v1
        return difference

    def drawBezier(self):
        if(len(self.dots) >= 3):
            points = []
            step = 0.01
            for t in np.arange(0, 1+step, step):
                queue = self.dots[:]

                while len(queue) != 1:
                    queue = self.duplicate(queue)
                    for j in range(len(queue)-1):
                        p1 = queue.pop(0)
                        p2 = queue.pop(0)
                        p = self.lerp(p1, p2, t)
                        queue.append(p)

                points.append(queue[0])

            for t in range(len(points)-1):
                v1 = points[t]
                v2 = points[t+1]
                self.drawLine(v1[0], v1[1], v2[0], v2[1], clr='red', wd=2)

            for t in range(len(queue)-1):
                v1 = queue[t]
                v2 = queue[t+1]
                self.drawLine(v1[0], v1[1], v2[0], v2[1])

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
