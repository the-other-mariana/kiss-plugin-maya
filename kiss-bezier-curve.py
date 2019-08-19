#File:      kiss_v6.py
#Date:      09/04/2019
#Authors:	Mariana Ramirez and Mariana Avalos
#Description: kiss plugin using bezier curve for n points

import maya.cmds as cmds
import math
import maya.OpenMaya as OM

inputRadius = 3
inputHeight = 7
sides = 22
segments = 17


mesh = OM.MFnMesh()
mergeVerts = True
pointTolerance = 0.001

Pi = 3.1416
idealRadius = 6.00
idealHeight = 13.00

verts = []

def kissBezier(ctrlPoints):

    # sets N number of points in the curve
    N = len(ctrlPoints)
    temp = OM.MPoint(0, 0, 0)
    verts.append(temp)
    
    for t in range(0, segments):
        pt = []
        v = []
        
        # initializes the lists with the control points
        for i in range(0, N):
            pt.append(ctrlPoints[i])
        for i in range(0, N - 1):
            v.append((pt[i + 1][0] - pt[i][0], pt[i + 1][1] - pt[i][1]))
            
        # creates the bezier curve
        nAux3 = 0
        for n in range(N - 1, 0, -1):
            nAux = n
            nAux2 = n
            for i in range(0, n):
                pt.append(((v[len(v) - nAux][0] / segments * t) + pt[len(v) - nAux + nAux3][0], (v[len(v) - nAux][1] / segments * t) + pt[len(v) - nAux + nAux3][1]))
                nAux -= 1
            for j in range(0, n - 1):
                v.append((pt[len(pt) - nAux2 + 1][0] - pt[len(pt) - nAux2][0], pt[len(pt) - nAux2 + 1][1] - pt[len(pt) - nAux2][1]))
                nAux2 -= 1
            nAux3 += 1
        
        # rotates the basic points in a circle
        for i in range(sides):
            # radius is now each kiss point
            radius = pt[len(pt) - 1][0] * (inputRadius / idealRadius) 
            posY = pt[len(pt) - 1][1] * (inputHeight / idealHeight)
            posX = math.sin(math.radians(360.0/sides * i)) * radius
            posZ = math.cos(math.radians(360.0/sides * i)) * radius
            temp = OM.MPoint(posX, posY, posZ)
            verts.append(temp)
            
    # sets the last point of the upper base
    temp = OM.MPoint(0, pt[len(pt) - 2][1] * (inputHeight / idealHeight), 0)
    verts.append(temp)

####################################################################################

# sets the control points in a list
ctrlPoints = [ (-6.262, 0.0, 0.0),
            (-11.995, -0.180, 0.0),
            (-8.068, 8.945, 0.0),
            (1.289, 7.576, 0.0),
            (-0.982, 11.328, 0.0),
            (-1.281, 13.693, 0.0),
            (0.062, 13.251, 0.0) ]
kissBezier(ctrlPoints)

quadArray = OM.MPointArray()
quadArray.setLength(4)

# joins the vertices in quads
for j in range(0, segments - 1):
    exception = 0
    for i in range(sides):
        if(i == sides - 1):
            # when in last loop, exception is sides and joins last quad to beginning quad
            exception = sides 
        quadArray.set(verts[(i + 1) + (sides * j)], 0)
        quadArray.set(verts[(i + 2 - exception) + (sides * j)], 1)
        quadArray.set(verts[(i + (sides + 2) - exception) + (sides * j)], 2)
        quadArray.set(verts[(i + (sides + 1)) + (sides * j)], 3)
        mesh.addPolygon(quadArray, mergeVerts, pointTolerance)

# joins the two bases in triangles
baseArray = OM.MPointArray()
baseArray.setLength(3)
for j in range(2):
    exception = 0
    for i in range(sides):
        if(i == sides - 1):
            exception = sides
        baseArray.set(verts[0 + j * (len(verts) - 1)], 0)
        baseArray.set(verts[(i + 1) + j * (sides * (segments - 1))], 1)
        baseArray.set(verts[(i + 2 - exception) + j * (sides * (segments - 1))], 2)
        mesh.addPolygon(baseArray, mergeVerts, pointTolerance)