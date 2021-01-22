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
This scripted object represents a drive hinge.

The syntax is: 

joint: <label>, 
      drive hinge, 
         <node 1>,
            hinge, euler, 0., 0., 0., # relative axis orientation
         <node 2>,
            hinge, euler, 0., 0., 0., # relative axis orientation
         single, 0., 0., 1., scalar function, "Fun_Arm_Input", # position
            multilinear,
               0.0, 0.,
               0.5, 0.,
               1.0, 0.; 

label: an integer number to identify the joint, eg: 1,2,3... 
node1: the label of the first structural node (this node will drive the second node)
node1: the label of the first structural node (this node will be driven)

'''

#from FreeCAD import Units
import FreeCAD
import FreeCADGui
import Draft

class Drivehinge:
    def __init__(self, obj, label, node1, node2): 
               
        x = node1.position_X
        y = node1.position_Y
        z = node1.position_Z
        
        obj.addExtension("App::GroupExtensionPython", self)          
        
        #Create scripted object:
        obj.addProperty("App::PropertyString","label","Drive hinge","label",1).label = label        
        obj.addProperty("App::PropertyString","node 1","Drive hinge","node 1",1).node_1 = node1.label
        obj.addProperty("App::PropertyString","node 2","Drive hinge","node 2",1).node_2 = node2.label
        obj.addProperty("App::PropertyString","joint","Drive hinge","joint",1).joint = 'drive hinge'
        
        obj.addProperty("App::PropertyString","rotation axis","Drive hinge","rotation axis").rotation_axis = '0., 0., 1.'
        obj.addProperty("App::PropertyString","scalar function","Drive hinge","scalar function").scalar_function = "scalar_function: "+ label
        
        obj.addProperty("App::PropertyDistance","position X","Initial absolute position","position X").position_X = x
        obj.addProperty("App::PropertyDistance","position Y","Initial absolute position","position Y").position_Y = y
        obj.addProperty("App::PropertyDistance","position Z","Initial absolute position","position Z").position_Z = z
        
        #Relative rotation axis 1:
        obj.addProperty("App::PropertyAngle","relative orientation axis 1 yaw","Relative orientation axis 1","relative orientation axis 1 yaw",1).relative_orientation_axis_1_yaw = FreeCAD.Units.Quantity(0.0,FreeCAD.Units.Unit('deg'))
        obj.addProperty("App::PropertyAngle","relative orientation axis 1 pitch","Relative orientation axis 1","relative orientation axis 1 pitch",1).relative_orientation_axis_1_pitch = FreeCAD.Units.Quantity(0.0,FreeCAD.Units.Unit('deg'))
        obj.addProperty("App::PropertyAngle","relative orientation axis 1 roll","Relative orientation axis 1","relative orientation axis 1 roll",1).relative_orientation_axis_1_roll = FreeCAD.Units.Quantity(0.0,FreeCAD.Units.Unit('deg')) 
        
        #Relative rotation axis 2:
        obj.addProperty("App::PropertyAngle","relative orientation axis 2 yaw","Relative orientation axis 2","relative orientation axis 2 yaw",1).relative_orientation_axis_2_yaw = FreeCAD.Units.Quantity(0.0,FreeCAD.Units.Unit('deg'))
        obj.addProperty("App::PropertyAngle","relative orientation axis 2 pitch","Relative orientation axis 2","relative orientation axis 2 pitch",1).relative_orientation_axis_2_pitch = FreeCAD.Units.Quantity(0.0,FreeCAD.Units.Unit('deg'))
        obj.addProperty("App::PropertyAngle","relative orientation axis 2 roll","Relative orientation axis 2","relative orientation axis 2 roll",1).relative_orientation_axis_2_roll = FreeCAD.Units.Quantity(0.0,FreeCAD.Units.Unit('deg'))   
        
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
       
        obj = FreeCAD.ActiveDocument.addObject("App::TextDocument", "scalar_function: "+ label)   
        obj.Label = 'scalar function: '+ label
        #Add an example scalar function:
        obj.Text = """        
                #The first column represents time and the second column is the angle in radians.        
                #Consider the final time of your simulation.        
                0.0,    0., 
                0.5,    0.,
                1.0,    pi/4.,
                1.5,    pi/4.,
                2.0,    pi/2.,
                2.5,    pi/2.,
                3.0,    pi/4.,
                3.5,    pi/4.,
                4.0,    0,
                4.5,    0,
                5.0,    -pi/4.,
                5.5,    -pi/4.,
                6.0,    -pi/2.,
                6.5,    -pi/2.,
                7.0,    -pi/4.,
                7.5,    -pi/4.,
                8.0,    0.,
                8.5,    0.;""" 
                       
        FreeCAD.ActiveDocument.recompute()

    def onChanged(self, fp, prop):
        '''Do something when a property has changed'''
        try:
            if (len(FreeCADGui.Selection.getSelection()) == 1):
                #Get the new position and orientation
                x = FreeCADGui.Selection.getSelection()[0].position_X
                y = FreeCADGui.Selection.getSelection()[0].position_Y
                z = FreeCADGui.Selection.getSelection()[0].position_Z
                
                if (float(FreeCADGui.Selection.getSelection()[0].rotation_axis.split(",")[0])==0.0) and (float(FreeCADGui.Selection.getSelection()[0].rotation_axis.split(",")[1])==0.0) and (float(FreeCADGui.Selection.getSelection()[0].rotation_axis.split(",")[2])==1.0):
                    yaw = 0.
                    pitch = 0.
                    roll = 0.
                    
                if (float(FreeCADGui.Selection.getSelection()[0].rotation_axis.split(",")[0])==0.0) and (float(FreeCADGui.Selection.getSelection()[0].rotation_axis.split(",")[1])==1.0) and (float(FreeCADGui.Selection.getSelection()[0].rotation_axis.split(",")[2])==0.0):
                    yaw = 0.
                    pitch = 0.
                    roll = -90.

                if (float(FreeCADGui.Selection.getSelection()[0].rotation_axis.split(",")[0])==1.0) and (float(FreeCADGui.Selection.getSelection()[0].rotation_axis.split(",")[1])==0.0) and (float(FreeCADGui.Selection.getSelection()[0].rotation_axis.split(",")[2])==0.0):
                    yaw = 0.
                    pitch = -90.
                    roll = 0.
                                           
                #Move the arrows
                FreeCAD.ActiveDocument.getObjectsByLabel("x: joint: "+FreeCADGui.Selection.getSelection()[0].Label[-1])[0].Placement=FreeCAD.Placement(FreeCAD.Vector(x,y,z), FreeCAD.Rotation(yaw,pitch,roll), FreeCAD.Vector(0,0,0))
                FreeCAD.ActiveDocument.getObjectsByLabel("y: joint: "+FreeCADGui.Selection.getSelection()[0].Label[-1])[0].Placement=FreeCAD.Placement(FreeCAD.Vector(x,y,z), FreeCAD.Rotation(yaw,pitch,roll), FreeCAD.Vector(0,0,0))
                FreeCAD.ActiveDocument.getObjectsByLabel("z: joint: "+FreeCADGui.Selection.getSelection()[0].Label[-1])[0].Placement=FreeCAD.Placement(FreeCAD.Vector(x,y,z), FreeCAD.Rotation(yaw,pitch,roll), FreeCAD.Vector(0,0,0))            
            
        except:
            return True

        
    def execute(self, fp):
        '''Do something when doing a recomputation, this method is mandatory'''
        FreeCAD.Console.PrintMessage("Recompute...\n")                
               
