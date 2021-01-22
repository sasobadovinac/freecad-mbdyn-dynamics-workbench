# -*- coding: utf-8 -*-
from numpy import genfromtxt
from PyQt4 import QtCore
import FreeCAD
import os

__dir__ = os.path.dirname(__file__)

class Animation(object):
    def __init__(self):
        self.timer=QtCore.QTimer()
        self.placements = [] #List to store the initial placements of the structural bodies
        self.objects = [] #List to store al the solid bodies
        self.joints = [] #List to store al the joints
        #lists to store the center of mass of each object, so that the animation moves the objects relative to their centers of mass:        
        self.cmxs = []
        self.cmys = []
        self.cmzs = []
        #Lists to store the orientation (Euler anles) of each object, so that the rorations are made relative to the original orientations:
        self.xxs = []
        self.yys = []
        self.zzs = []
        self.error = 1.0/100.0
        QtCore.QObject.connect(self.timer, QtCore.SIGNAL("timeout()"),self.updateBodies)         
        #Count number of bodies and joints in the simulation:        
        self.numberjoints = 0 #Number of joints to be animated                        
        self.numberbodies = 0 #Number of bodies to be animated 
        for obj in FreeCAD.ActiveDocument.Objects:
            if(obj.Label.startswith('body:')):#Count number of bodies
                self.numberbodies = self.numberbodies + 1                 

            if(obj.Label.startswith('joint:')):#Count number of joints             
                self.numberjoints = self.numberjoints + 1 

                        
        if(self.numberbodies>0):#If there are bodies:
            self.data = genfromtxt(__dir__ + '/MBDyn/MBDynCase.mov', delimiter=' ')#read nodes data
            # data contains the possition (x,y,x); orientation (x,y,z euler angles [deg]); velocity (vx,vy,vz); angular velocity (wx,wy,wz). See: https://www.sky-engin.jp/en/MBDynTutorial/chap07/chap07.html 
            self.initTime = 0 #Initial simulation time (for the bodies)
            self.initTime1 = 0 #Initial simulation time (for the joints)
            self.endTime = int(len(self.data))-1 # Final simulation time is the length of the data array minus one
            #There must be bodies for joints to exist: 
            if(self.numberjoints>0):#If there are joints, retrieve joint's data:
                self.data1 = genfromtxt(__dir__ + '/MBDyn/MBDynCase.jnt', delimiter=' ',  usecols=(0,1,2,3,4,5,6,7,8,9,10,11,12))
            
            for x in range(1, self.numberbodies+1):
                #Stores all the bodies and their corresponing center of mass (equal to the placement), sorted ascendingly. 
                #The placements are then used to restore the object's possitions after the animation 
                aux = FreeCAD.ActiveDocument.getObjectsByLabel('body: '+str(x))[0]       
                aux1 = FreeCAD.ActiveDocument.getObjectsByLabel('structural: '+str(x))[0]       
                self.objects.append(aux)
                self.placements.append(aux.Placement)
                self.cmxs.append(aux.Shape.Solids[0].CenterOfMass[0])
                self.cmys.append(aux.Shape.Solids[0].CenterOfMass[1])
                self.cmzs.append(aux.Shape.Solids[0].CenterOfMass[2])
                self.xxs.append(float(aux1.position.split(',')[0]))
                self.yys.append(float(aux1.position.split(',')[1]))
                self.zzs.append(float(aux1.position.split(',')[2][:-2]))                

            for x in range(1, self.numberjoints+1):
                #Store all the joints and their vectores in a list. The possition in the list determines the number of joint.
                j = FreeCAD.ActiveDocument.getObjectsByLabel('joint: '+str(x))[0]
                f = FreeCAD.ActiveDocument.getObjectsByLabel('jf: '+str(x))[0]
                self.joints.append([j,f])
                     
    
    def updateBodies(self):
        #Obtain node at current time:
        aux1 = self.data[self.initTime][0]            
        #move objects relative to their center of mass:  
        if(aux1==1):#Update all the bodie's possitions every time the first body is found in the .mov file:
            self.initTime1 = self.initTime1+1
            for x in range(0, self.numberbodies):#Move all the bodies
                aux = self.data[self.initTime + x]#Get the data at current time for the current joint
                #get the possition from the MBDyn results:                
                poss = FreeCAD.Vector((aux[1]-self.xxs[int(aux[0])-1])*1000.0,(aux[2]-self.yys[int(aux[0])-1])*1000.0,(aux[3]-self.zzs[int(aux[0])-1])*1000.0)
                rotation = FreeCAD.Rotation(aux[6],aux[5],aux[4])#get the rotation from the MBDyn results
                rotationcenter = FreeCAD.Vector(self.cmxs[int(aux[0])-1],self.cmys[int(aux[0])-1],self.cmzs[int(aux[0])-1])#The rotation center is the center of mass
                self.objects[int(aux[0])-1].Placement = FreeCAD.Placement(poss, rotation, rotationcenter).multiply(self.placements[int(aux[0])-1])                
       
        if(self.numberjoints>0):#Animate the joint's force vectors only if there are joints
            aux2 = self.data1[self.initTime1-1][0]
            if(aux2==1):#update all the joint's vectors when the first joint is found in the .jnt output file
                for y in range(0, self.numberjoints):#Unpate all the joint's vectors
                    auxj = self.data1[self.initTime1 +y]#Get the data at current time for the current joint
                    current_joint = self.joints[y][0].joint#To see what kind of joint (hinge, pin, clamp, etc) is currently being updated
                    animate = self.joints[y][0].animate#See if the joint is supposed to be animated                  
                    force_vector_multiplier = float(self.joints[y][0].force_vector_multiplier)#Get the joint's multipliers
                    frame = self.joints[y][0].frame#Get the joint's frame (local or global forces)                                      
                    if((current_joint=='revolute hinge')and(animate=='true')):#Update the revolute hinges (move the origin)
                        #update the lines (vectors): 
                        body = 'body: '+str(self.joints[y][0].structural_dummy)#Get the dummy body asociated to the joint
                        #Get the asociated dumy node's possition:
                        xx = FreeCAD.ActiveDocument.getObjectsByLabel(body)[0].Shape.CenterOfMass[0]
                        yy = FreeCAD.ActiveDocument.getObjectsByLabel(body)[0].Shape.CenterOfMass[1]
                        zz = FreeCAD.ActiveDocument.getObjectsByLabel(body)[0].Shape.CenterOfMass[2]
                        self.joints[y][1].X1 = str(xx)+' mm'
                        self.joints[y][1].Y1 = str(yy)+' mm'
                        self.joints[y][1].Z1 = str(zz)+' mm'     
                        if(frame=='local'):#Animate the reaction forces in local frame
                            self.joints[y][1].X2 = str(xx-auxj[1]*force_vector_multiplier)+' mm'                       
                            self.joints[y][1].Y2 = str(yy-auxj[2]*force_vector_multiplier)+' mm'                       
                            self.joints[y][1].Z2 = str(zz-auxj[3]*force_vector_multiplier)+' mm'
                            return
                        if(frame=='global'):#Animate the reaction forces in global frame
                            self.joints[y][1].X2 = str(xx-auxj[7]*force_vector_multiplier)+' mm'                       
                            self.joints[y][1].Y2 = str(yy-auxj[8]*force_vector_multiplier)+' mm'                       
                            self.joints[y][1].Z2 = str(zz-auxj[9]*force_vector_multiplier)+' mm' 
                            return
                        return
                    
                    if((current_joint=='revolute pin')and(animate=='true')):#Update the revolute pins (don't move the origin)
                        #update the three lines (vectors): 
                        xx = float(str(self.joints[y][1].X1)[:-3])                    
                        yy = float(str(self.joints[y][1].Y1)[:-3])
                        zz = float(str(self.joints[y][1].Z1)[:-3])
                        if(frame=='local'):#Animate the reaction forces in local frame
                            self.joints[y][1].X2 = str(xx-auxj[1]*force_vector_multiplier)+' mm'                       
                            self.joints[y][1].Y2 = str(yy-auxj[2]*force_vector_multiplier)+' mm'                       
                            self.joints[y][1].Z2 = str(zz-auxj[3]*force_vector_multiplier)+' mm'
                            return
                        if(frame=='global'):#Animate the reaction forces in global frame
                            self.joints[y][1].X2 = str(xx-auxj[7]*force_vector_multiplier)+' mm'                       
                            self.joints[y][1].Y2 = str(yy-auxj[8]*force_vector_multiplier)+' mm'                       
                            self.joints[y][1].Z2 = str(zz-auxj[9]*force_vector_multiplier)+' mm' 
                            return
                        return
                    
                    if((current_joint=='clamp')and(animate=='true')):#Update the clamps (don't move the origin)
                        #update the three lines (vectors): 
                        xx = float(str(self.joints[y][1].X1)[:-3])                    
                        yy = float(str(self.joints[y][1].Y1)[:-3])
                        zz = float(str(self.joints[y][1].Z1)[:-3])
                        if(frame=='local'):#Animate the reaction forces in local frame
                            self.joints[y][1].X2 = str(xx-auxj[1]*force_vector_multiplier)+' mm'                       
                            self.joints[y][1].Y2 = str(yy-auxj[2]*force_vector_multiplier)+' mm'                       
                            self.joints[y][1].Z2 = str(zz-auxj[3]*force_vector_multiplier)+' mm'
                            return
                        if(frame=='global'):#Animate the reaction forces in global frame
                            self.joints[y][1].X2 = str(xx-auxj[7]*force_vector_multiplier)+' mm'                       
                            self.joints[y][1].Y2 = str(yy-auxj[8]*force_vector_multiplier)+' mm'                       
                            self.joints[y][1].Z2 = str(zz-auxj[9]*force_vector_multiplier)+' mm'
                            return                            
                        return
                    
                    if((current_joint=='axial rotation')and(animate=='true')):#Update the clamps (don't move the origin)
                        #update the three lines (vectors): 
                        xx = float(str(self.joints[y][1].X1)[:-3])                    
                        yy = float(str(self.joints[y][1].Y1)[:-3])
                        zz = float(str(self.joints[y][1].Z1)[:-3])
                        if(frame=='local'):#Animate the reaction forces in local frame
                            self.joints[y][1].X2 = str(xx-auxj[1]*force_vector_multiplier)+' mm'                       
                            self.joints[y][1].Y2 = str(yy-auxj[2]*force_vector_multiplier)+' mm'                       
                            self.joints[y][1].Z2 = str(zz-auxj[3]*force_vector_multiplier)+' mm'
                            return
                        if(frame=='global'):#Animate the reaction forces in global frame
                            self.joints[y][1].X2 = str(xx-auxj[7]*force_vector_multiplier)+' mm'                       
                            self.joints[y][1].Y2 = str(yy-auxj[8]*force_vector_multiplier)+' mm'                       
                            self.joints[y][1].Z2 = str(zz-auxj[9]*force_vector_multiplier)+' mm' 
                            return
                        return
                           
            
        self.initTime = self.initTime+1#Increase time
        if(self.initTime == self.endTime):            
            self.initTime=0 # re-set the time for next animation
            self.initTime1=0 # re-set the time for next animation
            
    def restore(self):#Restores all the bodies to their original placements
        for x in range(0, self.numberbodies):
            self.objects[x].Placement=self.placements[x]    
       
    def start(self, speed):
        if(self.numberbodies>0):#Animate only if there are bodies to animate:
            self.timer.start(speed)
   
    def stop(self):
        self.timer.stop()