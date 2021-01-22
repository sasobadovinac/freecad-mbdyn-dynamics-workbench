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
This scripted object represents a spherical hinge.

The syntax is: 

joint: <label>, 
   spherical hinge, 
      <Node_1>,
         0., 0., 0., # relative offset
      <Node_2>,
         null;          #relative offset
'''

#from FreeCAD import Units
import FreeCAD
import FreeCADGui
import Draft

class Sphericalhinge:
    def __init__(self, obj, label, node1, node2):
        
        x = node1.position_X
        y = node1.position_Y
        z = node1.position_Z
        
        #Get the cylinder orientation. The joint's orientation is the same:
        #Yaw = (cylinder.Placement.Rotation.toEuler()[0])*math.pi/180.0
        #Pitch = (cylinder.Placement.Rotation.toEuler()[1])*math.pi/180.0
        #Roll = (cylinder.Placement.Rotation.toEuler()[2])*math.pi/180.0
        #Calculate the relative offset 1:            
        x1 = node2.position_X-x
        y1 = node2.position_Y-y
        z1 = node2.position_Z-z

        obj.addExtension("App::GroupExtensionPython", self)          
        
        #Create scripted object:
        obj.addProperty("App::PropertyString","label","Spherical hinge","label",1).label = label        
        obj.addProperty("App::PropertyString","node 1","Spherical hinge","node 1",1).node_1 = node1.label
        obj.addProperty("App::PropertyString","node 2","Spherical hinge","node 2",1).node_2 = node2.label
        obj.addProperty("App::PropertyString","joint","Spherical hinge","joint",1).joint = 'spherical hinge'

        #Absolute position:
        obj.addProperty("App::PropertyDistance","position X","Initial absolute position","position X",1).position_X = x
        obj.addProperty("App::PropertyDistance","position Y","Initial absolute position","position Y",1).position_Y = y
        obj.addProperty("App::PropertyDistance","position Z","Initial absolute position","position Z",1).position_Z = z
        
        #Relative offset:          
        obj.addProperty("App::PropertyDistance","relative offset X","Relative offset","relative offset X",1).relative_offset_X = x1
        obj.addProperty("App::PropertyDistance","relative offset Y","Relative offset","relative offset Y",1).relative_offset_Y = y1
        obj.addProperty("App::PropertyDistance","relative offset Z","Relative offset","relative offset Z",1).relative_offset_Z = z1
        
        #Animation parameters:
        obj.addProperty("App::PropertyEnumeration","animate","Animation","animate")
        obj.animate=['false','true']

        obj.addProperty("App::PropertyEnumeration","frame","Animation","frame")
        obj.frame=['global','local']        
        
        obj.addProperty("App::PropertyString","force vector multiplier","Animation","force vector multiplier").force_vector_multiplier = '1'
        
        obj.addProperty("App::PropertyString","structural dummy","Animation","structural dummy").structural_dummy = '1'

        obj.Proxy = self
        
        #Add the coordinate system and an system to the GUI. The coordinate system represents the position of the node in space:
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
        p2 = FreeCAD.Vector(0, 0, 0+length)
        l = Draft.makeLine(p1, p2)
        l.Label = 'z: joint: '+ label
        l.ViewObject.ArrowType = u"Arrow"            
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
                yaw = FreeCADGui.Selection.getSelection()[0].relative_orientation_axis_1_yaw
                pitch = FreeCADGui.Selection.getSelection()[0].relative_orientation_axis_1_pitch
                roll = FreeCADGui.Selection.getSelection()[0].relative_orientation_axis_1_roll
                #Move the arrows and text
                FreeCAD.ActiveDocument.getObjectsByLabel("x: joint: "+FreeCADGui.Selection.getSelection()[0].Label[-1])[0].Placement=FreeCAD.Placement(FreeCAD.Vector(x,y,z), FreeCAD.Rotation(yaw,pitch,roll), FreeCAD.Vector(0,0,0))
                FreeCAD.ActiveDocument.getObjectsByLabel("y: joint: "+FreeCADGui.Selection.getSelection()[0].Label[-1])[0].Placement=FreeCAD.Placement(FreeCAD.Vector(x,y,z), FreeCAD.Rotation(yaw,pitch,roll), FreeCAD.Vector(0,0,0))
                FreeCAD.ActiveDocument.getObjectsByLabel("z: joint: "+FreeCADGui.Selection.getSelection()[0].Label[-1])[0].Placement=FreeCAD.Placement(FreeCAD.Vector(x,y,z), FreeCAD.Rotation(yaw,pitch,roll), FreeCAD.Vector(0,0,0))
                FreeCAD.ActiveDocument.getObjectsByLabel("i: joint: "+FreeCADGui.Selection.getSelection()[0].Label[-1])[0].Placement=FreeCAD.Placement(FreeCAD.Vector(x,y,z), FreeCAD.Rotation(yaw,pitch,roll), FreeCAD.Vector(0,0,0)) 
            
        except:
            return True

        
    def execute(self, fp):
        '''Do something when doing a recomputation, this method is mandatory'''
        FreeCAD.Console.PrintMessage("Recompute...\n")                
               
