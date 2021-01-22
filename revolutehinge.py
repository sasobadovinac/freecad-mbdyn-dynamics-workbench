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
This scripted object represents a revolute hinge. See: https://www.sky-engin.jp/en/MBDynTutorial/chap14/chap14.html

The syntax is: 

joint: <label>, 
      revolute hinge, 
         <node 1>,
            <relative offset 1>,
            euler, 0.,0.,0., #<relative orientation matrix>
         <node 2>,
            <relative offset 2>,
            euler, 0.,0.,0., #<relative orientation matrix>;

label: an integer number to identify the joint, eg: 1,2,3... 
node1: the label of the first structural node to which the joint is attached, eg: 1,2,3... 
relative offset: the possition of the joint relative to it's structural node. For the example in the above web page is '-0.5, 0.0, 0.0', because the node is at '0.5, 0.0, 0.0' relative to the absolute origin

Example:

joint: 2, 
      revolute hinge, 
         1,                                      # first node or body
            0.5, 0., 0.,                         # relative offset
            hinge, 1, 1., 0., 0., 3, 0., 1., 0., # relative axis orientation
         2,                                      # second node or body
            0., 0., -0.5,                        # relative offset
            hinge, 1, 1., 0., 0., 3, 0., 1., 0.; # relative axis orientation
       
       relative axis orientation and absolute pin orientation
       to rotate around x axis: euler, 0., pi/2., 0.
       to rotate around y axis: euler, pi/2., 0., 0.
'''

#from FreeCAD import Units
import FreeCAD
import FreeCADGui
import Draft

class Revolutehinge:
    def __init__(self, obj, label, node1, node2, cylinder):
        
        #Get the cylinder's center of mass, so that the joint is placed here:
        x = FreeCAD.Units.Quantity(cylinder.Shape.CenterOfMass[0],FreeCAD.Units.Unit('mm'))
        y = FreeCAD.Units.Quantity(cylinder.Shape.CenterOfMass[1],FreeCAD.Units.Unit('mm'))
        z = FreeCAD.Units.Quantity(cylinder.Shape.CenterOfMass[2],FreeCAD.Units.Unit('mm')) 
        
        #Get the cylinder orientation. The joint's orientation is the same:
        #Yaw = (cylinder.Placement.Rotation.toEuler()[0])*math.pi/180.0
        #Pitch = (cylinder.Placement.Rotation.toEuler()[1])*math.pi/180.0
        #Roll = (cylinder.Placement.Rotation.toEuler()[2])*math.pi/180.0
        #Calculate the relative offset 1:       
        x1 = x-node1.position_X
        y1 = y-node1.position_Y
        z1 = z-node1.position_Z
        
        #Calculate the relative offset 2:       
        x2 = x-node2.position_X
        y2 = y-node2.position_Y
        z2 = z-node2.position_Z

        obj.addExtension("App::GroupExtensionPython", self)          
        
        #Create scripted object:
        obj.addProperty("App::PropertyString","label","Revolute hinge","label",1).label = label        
        obj.addProperty("App::PropertyString","node 1","Revolute hinge","node 1",1).node_1 = node1.label
        obj.addProperty("App::PropertyString","node 2","Revolute hinge","node 2",1).node_2 = node2.label
        obj.addProperty("App::PropertyString","joint","Revolute hinge","joint",1).joint = 'revolute hinge'

        #Absolute position:
        obj.addProperty("App::PropertyDistance","position X","Initial absolute position","position X",1).position_X = x
        obj.addProperty("App::PropertyDistance","position Y","Initial absolute position","position Y",1).position_Y = y
        obj.addProperty("App::PropertyDistance","position Z","Initial absolute position","position Z",1).position_Z = z
        
        #Relative offset 1:          
        obj.addProperty("App::PropertyDistance","relative offset 1 X","Relative offset 1","relative offset 1 X",1).relative_offset_1_X = x1
        obj.addProperty("App::PropertyDistance","relative offset 1 Y","Relative offset 1","relative offset 1 Y",1).relative_offset_1_Y = y1
        obj.addProperty("App::PropertyDistance","relative offset 1 Z","Relative offset 1","relative offset 1 Z",1).relative_offset_1_Z = z1
        
        #Relative offset 2: 
        obj.addProperty("App::PropertyDistance","relative offset 2 X","Relative offset 2","relative offset 2 X",1).relative_offset_2_X = x2
        obj.addProperty("App::PropertyDistance","relative offset 2 Y","Relative offset 2","relative offset 2 Y",1).relative_offset_2_Y = y2
        obj.addProperty("App::PropertyDistance","relative offset 2 Z","Relative offset 2","relative offset 2 Z",1).relative_offset_2_Z = z2
        
        #Relative rotation axis 1:
        obj.addProperty("App::PropertyAngle","relative orientation axis 1 yaw","Relative orientation axis 1","relative orientation axis 1 yaw").relative_orientation_axis_1_yaw = FreeCAD.Units.Quantity(0.0,FreeCAD.Units.Unit('deg'))
        obj.addProperty("App::PropertyAngle","relative orientation axis 1 pitch","Relative orientation axis 1","relative orientation axis 1 pitch").relative_orientation_axis_1_pitch = FreeCAD.Units.Quantity(0.0,FreeCAD.Units.Unit('deg'))
        obj.addProperty("App::PropertyAngle","relative orientation axis 1 roll","Relative orientation axis 1","relative orientation axis 1 roll").relative_orientation_axis_1_roll = FreeCAD.Units.Quantity(0.0,FreeCAD.Units.Unit('deg')) 
        
        #Relative rotation axis 2:
        obj.addProperty("App::PropertyAngle","relative orientation axis 2 yaw","Relative orientation axis 2","relative orientation axis 2 yaw").relative_orientation_axis_2_yaw = FreeCAD.Units.Quantity(0.0,FreeCAD.Units.Unit('deg'))
        obj.addProperty("App::PropertyAngle","relative orientation axis 2 pitch","Relative orientation axis 2","relative orientation axis 2 pitch").relative_orientation_axis_2_pitch = FreeCAD.Units.Quantity(0.0,FreeCAD.Units.Unit('deg'))
        obj.addProperty("App::PropertyAngle","relative orientation axis 2 roll","Relative orientation axis 2","relative orientation axis 2 roll").relative_orientation_axis_2_roll = FreeCAD.Units.Quantity(0.0,FreeCAD.Units.Unit('deg'))   
        
        #Animation parameters:
        obj.addProperty("App::PropertyEnumeration","animate","Animation","animate")
        obj.animate=['false','true']

        obj.addProperty("App::PropertyEnumeration","frame","Animation","frame")
        obj.frame=['global','local']        
        
        obj.addProperty("App::PropertyString","force vector multiplier","Animation","force vector multiplier").force_vector_multiplier = '1'
        
        obj.addProperty("App::PropertyString","structural dummy","Animation","structural dummy").structural_dummy = '1'

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
               
