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
        self.window.bind("<Key>", self.deger)
        self.canv.place(x=0, y=0)
        self.dots = []
        self.knots = []
        self.degree = 2
        self.step_size = 0.01
        self.update()

    def clearScreen(self):
        self.canv.delete("all")

    def drawSpline(self):
        self.clearScreen()
        step_size = self.step_size
        points = []
        controlPoints = []

        for i in range(len(self.dots)):
            controlPoints.append(np.array([self.dots[i][0], self.dots[i][1]]))

        degree = self.degree
        mknots = []
        n = len(self.dots)
        flen = n + degree + 1
        for i in range(flen):
            if i <= degree:
                mknots.append(0)
            elif i < (flen - degree - 1):
                mknots.append(i/flen)
            else:
                mknots.append(1)
        self.knots = mknots

        pointsAmount = len(self.dots)
        u = 0

        while u < 1:
            vec = np.array([0, 0], dtype=np.float64)
            for i in range(pointsAmount):
                scale_num = self.N(i, degree, u)
                x = self.dots[i][0] * scale_num
                y = self.dots[i][1] * scale_num
                scale_point = np.array([x, y], dtype=np.float64)
                vec += scale_point
            points.append(vec)
            u += step_size
        
        for i in range(len(self.dots)-1):
            #Ломаная
            v1 = self.dots[i]
            v2= self.dots[i+1]
            self.drawLine(v1[0], v1[1], v2[0], v2[1],"red")

        for i in range(len(points)-1):
            #Кривая
            v1 = points[i]
            v2 = points[i+1]
            self.drawLine(v1[0], v1[1], v2[0], v2[1],wd=2)

        self.drawLine(points[len(points)-1][0], points[len(points)-1][1],
                      self.dots[len(self.dots)-1][0], self.dots[len(self.dots)-1][1])


    def N(self, i, m, u):
        if m == 0:
            if self.knots[i] <= u and u <= self.knots[i+1]:
                return 1
            return 0
        part1 = 0
        part2 = 0
        if self.knots[i+m] == self.knots[i]:
            if u == self.knots[i]:
                part1 = 0
            else:
                part1 = 1
        else:
            part1 = (u - self.knots[i]) / (self.knots[i+m]-self.knots[i])

        if self.knots[i + m + 1] == self.knots[i+1]:
            if self.knots[i+m+1] == u:
                part2 = 0
            else:
                part2 = 1
        else:
            part2 = (self.knots[i+m+1]-u) / (self.knots[i+m+1]-self.knots[i+1])

        return part1 * self.N(i, m-1, u) + part2 * self.N(i+1, m-1, u)

    def deger(self, event):
        if event.char == 'w':
            self.degree += 1
        if event.char == 's' and self.degree > 2:
            self.degree -= 1

    def showDots(self):
        for i in self.dots:
            self.placeDot(i[0], i[1])

    def addPoint(self, event):
        self.placeDot(event.x, event.y)
        self.dots.append(np.array([event.x, event.y], dtype=np.float64))

    def drawLine(self, x1, y1, x2, y2, clr="black", wd=1):
        self.canv.create_line(x1, y1, x2, y2, fill=clr, width=wd)

    def placeDot(self, x, y, size=0, color="black"):
        self.canv.create_rectangle((x, y), (x+size, y+size), fill = color, outline=color)

    def clearScreen(self):
        self.canv.delete("all")

    def labeler(self):
        mystr = "Degree:" + str(self.degree) + \
            ". Points amount:" + str(len(self.dots))
        self.window.title(mystr)

    def update(self):
        while(True):
            self.window.update()
            self.showDots()
            self.labeler()
            if(len(self.dots) > 2):
                self.drawSpline()
            time.sleep(0.1)


TKWindow()        