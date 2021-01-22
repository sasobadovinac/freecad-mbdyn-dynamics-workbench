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
This class implements an in-plane joint between two nodes. It receives an integer number which is used to label the joint, and two nodes. The second node is then constrained to a line fixed to the first node.

An in-line joint forces a point relative to the second node to move along a line attached to the first node.
A point, optionally offset by "relative offset" from the position of "node 2", slides along a
line that passes through a point that is rigidly offset by "relative_line_position" from the position of
"node 1", and is directed as direction 3 (the Z axis) of "relative orientation". 

The joint is defined as:

     joint: 2, #joint label
            in plane,
            2, # first asociated node
                position, 0., 0., 0., #relative plane position
                0., 0., 1., #relative normal direction
            1, # second asociated node
                offset, 0.0, 0.0, 0.0; # relatove offset

'''

#from FreeCAD.Units.Units import FreeCAD.Units.Unit,FreeCAD.Units.Quantity
import FreeCAD
import Draft
import FreeCADGui

class Inplane:
    def __init__(self, obj, label, node1, node2):

        x = node1.position_X
        y = node1.position_Y
        z = node1.position_Z
     
        obj.addExtension("App::GroupExtensionPython", self)  
        
        #Create scripted object:
        obj.addProperty("App::PropertyString","label","In line joint","label").label = label
        obj.addProperty("App::PropertyString","joint","In line joint","joint").joint = 'in plane'
        obj.addProperty("App::PropertyString","node 1","In line joint","node 1").node_1 = node1.label
        obj.addProperty("App::PropertyString","node 2","In line joint","node 2").node_2 = node2.label
        
        #The absolute position is set at the node 1 position, only for animation, not for MBDyn sumulation:        
        obj.addProperty("App::PropertyDistance","position X","Initial absolute position","position X",1).position_X = x
        obj.addProperty("App::PropertyDistance","position Y","Initial absolute position","position Y",1).position_Y = y
        obj.addProperty("App::PropertyDistance","position Z","Initial absolute position","position Z",1).position_Z = z 

        #The relative plane position is initially set to (0,0,0), this is, the line passes through node 1
        obj.addProperty("App::PropertyDistance","relative plane position X","Relative plane position","relative plane position X").relative_plane_position_X = FreeCAD.Units.Quantity(0.0,FreeCAD.Units.Unit('mm'))
        obj.addProperty("App::PropertyDistance","relative plane position Y","Relative plane position","relative plane position Y").relative_plane_position_Y = FreeCAD.Units.Quantity(0.0,FreeCAD.Units.Unit('mm'))
        obj.addProperty("App::PropertyDistance","relative plane position Z","Relative plane position","relative plane position Z").relative_plane_position_Z = FreeCAD.Units.Quantity(0.0,FreeCAD.Units.Unit('mm'))
        
        #The relative plane orientation is initially set to (0,0,1), this is, the X-Y plane.
        obj.addProperty("App::PropertyString","relative normal direction","Relative normal direction","relative normal direction").relative_normal_direction = '0., 0., 1.'
        
        
        #The relative offset is initially set to (0,0,0), this is, node 2 is at the plane, without offset
        obj.addProperty("App::PropertyDistance","relative offset X","Node offset relative to line","relative offset X").relative_offset_X = FreeCAD.Units.Quantity(0.0,FreeCAD.Units.Unit('mm'))
        obj.addProperty("App::PropertyDistance","relative offset Y","Node offset relative to line","relative offset Y").relative_offset_Y = FreeCAD.Units.Quantity(0.0,FreeCAD.Units.Unit('mm'))
        obj.addProperty("App::PropertyDistance","relative offset Z","Node offset relative to line","relative offset Z").relative_offset_Z = FreeCAD.Units.Quantity(0.0,FreeCAD.Units.Unit('mm'))
        
        
        #Animation parameters:
        obj.addProperty("App::PropertyEnumeration","animate","Animation","animate")
        obj.animate=['false','true']

        obj.addProperty("App::PropertyEnumeration","frame","Animation","frame")
        obj.frame=['global','local']  
        
        obj.addProperty("App::PropertyString","structural dummy","Animation","structural dummy").structural_dummy = '2'
        
        obj.addProperty("App::PropertyString","force vector multiplier","Animation","force vector multiplier").force_vector_multiplier = '1'

        obj.Proxy = self
        
        length = FreeCAD.ActiveDocument.getObjectsByLabel("x: structural: " + node1.label)[0].Length.Value # Calculate the body characteristic length. Will be used to size the arrows that represent the node.
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
        p2 = FreeCAD.Vector(0, 0, length)
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
        d.ViewObject.Selectable = False
        d.Label = "jf: "+ label                    
                       
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
                FreeCAD.ActiveDocument.getObjectsByLabel("x: joint: "+FreeCADGui.Selection.getSelection()[0].label)[0].Placement=FreeCAD.Placement(FreeCAD.Vector(x,y,z), FreeCAD.Rotation(yaw,pitch,roll), FreeCAD.Vector(0,0,0))
                FreeCAD.ActiveDocument.getObjectsByLabel("y: joint: "+FreeCADGui.Selection.getSelection()[0].label)[0].Placement=FreeCAD.Placement(FreeCAD.Vector(x,y,z), FreeCAD.Rotation(yaw,pitch,roll), FreeCAD.Vector(0,0,0))
                FreeCAD.ActiveDocument.getObjectsByLabel("z: joint: "+FreeCADGui.Selection.getSelection()[0].label)[0].Placement=FreeCAD.Placement(FreeCAD.Vector(x,y,z), FreeCAD.Rotation(yaw,pitch,roll), FreeCAD.Vector(0,0,0))
                FreeCAD.ActiveDocument.getObjectsByLabel("i: joint: "+FreeCADGui.Selection.getSelection()[0].label)[0].Placement=FreeCAD.Placement(FreeCAD.Vector(x,y,z), FreeCAD.Rotation(yaw,pitch,roll), FreeCAD.Vector(0,0,0))        
        except:
            return True
        
    def execute(self, fp):
        '''Do something when doing a recomputation, this method is mandatory'''
        FreeCAD.Console.PrintMessage("Recompute...\n")                                  