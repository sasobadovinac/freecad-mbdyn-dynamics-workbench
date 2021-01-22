# -*- coding: utf-8 -*-
###################################################################################
#
#  Copyright 2021 Jose Gabriel Egas Ortuno
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#
###################################################################################
'''
This class animates the 3D scene according to the results provided by the MBDyn simulation. There are some rules for this class to work propperly.
First.- Each body must have a node asociated to it, and vice-versa. Dynamic nodes are asociated to rigid bodies. Static and dummy nodes are asociated to static or dummy bodies, which are both the same (zero mass bodies).
Second.- Each joint must have an arrow in the 3D scene, which is used to visualize the reaction forces over the joint. In the case of joints asociated to moving objects, 
'''

from numpy import genfromtxt
from PySide import QtCore
import FreeCAD
import FreeCADGui
#import os
#import numpy as np
import time
import tempfile

__dir__ = tempfile.gettempdir()

class Animation(object):
    def __init__(self):
        self.timer=QtCore.QTimer()#A timer for the animation
        QtCore.QObject.connect(self.timer, QtCore.SIGNAL("timeout()"),self.updateBodies)         
        self.placements = [] #List to store the initial placements of the structural bodies
        self.objects = [] #List to store al the solid bodies
        self.joints = [] #List to store al the joints
        #lists to store the center of mass of each object, so that the animation moves the objects relative to their centers of mass:        
        self.cmxs = []
        self.cmys = []
        self.cmzs = []
        #Lists to store the position of each object, so that the movements are made relative to the original positions:
        self.xxs = []
        self.yys = []
        self.zzs = []
        #Lists to store the orientation (Euler anles) of each object, so that the rorations are made relative to the original orientations:
        self.yaw = []
        self.pitch = []
        self.roll = []
        #Variables to count number of bodies and joints in the simulation:        
        self.numberjoints = 0 #Number of joints to be animated                        
        self.numberbodies = 0 #Number of bodies to be animated   
        
    def retrieve(self):#Get all the information, from the CAD model, before performing the animation
        #Clean variables:
        self.placements = [] 
        self.objects = [] 
        self.joints = []        
        self.cmxs = []
        self.cmys = []
        self.cmzs = []        
        self.xxs = []
        self.yys = []
        self.zzs = [] 
        self.yaw = []
        self.pitch = []
        self.roll = []
        self.numberjoints = 0                         
        self.numberbodies = 0
        #Sweep all the objects to count number of bodies and joints in the simulation
        for obj in FreeCAD.ActiveDocument.Objects:
            if(obj.Label.startswith('body:')):#Count number of bodies
                self.numberbodies = self.numberbodies + 1                 

            if(obj.Label.startswith('joint:')):#Count number of joints             
                self.numberjoints = self.numberjoints + 1 
                
                   
        if(self.numberbodies>0):#If there are bodies:            
            self.data = genfromtxt(__dir__ + '/MBDynCase.mov', delimiter=' ')#Read the node's data from the MBDyn output file
            #Now self.data contains the possition (x,y,x); orientation (x,y,z euler angles [deg]); velocity (vx,vy,vz); angular velocity (wx,wy,wz). See: https://www.sky-engin.jp/en/MBDynTutorial/chap07/chap07.html 
            self.initTime = 0 #Initial simulation time (for the bodies)
            #To show the time in the "Animation" scripted object in FreeCAD:
            self.timestep = float(FreeCAD.ActiveDocument.getObject("MBDyn").time_step[:-2])
            #Re-set the counter variable, which is used to iterate through the objects in the "UpdateBodies" method
            self.counter = 0
            # Final simulation time is the length of the data array minus one
            self.endTime = int(len(self.data))-1 
            #If there are joints, retrieve joint's data:
            if(self.numberjoints>0):
                self.data1 = genfromtxt(__dir__ + '/MBDynCase.jnt', delimiter=' ',  usecols=(0,1,2,3,4,5,6,7,8,9,10,11,12))
            
            for x in range(1, self.numberbodies+1):#Retrieve bodie's information in order to re/set the 3D scene after animating
                #Here I store all the bodies and their corresponing center of mass (which in FreeCAD is equal to the placement), sorted ascendingly. 
                #These placements are then used to restore the object's possitions after the animation has finished
                aux = FreeCAD.ActiveDocument.getObjectsByLabel('body: '+str(x))[0]       
                aux1 = FreeCAD.ActiveDocument.getObjectsByLabel('structural: '+str(x))[0] #Every body must have a structural node linked to it    
                #objects and placements contain all the 3D objects and their respective placements sorted ascendengly
                self.objects.append(aux)
                self.placements.append(aux.Placement)
                #Centers of mass:
                self.cmxs.append(aux.Shape.Solids[0].CenterOfMass[0])
                self.cmys.append(aux.Shape.Solids[0].CenterOfMass[1])
                self.cmzs.append(aux.Shape.Solids[0].CenterOfMass[2])
                #Initial positions:
                self.xxs.append(aux1.position_X.Value)
                self.yys.append(aux1.position_Y.Value)
                self.zzs.append(aux1.position_Z.Value)   
                #Initial orientations:
                self.yaw.append(aux1.yaw.Value)
                self.pitch.append(aux1.pitch.Value)
                self.roll.append(aux1.roll.Value) 

            for x in range(1, self.numberjoints+1):#Retrieve joint's information in order to re/set the 3D scene after animating
                #Store all the joints and their vectors in a list. The possition in the list determines the number of joint.
                jo = FreeCAD.ActiveDocument.getObjectsByLabel('joint: '+str(x))[0]
                if((jo.joint == "revolute hinge") or (jo.joint == "in line") or (jo.joint == "in plane")):                    
                    xxx,yyy,zzz = [],[],[] #Vectors for the joint's positions in the 3D scene
                    fx,fy,fz = [],[],[] #Vectors for the lenght joint's foces arrows
                    for row in self.data:#Retrieve the positions as the animation goes
                        if(row[0]==int(jo.structural_dummy)):#During the animation, revolute hinges and in-line joint folow a dummy node or a dynamic node
                            xxx.append(float(row[1])*1000.0) 
                            yyy.append(float(row[2])*1000.0)
                            zzz.append(float(row[3])*1000.0)
                            
                    for row in self.data1:#Retrieve the forces in order to make the arrow's lenght proportional to the reaction forces
                        if(row[0]==int(jo.label)):
                            if(jo.frame=="local"):#Animate forces relative to the local reference frame
                                fx.append(float(row[2])*float(jo.force_vector_multiplier))#Scale the vector according to the multiplier 
                                fy.append(float(row[1])*float(jo.force_vector_multiplier))
                                fz.append(float(row[3])*float(jo.force_vector_multiplier))
                            
                            if(jo.frame=="global"):#Animate forces relative to the global reference frame
                                fx.append(float(row[7])*float(jo.force_vector_multiplier))#Scale the vector according to the multiplier 
                                fy.append(float(row[8])*float(jo.force_vector_multiplier))
                                fz.append(float(row[9])*float(jo.force_vector_multiplier))
                            
                    ve = FreeCAD.ActiveDocument.getObjectsByLabel('jf: '+str(x))[0]#get the vector itself
                    self.joints.append([ve,xxx,yyy,zzz,fx,fy,fz,jo.animate,"none"])#Store the vector, the possitions of the asociated node (if the vector will move with the node), and the reaction force vectors
                
                #These joints do not follow any moving body in the 3D scene, thus, I do not have to retrieve the possitions of the bodies they will follow
                if((jo.joint == "revolute pin") or (jo.joint == "clamp") or (jo.joint == "drive hinge") or (jo.joint == "axial rotation") or (jo.joint == "prismatic") 
                   or (jo.joint == "deformable displacement joint") or (jo.joint == "spherical hinge")):
                    xxx,yyy,zzz = [],[],[] #Vectors for the joint's positions in the 3D scene
                    fx,fy,fz = [],[],[] #Vectors for the lenght joint's foces arrows
                    for row in self.data1: #Store the constan possition of these vectors in the 3D scene
                        if(row[0]==1):                            
                            xxx.append(jo.position_X.Value)  
                            yyy.append(jo.position_Y.Value)
                            zzz.append(jo.position_Z.Value)
                    
                    for row in self.data1:#Retrieve the forces in order to make the arrow's lenght proportional to the reaction forces
                        if(row[0]==int(jo.label)):
                            if(jo.frame=="local"):#Animate forces relative to the local reference frame
                                fx.append(float(row[2])*float(jo.force_vector_multiplier))#Scale the vector according to the multiplier 
                                fy.append(float(row[1])*float(jo.force_vector_multiplier))
                                fz.append(float(row[3])*float(jo.force_vector_multiplier))        
                            
                            if(jo.frame=="global"):#Animate forces relative to the global reference frame
                                fx.append(float(row[7])*float(jo.force_vector_multiplier))#Scale the vector according to the multiplier 
                                fy.append(float(row[8])*float(jo.force_vector_multiplier))
                                fz.append(float(row[9])*float(jo.force_vector_multiplier))        

                            
                    ve = FreeCAD.ActiveDocument.getObjectsByLabel('jf: '+str(x))[0]#get the vector itself
                    
                    if (jo.joint != "deformable displacement joint"):#These joints do not have a flexible spring in the 3D view
                        self.joints.append([ve,xxx,yyy,zzz,fx,fy,fz,jo.animate,"none"])#Store the vector, the possitions of the asociated node (if the vector will move with the node), and the reaction force vectors
                    
                    if (jo.joint == "deformable displacement joint"):#If the joint is a deformable displacement joint, it must have a spring, so get the spring
                        sp = FreeCAD.ActiveDocument.getObjectsByLabel('sp: '+str(x))[0]#get the spring
                        le = FreeCAD.ActiveDocument.getObjectsByLabel('sp: '+str(x))[0].Height#Get the spring's lenght, to restore after the animation
                        self.joints.append([ve,xxx,yyy,zzz,fx,fy,fz,jo.animate,sp,le,jo.node_1,jo.node_2])#Store the vector, the possitions of the asociated node (if the vector will move with the node), and the reaction force vectors
    
    def getJointsPossitions(self,bodynumber):
        xyz = []            
        for row in self.data:
            if(row[0]==bodynumber):
                aux = float(row[1])#,float(row[2]),float(row[3])]
                xyz.append(aux)
        
        return xyz
               
    
    def updateBodies(self):#This method updates the placement of all the bodies and also moves the arrows to animate the reaction forces
        self.counter = self.counter+1
        FreeCAD.ActiveDocument.getObject("Animation").current_time = str(self.timestep*self.counter)+' s'
        if(self.initTime >= self.endTime):
            self.counter = 0                        
            if(FreeCAD.ActiveDocument.getObject("Animation").continous == "true"):
                time.sleep(1)
                self.initTime=0 # re-set the time for next animation
            
            if(FreeCAD.ActiveDocument.getObject("Animation").continous == "false"):
                self.stop()
                      
        for x in range(0, self.numberbodies):#Move all the bodies
            aux = self.data[self.initTime + x]#Get the possition data at current time for the current joint
            #get the possition from the MBDyn results:                
            position = FreeCAD.Vector((aux[1]*1000)-self.xxs[int(aux[0])-1],(aux[2]*1000)-self.yys[int(aux[0])-1],(aux[3]*1000)-self.zzs[int(aux[0])-1])
            #rotation = FreeCAD.Rotation(aux[6],aux[5]-self.pitch[int(aux[0])-1],aux[4]+0)#get the rotation from the MBDyn results
            rotation = FreeCAD.Rotation(aux[4],aux[5],aux[6])#get the rotation from the MBDyn results
            #rotationcenter = FreeCAD.Vector(self.cmxs[int(aux[0])-1],self.cmys[int(aux[0])-1],self.cmzs[int(aux[0])-1])#The rotation center is the center of mass
            rotationcenter = FreeCAD.Vector((self.xxs[int(aux[0])-1]),(self.yys[int(aux[0])-1]),(self.zzs[int(aux[0])-1]))#The rotation center is the node´s position
            
            self.objects[int(aux[0])-1].Placement = FreeCAD.Placement(position, rotation, rotationcenter).multiply(self.placements[int(aux[0])-1])   #AQUI PUEDE ESTAR EL ERROR!!    
            
            #self.objects[int(aux[0])-1].Placement = FreeCAD.Placement(position, rotation, rotationcenter)
            #App.Placement(position, App.Rotation(App.Vector(0,1,0),pitch), rotationcenter)
            #App.Placement(position, App.Rotation(App.Vector(0,0,1),yae), rotationcenter)            
            #App.Placement(App.Vector(Px,Py,Pz), App.Rotation(App.Vector(1,0,0),roll), App.Vector(RCx,RCy,Rcz))
        
        #Here I update the joint's force vectors and the springs in the case of deformable displacement joints
        for y in range(0, self.numberjoints):#Unpate all the joint's vectors 
            if(self.joints[y][7]=='true'):#Only if the "animate" property is set to true
                a = float(self.joints[y][1][int(self.initTime/self.numberbodies)])
                b = float(self.joints[y][2][int(self.initTime/self.numberbodies)])
                c = float(self.joints[y][3][int(self.initTime/self.numberbodies)])
                fx = float(self.joints[y][4][int(self.initTime/self.numberbodies)])
                fy = float(self.joints[y][5][int(self.initTime/self.numberbodies)])
                fz = float(self.joints[y][6][int(self.initTime/self.numberbodies)])
                self.joints[y][0].Start = (a, b, c)
                #self.joints[y][0].Dimline = (a, b, c)
                self.joints[y][0].End = (a+fx, b+fy, c+fz)
                #FreeCADGui.ActiveDocument.getObject(self.joints[y][0].Name).ArrowSize = str( (abs(fx)+abs(fy)+abs(fz))/20 )
                self.joints[y][0].recompute()
                
            if(self.joints[y][8] !='none'):                
                Length = FreeCAD.ActiveDocument.getObjectsByLabel('body: '+self.joints[y][11])[0].Shape.Solids[0].CenterOfMass[2]
                self.joints[y][8].Height = Length
                self.joints[y][8].Pitch =  Length / 5
      
            
        self.initTime = self.initTime+self.numberbodies
        
            
            
    def restore(self):#Restore all the bodies to their original placements and all the vectors to their original start and end points
        FreeCAD.ActiveDocument.getObject("Animation").current_time = '0 s'
        #Restores all the bodies to their original placements:
        for x in range(0, self.numberbodies):
            self.objects[x].Placement=FreeCAD.ActiveDocument.getObjectsByLabel(self.objects[x].label)[0].Placement
                           
        #Rstore the springs linked to all the mass-spring-damper joints   
        for obj in FreeCAD.ActiveDocument.Objects:             
            if obj.Label.startswith('joint: ') and obj.joint == "deformable displacement joint":
                l = FreeCAD.ActiveDocument.getObjectsByLabel("sp: "+obj.label)[0]
                l.Height = FreeCAD.ActiveDocument.getObjectsByLabel('body: '+obj.node_2)[0].Shape.Solids[0].CenterOfMass[2]
                l.Pitch = FreeCAD.ActiveDocument.getObjectsByLabel('body: '+obj.node_2)[0].Shape.Solids[0].CenterOfMass[2] / 5
                  
        #Restores all the froces vectors: 
        for y in range(1, self.numberjoints+1):
            jo = FreeCAD.ActiveDocument.getObjectsByLabel('joint: '+str(y))[0]
            a = jo.position_X.Value
            b = jo.position_Y.Value
            c = jo.position_Z.Value
            length = FreeCAD.ActiveDocument.getObjectsByLabel("X")[0].End[0]/4
            #FreeCADGui.ActiveDocument.getObject(self.joints[y-1][0].Name).ArrowSize = str(length/30)+' mm'
            self.joints[y-1][0].Start = (a, b, c)
            self.joints[y-1][0].End = (a+length, b+length, c+length)
            self.joints[y-1][0].recompute()
        
        #Show all the elements that were hidden:                
        for obj in FreeCAD.ActiveDocument.Objects:
            if obj.Label.startswith('structural: ') or obj.Label.startswith('joint: '):               
                FreeCADGui.ActiveDocument.getObject(obj.Name).Visibility = True   


            
            
    def start(self):
        self.retrieve()
        self.restore() 
        speed = float(FreeCAD.ActiveDocument.getObject("Animation").speed)
        #Hide all the elements that are not part of the animation:
        for obj in FreeCAD.ActiveDocument.Objects:
            if obj.Label.startswith('structural: '):
                FreeCADGui.ActiveDocument.getObject(obj.Name).Visibility = False

            if obj.Label.startswith('joint: ') and obj.animate == "false":
                FreeCADGui.ActiveDocument.getObject(obj.Name).Visibility = False                

            if obj.Label.startswith('joint: ') and obj.animate == "true":
                FreeCADGui.ActiveDocument.getObject(obj.Name).Visibility = False
                l = FreeCAD.ActiveDocument.getObjectsByLabel("jf: "+obj.label)[0]
                FreeCADGui.ActiveDocument.getObject(l.Name).Visibility = True
            
            if obj.Label.startswith('joint: ') and obj.animate == "true" and obj.joint == "deformable displacement joint":
                FreeCADGui.ActiveDocument.getObject(obj.Name).Visibility = False
                l = FreeCAD.ActiveDocument.getObjectsByLabel("jf: "+obj.label)[0]
                FreeCADGui.ActiveDocument.getObject(l.Name).Visibility = True            
                l = FreeCAD.ActiveDocument.getObjectsByLabel("sp: "+obj.label)[0]
                FreeCADGui.ActiveDocument.getObject(l.Name).Visibility = True    
        
                                    
        if(self.numberbodies>0):#Animate only if there are bodies to animate:
            self.timer.start(speed)
   
    def stop(self):
        self.timer.stop()