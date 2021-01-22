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
"""
This class receives a base node and a non-parametric base body, and creates a dummy node positioned at the base body's center of mass, and attached to the base node.
A dummy node does not own any dregree of freedom. It gets its possition and orientation from its base node, and allows measuring the possition and orientation of a ponit attached to a dynamic node.  

The syntax is:

structural: <label>,
            dummy,
            <base_node>,
            offset,
            <offset_relative_to_the_base_node>,
            <orientation_relative_to_the_base_node>;
Where:
<label> is an integer number that identifies the node. Label the base body in FreeCAD with a unique integer number to identify it's node, before you call this class.
<base_node> is the label of the structural dynamic node to which the dummy node is attached.
<offset_relative_to_the_base_node>, is the offset (z,y,z) of the dummy node relative to its structural dynamic node.
<orientation_relative_to_the_base_node> is the initial orientation of the dummy node relative to the orientation of its structural dynamic node. I use "eye" by default, to assume the same orientation as the structural dynamic node.
"""

import FreeCAD
import Draft

class Dummynode: 
    def __init__(self, obj, baseNode, baseBody):
        
        #Here, I create a dummy node at the center of mass of the base body CAD object (baseBody). 
        #I first obtain the center of mass of the baseBody (x,y,z):
        x = FreeCAD.Units.Quantity(baseBody.Shape.Solids[0].CenterOfMass[0],FreeCAD.Units.Unit('mm')) 
        y = FreeCAD.Units.Quantity(baseBody.Shape.Solids[0].CenterOfMass[1],FreeCAD.Units.Unit('mm')) 
        z = FreeCAD.Units.Quantity(baseBody.Shape.Solids[0].CenterOfMass[2],FreeCAD.Units.Unit('mm')) 
        
        #Then, I obtain the offset (x1,y1,z1), this is, the possition of the dummy node relative to the baseNode
        x1 = x-baseNode.position_X
        y1 = y-baseNode.position_Y
        z1 = z-baseNode.position_Z
        
        #By now, al the nodes are created with initial orientation (yaw=0, pitch=0, roll=0). Give the node an initial absolute orienation in Euler angles:  
        yaw = FreeCAD.Units.Quantity(0.0,FreeCAD.Units.Unit('deg'))
        pitch = FreeCAD.Units.Quantity(0.0,FreeCAD.Units.Unit('deg'))
        roll = FreeCAD.Units.Quantity(0.0,FreeCAD.Units.Unit('deg')) 

        #Give the object the ability to contain other objetcs:
        obj.addExtension("App::GroupExtensionPython", self)        

        #Give the object its properties:        
        obj.addProperty("App::PropertyString","type","Dummy node","type",1).type = 'dummy'
        obj.addProperty("App::PropertyString","label","Dummy node","label",1).label = baseBody.Label
        
        #Node possition:        
        obj.addProperty("App::PropertyDistance","position_X","Possition","position X",1).position_X = x
        obj.addProperty("App::PropertyDistance","position_Y","Possition","position Y",1).position_Y = y
        obj.addProperty("App::PropertyDistance","position_Z","Possition","position Z",1).position_Z = z
        
        #Base node label:
        obj.addProperty("App::PropertyString","base node","Dummy node","base node",1).base_node = baseNode.label
        
        #Offset relative to dynamic node:
        obj.addProperty("App::PropertyDistance","relative offset X","Relative offset","relative offset X",1).relative_offset_X = x1
        obj.addProperty("App::PropertyDistance","relative offset Y","Relative offset","relative offset Y",1).relative_offset_Y = y1       
        obj.addProperty("App::PropertyDistance","relative offset Z","Relative offset","relative offset Z",1).relative_offset_Z = z1
        
        #Initial orientation:                
        obj.addProperty("App::PropertyAngle","yaw","Initial absolute orientation","yaw",1).yaw = yaw    
        obj.addProperty("App::PropertyAngle","pitch","Initial absolute orientation","pitch",1).pitch = pitch    
        obj.addProperty("App::PropertyAngle","roll","Initial absolute orientation","roll",1).roll = roll    
                
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
                       
        FreeCAD.ActiveDocument.recompute()

        
    def execute(self, fp):
        '''Do something when doing a recomputation, this method is mandatory'''
        FreeCAD.Console.PrintMessage("Recompute...\n")
        
        
