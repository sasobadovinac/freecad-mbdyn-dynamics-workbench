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


#from FreeCAD.Units.Units import FreeCAD.Units.Unit,FreeCAD.FreeCAD.Units.Units.Quantity
import FreeCAD, FreeCADGui
from PySide import QtGui
from random import random
import subprocess
import os
from sys import platform
#Import the required clases
from gravity import Gravity
from mbdyn import MBDyn
from createworld import Createworld
from animation_parameters import Animation_parameters
from rigidbody import Rigidbody
from structuraldynamicnode import Structuraldynamicnode
from revolutepin import Revolutepin
from dummynode import Dummynode
from dummybody import Dummybody
from revolutehinge import Revolutehinge
from structuralstaticnode import Structuralstaticnode
from clamp import Clamp
from inline import Inline
from inplane import Inplane
from prismatic import Prismatic
from axialrotation import Axialrotation
from writeinpfile import Writeinpfile
from animation import Animation
from plot import Plotnode, Plotjoint
from customview import CustomView
from structuralforce import StructuralForce
from deformabledisplacement import DeformableDisplacement
from drivehinge import Drivehinge
from sphericalhinge import Sphericalhinge
from controldata import ControlData
import ObjectsFem
import tempfile

ani = Animation()

__dir__ = os.path.dirname(__file__)

class Dynamics:
    def __init__(self):
        return

#########################################################################################################################################################################################################################################################    
    def AddRigidBody(self, baseBody):#This metod receives a non-parametric body and creates a rigid body
        existingbodies = 0
        for obj1 in FreeCAD.ActiveDocument.Objects:#Count the existing bodies            
            if obj1.Label.startswith('body'):
                existingbodies = existingbodies+1
        #If a body with the next label already exists, rename it:
        if(len(FreeCAD.ActiveDocument.getObjectsByLabel(str(existingbodies+1)))>0):
            FreeCAD.ActiveDocument.getObjectsByLabel(str(existingbodies+1))[0].Label=str(existingbodies+2)
                        
        baseBody.Label=str(existingbodies+1)                
        FreeCADGui.ActiveDocument.getObject(baseBody.Name).Visibility=False
        obj = 'body_'+baseBody.Label
        a = FreeCAD.ActiveDocument.addObject("Part::FeaturePython",obj)
        Rigidbody(a,baseBody)#Create the rigid body
        a.Shape = baseBody.Shape 
        a.Label='body: '+baseBody.Label
        FreeCAD.ActiveDocument.getObject("Rigid_bodies").addObject(a)              
        a.ViewObject.Transparency = 85
        a.ViewObject.LineWidth = 1.00
        a.ViewObject.PointSize = 1.00
        c1,c2,c3=random(),random(),random()
        a.ViewObject.LineColor = (c1,c2,c3)
        a.ViewObject.PointColor = (c1,c2,c3)
        a.ViewObject.ShapeColor = (c1,c2,c3)
        #a.ViewObject.Selectable = False
        a.ViewObject.Proxy=0 
        #Add the material to the rigid body:
        material_object = ObjectsFem.makeMaterialSolid(FreeCAD.ActiveDocument)
        material_object.Label="material: "+baseBody.Label        
        mat = material_object.Material
        mat['Name'] = "Steel-Generic"
        mat['YoungsModulus'] = "210000 MPa"
        mat['PoissonRatio'] = "0.30"
        mat['Density'] = "7900 kg/m^3"
        material_object.Material = mat
        FreeCAD.ActiveDocument.getObject("Materials").addObject(material_object)             
#########################################################################################################################################################################################################################################################            
    def AddDummyOrStaticBody(self, baseBody):
        FreeCADGui.ActiveDocument.getObject(baseBody.Name).Visibility=False
        existingbodies = 0
        for obj1 in FreeCAD.ActiveDocument.Objects:#Count the existing bodies            
            if obj1.Label.startswith('body'):
                existingbodies = existingbodies+1
        #If a adding body withe the label already exists, rename it:
        if(len(FreeCAD.ActiveDocument.getObjectsByLabel(str(existingbodies+1)))>0):
            FreeCAD.ActiveDocument.getObjectsByLabel(str(existingbodies+1))[0].Label=str(existingbodies+2)        

        baseBody.Label=str(existingbodies+1)        
        obj = 'body_'+baseBody.Label
        a = FreeCAD.ActiveDocument.addObject("Part::FeaturePython",obj)
        Dummybody(a, baseBody, baseBody.Label)
        FreeCAD.ActiveDocument.getObject("Dummy_bodies").addObject(FreeCAD.ActiveDocument.getObjectsByLabel(obj)[0])
        FreeCAD.ActiveDocument.getObjectsByLabel(obj)[0].Shape = baseBody.Shape
        FreeCAD.ActiveDocument.getObjectsByLabel(obj)[0].Label='body: '+baseBody.Label
        FreeCADGui.ActiveDocument.getObject(obj).Transparency = 85
        FreeCADGui.ActiveDocument.getObject(obj).LineWidth = 1.00
        FreeCADGui.ActiveDocument.getObject(obj).PointSize = 1.00
        #FreeCADGui.ActiveDocument.getObject(obj).Selectable = False
        a.ViewObject.Proxy=0        
#########################################################################################################################################################################################################################################################        
    def AddStructuralDynamicNode(self, baseBody):
        obj = 'structural_'+baseBody.Label
        node = FreeCAD.ActiveDocument.addObject("Part::FeaturePython",obj)
        Structuraldynamicnode(node,baseBody)
        CustomView(node.ViewObject)
        node.Label = 'structural: '+baseBody.Label  
        #Move objects to their container
        FreeCAD.ActiveDocument.getObject("Dynamic_nodes").addObject(node)
        node.addObject(FreeCAD.ActiveDocument.getObjectsByLabel('x: structural: '+baseBody.Label)[0])
        node.addObject(FreeCAD.ActiveDocument.getObjectsByLabel('y: structural: '+baseBody.Label)[0])
        node.addObject(FreeCAD.ActiveDocument.getObjectsByLabel('z: structural: '+baseBody.Label)[0])   
#########################################################################################################################################################################################################################################################               
    def AddStructuralStaticNode(self, baseBody):    
        obj = 'structural_'+baseBody.Label
        a = FreeCAD.ActiveDocument.addObject("Part::FeaturePython",obj)
        Structuralstaticnode(a,baseBody)
        CustomView(a.ViewObject)
        a.Label = "structural: "+baseBody.Label
        #Move objects to their container:
        FreeCAD.ActiveDocument.getObject("Static_nodes").addObject(a) 
        a.addObject(FreeCAD.ActiveDocument.getObjectsByLabel("x: structural: "+baseBody.Label)[0])
        a.addObject(FreeCAD.ActiveDocument.getObjectsByLabel("y: structural: "+baseBody.Label)[0])
        a.addObject(FreeCAD.ActiveDocument.getObjectsByLabel("z: structural: "+baseBody.Label)[0])        
#########################################################################################################################################################################################################################################################               
    def AddStructuralDumyNode(self, node, baseBody):
        obj = 'structural_'+baseBody.Label
        a = FreeCAD.ActiveDocument.addObject("Part::FeaturePython",obj)
        Dummynode(a, node ,baseBody) 
        CustomView(a.ViewObject)
        a.Label='structural: '+baseBody.Label 
        #Move objects to their container
        FreeCAD.ActiveDocument.getObject("Dummy_nodes").addObject(a)
        a.addObject(FreeCAD.ActiveDocument.getObjectsByLabel("x: structural: "+baseBody.Label)[0])
        a.addObject(FreeCAD.ActiveDocument.getObjectsByLabel("y: structural: "+baseBody.Label)[0])
        a.addObject(FreeCAD.ActiveDocument.getObjectsByLabel("z: structural: "+baseBody.Label)[0])
#########################################################################################################################################################################################################################################################                               
    def AddRevolutePin(self, node, referenceCylinder):#This method receives a dynamic node and a cylinder and adds a revolute pin to the node, and around the center of mass of the cylinder
        obj = 'joint_'+node.label
        referenceCylinder.ViewObject.Visibility = False#Hide the reference cylinder
        #Count the existing joints:             
        existingjoints = 1
        for obj1 in FreeCAD.ActiveDocument.Objects:#Count the existing joints            
            if obj1.Label.startswith('joint'):
                existingjoints = existingjoints+1
                
        a = FreeCAD.ActiveDocument.addObject("Part::FeaturePython",obj)
        Revolutepin(a,str(existingjoints),node, referenceCylinder) 
        CustomView(a.ViewObject)
        a.ViewObject.Transparency = 85
        a.ViewObject.LineWidth = 1.00    
        #a.ViewObject.Selectable = False
        a.Shape = referenceCylinder.Shape 
        #a.ViewObject.Selectable = False
        a.Label='joint: '+str(existingjoints) #rename the hinge 
        #Move objects to their containers:
        FreeCAD.ActiveDocument.getObject('Revolute_pin_joints').addObject(a)
        a.addObject(FreeCAD.ActiveDocument.getObjectsByLabel("x: joint: "+str(existingjoints))[0])
        a.addObject(FreeCAD.ActiveDocument.getObjectsByLabel("y: joint: "+str(existingjoints))[0])
        a.addObject(FreeCAD.ActiveDocument.getObjectsByLabel("z: joint: "+str(existingjoints))[0]) 
        a.addObject(FreeCAD.ActiveDocument.getObjectsByLabel("jf: "+str(existingjoints))[0])                      
#########################################################################################################################################################################################################################################################                               
    def AddDriveHingeJoint(self, node1, node2):
        obj = 'joint_'+node1.label+'_'+node2.label
        #Count the existing joints:             
        existingjoints = 1
        for obj1 in FreeCAD.ActiveDocument.Objects:#Count the existing joints            
            if obj1.Label.startswith('joint'):
                existingjoints = existingjoints+1
                
        a = FreeCAD.ActiveDocument.addObject("Part::FeaturePython",obj)
        Drivehinge(a,str(existingjoints), node1, node2)
        CustomView(a.ViewObject)   
        #ManageAxes.AddAxes(cylinder,'joint',str(existingjoints))
        a.Label='joint: '+str(existingjoints) #rename the hinge
        #Move objects to their containers:
        FreeCAD.ActiveDocument.getObject('Drive_hinge_joints').addObject(a) 
        a.addObject(FreeCAD.ActiveDocument.getObjectsByLabel("x: joint: "+str(existingjoints))[0])
        a.addObject(FreeCAD.ActiveDocument.getObjectsByLabel("y: joint: "+str(existingjoints))[0])
        a.addObject(FreeCAD.ActiveDocument.getObjectsByLabel("z: joint: "+str(existingjoints))[0])  
        a.addObject(FreeCAD.ActiveDocument.getObjectsByLabel("jf: "+str(existingjoints))[0]) 
        a.addObject(FreeCAD.ActiveDocument.getObjectsByLabel("scalar function: "+str(existingjoints))[0]) 
#########################################################################################################################################################################################################################################################                               
    def AddRevoluteHingeJoint(self, node1, node2, cylinder):
        obj = 'joint_'+node1.label+'_'+node2.label
        #Count the existing joints:             
        existingjoints = 1
        for obj1 in FreeCAD.ActiveDocument.Objects:#Count the existing joints            
            if obj1.Label.startswith('joint'):
                existingjoints = existingjoints+1
                
        a = FreeCAD.ActiveDocument.addObject("Part::FeaturePython",obj)
        Revolutehinge(a,str(existingjoints), node1, node2, cylinder)
        CustomView(a.ViewObject)   
        #ManageAxes.AddAxes(cylinder,'joint',str(existingjoints))
        a.Label='joint: '+str(existingjoints) #rename the hinge
        #Move objects to their containers:
        FreeCAD.ActiveDocument.getObject('Revolute_hinge_joints').addObject(a) 
        a.addObject(FreeCAD.ActiveDocument.getObjectsByLabel("x: joint: "+str(existingjoints))[0])
        a.addObject(FreeCAD.ActiveDocument.getObjectsByLabel("y: joint: "+str(existingjoints))[0])
        a.addObject(FreeCAD.ActiveDocument.getObjectsByLabel("z: joint: "+str(existingjoints))[0])  
        a.addObject(FreeCAD.ActiveDocument.getObjectsByLabel("jf: "+str(existingjoints))[0])    
#########################################################################################################################################################################################################################################################               
    def AddClampJoint(self, node):
        #Count the existing joints:             
        existingjoints = 1
        for obj1 in FreeCAD.ActiveDocument.Objects:#Count the existing joints            
            if obj1.Label.startswith('joint'):
                existingjoints = existingjoints+1
                
        obj = 'joint_'+node.label
        a = FreeCAD.ActiveDocument.addObject("Part::FeaturePython",obj)
        Clamp(a,str(existingjoints),node) 
        CustomView(a.ViewObject)   
        #Move objects to their containers:        
        FreeCAD.ActiveDocument.getObject('Clamp_joints').addObject(a) 
        a.addObject(FreeCAD.ActiveDocument.getObjectsByLabel("x: joint: "+str(existingjoints))[0])
        a.addObject(FreeCAD.ActiveDocument.getObjectsByLabel("y: joint: "+str(existingjoints))[0])
        a.addObject(FreeCAD.ActiveDocument.getObjectsByLabel("z: joint: "+str(existingjoints))[0]) 
        a.addObject(FreeCAD.ActiveDocument.getObjectsByLabel("jf: "+str(existingjoints))[0])            
        a.Label='joint: '+str(existingjoints) #rename the clamp    
#########################################################################################################################################################################################################################################################               
    def AddInLineJoint(self, node1, node2):
        existingjoints = 1
        for obj1 in FreeCAD.ActiveDocument.Objects:#Count the existing joints            
            if obj1.Label.startswith('joint'):
                existingjoints = existingjoints+1
                
        obj = 'joint_'+node1.label+'_'+node2.label
        a = FreeCAD.ActiveDocument.addObject("Part::FeaturePython",obj)
        Inline(a,str(existingjoints),node1,node2)
        CustomView(a.ViewObject)
        #Move the object to it's container            
        FreeCAD.ActiveDocument.getObject("In_line_joints").addObject(a)
        a.addObject(FreeCAD.ActiveDocument.getObjectsByLabel("x: joint: "+str(existingjoints))[0])
        a.addObject(FreeCAD.ActiveDocument.getObjectsByLabel("y: joint: "+str(existingjoints))[0])
        a.addObject(FreeCAD.ActiveDocument.getObjectsByLabel("z: joint: "+str(existingjoints))[0]) 
        a.addObject(FreeCAD.ActiveDocument.getObjectsByLabel("jf: "+str(existingjoints))[0]) 
        a.Label='joint: '+str(existingjoints) #rename the joint    
#########################################################################################################################################################################################################################################################               
    def AddInPlaneJoint(self, node1, node2):
        existingjoints = 1
        for obj1 in FreeCAD.ActiveDocument.Objects:#Count the existing joints            
            if obj1.Label.startswith('joint'):
                existingjoints = existingjoints+1
                
        obj = 'joint_'+node1.label+'_'+node2.label
        a = FreeCAD.ActiveDocument.addObject("Part::FeaturePython",obj)
        Inplane(a,str(existingjoints),node1,node2)
        CustomView(a.ViewObject)
        #Move the object to it's container            
        FreeCAD.ActiveDocument.getObject("In_plane_joints").addObject(a)
        a.addObject(FreeCAD.ActiveDocument.getObjectsByLabel("x: joint: "+str(existingjoints))[0])
        a.addObject(FreeCAD.ActiveDocument.getObjectsByLabel("y: joint: "+str(existingjoints))[0])
        a.addObject(FreeCAD.ActiveDocument.getObjectsByLabel("z: joint: "+str(existingjoints))[0]) 
        a.addObject(FreeCAD.ActiveDocument.getObjectsByLabel("jf: "+str(existingjoints))[0]) 
        a.Label='joint: '+str(existingjoints) #rename the joint          
#########################################################################################################################################################################################################################################################               
    def AddSphericalHinge(self, node1, node2):
        existingjoints = 1
        for obj1 in FreeCAD.ActiveDocument.Objects:#Count the existing joints            
            if obj1.Label.startswith('joint'):
                existingjoints = existingjoints+1
                
        obj = 'joint_'+node1.label+'_'+node2.label
        a = FreeCAD.ActiveDocument.addObject("Part::FeaturePython",obj)
        Sphericalhinge(a,str(existingjoints),node1,node2)
        CustomView(a.ViewObject)
        #Move the object to it's container            
        FreeCAD.ActiveDocument.getObject("Spherical_hinge_joints").addObject(a)
        a.addObject(FreeCAD.ActiveDocument.getObjectsByLabel("x: joint: "+str(existingjoints))[0])
        a.addObject(FreeCAD.ActiveDocument.getObjectsByLabel("y: joint: "+str(existingjoints))[0])
        a.addObject(FreeCAD.ActiveDocument.getObjectsByLabel("z: joint: "+str(existingjoints))[0]) 
        a.addObject(FreeCAD.ActiveDocument.getObjectsByLabel("jf: "+str(existingjoints))[0]) 
        a.Label='joint: '+str(existingjoints) #rename the joint            
#########################################################################################################################################################################################################################################################               
    def AddPrismaticJoint(self, node1, node2):
        existingjoints = 1
        for obj1 in FreeCAD.ActiveDocument.Objects:#Count the existing joints            
            if obj1.Label.startswith('joint'):
                existingjoints = existingjoints+1
                
        obj = 'joint_'+node1.label+'_'+node2.label
        a = FreeCAD.ActiveDocument.addObject("Part::FeaturePython",obj)
        Prismatic(a,str(existingjoints),node1,node2)
        CustomView(a.ViewObject)
        #Move the object to it's container            
        FreeCAD.ActiveDocument.getObject("Prismatic_joints").addObject(a)
        a.addObject(FreeCAD.ActiveDocument.getObjectsByLabel("x: joint: "+str(existingjoints))[0])
        a.addObject(FreeCAD.ActiveDocument.getObjectsByLabel("y: joint: "+str(existingjoints))[0])
        a.addObject(FreeCAD.ActiveDocument.getObjectsByLabel("z: joint: "+str(existingjoints))[0]) 
        a.addObject(FreeCAD.ActiveDocument.getObjectsByLabel("jf: "+str(existingjoints))[0]) 
        a.Label='joint: '+str(existingjoints) #rename the joint     
#########################################################################################################################################################################################################################################################               
    def AddAxialRotationJoint(self, static, dynamic):
        existingjoints = 1
        for obj1 in FreeCAD.ActiveDocument.Objects:#Count the existing joints            
            if obj1.Label.startswith('joint'):
                existingjoints = existingjoints+1
                
        obj = 'joint_'+static.label+'_'+dynamic.label
        a = FreeCAD.ActiveDocument.addObject("Part::FeaturePython",obj)
        Axialrotation(a,str(existingjoints),static,dynamic)
        CustomView(a.ViewObject) 
        #Move the object to it's container            
        FreeCAD.ActiveDocument.getObject('Axial_rotation_joints').addObject(a)
        a.addObject(FreeCAD.ActiveDocument.getObjectsByLabel("x: joint: "+str(existingjoints))[0])
        a.addObject(FreeCAD.ActiveDocument.getObjectsByLabel("y: joint: "+str(existingjoints))[0])
        a.addObject(FreeCAD.ActiveDocument.getObjectsByLabel("z: joint: "+str(existingjoints))[0]) 
        a.addObject(FreeCAD.ActiveDocument.getObjectsByLabel("jf: "+str(existingjoints))[0])
        #Add vectors to animate reaction forces:
        a.Label='joint: '+str(existingjoints) #rename the joint   
#########################################################################################################################################################################################################################################################               
    def AddDeformableDisplacementJoint(self, node1, node2):
        existingjoints = 1
        for obj1 in FreeCAD.ActiveDocument.Objects:#Count the existing joints            
            if obj1.Label.startswith('joint'):
                existingjoints = existingjoints+1
                
        obj = 'joint_'+node1.label+'_'+node2.label
        a = FreeCAD.ActiveDocument.addObject("Part::FeaturePython",obj)
        DeformableDisplacement(a, existingjoints, node1, node2)
        a.Label='joint: '+str(existingjoints)
        CustomView(a.ViewObject)
        #Move the object to it's container            
        a.addObject(FreeCAD.ActiveDocument.getObjectsByLabel("x: joint: "+str(existingjoints))[0])
        a.addObject(FreeCAD.ActiveDocument.getObjectsByLabel("y: joint: "+str(existingjoints))[0])
        a.addObject(FreeCAD.ActiveDocument.getObjectsByLabel("z: joint: "+str(existingjoints))[0]) 
        a.addObject(FreeCAD.ActiveDocument.getObjectsByLabel("jf: "+str(existingjoints))[0])
        a.addObject(FreeCAD.ActiveDocument.getObjectsByLabel("sp: "+str(existingjoints))[0])
        FreeCAD.ActiveDocument.getObject("Deformable_displacement_joints").addObject(a)                      
#########################################################################################################################################################################################################################################################               
    def PlotNode(self, node, expression):
        Plotnode(node,expression)
#########################################################################################################################################################################################################################################################                       
    def PlotJoint(self, joint, expression):
        Plotjoint(joint,expression)    
#########################################################################################################################################################################################################################################################               
    def RestoreScene(self):
        ani.restore()
#########################################################################################################################################################################################################################################################               
    def StartAnimation(self):
        ani.start()
#########################################################################################################################################################################################################################################################               
    def StopAnimation(self):
        ani.stop()
#########################################################################################################################################################################################################################################################               
#Execute MBDyn using the input file generated:
    def Run(self):
        #Writeinpfile()
        # Open the FreeCAD text file and create a text document to be used as input file for MBDyn:
        __dir1__ = tempfile.gettempdir()#'C:/Users/Equipo/AppData/Local/Temp'  
        text = FreeCAD.ActiveDocument.getObject("input_file").Text
        #file = open(__dir__ + '/MBDyn/MBDynCase.mbd','w') 
        file = open(__dir1__ + '/MBDynCase.mbd','w') 
        file.write(text)        
        file.close()
        # Execute MBDyn:
        msgBox = QtGui.QMessageBox()
        if platform == "linux" or platform == "linux2":            
            process = subprocess.Popen(["mbdyn", "-f", __dir1__+"/MBDynCase.mbd"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = process.communicate()           
            if(len(err)>0):            
                msgBox.setText("Possible simulation error:")
                msgBox.setInformativeText(err.decode('utf8'))
                msgBox.exec_()
            else:
                msgBox.setText("SUCCESSFUL SIMULATION!")
                msgBox.setInformativeText(out[:555].decode('utf8'))
                msgBox.exec_()
                
        if platform == "win32": 
            process = subprocess.Popen([ __dir__+"\mbdyn-1.7.2-win32\mbdyn.exe","-f", __dir1__+"/MBDynCase.mbd"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = process.communicate()           
            if(len(err)>0):            
                msgBox.setText("Possible simulation error:")
                msgBox.setInformativeText(err.decode('utf8'))
                msgBox.exec_()
            else:
                msgBox.setText("SUCCESSFUL SIMULATION!")
                msgBox.setInformativeText(out[:555].decode('utf8'))
                msgBox.exec_()
#########################################################################################################################################################################################################################################################               
    def WriteInputFile(self):
        Writeinpfile()
        #QtGui.QMessageBox.information(None,"MBDyn input file was written. You ")
#########################################################################################################################################################################################################################################################                       
    def AddGravity(self):#This method adds gravity to the simulation:
        if(len(FreeCAD.ActiveDocument.getObjectsByLabel("MBDyn_simulation"))==1):#Only if a world exists:
            #Add gravity:            
            obj = FreeCAD.ActiveDocument.addObject("App::FeaturePython","gravity")
            Gravity(obj)
            CustomView(obj.ViewObject)
            #Move the gravity object to it's container:
            FreeCAD.ActiveDocument.getObject("Forces").addObject(obj)
        else:
            QtGui.QMessageBox.information(None,'Error.','You have to create a world firts.')
#########################################################################################################################################################################################################################################################               
    def Inspect(self, BaseBody, density):
        density = density /1000.0
        precision = int(FreeCAD.ActiveDocument.getObjectsByLabel('MBDyn')[0].precision)
        #obtain object's volume in mm^3:      
        volume = FreeCAD.Units.Quantity(BaseBody.Shape.Volume,FreeCAD.Units.Unit('mm^3')) 
            #calculate object's mass, in kilograms:
        mass = FreeCAD.Units.Quantity(volume*density,FreeCAD.Units.Unit('kg'))
            #Returns moments of inertia divided by density:
        inertia = BaseBody.Shape.Solids[0].MatrixOfInertia
            #Store inertia moments without mass in mm^2:
        iixx = FreeCAD.Units.Quantity(inertia.A[0],FreeCAD.Units.Unit('mm^5'))
        iiyy = FreeCAD.Units.Quantity(inertia.A[5],FreeCAD.Units.Unit('mm^5'))
        iizz = FreeCAD.Units.Quantity(inertia.A[10],FreeCAD.Units.Unit('mm^5'))
            #Compute inertia moments, in kg*mm^2:      
        ixx = FreeCAD.Units.Quantity(iixx*density,FreeCAD.Units.Unit('kg*mm^2'))
        iyy = FreeCAD.Units.Quantity(iiyy*density,FreeCAD.Units.Unit('kg*mm^2'))
        izz = FreeCAD.Units.Quantity(iizz*density,FreeCAD.Units.Unit('kg*mm^2'))
            #Compute absolute center of mass possition, relative to global frame:
        x = FreeCAD.Units.Quantity(BaseBody.Shape.Solids[0].CenterOfMass[0],FreeCAD.Units.Unit('mm'))
        y = FreeCAD.Units.Quantity(BaseBody.Shape.Solids[0].CenterOfMass[1],FreeCAD.Units.Unit('mm'))
        z = FreeCAD.Units.Quantity(BaseBody.Shape.Solids[0].CenterOfMass[2],FreeCAD.Units.Unit('mm'))
        
        length = FreeCAD.Units.Quantity(FreeCAD.ActiveDocument.getObject("Line").End[0],FreeCAD.Units.Unit('mm'))
        
        FreeCAD.ActiveDocument.cmx.X1=x+length
        FreeCAD.ActiveDocument.cmx.Y1=y
        FreeCAD.ActiveDocument.cmx.Z1=z
        FreeCAD.ActiveDocument.cmx.X2=x-length#+body.Label
        FreeCAD.ActiveDocument.cmx.Y2=y
        FreeCAD.ActiveDocument.cmx.Z2=z
        
        FreeCAD.ActiveDocument.cmy.X1=x
        FreeCAD.ActiveDocument.cmy.Y1=y+length
        FreeCAD.ActiveDocument.cmy.Z1=z
        FreeCAD.ActiveDocument.cmy.X2=x
        FreeCAD.ActiveDocument.cmy.Y2=y-length
        FreeCAD.ActiveDocument.cmy.Z2=z
        
        FreeCAD.ActiveDocument.cmz.X1=x
        FreeCAD.ActiveDocument.cmz.Y1=y
        FreeCAD.ActiveDocument.cmz.Z1=z+length
        FreeCAD.ActiveDocument.cmz.X2=x
        FreeCAD.ActiveDocument.cmz.Y2=y
        FreeCAD.ActiveDocument.cmz.Z2=z-length
        
        FreeCAD.ActiveDocument.recompute()
        QtGui.QMessageBox.information(None,'Physical properties:','Volume [cm^3]: '+str(round(volume.getValueAs('cm^3').Value,precision))+'\n\n'+'Mass [kg]: '+str(round(mass.Value,precision))+'\n\n'+'Center of mass:\n\n'+'    cmx [mm]: '+str(round(x.Value,precision))+'\n'+'    cmy [mm]: '+str(round(y.Value,precision))+'\n'+'    cmz [mm]: '+str(round(z.Value,precision))+'\n\n'+'Moments of inertia:\n\n'+'    ixx [kg*mm^2] :'+str(round(ixx.Value,precision))+'\n'+'    iyy [kg*mm^2] :'+str(round(iyy.Value,precision))+'\n'+'    izz [kg*mm^2] :'+str(round(izz.Value,precision))+'\n')


    def AddStructuralForce(self, node):
        existingforces = 1
        for obj1 in FreeCAD.ActiveDocument.Objects:#Count the existing joints            
            if obj1.Label.startswith('force'):
                existingforces = existingforces+1
                
        obj = 'force_'+node.label
        a = FreeCAD.ActiveDocument.addObject("App::FeaturePython",obj)
        StructuralForce(a,str(existingforces),node)
        CustomView(a.ViewObject)
        #Move the object to it's container            
        FreeCAD.ActiveDocument.getObject("Structural_forces").addObject(a)
        a.Label='force: '+str(existingforces) #rename the joint 









    



      

                 

    
  



     



    #def RunMBDyn(self):#This method executes MBDyn using the input file previously generated
    #    subprocess.Popen(["mbdyn", "-f", __dir__+"/MBDyn/MBDynCase.mbd"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def CreateWorld(self):#This method creates all the containers in the tree view and moves all the exiting objects into the "Bodies" container.
        if(len(FreeCAD.ActiveDocument.getObjectsByLabel("MBDyn_simulation"))==0):#Only if a world does not exist:
            if(len(FreeCAD.ActiveDocument.Objects)>0):            
                Createworld()#Adds all the goups and the global reference frame
                #Create a simulation and move it into the container:
                a = FreeCAD.ActiveDocument.addObject("App::FeaturePython","MBDyn")
                MBDyn(a)
                CustomView(a.ViewObject)
                FreeCAD.ActiveDocument.getObject("MBDyn_simulation").addObject(a) 
                #Create a simulation parameters object and move it to its container:
                b = FreeCAD.ActiveDocument.addObject("App::FeaturePython","Animation")        
                Animation_parameters(b)            
                CustomView(b.ViewObject)
                FreeCAD.ActiveDocument.getObject("MBDyn_simulation").addObject(b)
                #Create control data parameters object and move it to its container:
                c = FreeCAD.ActiveDocument.addObject("App::FeaturePython","ControlData")        
                ControlData(c)            
                CustomView(c.ViewObject)
                FreeCAD.ActiveDocument.getObject("MBDyn_simulation").addObject(c)
            else:
                QtGui.QMessageBox.information(None,'Error.','You need at least one solid object to create a simulation.')
        else:
            QtGui.QMessageBox.information(None,'Error.','A world has already been created.')
    



    def RandomColor(self, body):
            colorR, colorG, colorB = random(), random(), random()
            #b = FreeCADGui.Selection.getSelection()[0]            
            body.ViewObject.LineColor = (colorR,colorG,colorB)
            body.ViewObject.PointColor = (colorR,colorG,colorB)
            body.ViewObject.ShapeColor = (colorR,colorG,colorB)
            #if(len(FreeCAD.ActiveDocument.getObjectsByLabel("i: "+body.label))==1):
            #    FreeCAD.ActiveDocument.getObjectsByLabel("i: "+body.label)[0].ViewObject.TextColor = (colorR,colorG,colorB)

    def UpdateDynamicNode(self, objeto):#This method moves the coordinate system of a node to a new position and orientation:
        return
        #ManageAxes.MoveAxes(objeto)

    def UpdateJoint(self, objeto):
        return
        #ManageAxes.MoveAxes(objeto)
        #if(objeto.joint=='revolute pin'):
        #    node = FreeCAD.ActiveDocument.getObjectsByLabel("structural: "+joint.node)[0]
        #    #Get the joint possition:
        #    xc = joint.absolute_pin_position_X
        #    yc = joint.absolute_pin_position_Y
        #    zc = joint.absolute_pin_position_Z
            #Get the corresponding node possition:
        #    xcc = node.position_X
        #    ycc = node.position_Y
        #    zcc = node.position_Z
            #Remove  joint force vector and add a new one on the new possition:
        #    FreeCAD.ActiveDocument.removeObject(FreeCAD.ActiveDocument.getObjectsByLabel("jf: "+joint.label)[0].Name)
        #    Forceaxes(joint)
            #Update the joint's offset:
        #    joint.relative_offset_X = xc - xcc
        #    joint.relative_offset_Y = yc - ycc
        #    joint.relative_offset_Z = zc - zcc         
                  
    def UpdateRigidBody(self, Body):#This method gets a reigid body (b) and updates it in case of: 
       #a) The shape of the original body (parametric CAD) has changed, 
       #b) The user has changed the rigid body's density
       #c) The user has moved the asociated structural node.
        #Body = FreeCAD.ActiveDocument.getObjectsByLabel(body)[0]
        label = Body.label
        #Get the new shape from the corresponding parametric body:
        shape = FreeCAD.ActiveDocument.getObjectsByLabel(label)[0].Shape
        #Update the rigid body's shape
        Body.Shape = shape
        #Get the new inertia matrix:
        inertia = shape.Solids[0].MatrixOfInertia
        #get the new density (defined by the user in the Material object):
        Body.density = FreeCAD.ActiveDocument.getObjectsByLabel("material: "+Body.label)[0].Material['Density']
        density = FreeCAD.Units.Quantity(float(Body.density.split(' ')[0])/1000.0**3,FreeCAD.Units.Unit('kg/mm^3'))#Convert density to the appropriate units, to calculate moments of inertia
        #get the new volume:
        volume = FreeCAD.Units.Quantity(shape.Volume,FreeCAD.Units.Unit('mm^3'))  
        #calculate the new object's mass, in kilograms:
        mass = FreeCAD.Units.Quantity(volume*density,FreeCAD.Units.Unit('kg'))
        #get the new inertia moments without mass:
        iixx = FreeCAD.Units.Quantity(inertia.A[0],FreeCAD.Units.Unit('mm^5'))
        iiyy = FreeCAD.Units.Quantity(inertia.A[5],FreeCAD.Units.Unit('mm^5'))
        iizz = FreeCAD.Units.Quantity(inertia.A[10],FreeCAD.Units.Unit('mm^5'))
        #compute new inertia moments, in kg*mm^2: 
        ixx = FreeCAD.Units.Quantity(iixx*density,FreeCAD.Units.Unit(2,1))
        iyy = FreeCAD.Units.Quantity(iiyy*density,FreeCAD.Units.Unit(2,1))
        izz = FreeCAD.Units.Quantity(iizz*density,FreeCAD.Units.Unit(2,1))
        #Compute new absolute center of mass, relative to global frame:
        cmx = FreeCAD.Units.Quantity(shape.Solids[0].CenterOfMass[0],FreeCAD.Units.Unit('mm'))
        cmy = FreeCAD.Units.Quantity(shape.Solids[0].CenterOfMass[1],FreeCAD.Units.Unit('mm'))
        cmz = FreeCAD.Units.Quantity(shape.Solids[0].CenterOfMass[2],FreeCAD.Units.Unit('mm'))
        Body.mass = str(mass)#Update mass
        #Update moments of inertia with mass:
        Body.ixx = str(ixx)
        Body.iyy = str(iyy)
        Body.izz = str(izz)
        #Update moments of inertia witout mass:
        Body.iixx = str(iixx)
        Body.iiyy = str(iiyy)
        Body.iizz = str(iizz)            
        #Update the absolute center of mass:
        Body.absolute_center_of_mass_X = cmx
        Body.absolute_center_of_mass_Y = cmy
        Body.absolute_center_of_mass_Z = cmz
            
            #get the corresponding node's absolute possition:  
        if(len(FreeCAD.ActiveDocument.getObjectsByLabel("structural: "+label))==1):
            xcc = FreeCAD.ActiveDocument.getObjectsByLabel("structural: "+label)[0].position_X
            ycc = FreeCAD.ActiveDocument.getObjectsByLabel("structural: "+label)[0].position_Y
            zcc = FreeCAD.ActiveDocument.getObjectsByLabel("structural: "+label)[0].position_Z
            #Update the body's relative center of mass position:
            Body.relative_center_of_mass_X = Body.absolute_center_of_mass_X-xcc
            Body.relative_center_of_mass_Y = Body.absolute_center_of_mass_Y-ycc
            Body.relative_center_of_mass_Z = Body.absolute_center_of_mass_Z-zcc
        else:#If there is no structural node asociated to the body, issue an error:
            QtGui.QMessageBox.information(None,'Warning.','No structural node asociated to this body. Relative center of mass cannot be calculated.')
      
