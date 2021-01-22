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
This class receives a non-parametric body and creates a structural dynamic node positioned at the body's center of mass.
A structural node is an owner of kinematic degrees of freedom. 
It can assume the six degrees of freedom, three for possition and three for orientation.

The syntax is:

structural: <label>, 
            dynamic, 
            <position>, 
            <orientation>,
            <velocity>, 
            <angular velocity> ;
        
Where:
<label> is an integer number that identifies the node. Label the 3D body in FreeCAD with a unique integer number to identify it's node, before you call this class.
<position> is the node's possition relative to the absolute reference frame. This is equal to the body's center of mass position.
<orientation> is the node's orientation relative to the absolute reference frame. I assume all bodies start at: euler, 0., 0., 0.
<velocity> is the initial nodes's velocity. The user can define this from FreeCAD
<angular velocity> the initial angular velocity. To be defined by the user too.
'''

import FreeCAD
import FreeCADGui
import Draft

class Structuraldynamicnode: 
    def __init__(self, obj, baseBody):    
        
        #To create a node at the absolute possition of the center of mass of the CAD object, I first obtain the center of mass (x,y,z):
        x = FreeCAD.Units.Quantity(baseBody.Shape.Solids[0].CenterOfMass[0],FreeCAD.Units.Unit('mm'))
        y = FreeCAD.Units.Quantity(baseBody.Shape.Solids[0].CenterOfMass[1],FreeCAD.Units.Unit('mm'))
        z = FreeCAD.Units.Quantity(baseBody.Shape.Solids[0].CenterOfMass[2],FreeCAD.Units.Unit('mm'))
        
        #By now, al the nodes are created with initial orientation (yaw=0, pitch=0, roll=0). Give the node an initial absolute orienation in Euler angles:  
        yaw = FreeCAD.Units.Quantity(0.0,FreeCAD.Units.Unit('deg'))
        pitch = FreeCAD.Units.Quantity(0.0,FreeCAD.Units.Unit('deg'))
        roll = FreeCAD.Units.Quantity(0.0,FreeCAD.Units.Unit('deg')) 
        
        #All the nodes are created with an initial absolute velocity (relative to the absolute coordinate sistem) of (vx=0,vy=0,vz=0)
        #The user can afterwards change the initial velocity using the GUI
        #Give the node an initial velocity (mm/sec):  
        vx = FreeCAD.Units.Quantity(0.0,FreeCAD.Units.Unit('mm/s'))
        vy = FreeCAD.Units.Quantity(0.0,FreeCAD.Units.Unit('mm/s'))
        vz = FreeCAD.Units.Quantity(0.0,FreeCAD.Units.Unit('mm/s')) 
        
        #All the nodes are created with an initial angular absolute velocity (relative to the absolute coordinate sistem) of (wx=0,wy=0,wz=0)
        #The user can afterwards change the initial angular velocity using the GUI
        #Give the node an initial angular velocity (deg/sec):  
        wx = FreeCAD.Units.Quantity(0.0,FreeCAD.Units.Unit('deg/s'))
        wy = FreeCAD.Units.Quantity(0.0,FreeCAD.Units.Unit('deg/s'))
        wz = FreeCAD.Units.Quantity(0.0,FreeCAD.Units.Unit('deg/s')) 
        
        #Give the object the ability to contain other objetcs:
        obj.addExtension("App::GroupExtensionPython", self)        
        
        #Give the object its properties:
        obj.addProperty("App::PropertyString","label","Structural dynamic node","label",1).label = baseBody.Label    
        obj.addProperty("App::PropertyString","type","Structural dynamic node","type",1).type = 'dynamic'
        
        obj.addProperty("App::PropertyDistance","position X","Initial absolute position","position X").position_X = x
        obj.addProperty("App::PropertyDistance","position Y","Initial absolute position","position Y").position_Y = y
        obj.addProperty("App::PropertyDistance","position Z","Initial absolute position","position Z").position_Z = z
        
        obj.addProperty("App::PropertyAngle","yaw","Initial absolute orientation","yaw",1).yaw = yaw    
        obj.addProperty("App::PropertyAngle","pitch","Initial absolute orientation","pitch",1).pitch = pitch    
        obj.addProperty("App::PropertyAngle","roll","Initial absolute orientation","roll",1).roll = roll    
        
        obj.addProperty("App::PropertySpeed","velocity_X","Initial absolute velocity","velocity_X").velocity_X = vx
        obj.addProperty("App::PropertySpeed","velocity_Y","Initial absolute velocity","velocity_Y").velocity_Y = vy
        obj.addProperty("App::PropertySpeed","velocity_Z","Initial absolute velocity","velocity_Z").velocity_Z = vz
        
        obj.addProperty("App::PropertyString","angular velocity X","Initial absolute angular velocity","angular velocity X").angular_velocity_X = str(wx)
        obj.addProperty("App::PropertyString","angular velocity Y","Initial absolute angular velocity","angular velocity Y").angular_velocity_Y = str(wy)
        obj.addProperty("App::PropertyString","angular velocity Z","Initial absolute angular velocity","angular velocity Z").angular_velocity_Z = str(wz)
        
        obj.Proxy = self
                     
        #Add the coordinate system and an system to the GUI. The coordinate system represents the position of the node in space:
        length = (baseBody.Shape.BoundBox.XLength+baseBody.Shape.BoundBox.YLength+baseBody.Shape.BoundBox.ZLength)/6 # Calculate the body characteristic length. Will be used to size the arrows that represent the node.
        p1 = FreeCAD.Vector(0, 0, 0)
        #Add x vector of the coordinate system:
        p2 = FreeCAD.Vector(length, 0, 0)
        l = Draft.makeLine(p1, p2) 
        l.Label = 'x: structural: '+ baseBody.Label          
        l.ViewObject.LineColor = (1.00,0.00,0.00)
        l.ViewObject.PointColor = (1.00,0.00,0.00)
        l.Placement=FreeCAD.Placement(FreeCAD.Vector(x,y,z), FreeCAD.Rotation(FreeCAD.Vector(0,0,1),0), FreeCAD.Vector(0,0,0))
        l.ViewObject.EndArrow = True
        l.ViewObject.ArrowType = u"Arrow"
        l.ViewObject.LineWidth = 1.00
        l.ViewObject.PointSize = 1.00
        l.ViewObject.ArrowSize = str(length/15)+' mm'
        #l.ViewObject.Selectable = False
        #Add y vector of the coordinate system:
        p2 = FreeCAD.Vector(0, length, 0)
        l = Draft.makeLine(p1, p2)        
        l.Label = 'y: structural: '+ baseBody.Label        
        l.ViewObject.LineColor = (0.00,1.00,0.00)
        l.ViewObject.PointColor = (0.00,1.00,0.00)
        l.Placement=FreeCAD.Placement(FreeCAD.Vector(x,y,z), FreeCAD.Rotation(FreeCAD.Vector(0,0,1),0), FreeCAD.Vector(0,0,0))
        l.ViewObject.EndArrow = True
        l.ViewObject.ArrowType = u"Arrow"
        l.ViewObject.LineWidth = 1.00
        l.ViewObject.PointSize = 1.00
        l.ViewObject.ArrowSize = str(length/15)+' mm'  
        #l.ViewObject.Selectable = False
        #Add z vector of the coordinate system:
        p2 = FreeCAD.Vector(0, 0, 0+length)
        l = Draft.makeLine(p1, p2)        
        l.Label = 'z: structural: '+ baseBody.Label                        
        l.ViewObject.LineColor = (0.00,0.00,1.00)
        l.ViewObject.PointColor = (0.00,0.00,1.00)
        l.Placement=FreeCAD.Placement(FreeCAD.Vector(x,y,z), FreeCAD.Rotation(FreeCAD.Vector(0,0,1),0), FreeCAD.Vector(0,0,0))
        l.ViewObject.EndArrow = True  
        l.ViewObject.ArrowType = u"Arrow"
        l.ViewObject.LineWidth = 1.00
        l.ViewObject.PointSize = 1.00
        l.ViewObject.ArrowSize = str(length/15)+' mm'   
        #l.ViewObject.Selectable = False                                      
                       
        FreeCAD.ActiveDocument.recompute()
 
 
    def onChanged(self, fp, prop):
        '''Do something when a property has changed'''
        try:
            if (len(FreeCADGui.Selection.getSelection()) == 1):
                #Get the new position and orientation
                x = FreeCADGui.Selection.getSelection()[0].position_X
                y = FreeCADGui.Selection.getSelection()[0].position_Y
                z = FreeCADGui.Selection.getSelection()[0].position_Z
                yaw = FreeCADGui.Selection.getSelection()[0].yaw
                pitch = FreeCADGui.Selection.getSelection()[0].pitch
                roll = FreeCADGui.Selection.getSelection()[0].roll
                #Move the arrows and text
                FreeCAD.ActiveDocument.getObjectsByLabel("x: structural: "+FreeCADGui.Selection.getSelection()[0].label)[0].Placement=FreeCAD.Placement(FreeCAD.Vector(x,y,z), FreeCAD.Rotation(yaw,pitch,roll), FreeCAD.Vector(0,0,0))
                FreeCAD.ActiveDocument.getObjectsByLabel("y: structural: "+FreeCADGui.Selection.getSelection()[0].label)[0].Placement=FreeCAD.Placement(FreeCAD.Vector(x,y,z), FreeCAD.Rotation(yaw,pitch,roll), FreeCAD.Vector(0,0,0))
                FreeCAD.ActiveDocument.getObjectsByLabel("z: structural: "+FreeCADGui.Selection.getSelection()[0].label)[0].Placement=FreeCAD.Placement(FreeCAD.Vector(x,y,z), FreeCAD.Rotation(yaw,pitch,roll), FreeCAD.Vector(0,0,0))
                FreeCAD.ActiveDocument.getObjectsByLabel("i: structural: "+FreeCADGui.Selection.getSelection()[0].label)[0].Placement=FreeCAD.Placement(FreeCAD.Vector(x,y,z), FreeCAD.Rotation(yaw,pitch,roll), FreeCAD.Vector(0,0,0))        

        except:
            return True
            
        
    def execute(self, fp):
        '''Do something when doing a recomputation, this method is mandatory'''
        FreeCAD.Console.PrintMessage("Recompute...\n")
        
        
        
        