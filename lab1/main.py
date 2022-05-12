from hashlib import new
import math
import random
import time
import tkinter as tk
from tkinter import Canvas
import numpy as np
# lerp = np.interp
# matmul = np.matmul
# add =  np.+operator
# norm2 = np.linalg.norm


class WindowHuindow:
    def __init__(self) -> None:
        pass
        self.window = tk.Tk()
        self.window.geometry("800x600")
        self.window.bind("<Key>", self.rotator)
        self.window.bind("<Button 1>", self.placeDot)
        self.canvas = Canvas(self.window, width=800, height=600)
        self.canvas.place(x=0, y=0)

        self.width = 800
        self.height = 800

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
        self.scaleX = 600
        self.scaleY = 600
        self.scaleZ = 600

        # rotation params for all axis
        self.angleX = 0
        self.angleY = 0
        self.angleZ = 0

        self.update()

    def setPixel(self, x, y):
        self.canvas.create_rectangle(x, y, x+2, y+2)

    def placeDot(self, event):
        x = event.x
        y = event.y
        self.setPixel(x, y)
        normX = x / self.width - 0.5
        normY = y / self.height - 0.5
        normZ = random.uniform(-0.2, 0.2)

        self.coords.append(
            np.array([normX, normY, normZ]))

    def drawLine(self, x1, y1, x2, y2, clr="black", wd=1):
        self.canvas.create_line(x1, y1, x2, y2, fill=clr, width=wd)

    def clearScreen(self):
        self.canvas.delete("all")

    def rotator(self, event):
        if event.char == "x":

            self.angleX += 0.15

        if event.char == "y":

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

    def clearCoords(self):
        self.window.update()
        self.projCoords = []

    def convertCoords(self, x, y):
        x += 400
        y += 400
        return np.array([x, y, 0])

    def connectProjectedDots(self, startNum, endNum):
        end = self.projCoords[endNum]
        start = self.projCoords[startNum]
        start = self.convertCoords(start[0], start[1])
        end = self.convertCoords(end[0], end[1])

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
            [cos(angleY), 0, sin(angleY)],
            [0, 1, 0],
            [-sin(angleY), 0, cos(angleY)]
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

    def displayCoords(self):
        self.clearScreen()
        self.updateRotation()
        self.updateProjection()

        self.projCoords = []
        centerVec = np.array([0, 0, 0], dtype=np.float64)

        for vec in self.coords:
            centerVec += vec

        centerVec /= len(self.coords)

        # transform all coords
        for proj2D in self.coords:
            transObject = np.array([
                self.translationX,
                self.translationY,
                self.translationZ,
            ])

            proj2D -= centerVec
            proj2D = proj2D @ self.rotationX
            proj2D = proj2D @ self.rotationY
            proj2D = proj2D @ self.rotationY
            proj2D += centerVec

            proj2D = proj2D @ self.projection
            proj2D += transObject

            self.projCoords.append(proj2D)

        for i in range(len(self.projCoords) - 1):
            self.connectProjectedDots(i, i + 1)

    def update(self):
        self.window.update()
        while True:
            if len(self.coords) > 0:
                self.displayCoords()
            self.canvas.update()
            time.sleep(0.01)


WindowHuindow()
