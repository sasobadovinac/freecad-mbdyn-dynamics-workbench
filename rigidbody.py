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
This scripted object represents a rigid body
https://www.sky-engin.jp/en/MBDynTutorial/chap05/chap05.html
A structural node provides the degrees of freedom for a rigid body but it does not define a rigid body. 
To define a rigid body, information of mass, center of mass, and inertia tensor is required. 
It is an element called body that carries that information and it is defined in the elements block. 

The syntax is:

body:   <label>, 
        <node>, 
        <mass>, 
        <relative center of mass>, 
        <inertia matrix>;

where:

label: an integer number to identify the body, eg: 1,2,3... 
node: the label of the structural node to which the body belongs, eg: 1,2,3... 
mass: body's mass in kg
relative center of mass: the possition of the body's center of mass relative to it's structural node. 
At this stage, all the structural nodes are defined at the center of mass of their objects (obtained from the CAD part),
therefore for all the bodies the relative center of mass is 0,0,0
inertia matrix: contains the three inertia moments of the body. The inertia moments are calculated below, from the CAD shape. 

Rigid body scripted objects take the shape of the original 3D object (BaseBody). To animate the MBDyn simulation, the possitions
of all the rigid bodies are updated according to the values in the 
MBDynCase.mov file. See: https://www.sky-engin.jp/en/MBDynTutorial/chap07/chap07.html
'''

#from FreeCAD import Units
import FreeCAD

class Rigidbody:                  
    def __init__(self, obj, BaseBody):#density in kg/mm^3 
        #the rigid body label is the same as the BaseBody label:
        label =  BaseBody.Label
        #Body is initially created with a density of 1 g/cm^3:
        density = FreeCAD.Units.Quantity(1e-6,FreeCAD.Units.Unit('kg/mm^3'))
        #obtain object's volume in mm^3:      
        volume = FreeCAD.Units.Quantity(BaseBody.Shape.Volume,FreeCAD.Units.Unit('mm^3')) 
        #calculate object's mass, in kilograms:
        mass = FreeCAD.Units.Quantity(volume*density,FreeCAD.Units.Unit('kg'))
        #Returns moments of inertia divided by density:
        inertia = BaseBody.Shape.Solids[0].MatrixOfInertia
        #Store inertia moments without mass in mm^2:
        iixx = FreeCAD.Units.Quantity(inertia.A[0],FreeCAD.Units.Unit('mm^5'))
        iiyy = FreeCAD.Units.Quantity(inertia.A[5],FreeCAD.Units.Unit('mm^5'))
        iizz = FreeCAD.Units.Quantity(inertia.A[10],FreeCAD.Units.Unit('mm^5'))
        #Compute inertia moments, in kg*mm^2:      
        ixx = FreeCAD.Units.Quantity(iixx*density,FreeCAD.Units.Unit('kg*mm^2'))
        iyy = FreeCAD.Units.Quantity(iiyy*density,FreeCAD.Units.Unit('kg*mm^2'))
        izz = FreeCAD.Units.Quantity(iizz*density,FreeCAD.Units.Unit('kg*mm^2'))
        #Compute absolute center of mass, relative to global frame:
        cmx = FreeCAD.Units.Quantity(BaseBody.Shape.Solids[0].CenterOfMass[0],FreeCAD.Units.Unit('mm'))
        cmy = FreeCAD.Units.Quantity(BaseBody.Shape.Solids[0].CenterOfMass[1],FreeCAD.Units.Unit('mm'))
        cmz = FreeCAD.Units.Quantity(BaseBody.Shape.Solids[0].CenterOfMass[2],FreeCAD.Units.Unit('mm'))
        #since initially the node is at the center of mass, the relative center of mass (relative to the node) is [0,0,0]:
        cmxx = FreeCAD.Units.Quantity(0.0,FreeCAD.Units.Unit('mm'))
        cmyy = FreeCAD.Units.Quantity(0.0,FreeCAD.Units.Unit('mm'))
        cmzz = FreeCAD.Units.Quantity(0.0,FreeCAD.Units.Unit('mm'))  
        
        #Rigid body identifiers:       
        obj.addProperty("App::PropertyString","label","Rigid body","label",1).label = label
        obj.addProperty("App::PropertyString","type","Rigid body","type",1).type = 'rigid'
        obj.addProperty("App::PropertyString","node","Rigid body","node",1).node = label #The body's asociated structural node  
        #Rigid body physical quantities:         
        obj.addProperty("App::PropertyString","density","Properties","density",1).density = '1000 kg/m^3'
        obj.addProperty("App::PropertyString","volume","Properties","volume",1).volume = str(volume)
        obj.addProperty("App::PropertyString","mass","Properties","mass",1).mass = str(mass) 
        #absolute center of mass is the center of mass relative to the absolute coordinate system:
        obj.addProperty("App::PropertyDistance","absolute center of mass X","Absolute center of mass","absolute center of mass X",1).absolute_center_of_mass_X = cmx
        obj.addProperty("App::PropertyDistance","absolute center of mass Y","Absolute center of mass","absolute center of mass Y",1).absolute_center_of_mass_Y = cmy
        obj.addProperty("App::PropertyDistance","absolute center of mass Z","Absolute center of mass","absolute center of mass Z",1).absolute_center_of_mass_Z = cmz
        #since initially the node is at the center of mass, the relative center of mass (relative to the node) is [0,0,0]:
        obj.addProperty("App::PropertyDistance","relative center of mass X","Relative center of mass","relative center of mass X",1).relative_center_of_mass_X = cmxx       
        obj.addProperty("App::PropertyDistance","relative center of mass Y","Relative center of mass","relative center of mass Y",1).relative_center_of_mass_Y = cmyy    
        obj.addProperty("App::PropertyDistance","relative center of mass Z","Relative center of mass","relative center of mass Z",1).relative_center_of_mass_Z = cmzz     
        #Moments of inertia:
        obj.addProperty("App::PropertyString","ixx","Moments of inertia with mass","ixx",1).ixx = str(ixx)
        obj.addProperty("App::PropertyString","iyy","Moments of inertia with mass","iyy",1).iyy = str(iyy)    
        obj.addProperty("App::PropertyString","izz","Moments of inertia with mass","izz",1).izz = str(izz)
        obj.addProperty("App::PropertyString","iixx","Moments of inertia without mass (divided by density)","iixx",1).iixx = str(iixx)
        obj.addProperty("App::PropertyString","iiyy","Moments of inertia without mass (divided by density)","iiyy",1).iiyy = str(iiyy)    
        obj.addProperty("App::PropertyString","iizz","Moments of inertia without mass (divided by density)","iizz",1).iizz = str(iizz)
        
        obj.Proxy = self
        
                
    def execute(self, fp):
        '''Do something when doing a recomputation, this method is mandatory'''
        FreeCAD.Console.PrintMessage("Recompute Python Box feature\n")
             
