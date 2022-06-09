
import math
import time
import tkinter as tk
from tkinter import Canvas
from tkinter import ttk
import numpy as np

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

        self.angleX = 90
        self.angleY = 0
        self.angleZ = 0 

        self.scaleX =   100
        self.scaleY = 100  
        self.scaleZ = 100
        self.maxScale = 400

        self.traslation = np.zeros((1,3))
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
        self.addCoordsManually()
        self.update()

    def addCoordsManually(self):
        for _ in range (0, math.ceil(self.surfaceH / self.surfaceStepY)):
            self.gridCoords.append([])

        for x in np.arange(self.surfaceInitialShiftX, self.surfaceW, self.surfaceStepX):
            j = 0
            for y in np.arange(self.surfaceInitialShiftY, self.surfaceH, self.surfaceStepY):
                coordX = self.fx(x,y)
                coordY = self.fy(x,y)
                coordZ = self.fz(x,y)
                surfacePoint = np.array([coordX,coordY,coordZ])
                self.originalCoords.append(surfacePoint)
                self.gridCoords[j].append(surfacePoint)                           
                j = j+1

    def drawLine(self, x1, y1, x2, y2, clr="black", wd=1):
        self.canv.create_line(x1, y1, x2, y2, fill=clr, width=wd)

    # def fx(self, u, v):
    #     R = 0.5
    #     r = 0.2
    #     return (R + r*math.cos(v))* math.cos(u)

    # def fy(self, u, v):
    #     R = 0.5
    #     r = 0.2
    #     return ((R + r*math.cos(v)) * math.sin(u))
    # def fz(self, u, v):
    #     R = 0.5
    #     r = 0.2
    #     return (r*math.sin(v))
    #Cylinder
    def fx(self, u, v):
        a = 2
        return (a*math.cos(u))
    def fy(self, u, v):
        a = 2
        return (a*math.sin(u))
    def fz(self, u, v):      
        return (v)        

    
    def placeDot(self, x, y):
        self.canv.create_rectangle((x,y)*2)

    def surfaceFunction(x, y):
        return math.sin(2*y) + math.sin(2*x)

    def clearScreen(self):
        self.canv.delete("all")

    def displayCoords(self):
        self.clearScreen()
        self.updateRotation()
        self.updateProjection()
        self.projCoords = []
        centerVec = np.array([0,0,0],dtype=np.float64)
        for i in range (len(self.originalCoords)):
            vec = self.originalCoords[i]
            centerVec+=vec
        centerVec*= (1/len(self.originalCoords))

        i = 0
        projectedGridCoords = []
        for i in range (len(self.gridCoords)):
            projectedGridCoords.append([])

        for i in range(len(self.gridCoords)):
            for j in range(len(self.gridCoords[0])):
                coord = self.gridCoords[i][j]
                proj2D = np.array([coord[0],coord[1],coord[2]])

                #trans = np.array([self.translationX,self.translationY,self.translationZ])
                objTrans = np.array([self.translationX,self.translationY,self.translationZ])
                proj2D += (centerVec*-1)
                proj2D = proj2D @ self.rotationX
                proj2D = proj2D @ self.rotationY
                proj2D = proj2D @ self.rotationZ
                proj2D += centerVec
                proj2D = proj2D @ self.projection
                proj2D += objTrans
                self.projCoords.append(proj2D)
                convertedCoords = np.array(self.convertCoords(proj2D[0],proj2D[1]))
                self.placeDot(convertedCoords[0],convertedCoords[1])
                projectedGridCoords[i].append(convertedCoords)
        
        def relu(x,max): return 0 if x >= max else x 

        for i in range(len(self.gridCoords)):
            for j in range(len(self.gridCoords[0])):
                start = projectedGridCoords[i][j]
                end = projectedGridCoords[relu(i+1,len(self.gridCoords))][j]
                self.drawLine(start[0],start[1],end[0],end[1])

                end = projectedGridCoords[i][relu(j+1,len(self.gridCoords[0]))]
                self.drawLine(start[0],start[1],end[0],end[1])

        projectedGridCoords =[]
        self.angleX += 0.001
        self.angleY +=0.05
        self.angleZ += 0.001

    def convertCoords(self,x,y):
        x+=500
        y+=500
        return np.array([x,y,0])

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
        while(True):
            self.window.update()
            self.clearScreen()
            if len(self.originalCoords) > 0:
                self.displayCoords()
            time.sleep(0.03) 

TKWindow()   