import math
import time
import tkinter as tk
from tkinter import Canvas
from tkinter import ttk
from turtle import clearscreen
import numpy as np
import copy

class TKWindow:
    def __init__(self) -> None:    
        self.window = tk.Tk()
        self.window.geometry('1000x1000')
        #self.window.bind("<Key>", self.rotator)
        self.canv = Canvas(self.window, width=1000, height=1000)
        self.canv.place(x=0,y=0)

        self.originalCoords = []
        self.projCoords = []

        self.projection = np.zeros((3,3))

        self.rotationX = np.zeros((3,3))
        self.rotationY = np.zeros((3,3))      
        self.rotationZ = np.zeros((3,3))

        self.angleX = 0
        self.angleY = 0
        self.angleZ = 0 

        self.scaleX = 200
        self.scaleY = 200  
        self.scaleZ = 200
        self.maxScale = 600

        self.traslation = []
        self.translationX = 0
        self.translationY = 0        
        self.translationZ = 0

        self.surfaceW = 2 * math.pi
        self.surfaceH = 2 * math.pi
        self.surfaceStepX = 0.2
        self.surfaceStepY = 0.2
        self.surfaceInitialShiftX = 0
        self.surfaceInitialShiftY = 0

        self.gridCoords = []


    def addCoordsManually(self):
        for i in range (0, math.ceil(self.surfaceH/ self.surfaceStepY)):
            self.gridCoords.append(np.zeros(1,3))
            i = 0
        for x in np.arange(self.surfaceInitialShiftX, self.surfaceW, self.surfaceStepX):
            j = 0
            i=i+1
            for y in np.arange(self.surfaceInitialShiftY, self.surfaceH, self.surfaceStepY):
                coordX = self.fx(x,y)
                coordY = self.fy(x,y)
                coordZ = self.fz(x,y)
                surfacePoint = np.array([coordX,coordY,coordZ])
                self.originalCoords.append(surfacePoint)

                self.gridCoords[j].append(surfacePoint)
                
                
                j = j+1

    def fx(u,v):
        R = 0.5
        r = 0.4
        return (R*math.sin(u) + r*math.cos(v) * math.cos(u))
    def fy(u,v):
        R = 0.5
        r = 0.4
        return (R*math.sin(u) + r*math.cos(v) * math.sin(u))
    def fz(u,v):
        R = 0.5
        r = 0.4
        return (r*math.sin(v))        

    def surfaceFunction(x, y):
        return math.sin(2*y) + math.sin(2*x)

    def clearScreen(self):
        self.canv.delete("all")

    def update(self):
        while(True):
            self.window.update()
            self.clearWindow()
            self.clearScreen()
            if len(self.originalCoords) > 0:
                self.displayCoords()
            time.sleep(0.03) 

TKWindow()   