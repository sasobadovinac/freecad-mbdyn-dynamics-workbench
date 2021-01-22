# -*- coding: utf-8 -*-
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
 joint: 2, 
      axial rotation, 
         1,                           # node 1 label (static node, it seems it could be a dynamic node too, in such a case the axial rotation node would be mooving around)
            null,                     # relative offset (null = the motor is at the static node)
            hinge, euler, 0., 0., 0.  # relative orientation
         2,                           # node 2 label (dynamic node)
            0.025, 0., 0., # relative offset (to the dynamic node)
            hinge, euler, 0., 0., 0.  # relative orientation
         ramp, 2.*pi, 0., 1., 0.;     # angular velocity  
 
'''
#from FreeCAD import Units

import FreeCAD
import Draft
import FreeCADGui

class Axialrotation:
    def __init__(self, obj, label, static, dynamic):
        #Get the cylinder's center of mass, so that the joint is placed here: 
        x = static.position_X - dynamic.position_X
        y = static.position_Y - dynamic.position_Y
        z = static.position_Z - dynamic.position_Z
        
        yaw = FreeCAD.Units.Quantity(0.0,FreeCAD.Units.Unit('deg'))
        pitch = FreeCAD.Units.Quantity(0.0,FreeCAD.Units.Unit('deg'))
        roll = FreeCAD.Units.Quantity(0.0,FreeCAD.Units.Unit('deg')) 
        
        obj.addExtension("App::GroupExtensionPython", self)          
        
        #Create scripted object:
        obj.addProperty("App::PropertyString","label","Axial Rotation","label",1).label = label
        obj.addProperty("App::PropertyString","joint","Axial Rotation","joint",1).joint = 'axial rotation'
        obj.addProperty("App::PropertyString","static node","Axial Rotation","static node",1).static_node = static.label
        obj.addProperty("App::PropertyString","dynamic node","Axial Rotation","dynami cnode",1).dynamic_node = dynamic.label        
        obj.addProperty("App::PropertyString","relative offset","Axial Rotation","relative offset",1).relative_offset = 'null'
        
        obj.addProperty("App::PropertyDistance","relative offset 1 X","Relative offset 1","relative offset 1 X",1).relative_offset_1_X = x
        obj.addProperty("App::PropertyDistance","relative offset 1 Y","Relative offset 1","relative offset 1 Y",1).relative_offset_1_Y = y
        obj.addProperty("App::PropertyDistance","relative offset 1 Z","Relative offset 1","relative offset 1 Z",1).relative_offset_1_Z = z
        
        obj.addProperty("App::PropertyAngle","yaw","Relative orientation 1","yaw").yaw = yaw    
        obj.addProperty("App::PropertyAngle","pitch","Relative orientation 1","pitch").pitch = pitch    
        obj.addProperty("App::PropertyAngle","roll","Relative orientation 1","roll").roll = roll   
        
        obj.addProperty("App::PropertyAngle","yaw1","Relative orientation 2","yaw1").yaw1 = yaw    
        obj.addProperty("App::PropertyAngle","pitch1","Relative orientation 2","pitch1").pitch1 = pitch    
        obj.addProperty("App::PropertyAngle","roll1","Relative orientation 2","roll1").roll1 = roll   
        
        obj.addProperty("App::PropertyString","angular velocity","Axial Rotation","angular velocity").angular_velocity = 'const, 10.'
        
        obj.addProperty("App::PropertyDistance","position X","Initial absolute position","position X",1).position_X = static.position_X
        obj.addProperty("App::PropertyDistance","position Y","Initial absolute position","position Y",1).position_Y = static.position_Y
        obj.addProperty("App::PropertyDistance","position Z","Initial absolute position","position Z",1).position_Z = static.position_Z 
        
        #Animation parameters:
        obj.addProperty("App::PropertyEnumeration","animate","Animation","animate")
        obj.animate=['false','true']

        obj.addProperty("App::PropertyEnumeration","frame","Animation","frame")
        obj.frame=['global','local']        
        
        obj.addProperty("App::PropertyString","force vector multiplier","Animation","force vector multiplier").force_vector_multiplier = '1'

        obj.Proxy = self   
        
        x = static.position_X
        y = static.position_Y 
        z = static.position_Z
        
        length = FreeCAD.ActiveDocument.getObjectsByLabel("x: structural: " + static.label)[0].Length.Value # Calculate the body characteristic length. Will be used to size the arrows that represent the node.
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
                FreeCAD.ActiveDocument.getObjectsByLabel("x: joint: "+FreeCADGui.Selection.getSelection()[0].Label[-1])[0].Placement=FreeCAD.Placement(FreeCAD.Vector(x,y,z), FreeCAD.Rotation(yaw,pitch,roll), FreeCAD.Vector(0,0,0))
                FreeCAD.ActiveDocument.getObjectsByLabel("y: joint: "+FreeCADGui.Selection.getSelection()[0].Label[-1])[0].Placement=FreeCAD.Placement(FreeCAD.Vector(x,y,z), FreeCAD.Rotation(yaw,pitch,roll), FreeCAD.Vector(0,0,0))
                FreeCAD.ActiveDocument.getObjectsByLabel("z: joint: "+FreeCADGui.Selection.getSelection()[0].Label[-1])[0].Placement=FreeCAD.Placement(FreeCAD.Vector(x,y,z), FreeCAD.Rotation(yaw,pitch,roll), FreeCAD.Vector(0,0,0))
                FreeCAD.ActiveDocument.getObjectsByLabel("i: joint: "+FreeCADGui.Selection.getSelection()[0].Label[-1])[0].Placement=FreeCAD.Placement(FreeCAD.Vector(x,y,z), FreeCAD.Rotation(yaw,pitch,roll), FreeCAD.Vector(0,0,0))        
        except:
            return True          