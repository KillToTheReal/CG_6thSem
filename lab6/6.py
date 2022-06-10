import math
import time
import random
import tkinter as tk
from tkinter import Canvas
from tkinter import ttk
import numpy as np
# SPLINE


class TKWindow:
    def __init__(self) -> None:
        self.window = tk.Tk()
        self.width = 1000 
        self.height = 1000
        self.window.geometry(f'{self.width}x{self.height}')
        self.window.bind("<Key>", self.rotator)
        self.canv = Canvas(self.window, width=self.width, height=self.height)
        self.canv.place(x=0, y=0)

        self.projection = np.zeros((3, 3))

        self.rotationX = np.zeros((3, 3))
        self.rotationY = np.zeros((3, 3))
        self.rotationZ = np.zeros((3, 3))

        self.angleX = 0
        self.angleY = 0
        self.angleZ = 0

        self.scaleX = self.width / 4
        self.scaleY = self.height / 4
        self.scaleZ = 200

        self.traslation = np.zeros((1, 3))
        self.translationX = 0
        self.translationY = 0
        self.translationZ = 0

        self.originalCoords = []
        self.transformedCoords = []
        self.projectedCoords = []
        self.traversalIndexes = []
        self.backfaceCulled = []
        self.objFaces = []
        self.addCoords()
        self.update()

    def addCoords(self):
        coords = [
        [-0.5, -0.5, -0.5],
        [0.5, -0.5, -0.5],
        [0.5, 0.5, -0.5],
        [-0.5, 0.5, -0.5],

        [-0.5, -0.5, 0.5],
        [0.5, -0.5, 0.5],
        [0.5, 0.5, 0.5],
        [-0.5, 0.5, 0.5]]
        for item in coords:
            self.originalCoords.append(np.array([item[0],item[1],item[2]]))

        travIndexes =  [
            [0, 1],
            [1, 2],
            [2, 3],
            [3, 0],
          
            [4, 5],
            [5, 6],
            [6, 7],
            [7, 4],
       
            [0, 4],
            [1, 5],
            [2, 6],
            [3, 7],]
        self.traversalIndexes = travIndexes
        objFaces = [[0, 1, 2, 3],
                    [0, 4, 5, 1],
                    [4, 7, 6, 5],
                    [2, 6, 7, 3],
                    [1, 5, 6, 2],
                    [0, 3, 7, 4],]    
        self.objFaces = objFaces

    def cullFaces(self):
        canvVector = np.array([0,0,-1])
        for face in self.objFaces:
            point0Index = face[0]
            point1Index = face[1]
            point2Index = face[2]
            point0 = self.projectedCoords[point0Index]
            point1 = self.projectedCoords[point1Index]
            point2 = self.projectedCoords[point2Index]
            a = point1 + (point0 * -1)
            b = point2 + (point0 * -1)
            normal = np.cross(a,b)
            angleBeetwen = np.dot(normal,canvVector)
            if angleBeetwen < 0:
                self.backfaceCulled.append(face)

    def displayCoords(self):
        self.clearScreen()
        self.updateRotation()
        self.updateProjection()
        self.projectedCoords = []
        centerVec = np.array([0, 0, 0], dtype=np.float64)
        for i in range(len(self.originalCoords)):
            vec = self.originalCoords[i]
            centerVec += vec
        centerVec *= (1/len(self.originalCoords))
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
            self.projectedCoords.append(proj2D)
            i+=1
        self.cullFaces()
        for objectFace in self.backfaceCulled:
            leng = len(objectFace)
            for i in range(leng):
                projPointind0 = objectFace[i % leng]
                projPointind1 = objectFace[(i+1) % leng]
                coord1 = self.convertCoords(self.projectedCoords[projPointind0][0],self.projectedCoords[projPointind0][1])
                coord2 =self.convertCoords(self.projectedCoords[projPointind1][0],self.projectedCoords[projPointind1][1])
                self.drawLine(coord1[0],coord1[1],coord2[0],coord2[1],wd=2)
              
        self.backfaceCulled = []

        self.angleX += 0.003
        self.angleY +=0.003
        self.angleZ +=0.003
    
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
            if len(self.originalCoords) > 0:
                self.displayCoords()
            time.sleep(0.1)


TKWindow()
