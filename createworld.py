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
import FreeCADGui
import Draft

from customviews import PrismaticCustomView, DynamicNodeCustomView, DummyNodeCustomView, StaticNodeCustomView, RigidBodyCustomView
from customviews import DummyBodyCustomView, RevolutePinCustomView, RevoluteHingeCustomView, ClampCustomView, InLineCustomView, AxialCustomView
from customviews import StructuralForceCustomView, DriveHingeCustomView, SphericalCustomView, DeformableDisplacementCustomView, InPlaneCustomView

class Createworld: 
    def __init__(self):
        l = []            
        for obj in FreeCAD.ActiveDocument.Objects:
            try:
                l.append(abs(obj.Shape.BoundBox.XMax))
                l.append(abs(obj.Shape.BoundBox.XMin))
                l.append(abs(obj.Shape.BoundBox.YMax))
                l.append(abs(obj.Shape.BoundBox.YMin))
                l.append(abs(obj.Shape.BoundBox.ZMax))
                l.append(abs(obj.Shape.BoundBox.ZMin))                
            except:
                pass
                      
        Length = max(l)*4.0       
        p1 = FreeCAD.Vector(-Length/2, 0, 0)
        p2 = FreeCAD.Vector(Length/2, 0, 0)
        Draft.makeLine(p1, p2)
        FreeCAD.ActiveDocument.getObject("Line").Label = "X"
        FreeCADGui.ActiveDocument.getObject("Line").LineColor = (1.00,0.00,0.00)
        FreeCADGui.ActiveDocument.getObject("Line").PointColor = (1.00,0.00,0.00)
        FreeCADGui.ActiveDocument.getObject("Line").DrawStyle = u"Dotted"
        FreeCADGui.ActiveDocument.getObject("Line").PointSize = 1.00
        FreeCADGui.ActiveDocument.getObject("Line").LineWidth = 1.00
        FreeCADGui.ActiveDocument.getObject("Line").Selectable = False
        #FreeCADGui.ActiveDocument.getObject("Line").EndArrow = True
        #FreeCADGui.ActiveDocument.getObject("Line").ArrowType = u"Arrow"
        #FreeCADGui.ActiveDocument.getObject("Line").ArrowSize = str(Length/100)+' mm'
        #FreeCADGui.ActiveDocument.getObject("Line").Selectable = False
        #FreeCAD.ActiveDocument.recompute()
        p1 = FreeCAD.Vector(0, -Length/2, 0)
        p2 = FreeCAD.Vector(0, Length/2, 0)
        Draft.makeLine(p1, p2)
        FreeCAD.ActiveDocument.getObject("Line001").Label = "Y"
        FreeCADGui.ActiveDocument.getObject("Line001").LineColor = (0.00,1.00,0.00)
        FreeCADGui.ActiveDocument.getObject("Line001").PointColor = (0.00,1.00,0.00)
        FreeCADGui.ActiveDocument.getObject("Line001").DrawStyle = u"Dotted"
        FreeCADGui.ActiveDocument.getObject("Line001").PointSize = 1.00
        FreeCADGui.ActiveDocument.getObject("Line001").LineWidth = 1.00
        FreeCADGui.ActiveDocument.getObject("Line001").Selectable = False
        #FreeCADGui.ActiveDocument.getObject("Line001").EndArrow = True
        #FreeCADGui.ActiveDocument.getObject("Line001").ArrowType = u"Arrow"
        #FreeCADGui.ActiveDocument.getObject("Line001").ArrowSize = str(Length/100)+' mm'
        #FreeCADGui.ActiveDocument.getObject("Line001").Selectable = False
        #FreeCAD.ActiveDocument.recompute()
        p1 = FreeCAD.Vector(0, 0, -Length/2)
        p2 = FreeCAD.Vector(0, 0, Length/2)
        Draft.makeLine(p1, p2)
        FreeCAD.ActiveDocument.getObject("Line002").Label = "Z"
        FreeCADGui.ActiveDocument.getObject("Line002").LineColor = (0.00,0.00,1.00)
        FreeCADGui.ActiveDocument.getObject("Line002").PointColor = (0.00,0.00,1.00)
        FreeCADGui.ActiveDocument.getObject("Line002").DrawStyle = u"Dotted"
        FreeCADGui.ActiveDocument.getObject("Line002").PointSize = 1.00
        FreeCADGui.ActiveDocument.getObject("Line002").LineWidth = 1.00
        FreeCADGui.ActiveDocument.getObject("Line002").Selectable = False
        #FreeCADGui.ActiveDocument.getObject("Line002").EndArrow = True
        #FreeCADGui.ActiveDocument.getObject("Line002").ArrowType = u"Arrow"
        #FreeCADGui.ActiveDocument.getObject("Line002").ArrowSize = str(Length/100)+' mm'
        #FreeCADGui.ActiveDocument.getObject("Line002").Selectable = False
        
        FreeCADGui.SendMsgToActiveView("ViewFit")

        FreeCADGui.activeDocument().activeView().viewAxonometric()
        #Add containers:
        FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroup","Solid_objects")
        #Move all the solid objects in the "Solid_objects" group:
        for obj in FreeCAD.ActiveDocument.Objects[:-1]:
            FreeCAD.ActiveDocument.getObject("Solid_objects").addObject(obj)    
            
        FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroup","Bodies")                
        FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroup","Materials")
        FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroup","Forces") 
        FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroup","Global_reference_frame")
        FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroup","Joints")        
        FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroup","MBDyn_simulation")
        FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroup","Structural_nodes")                
        
        obj = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython","Dynamic_nodes")
        FreeCAD.ActiveDocument.getObject("Structural_nodes").addObject(obj) 
        DynamicNodeCustomView(obj.ViewObject)

        obj = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython","Dummy_nodes")
        FreeCAD.ActiveDocument.getObject("Structural_nodes").addObject(obj) 
        DummyNodeCustomView(obj.ViewObject)
        
        obj = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython","Static_nodes")
        FreeCAD.ActiveDocument.getObject("Structural_nodes").addObject(obj) 
        StaticNodeCustomView(obj.ViewObject)        
 
        obj = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython","Rigid_bodies")
        FreeCAD.ActiveDocument.getObject("Bodies").addObject(obj) 
        RigidBodyCustomView(obj.ViewObject)
        
        obj = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython","Dummy_bodies")
        FreeCAD.ActiveDocument.getObject("Bodies").addObject(obj) 
        DummyBodyCustomView(obj.ViewObject)        
        
        obj = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython","Revolute_pin_joints")
        FreeCAD.ActiveDocument.getObject("Joints").addObject(obj) 
        RevolutePinCustomView(obj.ViewObject)
        
        obj = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython","Spherical_hinge_joints")
        FreeCAD.ActiveDocument.getObject("Joints").addObject(obj) 
        SphericalCustomView(obj.ViewObject)
                   
        obj = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython","Revolute_hinge_joints")
        FreeCAD.ActiveDocument.getObject("Joints").addObject(obj) 
        RevoluteHingeCustomView(obj.ViewObject)
        
        obj = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython","Clamp_joints")
        FreeCAD.ActiveDocument.getObject("Joints").addObject(obj) 
        ClampCustomView(obj.ViewObject)
        
        obj = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython","In_line_joints")
        FreeCAD.ActiveDocument.getObject("Joints").addObject(obj) 
        InLineCustomView(obj.ViewObject)
        
        obj = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython","In_plane_joints")
        FreeCAD.ActiveDocument.getObject("Joints").addObject(obj) 
        InPlaneCustomView(obj.ViewObject)
        
        obj = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython","Axial_rotation_joints")
        FreeCAD.ActiveDocument.getObject("Joints").addObject(obj) 
        AxialCustomView(obj.ViewObject)

        obj = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython","Drive_hinge_joints")
        FreeCAD.ActiveDocument.getObject("Joints").addObject(obj) 
        DriveHingeCustomView(obj.ViewObject)
        
        obj = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython","Prismatic_joints")
        FreeCAD.ActiveDocument.getObject("Joints").addObject(obj) 
        PrismaticCustomView(obj.ViewObject)
        
        obj = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython","Deformable_displacement_joints")
        FreeCAD.ActiveDocument.getObject("Joints").addObject(obj) 
        DeformableDisplacementCustomView(obj.ViewObject)
        
        obj = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython","Structural_forces")
        FreeCAD.ActiveDocument.getObject("Forces").addObject(obj) 
        StructuralForceCustomView(obj.ViewObject)     
        
        obj = FreeCAD.ActiveDocument.addObject("App::TextDocument", "input_file")
        FreeCAD.ActiveDocument.getObject("MBDyn_simulation").addObject(obj)
        
        #Move axes into container:
        FreeCAD.ActiveDocument.getObject("Global_reference_frame").addObject(FreeCAD.ActiveDocument.getObject("Line"))
        FreeCAD.ActiveDocument.getObject("Global_reference_frame").addObject(FreeCAD.ActiveDocument.getObject("Line001"))
        FreeCAD.ActiveDocument.getObject("Global_reference_frame").addObject(FreeCAD.ActiveDocument.getObject("Line002"))
        #Add lines to mark center of mass of any body:
        FreeCAD.ActiveDocument.addObject("Part::Line","cmx")
        FreeCAD.ActiveDocument.addObject("Part::Line","cmy")
        FreeCAD.ActiveDocument.addObject("Part::Line","cmz")   
        FreeCADGui.ActiveDocument.getObject("cmx").LineWidth = 1.00
        FreeCADGui.ActiveDocument.getObject("cmy").LineWidth = 1.00
        FreeCADGui.ActiveDocument.getObject("cmz").LineWidth = 1.00
        FreeCADGui.ActiveDocument.getObject("cmx").PointSize = 1.00
        FreeCADGui.ActiveDocument.getObject("cmy").PointSize = 1.00
        FreeCADGui.ActiveDocument.getObject("cmz").PointSize = 1.00
        FreeCADGui.ActiveDocument.getObject("cmx").DrawStyle = u"Dotted"
        FreeCADGui.ActiveDocument.getObject("cmy").DrawStyle = u"Dotted"
        FreeCADGui.ActiveDocument.getObject("cmz").DrawStyle = u"Dotted" 
        #Move the lines to their folder:        
        FreeCAD.ActiveDocument.getObject("Global_reference_frame").addObject(FreeCAD.ActiveDocument.getObject("cmx"))
        FreeCAD.ActiveDocument.getObject("Global_reference_frame").addObject(FreeCAD.ActiveDocument.getObject("cmy"))
        FreeCAD.ActiveDocument.getObject("Global_reference_frame").addObject(FreeCAD.ActiveDocument.getObject("cmz"))

        
        FreeCAD.ActiveDocument.recompute()