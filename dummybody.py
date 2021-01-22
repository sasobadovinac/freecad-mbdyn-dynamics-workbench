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
This scripted object represents a dummy body
The "dummy body" object does not exist in MBDyn. It is simply a 3D object in the FreeCAD scene that allows the user visualize the 
motion of a dummy node (see the dummynode class). Since it is only to visualize the motion of a dummy node, 
a dummy body does not have mass, center of mass or inertia matrix. It does have, however, a placement propperty, used to visualize the animation.
The user cannot modify any property o a dummy body.
'''

import FreeCAD

class Dummybody: 
    def __init__(self, obj, BaseBody, label):

        #Compute absolute center of mass, relative to global frame:
        cmx = FreeCAD.Units.Quantity(BaseBody.Shape.Solids[0].CenterOfMass[0],FreeCAD.Units.Unit('mm'))
        cmy = FreeCAD.Units.Quantity(BaseBody.Shape.Solids[0].CenterOfMass[1],FreeCAD.Units.Unit('mm'))
        cmz = FreeCAD.Units.Quantity(BaseBody.Shape.Solids[0].CenterOfMass[2],FreeCAD.Units.Unit('mm'))        
        
        obj.addProperty("App::PropertyString","label","Dummy body","label",1).label = label
        obj.addProperty("App::PropertyString","type","Dummy body","type",1).type = 'dummy'
        obj.addProperty("App::PropertyString","node","Dummy body","node",1).node = label   
        #The center of mass in a dummy body is just to be able to visualize its position in the 3D scene. It does not play any role in the simulation:
        obj.addProperty("App::PropertyDistance","absolute center of mass X","Absolute center of mass","absolute center of mass X",1).absolute_center_of_mass_X = cmx
        obj.addProperty("App::PropertyDistance","absolute center of mass Y","Absolute center of mass","absolute center of mass Y",1).absolute_center_of_mass_Y = cmy
        obj.addProperty("App::PropertyDistance","absolute center of mass Z","Absolute center of mass","absolute center of mass Z",1).absolute_center_of_mass_Z = cmz

        obj.Proxy = self