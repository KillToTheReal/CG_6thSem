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
        self.window.bind("<Key>", self.rotator)
        self.canv = Canvas(self.window, width=1000, height=1000)
        self.canv.place(x=0,y=0)

        self.originalCoords = []
        self.transCoords = []
        self.projCoords = []
        self.travIndexes = []

        self.angleX = 0
        self.angleY = 0
        self.angleZ = 0        
        
        self.scaleX = 200
        self.scaleY = 200  
        self.scaleZ = 200
        self.maxScale = 600

        self.projection = np.zeros((3,3))

        self.rotationX = np.zeros((3,3))
        self.rotationY = np.zeros((3,3))      
        self.rotationZ = np.zeros((3,3))

        self.traslation = []
        self.translationX = 0
        self.translationY = 0        
        self.translationZ = 0

        self.labels = []

        self.addCoordsMan()
        self.update()

    
    def rotator(self, event):
        if event.char == "x":

            self.angleX += 0.15

        if event.char == "c":

            self.angleY += 0.15

        if event.char == "z":

            self.angleZ += 0.15

        if event.char == "q":

            self.translationX += 1

        if event.char == "w":
            self.translationY += 1

        if event.char == "e":
            self.translationZ += 1

        if event.char == "a":
            self.scaleX += 1

        if event.char == "s":
            self.scaleY += 1

        if event.char == "d":
            self.scaleZ += 1

    def convertCoords(self,x,y):
        x+=500/2
        y+=500/2
        return np.array([x,y,0])

    def drawLine(self, x1, y1, x2, y2, clr="black", wd=1):
        self.canv.create_line(x1, y1, x2, y2, fill=clr, width=wd)

    def addCoordsMan(self):
        coords =[[-0.5, -0.5, -0.5], #0
                [0.5, -0.5, -0.5], #1
                [0.5, 0.5, -0.5], #2 
                [-0.5, 0.5, -0.5], #3

                [-0.5, -0.5, 0.5], #4
                [0.5, -0.5, 0.5],  #5
                [0.5, 0.5, 0.5], #6
                [-0.5, 0.5, 0.5], #7
                #new coord
                [0.,0.,0.]] #8
        for item in coords:
            self.originalCoords.append(np.array([item[0],item[1],item[2]])) 

        travIndexes = [ #[0,1],
                        [1, 2],[2, 3],[3, 0],
                        [4, 5],[5, 6],[6, 7],[7, 4],
                        [0, 4],[1, 5],[2, 6],[3, 7],
                        #Невыпуклость
                        [0, 8],[8, 1]
                                ]
        self.travIndexes = travIndexes

    def dotNum(self, i, x, y):
        lbl = tk.Label(self.window, text=str(i),font=('Arial',10))
        lbl.place(x=x,y=y,width=7,height=10)
        self.labels.append(lbl)

    def placeDot(self, x, y):
        self.canv.create_rectangle((x,y)*2)
    #из 1 лабы
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

    def connectProjectedDots(self,startNum, endNum):
        start = self.projCoords[startNum]
        end = self.projCoords[endNum]
        start = self.convertCoords(start[0],start[1])
        end = self.convertCoords(end[0],end[1])
        self.drawLine(start[0],start[1],end[0],end[1])

    def displayCoords(self):
        self.clearScreen()
        self.updateRotation()
        self.updateProjection()
        self.projCoords = []
        centerVec = np.array([0,0,0],dtype=np.float64)

        for i in range(len(self.originalCoords)):
            vec = self.originalCoords[i]
            centerVec+=(vec)

        centerVec*= 1 / len(self.originalCoords)
        i = 0
        for coords in self.originalCoords:
            proj2D = np.array([coords[0],coords[1],coords[2]])
            transObj = np.array([self.translationX,self.translationY,self.translationZ])
            proj2D += (centerVec * -1)
            proj2D = proj2D @ self.rotationX
            proj2D = proj2D @ self.rotationY
            proj2D = proj2D @ self.rotationZ
            proj2D += centerVec
            proj2D = self.projection @ proj2D
            proj2D +=transObj
            self.projCoords.append(proj2D)
            convertedCoords = self.convertCoords(proj2D[0],proj2D[1])
            self.dotNum(i,convertedCoords[0],convertedCoords[1])
            self.placeDot(convertedCoords[0],convertedCoords[1])
            i+=1

        for trav in self.travIndexes:
            self.connectProjectedDots(trav[0],trav[1])  

        self.angleX += 0.001
        self.angleY +=0.003
        self.angleZ +=0.001      

    def clearWindow(self):
        for lbl in self.labels:
            lbl.destroy()

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