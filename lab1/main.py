from hashlib import new
import math
import random
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
        self.canvas = Canvas(self.window, width=self.width, height=self.height)
        self.canvas.place(x=0, y=0)
        self.window.bind("<Key>", self.rotator)
        self.window.bind("<Button 1>", self.placeDot)
   

        self.width = 800
        self.height = 600

        self.coords = []
        self.projCoords = np.array([[]])
        # projection matrix
        self.projection = np.array([[]])

        # rotation matrix for each axis
        self.rotationX = np.zeros((3, 3))
        self.rotationZ = np.zeros((3, 3))
        self.rotationY = np.zeros((3, 3))

        # translationvec
        self.translation = np.array([[]])

        # translation params
        self.translationX = 0
        self.translationY = 0
        self.translationZ = 0

        # scale params for all axis
        self.scaleX = 1
        self.scaleY = 1
        self.scaleZ = 1

        # rotation params for all axis
        self.angleX = 0
        self.angleY = 0
        self.angleZ = 0

        self.update()


    def displayCoords(self):
        self.clearScreen()
        self.updateRotation()
        self.updateProjection()
        self.projCoords = []
        centerVec = np.array([0, 0, 0], dtype=np.float64)

        for vec in self.coords:
            centerVec += vec

        centerVec /= len(self.coords)
        transObject = np.array([
                self.translationX,
                self.translationY,
                self.translationZ,
            ])
        coords2 = copy.deepcopy(self.coords)
        self.projection = self.rotationX @ self.rotationY @ self.rotationZ @ self.projection    
        # transform all coords
        for proj2D in coords2:
        
            proj2D -= centerVec
            proj2D = self.projection @ proj2D
            proj2D += centerVec            
            proj2D += transObject
            self.projCoords.append(proj2D)
        for i in range(len(self.projCoords) - 1):
            self.connectProjectedDots(i, i + 1)    

    def setPixel(self, x, y):
        self.canvas.create_rectangle(x, y, x+2, y+2)

    def placeDot(self, event):
        x = event.x
        y = event.y
        self.setPixel(x, y)
        normX = x
        normY = y 
        normZ = random.uniform(-0.2, 0.2)

        self.coords.append(
            np.array([normX, normY, normZ]))

    def drawLine(self, x1, y1, x2, y2, clr="black", wd=1):
        self.canvas.create_line(x1, y1, x2, y2, fill=clr, width=wd)

    def clearScreen(self):
        self.canvas.delete("all")

    def rotator(self, event):
        if event.char == "x" or event.char == "ч":
            self.angleX += 0.15
        if event.char == "c" or event.char =="с":
            self.angleY += 0.15
        if event.char == "z" or event.char =="я":
            self.angleZ += 0.15
        if event.char == "q" or event.char =="й":
            self.translationX += 1
        if event.char == "w" or event.char =="ц":
            self.translationY += 1
        if event.char == "e" or event.char =="у":
            self.translationZ += 1
        if event.char == "a" or event.char =="ф":
            self.scaleX += 1
        if event.char == "s" or event.char =="ы":
            self.scaleY += 1
        if event.char == "d" or event.char =="в":
            self.scaleZ += 1

    def clearCoords(self):
        self.window.update()
        self.projCoords = []

    def connectProjectedDots(self, startNum, endNum):
        end = self.projCoords[endNum]
        start = self.projCoords[startNum]
        self.drawLine(start[0], start[1], end[0], end[1])

    def updateRotation(self):
        angleX = self.angleX
        angleY = self.angleY
        angleZ = self.angleZ

        def cos(x): return math.cos(x)
        def sin(x): return math.sin(x)

        self.rotationZ = np.array([
            [cos(angleZ), -sin(angleZ), 0],
            [sin(angleZ), cos(angleZ), 0],
            [0, 0, 1]
        ])

        self.rotationX = np.array([
            [1, 0, 0],
            [0, cos(angleX), -sin(angleX)],
            [0, sin(angleX), cos(angleX)]
        ])

        self.rotationY = np.array([
            [cos(angleY), 0, -sin(angleY)],
            [0, 1, 0],
            [sin(angleY), 0, cos(angleY)]
        ])

    def updateProjection(self):
        scaleX = self.scaleX
        scaleY = self.scaleY
        scaleZ = self.scaleZ

        self.projection = np.array([
            np.array([1, 0, 0]) * scaleX,
            np.array([0, 1, 0]) * scaleY,
            np.array([0, 0, 1]) * scaleZ,
        ])

    def update(self):
        while True:
            self.window.update()
            if len(self.coords) > 0:
                self.displayCoords()
            time.sleep(0.02)

TKWindow()
