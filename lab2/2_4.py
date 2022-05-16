import math
import time
import tkinter as tk
from tkinter import Canvas
import numpy as np
import string
import copy

class TKWindow:
    def __init__(self) -> None:
        self.window = tk.Tk()
        self.window.geometry('800x600')
        self.canv = Canvas(self.window, width=800, height=600)
        self.window.bind("<Key>",self.weighter)
        self.canv.bind("<Button 1>", self.addPoint)
        self.canv.place(x=0,y=0)
        self.part = True
        self.chosendot = -1
        self.dots = []
        self.weights = []
        self.update()


    def drawLine(self, x1, y1, x2, y2, clr="black", wd=1):
        self.canv.create_line(x1, y1, x2, y2, fill=clr, width=wd)

    def placeDot(self, x, y):
        self.canv.create_rectangle((x,y)*2)

    def addPoint(self,event):
        self.placeDot(event.x,event.y)
        self.dots.append(np.array([event.x,event.y],dtype=np.float64))
        self.weights.append(1)
        self.drawBezier()

    def changeweights(self,pos,num):
        if self.weights[pos]!= None:
            if self.weights[pos] < 10 and self.weights[pos] > 0.2:
                self.weights[pos]+=num

    def weighter(self,event):
        print(event.char)
        print(self.chosendot)
        if event.char == 'w':
            if self.chosendot+1 < len(self.dots):
                self.chosendot+= 1
        if event.char == 's':
             if self.chosendot-1 >= 0 :
                self.chosendot -=1
        if event.char == 'a':  
            self.changeweights(self.chosendot,-0.15)  

        if event.char == 'd':  
            self.changeweights(self.chosendot,0.15) 

    def highliter(self):
        if len(self.dots) > 0:
            x =self.dots[self.chosendot][0]
            y = self.dots[self.chosendot][1]
            self.canv.create_rectangle(x,y,x+3,y+3,fill="#ff0000")

    def labeler(self):
        num = self.chosendot
        if(self.chosendot!=-1):
            val = self.weights[num]-1
        else: 
            val = 0    
        mystr = "chosen dot:" + str(num)+ " value: " + str(val) 
        self.window.title(mystr)

    def showDots(self):
        for i in self.dots:
            self.placeDot(i[0],i[1])

    def B(self,t,i,degreeFac,degree):
        fact = degreeFac / (math.factorial(i)*math.factorial(degree-1))
        power = (1-t)**(degree-i)
        power_t = t**i
        return fact * power * power_t

    def sigma(self,t, degreeFac, degree):
        totalSum = 0
        for j in range(0, len(self.dots)):
            totalSum += self.B(t,j, degreeFac, degree) * self.weights[j]
        return totalSum

    def R(self,t, i , degreeFac, degree):
        B1 = self.B(t,i,degreeFac,degree)
        sigma1 = self.sigma(t,degreeFac,degree)
        return B1/sigma1

    def drawBezier(self):
        if len(self.dots) >=3:
            points =[]
            delta = 0.01
            degree = len(self.dots)-1
            degreeFac = math.factorial(degree)
            queue = self.dots[:]
            for t in np.arange(0,1.02,delta):
                point = np.array([0,0],dtype=np.float64)
                for i in range(degree+1):
                    vec = np.array([queue[i][0],queue[i][1]],dtype=np.float64)
                    R = self.R(t,i,degreeFac,degree)
                    vec*=R
                    point+=vec
                points.append(point)
            for i in range(len(points)-1):
                v1 = points[i]
                v2 = points[i+1]
                self.drawLine(v1[0],v1[1],v2[0],v2[1])    


    def clearScreen(self):
        self.canv.delete("all")

    def update(self):
        while(True):
            self.window.update()
            self.labeler()
            self.clearScreen()
            self.showDots()
            self.highliter()
            self.drawBezier()
            time.sleep(0.01)    

TKWindow()       