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
https://www.sky-engin.jp/en/MBDynTutorial/chap14/chap14.html
This joint constrains a node only allowing rotation about one axis. The basic syntax for the statement that defines a revolute pin is as follows.

The syntax is: 

joint: <label>, 
       revolute pin, 
       <node>, 
       <relative offset>, 
       hinge, 
       <relative orientation matrix>,
       <absolute pin position>, 
       hinge, 
       <absolute pin orientation matrix>;

<label>: an integer number to identify the joint, eg: 1,2,3... 
<node>: the label of the structural node to which the joint is attached, eg: 1,2,3... 
<relative offset>: the possition of the joint relative to it's structural node. 
For the example in the above web page is '-0.5, 0.0, 0.0', because the node is at '0.5, 0.0, 0.0' relative to the absolute origin
<relative orientation matrix>:
<absolute pin position>: pin possition relative to the absolute reference frame. It is the center of mass of the FreeCAD cylinder.
 
'''

import FreeCAD
import FreeCADGui
import Draft

class Revolutepin:
    def __init__(self, obj, label, node, cylinder):
        
        #Get the cylinder's center of mass, so that the joint is placed here:
        x = FreeCAD.Units.Quantity(cylinder.Shape.Solids[0].CenterOfMass[0],FreeCAD.Units.Unit('mm'))  
        y = FreeCAD.Units.Quantity(cylinder.Shape.Solids[0].CenterOfMass[1],FreeCAD.Units.Unit('mm'))  
        z = FreeCAD.Units.Quantity(cylinder.Shape.Solids[0].CenterOfMass[2],FreeCAD.Units.Unit('mm'))  
        
        #Get the cylinder orientation. The joint's orientation is the same:(This idea didn't wor well, so by now orientation has to be inserted manually)
        yaw = FreeCAD.Units.Quantity(0.0,FreeCAD.Units.Unit('deg'))
        pitch = FreeCAD.Units.Quantity(0.0,FreeCAD.Units.Unit('deg'))
        roll = FreeCAD.Units.Quantity(0.0,FreeCAD.Units.Unit('deg')) 
        
        #Calculate the joint possition relative to it's node (relative offset)        
        x1 = x-node.position_X
        y1 = y-node.position_Y
        z1 = z-node.position_Z
        obj.addExtension("App::GroupExtensionPython", self) 
        
        #Create scripted object:
        obj.addProperty("App::PropertyString","label","Revolute pin","label",1).label = label
        obj.addProperty("App::PropertyString","node","Revolute pin","node",1).node = node.label
        obj.addProperty("App::PropertyString","joint","Revolute pin","joint",1).joint = 'revolute pin'
        
        #pin possition relative to it's node:
        obj.addProperty("App::PropertyDistance","relative offset X","Offset relative to node","relative offset X",1).relative_offset_X = x1
        obj.addProperty("App::PropertyDistance","relative offset Y","Offset relative to node","relative offset Y",1).relative_offset_Y = y1
        obj.addProperty("App::PropertyDistance","relative offset Z","Offset relative to node","relative offset Z",1).relative_offset_Z = z1
        
        #pin relative orientation:
        obj.addProperty("App::PropertyAngle","relative orientation yaw","Orientation relative to node","relative orientation yaw").relative_orientation_yaw = FreeCAD.Units.Quantity(0.0,FreeCAD.Units.Unit('deg'))        
        obj.addProperty("App::PropertyAngle","relative orientation pitch","Orientation relative to node","relative orientation pitch").relative_orientation_pitch = FreeCAD.Units.Quantity(0.0,FreeCAD.Units.Unit('deg'))
        obj.addProperty("App::PropertyAngle","relative orientation roll","Orientation relative to node","relative orientation roll").relative_orientation_roll = FreeCAD.Units.Quantity(0.0,FreeCAD.Units.Unit('deg'))        
        
        obj.addProperty("App::PropertyDistance","position X","Initial absolute position","position X",1).position_X = x
        obj.addProperty("App::PropertyDistance","position Y","Initial absolute position","position Y",1).position_Y = y
        obj.addProperty("App::PropertyDistance","position Z","Initial absolute position","position Z",1).position_Z = z
        
        obj.addProperty("App::PropertyAngle","yaw","Initial absolute orientation","yaw").yaw = yaw    
        obj.addProperty("App::PropertyAngle","pitch","Initial absolute orientation","pitch").pitch = pitch    
        obj.addProperty("App::PropertyAngle","roll","Initial absolute orientation","roll").roll = roll 
        
        #Animation parameters:
        obj.addProperty("App::PropertyEnumeration","animate","Animation","animate")
        obj.animate=['false','true']

        obj.addProperty("App::PropertyEnumeration","frame","Animation","frame")
        obj.frame=['global','local']        
        
        obj.addProperty("App::PropertyString","force vector multiplier","Animation","force vector multiplier").force_vector_multiplier = '1'
        
        obj.Proxy = self
        
        #Add the coordinate system and an system to the GUI. The coordinate system represents the position of the node in space:
        length = (cylinder.Shape.BoundBox.XLength+cylinder.Shape.BoundBox.YLength+cylinder.Shape.BoundBox.ZLength)/6 # Calculate the body characteristic length. Will be used to size the arrows that represent the node.
        p1 = FreeCAD.Vector(0, 0, 0)
        #Add x vector of the coordinate system:
        p2 = FreeCAD.Vector(length, 0, 0)
        l = Draft.makeLine(p1, p2)
        l.Label = 'x: joint: '+ label            
        l.ViewObject.LineColor = (1.00,0.00,0.00)
        l.ViewObject.PointColor = (1.00,0.00,0.00)
        l.Placement=FreeCAD.Placement(FreeCAD.Vector(x,y,z), FreeCAD.Rotation(FreeCAD.Vector(0,0,1),0), FreeCAD.Vector(0,0,0))
        l.ViewObject.EndArrow = True
        l.ViewObject.ArrowType = u"Arrow"
        l.ViewObject.LineWidth = 1.00
        l.ViewObject.PointSize = 1.00
        l.ViewObject.ArrowSize = str(length/15)+' mm'
        l.ViewObject.Selectable = False 
        #Add y vector of the coordinate system:
        p2 = FreeCAD.Vector(0, length, 0)
        l = Draft.makeLine(p1, p2)
        l.Label = 'y: joint: '+ label            
        l.ViewObject.LineColor = (0.00,1.00,0.00)
        l.ViewObject.PointColor = (0.00,1.00,0.00)
        l.Placement=FreeCAD.Placement(FreeCAD.Vector(x,y,z), FreeCAD.Rotation(FreeCAD.Vector(0,0,1),0), FreeCAD.Vector(0,0,0))
        l.ViewObject.EndArrow = True
        l.ViewObject.ArrowType = u"Arrow"
        l.ViewObject.LineWidth = 1.00
        l.ViewObject.PointSize = 1.00
        l.ViewObject.ArrowSize = str(length/15)+' mm'
        l.ViewObject.Selectable = False         
        #Add z vector of the coordinate system:
        p2 = FreeCAD.Vector(0, 0, 0+length)
        l = Draft.makeLine(p1, p2)
        l.Label = 'z: joint: '+ label
        l.ViewObject.ArrowType = u"Dot"            
        l.ViewObject.LineColor = (0.00,0.00,1.00)
        l.ViewObject.PointColor = (0.00,0.00,1.00)
        l.Placement=FreeCAD.Placement(FreeCAD.Vector(x,y,z), FreeCAD.Rotation(FreeCAD.Vector(0,0,1),0), FreeCAD.Vector(0,0,0))
        l.ViewObject.EndArrow = True        
        l.ViewObject.LineWidth = 1.00
        l.ViewObject.PointSize = 1.00
        l.ViewObject.ArrowSize = str(length/15)+' mm' 
        l.ViewObject.Selectable = False              
        #Add the vector to visualize reaction forces
        Llength = FreeCAD.Units.Quantity(FreeCAD.ActiveDocument.getObjectsByLabel("X")[0].End[0]/4,FreeCAD.Units.Unit('mm'))
        p1 = FreeCAD.Vector(x, y, z)
        p2 = FreeCAD.Vector(x+Llength, y+Llength, z+Llength)    
        d = Draft.makeLine(p1, p2)
        d.ViewObject.LineColor = (1.00,0.00,0.00)
        d.ViewObject.PointColor = (1.00,0.00,0.00)  
        d.ViewObject.LineWidth = 1.00
        d.ViewObject.PointSize = 1.00
        d.ViewObject.EndArrow = True
        d.ViewObject.ArrowType = u"Arrow"
        d.ViewObject.ArrowSize = str(Llength/75)#+' mm'
        d.Label = "jf: "+ label   
        d.ViewObject.Selectable = False 

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
                #Set the orientation relative to the node (by now the orientation of the dynamic nodes cannot be changed, so that the orientation of the hinge relative to the node is the same as the orientation of the hinge relative to the global frame):
                #FreeCADGui.Selection.getSelection()[0].relative_orientation_yaw = str(FreeCADGui.Selection.getSelection()[0].yaw)
                #FreeCADGui.Selection.getSelection()[0].relative_orientation_pitch = str(FreeCADGui.Selection.getSelection()[0].pitch)
                #FreeCADGui.Selection.getSelection()[0].relative_orientation_roll = str(FreeCADGui.Selection.getSelection()[0].roll)
                #Move the arrows
                FreeCAD.ActiveDocument.getObjectsByLabel("x: joint: "+FreeCADGui.Selection.getSelection()[0].Label[-1])[0].Placement=FreeCAD.Placement(FreeCAD.Vector(x,y,z), FreeCAD.Rotation(yaw,pitch,roll), FreeCAD.Vector(0,0,0))
                FreeCAD.ActiveDocument.getObjectsByLabel("y: joint: "+FreeCADGui.Selection.getSelection()[0].Label[-1])[0].Placement=FreeCAD.Placement(FreeCAD.Vector(x,y,z), FreeCAD.Rotation(yaw,pitch,roll), FreeCAD.Vector(0,0,0))
                FreeCAD.ActiveDocument.getObjectsByLabel("z: joint: "+FreeCADGui.Selection.getSelection()[0].Label[-1])[0].Placement=FreeCAD.Placement(FreeCAD.Vector(x,y,z), FreeCAD.Rotation(yaw,pitch,roll), FreeCAD.Vector(0,0,0))
                FreeCAD.ActiveDocument.getObjectsByLabel("i: joint: "+FreeCADGui.Selection.getSelection()[0].Label[-1])[0].Placement=FreeCAD.Placement(FreeCAD.Vector(x,y,z), FreeCAD.Rotation(yaw,pitch,roll), FreeCAD.Vector(0,0,0))        
        except:
            return True

        
    def execute(self, fp):
        '''Do something when doing a recomputation, this method is mandatory'''
        FreeCAD.Console.PrintMessage("Recompute...\n")                
               
