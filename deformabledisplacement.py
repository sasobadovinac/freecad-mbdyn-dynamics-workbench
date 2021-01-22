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
This scripted object represents a deformable displacement joint

The syntax is:

joint: <label>,
    deformable displacement joint,
    <node1>, # a (static) node to which the joint is fixed 
    null, # relative offset
    <node2>, # a dynamic node which will oscilate
    null, # relative offset
    linear viscoelastic isotropic,
    <stiffness>,    # spring stiffness
    <viscosity>,    # viscosity coefficient
    prestrain, single, <direction>, const, <lenght>;

where:

label: an integer number to identify the joint, eg: 1,2,3... 
node1: the label of the structural node to which the joint is fixed, eg: 1,2,3... 
node2: the label of the structural node that oscilates, eg: 1,2,3... 
stiffness: the spring stiffness coefficient in [N/m]
viscosity: the damper Damping Coefficient in [Ns/m]
direction: the direction in which the body will oscilate, for instance: 0., 0., -1
lenght: spring natural lenght in [m]
'''

#from FreeCAD import Units
import FreeCAD
import Draft
import FreeCADGui

class DeformableDisplacement:                  
    def __init__(self, obj, label, node1, node2):
        
        x = node1.position_X
        y = node1.position_Y
        z = node1.position_Z         

        x1 = node2.position_X
        y1 = node2.position_Y
        z1 = node2.position_Z

        #Initial spring stiffness: 
        k = FreeCAD.Units.Quantity(1.0,FreeCAD.Units.Unit('N/m'))
        
        #Initial damping coeficient (viscosity): 
        u = FreeCAD.Units.Quantity(0.003,FreeCAD.Units.Unit('N*s/m'))
        
        #Initial oscilation directon: 
        d = '0., 0., -1'

        #Initial lenght is the distance between the two nodes       
        aux = pow(pow((node2.position_X - node1.position_X),2) + pow((node2.position_Y - node1.position_Y),2) + pow((node2.position_Z - node1.position_Z),2),(0.5)) 
        lenght = FreeCAD.Units.Quantity(aux,FreeCAD.Units.Unit('m')) 
        
        obj.addExtension("App::GroupExtensionPython", self)        
        
        obj.addProperty("App::PropertyString","joint","Deformable displacement joint","joint",1).joint = "deformable displacement joint"    
        obj.addProperty("App::PropertyString","label","Deformable displacement joint","label").label = str(label)
        obj.addProperty("App::PropertyString","node_1","Deformable displacement joint","node_1").node_1 = str(node1.label)
        obj.addProperty("App::PropertyString","node_2","Deformable displacement joint","node_2").node_2 = str(node2.label)
        obj.addProperty("App::PropertyString","stiffness","Deformable displacement joint","stiffness").stiffness = str(k)
        obj.addProperty("App::PropertyString","viscosity","Deformable displacement joint","viscosity").viscosity = str(u)
        obj.addProperty("App::PropertyString","direction","Deformable displacement joint","direction").direction = d
        obj.addProperty("App::PropertyDistance","lenght","Deformable displacement joint","lenght").lenght = lenght

        obj.addProperty("App::PropertyDistance","position X","Initial absolute position","position X",1).position_X = x
        obj.addProperty("App::PropertyDistance","position Y","Initial absolute position","position Y",1).position_Y = y
        obj.addProperty("App::PropertyDistance","position Z","Initial absolute position","position Z",1).position_Z = z
        
        obj.addProperty("App::PropertyString","force vector multiplier","Animation","force vector multiplier").force_vector_multiplier = '1'
        obj.addProperty("App::PropertyString","frame","Animation","frame").frame = 'local'
        obj.addProperty("App::PropertyString","animate","Animation","animate").animate = 'false'
        
        obj.Proxy = self
 
        length = FreeCAD.ActiveDocument.getObjectsByLabel("x: structural: " + node1.label)[0].Length.Value # Calculate the body characteristic length. Will be used to size the arrows that represent the node.
        p1 = FreeCAD.Vector(0, 0, 0)
        #Add x vector of the coordinate system:
        p2 = FreeCAD.Vector(length, 0, 0)
        l = Draft.makeLine(p1, p2)
        l.Label = 'x: joint: '+ str(label)            
        l.ViewObject.LineColor = (1.00,0.00,0.00)
        l.ViewObject.PointColor = (1.00,0.00,0.00)
        l.Placement=FreeCAD.Placement(FreeCAD.Vector(x,y,z), FreeCAD.Rotation(FreeCAD.Vector(0,0,1),0), FreeCAD.Vector(0,0,0))
        l.ViewObject.EndArrow = True
        l.ViewObject.ArrowType = u"Arrow"
        l.ViewObject.LineWidth = 1.00
        l.ViewObject.PointSize = 1.00
        #l.ViewObject.ArrowSize = str(length/15)+' mm'
        l.ViewObject.Selectable = False
        #Add y vector of the coordinate system:
        p2 = FreeCAD.Vector(0, length, 0)
        l = Draft.makeLine(p1, p2)
        l.Label = 'y: joint: '+ str(label)           
        l.ViewObject.LineColor = (0.00,1.00,0.00)
        l.ViewObject.PointColor = (0.00,1.00,0.00)
        l.Placement=FreeCAD.Placement(FreeCAD.Vector(x,y,z), FreeCAD.Rotation(FreeCAD.Vector(0,0,1),0), FreeCAD.Vector(0,0,0))
        l.ViewObject.EndArrow = True
        l.ViewObject.ArrowType = u"Arrow"
        l.ViewObject.LineWidth = 1.00
        l.ViewObject.PointSize = 1.00
        #l.ViewObject.ArrowSize = str(length/15)+' mm' 
        l.ViewObject.Selectable = False
        #Add z vector of the coordinate system:
        p2 = FreeCAD.Vector(0, 0, length)
        l = Draft.makeLine(p1, p2)
        l.Label = 'z: joint: '+ str(label)
        l.ViewObject.ArrowType = u"Dot"            
        l.ViewObject.LineColor = (0.00,0.00,1.00)
        l.ViewObject.PointColor = (0.00,0.00,1.00)
        l.Placement=FreeCAD.Placement(FreeCAD.Vector(x,y,z), FreeCAD.Rotation(FreeCAD.Vector(0,0,1),0), FreeCAD.Vector(0,0,0))
        l.ViewObject.EndArrow = True        
        l.ViewObject.LineWidth = 1.00
        l.ViewObject.PointSize = 1.00
        #l.ViewObject.ArrowSize = str(length/15)+' mm' 
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
        #d.ViewObject.ArrowSize = str(length/15)#+' mm'
        d.ViewObject.Selectable = False
        d.Label = "jf: "+ str(label)
        #add the spring
        h = FreeCAD.ActiveDocument.addObject("Part::Helix","sp: "+ str(label))
        h.Label = "sp: "+ str(label)
        h.Pitch=2.00
        h.Height= pow (( pow((x1 - x),2) + pow((y1 - y),2) + pow((z1 - z),2) ), 1/2)
        h.Radius=Llength.Value/10
        h.Angle=0.00
        h.Placement = FreeCAD.Placement(FreeCAD.Vector(x,y,z), FreeCAD.Rotation(0,0,0), FreeCAD.Vector(0,0,0))
                           
                       
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
                FreeCAD.ActiveDocument.getObjectsByLabel("x: joint: "+FreeCADGui.Selection.getSelection()[0].Label[-1])[0].Placement=FreeCAD.Placement(FreeCAD.Vector(x,y,z), FreeCAD.Rotation(yaw,pitch,roll), FreeCAD.Vector(0,0,0))
                FreeCAD.ActiveDocument.getObjectsByLabel("y: joint: "+FreeCADGui.Selection.getSelection()[0].Label[-1])[0].Placement=FreeCAD.Placement(FreeCAD.Vector(x,y,z), FreeCAD.Rotation(yaw,pitch,roll), FreeCAD.Vector(0,0,0))
                FreeCAD.ActiveDocument.getObjectsByLabel("z: joint: "+FreeCADGui.Selection.getSelection()[0].Label[-1])[0].Placement=FreeCAD.Placement(FreeCAD.Vector(x,y,z), FreeCAD.Rotation(yaw,pitch,roll), FreeCAD.Vector(0,0,0))
                FreeCAD.ActiveDocument.getObjectsByLabel("i: joint: "+FreeCADGui.Selection.getSelection()[0].Label[-1])[0].Placement=FreeCAD.Placement(FreeCAD.Vector(x,y,z), FreeCAD.Rotation(yaw,pitch,roll), FreeCAD.Vector(0,0,0))        
        except:
            return True
        

    def execute(self, fp):
        '''Do something when doing a recomputation, this method is mandatory'''
        FreeCAD.Console.PrintMessage("Recompute Python Box feature\n")
             
