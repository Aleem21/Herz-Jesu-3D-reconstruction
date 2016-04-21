import numpy as np
from main import *

global folder, image_extension, camera_extension, projection_matrix_extension

class Camera:

    def __init__(self, filename):

        self.filename = filename

        file = open(name=folder+self.filename+image_extension+camera_extension, mode='r')

        lines = file.readlines()

        self.cameraMatrix = np.array([[float(digit) for digit in line.split()] for line in lines[:3]])

        self.distCoeffs = np.array(np.zeros(shape=(5,)))

        self.R = np.array([[float(digit) for digit in line.split()] for line in lines[4:7]])
        self.R = np.transpose(self.R)

        self.t = np.array([float(digit) for digit in lines[7].split()])
        self.t = -(self.R).dot(self.t)

        file.close()

    def readProjectionMatrix(self):
        file = open(name=folder+self.filename+image_extension+projection_matrix_extension, mode='r')
        self.P = np.array([[float(digit) for digit in line.split()] for line in file.readlines()[:3]])
        file.close()

        return self.P

    def checkParams(self):
        print "P':"
        print (self.cameraMatrix).dot(np.hstack([self.R, (self.t).reshape(3,1)]))

        print 'P:'
        print self.readProjectionMatrix()

    def getParams(self):
        return self.cameraMatrix, self.distCoeffs, self.R, self.t

    def showParams(self):
        print self.cameraMatrix
        print self.distCoeffs
        print self.R
        print self.t