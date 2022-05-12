from hashlib import new
import math
import random
import time
from nis import match
import tkinter as tk
from tkinter import *
from turtle import clearscreen, update
import numpy as np
# lerp = np.interp
# matmul = np.matmul
#add =  np.+operator
#norm2 = np.linalg.norm

class WindowHuindow:
    def __init__(self) -> None:
        pass
        self.window = tk.Tk()
        self.window.geometry("800x600")
        self.window.bind("<Key>",self.rotator)
        self.window.bind("<Button 1>", self.placeDot)
        self.w = Canvas(self.window, width=800, height=600) 
        self.w.place(x=0, y=0)

        self.coords = np.array([[0,0,0]])
        self.projCoords = np.array([[]])
        #projection matrix
        self.projection = np.array([[]])

        #rotation matrix for each axis
        self.rotationX = np.zeros((3,3))
        self.rotationZ = np.zeros((3,3))
        self.rotationY = np.zeros((3,3))

        #translationvec
        self.translation = np.array([[]])

        #translation params
        self.translationX = 0
        self.translationY = 0
        self.translationZ = 0

        #scale params for all axis
        self.scaleX = 800
        self.scaleY = 800
        self.scaleZ = 800

        #rotation params for all axis
        self.angleX = 0.
        self.angleY = 0.
        self.angleZ = 0.
        self.update()
        self.window.mainloop()

    def setPixel(self,x, y):
        self.w.create_rectangle((x,y)*2)

    def placeDot(self,event):
        self.setPixel(event.x,event.y)
        self.coords = np.append(self.coords,[[event.x,event.y,random.uniform(-0.2,0.2)]],axis=0)

    def connectDots(self,arr:np.ndarray):
        print(arr.shape)
        if arr.shape[0] > 2:
            for i in range(1,arr.shape[0]-1):
                self.drawLine(arr[i][0],arr[i][1],arr[i+1][0],arr[i+1][1])

    def drawLine(self,x1,y1,x2,y2, clr="black", wd = 2):
        self.w.create_line(x1,y1,x2,y2, fill=clr, width=wd)

    def clearScreen(self):
        self.w.delete("all")

    # def coordsAdd(self,arr, x,y,z):
    #     arr = np.append(arr,[[x,y,z]],axis=0)
    #     return arr

    def rotator(self,event):
        if event.char == "x":
            
            self.angleX+=0.15

        if event.char == "y":
            
            self.angleY+=0.15

        if event.char == "z":
         
            self.angleZ+=0.15

        if event.char == "q":

            self.translationX+=0.15

        if event.char == "w":
            self.translationY+=0.15

        if event.char == "e":
            self.translationZ+=0.15

        if event.char =="a":
            self.scaleX += 1

        if event.char =="s":
            self.scaleY+= 1 

        if event.char =="d":
            self.scaleZ += 1            

    def clearCoords(self):
        self.coords = np.array([[]])
        self.projCoords = np.array([[]])
        self.rojection = np.array([[]])
        self.rotationX = np.array([[]])
        self.rotationZ = np.array([[]])
        self.rotationY = np.array([[]])
        self.translation = np.array([[]])
        self.translationX = 0
        self.translationY = 0
        self.translationZ = 0
        self.scaleX = 800
        self.scaleY = 800
        self.scaleZ = 800
        self.angleX = 0
        self.angleY = 0
        self.angleZ = 0
            
    def convertCoords(x,y):
        x+= 400
        y+= 300
        return  np.array([[x,y,0]])

    def connectProjectedDots(self,startNum, endNum):
        end = self.projCoords[endNum]
        start = self.projCoords[startNum]
        start = self.convertCoords(start.x,start.y)
        end = self.convertCoords(end.x,end.y)
        self.drawLine(start.x,start.y,end.x,end.y)

    def updateRotation(self):
        #self.rotationX = np.delete(self.rotationX)
        self.rotationX = np.zeros((3,3))
        self.rotationX = np.vstack([self.rotationX,[1,0,0]])
        self.rotationX = np.vstack([self.rotationX,[0,math.cos(self.angleX),-math.sin(self.angleX)]])
        self.rotationX = np.vstack([self.rotationX,[0,math.sin(self.angleX),math.cos(self.angleX)]])

        self.rotationY = np.zeros((3,3))
        self.rotationY = np.vstack([self.rotationY,[math.cos(self.angleY),0,math.sin(self.angleY)]])
        self.rotationY = np.vstack([self.rotationY,[0,1,0]])
        self.rotationY = np.vstack([self.rotationY,[-math.sin(self.angleY),0,math.cos(self.angleY)]])

        self.rotationZ = np.zeros((3,3))
        self.rotationZ = np.vstack([self.rotationZ,[math.cos(self.angleZ),-math.sin(self.angleZ),0]])
        self.rotationZ = np.vstack([self.rotationZ,[math.sin(self.angleZ),math.cos(self.angleZ),0]])
        self.rotationZ = np.vstack([self.rotationZ,[0,0,1]])

    def updateProjection(self):
        print(np.array([1.0,0.0,0.0])*self.scaleX)
        self.projection = np.zeros((3,3))
        self.projection = np.vstack([self.projection,np.array([1.0,0.0,0.0])*self.scaleX])
        self.projection = np.vstack([self.projection,np.array([0.0,1.0,0.0])*self.scaleY])
        self.projection = np.vstack([self.projection,np.array([0.0,0.0,1.0])*self.scaleZ])

    def displayCoords(self):
        self.clearScreen()
        self.updateRotation()
        self.updateProjection()
        self.projCoords = np.array([0,0,0])
        centerVec = np.array([0,0,0],dtype=np.float64)
        for i in range(self.coords.shape[0]-1):
            centerVec+= np.array([self.coords[i][0],self.coords[i][1],self.coords[i][2]])


        centerVec *= np.array([1/self.coords.shape[0]-1])
        convertedCoords = np.array([])
        for i in range(1,self.coords.shape[0]-1):
            proj2D = np.array([self.coords[i][0],self.coords[i][1],self.coords[i][2]])
            transObj = np.array([self.translationX,self.translationY,self.translationZ])
            proj2D += centerVec * -1
            proj2D = np.matmul(self.rotationX,proj2D)
            proj2D = np.matmul(self.rotationY,proj2D)
            proj2D = np.matmul(self.rotationZ,proj2D)
            proj2D += centerVec
            proj2D *= transObj
            self.projCoords = np.append(self.projCoords,proj2D)
            convertedCoords = self.convertCoords(proj2D[0],proj2D[1])
            self.setPixel(convertedCoords[0],convertedCoords[1])
        self.connectDots(convertedCoords)
    def update(self):
        while True:
            self.displayCoords()
            self.window.update()
            time.sleep(0.1)
        


WindowHuindow()





