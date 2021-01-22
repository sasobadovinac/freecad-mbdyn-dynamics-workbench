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

import FreeCAD
import Draft

'''


   joint: <label>, 
      in line, 
         <node 1>,
            <relative line position>,
            <relative orientation>,
         <node 2>,
            [ offset, <relative offset> ];#Still don't get this, jut used 0,0,0

<node 2> (or the point offset by <relative offset>) is constrained on the straight line fixed to <node 1> 
that goes through <relative line position> and is parallel to the z-direction defined by <relative orientation>. 
'''

class Prismatic:
    def __init__(self, obj, label, node1, node2):
        
        x = node1.position_X
        y = node1.position_Y
        z = node1.position_Z 
     
        obj.addExtension("App::GroupExtensionPython", self)  
        #Create scripted object:
        obj.addProperty("App::PropertyString","label","In line joint","label",1).label = label
        obj.addProperty("App::PropertyString","joint","In line joint","joint",1).joint = 'prismatic'
        obj.addProperty("App::PropertyString","node 1","In line joint","node 1",1).node_1 = node1.label
        obj.addProperty("App::PropertyString","node 2","In line joint","node 2",1).node_2 = node2.label
            #Absolute position at the node 1 position, only for animation, not for MBDyn sumulation:  
        obj.addProperty("App::PropertyDistance","position X","Initial absolute position","position X",1).position_X = x
        obj.addProperty("App::PropertyDistance","position Y","Initial absolute position","position Y",1).position_Y = y
        obj.addProperty("App::PropertyDistance","position Z","Initial absolute position","position Z",1).position_Z = z

        obj.addProperty("App::PropertyString","animate","Animation","animate").animate = 'false'
        obj.addProperty("App::PropertyString","frame","Animation","frame").frame = 'local'
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
        d.ViewObject.Selectable = False
        d.Label = "jf: "+ label 
        
        FreeCAD.ActiveDocument.recompute()
        
    def execute(self, fp):
        '''Do something when doing a recomputation, this method is mandatory'''
        FreeCAD.Console.PrintMessage("Recompute...\n")                    