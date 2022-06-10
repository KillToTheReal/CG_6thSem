import math
import time
import random
import tkinter as tk
from tkinter import Canvas
from tkinter import ttk
import numpy as np
#BEZIER
class TKWindow:
    def __init__(self) -> None:    
        self.window = tk.Tk()
        self.width = 1000 
        self.height = 1000
        self.window.geometry(f'{self.width}x{self.height}')
        self.canv = Canvas(self.window, width=self.width, height=self.height)
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

        self.scaleX = 200
        self.scaleY = 200 
        self.scaleZ = 200
        self.maxScale = 400

        self.traslation = np.zeros((1,3))
        self.translationX = 0
        self.translationY = 0        
        self.translationZ = 0

        self.surfaceW = 2
        self.surfaceH = 2 
        self.surfaceStepX = 0.2
        self.surfaceStepY = 0.2
        self.surfaceInitialShiftX = 0
        self.surfaceInitialShiftY = 0

        self.gridCoords = []
        self.gridSurfaceCoords = []
        # Bspline
        self.knots = []
        self.degree = 2
        self.precision = 0.01

        self.addCoordsManually()
        self.update()


    def addCoordsManually(self):
        for _ in range (0, math.ceil(self.surfaceH / self.surfaceStepY)):
            self.gridCoords.append([])

        precision = 0.001
        
        for y in np.arange(self.surfaceInitialShiftY, self.surfaceH-precision, self.surfaceStepY):
            j = 0
            for x in np.arange(self.surfaceInitialShiftX, self.surfaceW-precision, self.surfaceStepX):
                coordX = x
                coordY = y
                coordZ = (random.uniform(0.0, 3.0))
                surfacePoint = np.array([coordX,coordY,coordZ])
                self.originalCoords.append(surfacePoint)
                self.gridCoords[j].append(surfacePoint)                           
                j = j+1
        parts = 30
        step = 1/parts
        for i in range(parts):
            self.gridSurfaceCoords.append([])

        N = len(self.gridCoords)
        M = len(self.gridCoords[0]) 
        u = 0
        for i in range(parts):
            v = 0
            for j in range(parts):
                surfacePoint = self.bezierPoint(u,v,M,N)
                self.gridSurfaceCoords[i].append(surfacePoint)
                v+=step
            u+=step

    def bezierPoint(self,u,v,m,n):
        surfacePoint = np.array([0,0,0],dtype=np.float64)
        for i in range(n):
            B_i = self.B(n-1,i,u) 
            for j in range(m):
                B_j = self.B(m-1,j,v)
                controlPoint = self.gridCoords[i][j]
                controlPoint = np.array([controlPoint[0],controlPoint[1],controlPoint[2]])
                controlPoint *= B_i * B_j
                surfacePoint+=controlPoint
        return surfacePoint            

    def B(self,n,i,t):
        factor = math.factorial(n) / (math.factorial(i)*math.factorial(n-i))
        power = (1-t)**(n-i)
        power_t = t**i
        B = factor * power * power_t
        return B

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

        
        projectedGridCoords = []
        for i in range (len(self.gridSurfaceCoords)):
            projectedGridCoords.append([])

        for i in range(len(self.gridCoords)):
            for j in range(len(self.gridCoords[0])):
                coord = self.gridCoords[i][j]
                proj2D = np.array([coord[0],coord[1],coord[2]]) 
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
        
        for i in range(len(self.gridSurfaceCoords)):
            for j in range(len(self.gridSurfaceCoords[0])):
                coord = self.gridSurfaceCoords[i][j]

                proj2D = np.array([coord[0],coord[1],coord[2]]) 
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

        for i in range(0,len(self.gridSurfaceCoords)-1):
            for j in range(len(self.gridSurfaceCoords[0])):
                start = projectedGridCoords[i][j]
                end = projectedGridCoords[relu(i+1,len(self.gridSurfaceCoords))][j]
                self.drawLine(start[0],start[1],end[0],end[1])

        for i in range(0,len(self.gridSurfaceCoords)):
            for j in range(len(self.gridSurfaceCoords[0])-1):
                start = projectedGridCoords[i][j]
                end = projectedGridCoords[i][relu(j+1,len(self.gridSurfaceCoords[0]))]
                self.drawLine(start[0],start[1],end[0],end[1])

        projectedGridCoords =[]
        self.angleX += 0.001
        self.angleY +=0.02
        self.angleZ += 0.001


    def drawLine(self, x1, y1, x2, y2, clr="black", wd=1):
        self.canv.create_line(x1, y1, x2, y2, fill=clr, width=wd)

    def placeDot(self, x, y, size=0, color="black"):
        self.canv.create_rectangle((x, y), (x+size, y+size), fill = color, outline=color)

    def clearScreen(self):
        self.canv.delete("all")

    def convertCoords(self, x, y):
        x += self.width / 4
        y += self.height / 4
        return np.array([x, y, 0])


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