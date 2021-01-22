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
This class receives a label and a node (normally a structural static node), applies a "clamp" joint to the node and labels the joint using the received label. 
The structure of a clamp joint is

joint: <label>, 
       clamp,
       <node>, 
       <absolute pin position>, 
       <absolute pin orientation>;        

Where:
<label> is an integer number that identifies the joint. 
<node> is the node to be clamped.
<absolute pin position> is the position of the clamp. By now I assume is the same as te possition of the node to be clamped.           
<absolute pin orientation> is the orientation of the clamp in reference to the global frame. I assume is the same as the node to be clamped. 
Since by now all the nodes have the same orientation, I assume the orientation of the clamp is: euler, 0.0, 0.0, 0.0
'''
#from FreeCAD import Units

import FreeCAD
import Draft

class Clamp:
    def __init__(self, obj, label, node):
        #Get the node's center of mass, so that the joint is placed here: 
        x = node.position_X
        y = node.position_Y
        z = node.position_Z
        
        #Orientation of the joint:
        yaw = FreeCAD.Units.Quantity(0.0,FreeCAD.Units.Unit('deg'))
        pitch = FreeCAD.Units.Quantity(0.0,FreeCAD.Units.Unit('deg'))
        roll = FreeCAD.Units.Quantity(0.0,FreeCAD.Units.Unit('deg'))  
        
        #Give the object the ability to contain other objetcs:
        obj.addExtension("App::GroupExtensionPython", self)         
        
        #Create scripted object:
        obj.addProperty("App::PropertyString","label","Clamp","label",1).label = label
        obj.addProperty("App::PropertyString","joint","Clamp","joint",1).joint = 'clamp'
        obj.addProperty("App::PropertyString","node","Clamp","node",1).node = node.label
        
        obj.addProperty("App::PropertyDistance","position X","Initial absolute position","position X",1).position_X = x
        obj.addProperty("App::PropertyDistance","position Y","Initial absolute position","position Y",1).position_Y = y
        obj.addProperty("App::PropertyDistance","position Z","Initial absolute position","position Z",1).position_Z = z
        
        #absolute pin orientation:        
        obj.addProperty("App::PropertyAngle","yaw","Initial absolute orientation","yaw",1).yaw = yaw    
        obj.addProperty("App::PropertyAngle","pitch","Initial absolute orientation","pitch",1).pitch = pitch    
        obj.addProperty("App::PropertyAngle","roll","Initial absolute orientation","roll",1).roll = roll         
        
        #Animation parameters:
        obj.addProperty("App::PropertyEnumeration","animate","Animation","animate")
        obj.animate=['false','true']

        obj.addProperty("App::PropertyEnumeration","frame","Animation","frame")
        obj.frame=['global','local']        
        
        obj.addProperty("App::PropertyString","force vector multiplier","Animation","force vector multiplier").force_vector_multiplier = '1'

        obj.Proxy = self
        
        #Add the coordinate system and an system to the GUI. The coordinate system represents the position of the node in space:
        length = FreeCAD.ActiveDocument.getObjectsByLabel("x: structural: " + node.label)[0].Length.Value # Calculate the body characteristic length. Will be used to size the arrows that represent the node.
        p1 = FreeCAD.Vector(0, 0, 0)
        #Add x vector of the coordinate system:
        p2 = FreeCAD.Vector(length, 0, 0)
        l = Draft.makeLine(p1, p2)
        l.Label = 'x: joint: '+ label            
        l.ViewObject.LineColor = (0.00,0.00,0.00)
        l.ViewObject.PointColor = (0.00,0.00,0.00)
        l.Placement=FreeCAD.Placement(FreeCAD.Vector(x,y,z), FreeCAD.Rotation(FreeCAD.Vector(0,0,1),0), FreeCAD.Vector(0,0,0))
        l.ViewObject.EndArrow = True
        l.ViewObject.ArrowType = u"Dot"
        l.ViewObject.LineWidth = 1.00
        l.ViewObject.PointSize = 1.00
        l.ViewObject.ArrowSize = str(length/15)+' mm'
        l.ViewObject.Selectable = False
        #Add y vector of the coordinate system:
        p2 = FreeCAD.Vector(0, length, 0)
        l = Draft.makeLine(p1, p2)
        l.Label = 'y: joint: '+ label            
        l.ViewObject.LineColor = (0.00,0.00,0.00)
        l.ViewObject.PointColor = (0.00,0.00,0.00)
        l.Placement=FreeCAD.Placement(FreeCAD.Vector(x,y,z), FreeCAD.Rotation(FreeCAD.Vector(0,0,1),0), FreeCAD.Vector(0,0,0))
        l.ViewObject.EndArrow = True
        l.ViewObject.ArrowType = u"Dot"
        l.ViewObject.LineWidth = 1.00
        l.ViewObject.PointSize = 1.00
        l.ViewObject.ArrowSize = str(length/15)+' mm' 
        l.ViewObject.Selectable = False
        #Add z vector of the coordinate system:
        p2 = FreeCAD.Vector(0, 0, length)
        l = Draft.makeLine(p1, p2)
        l.Label = 'z: joint: '+ label
        l.ViewObject.ArrowType = u"Dot"            
        l.ViewObject.LineColor = (0.00,0.00,0.00)
        l.ViewObject.PointColor = (0.00,0.00,0.00)
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
        d.ViewObject.Selectable = False
        d.Label = "jf: "+ label

        FreeCAD.ActiveDocument.recompute()
        
    def execute(self, fp):
        '''Do something when doing a recomputation, this method is mandatory'''
        FreeCAD.Console.PrintMessage("Recompute...\n")                   