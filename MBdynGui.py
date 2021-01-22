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
#from PyQt4 import QtGui,QtCore
from PySide import QtGui,QtCore
import os
#import subprocess
from tospreadsheet import Tospreadsheet
from info import Infonode, Infojoint
from dynamics import Dynamics
#from sys import platform

dyn = Dynamics()

__dir__ = os.path.dirname(__file__)
"""//////////////////////////////////////////////////////////////////////////////IN-PLANE JOINT////////////////////////////////////////////////////"""
class _AddInPlaneCmd:   
    def Activated(self):
        b = FreeCADGui.Selection.getSelection()
        if(len(b)==2):
            node1 = FreeCADGui.Selection.getSelection()[0]
            node2 = FreeCADGui.Selection.getSelection()[1]
            dyn.AddInPlaneJoint(node1,node2)            
                
        else:   
            QtGui.QMessageBox.information(None,"Error","Select two nodes first. The second node will be constrained a plane attached to the first node.")
              
    def GetResources(self):
        MenuText = QtCore.QT_TRANSLATE_NOOP(
            'MBDyn_add_in_plane_joint',
            'Add in plane joint')
        ToolTip = QtCore.QT_TRANSLATE_NOOP(
            'MBDyn_add_in_plane_joint',
            'Add in plane joint')
        return {
            'Pixmap': __dir__ + '/icons/in-plane.png',
            'MenuText': MenuText,
            'ToolTip': ToolTip}

    def IsActive(self):
        return not FreeCAD.ActiveDocument is None

FreeCADGui.addCommand('MBdyn_AddInPlane', _AddInPlaneCmd())  
"""//////////////////////////////////////////////////////////////////////////////PRISMATIC JOINT////////////////////////////////////////////////////"""
class _AddPrismaticCmd:   
    def Activated(self):
        b = FreeCADGui.Selection.getSelection()
        if(len(b)==2):
            node1 = FreeCADGui.Selection.getSelection()[0]
            node2 = FreeCADGui.Selection.getSelection()[1]
            dyn.AddPrismaticJoint(node1,node2)            
                
        else:   
            QtGui.QMessageBox.information(None,"Error","Select two nodes first. The orientation of the second node will be constrained to the orientation of the first node.")
              
    def GetResources(self):
        MenuText = QtCore.QT_TRANSLATE_NOOP(
            'MBDyn_add_prismatic_joint',
            'Add prismatic joint')
        ToolTip = QtCore.QT_TRANSLATE_NOOP(
            'MBDyn_add_prismatic_joint',
            'Add prismatic joint')
        return {
            'Pixmap': __dir__ + '/icons/prismatic.png',
            'MenuText': MenuText,
            'ToolTip': ToolTip}

    def IsActive(self):
        return not FreeCAD.ActiveDocument is None

FreeCADGui.addCommand('MBdyn_AddPrismatic', _AddPrismaticCmd())    
"""//////////////////////////////////////////////////////////////////////////////DEFORMABLE DISPLACEMENT JOINT////////////////////////////////////////////////////"""
class _AddDeformableDisplacementCmd:   
    def Activated(self):
        b = FreeCADGui.Selection.getSelection()
        if(len(b)==2):
            node1 = FreeCADGui.Selection.getSelection()[0]
            node2 = FreeCADGui.Selection.getSelection()[1]
            dyn.AddDeformableDisplacementJoint(node1,node2)            
                
        else:   
            QtGui.QMessageBox.information(None,"Error","Select two nodes first. The second node will be attached, through a deformable displacement joint, to the first node.")
              
    def GetResources(self):
        MenuText = QtCore.QT_TRANSLATE_NOOP(
            'Add deformable displacement joint',
            'Add deformable displacement joint')
        ToolTip = QtCore.QT_TRANSLATE_NOOP(
            'Add deformable displacement joint',
            'Add deformable displacement joint')
        return {
            'Pixmap': __dir__ + '/icons/spring.png',
            'MenuText': MenuText,
            'ToolTip': ToolTip}

    def IsActive(self):
        return not FreeCAD.ActiveDocument is None

FreeCADGui.addCommand('MBdyn_DeformableDisplacement', _AddDeformableDisplacementCmd()) 
"""//////////////////////////////////////////////////////////////////////////////IN-LINE JOINT////////////////////////////////////////////////////"""
class _AddInLineCmd:   
    def Activated(self):
        b = FreeCADGui.Selection.getSelection()
        if(len(b)==2):
            node1 = FreeCADGui.Selection.getSelection()[0]
            node2 = FreeCADGui.Selection.getSelection()[1]
            dyn.AddInLineJoint(node1,node2)            
                
        else:   
            helpp = """An in-line joint forces a node to move along a line attached to another node. 
            The second node, optionally offset by 'relative offset' from the position of the first node, slides along a line that passes through a point that is rigidly offset by 'relative line position' from the position of the first node, and is directed along the Z axis of its 'relative orientation'.
            HINT: Select two nodes and apply the in-line joint. The second node will be constrained to a line fixed to the first node.
            You can afterwards set the appropriate 'relative offset', 'relative line position'             
            """ 

            QtGui.QMessageBox.information(None,"Error",helpp)
              
    def GetResources(self):        

        MenuText = QtCore.QT_TRANSLATE_NOOP(
            'Apply an in-line joint between two nodes',
            'Apply an in-line joint between two nodes')
        ToolTip = QtCore.QT_TRANSLATE_NOOP(
            'Apply an in-line joint between two nodes',
            'Apply an in-line joint between two nodes')
        return {
            'Pixmap': __dir__ + '/icons/in-line.png',
            'MenuText': MenuText,
            'ToolTip': ToolTip}

    def IsActive(self):
        return not FreeCAD.ActiveDocument is None

FreeCADGui.addCommand('MBdyn_AddInLine', _AddInLineCmd()) 
"""//////////////////////////////////////////////////////////////////////////////INFO////////////////////////////////////////////////////"""
class _InfoCmd:  
    def Activated(self):
        b = FreeCADGui.Selection.getSelection()
        if(len(b)==0):
            QtGui.QMessageBox.information(None,"Error","Select a node or a joint first.")
        else:
            if(b[0].Label.startswith('structural:')):
                node = int(b[0].label)
                Infonode(node)#Show node's info
            
            if(b[0].Label.startswith('joint:')):
                joint = int(b[0].label)
                Infojoint(joint)#Show joint's info


    def GetResources(self):
        MenuText = QtCore.QT_TRANSLATE_NOOP(
            'MBdyn_export_summarized_simulation_results_to_a_FreeCAD_spreadsheet',
            'Export summarized simulation results to a FreeCAD spreadsheet')
        ToolTip = QtCore.QT_TRANSLATE_NOOP(
            'MBdyn_export_summarized_simulation_results_to_a_FreeCAD_spreadsheet',
            'Export summarized simulation results to a FreeCAD spreadsheet')
        return {
            'Pixmap': __dir__ + '/icons/spread1.png',
            'MenuText': MenuText,
            'ToolTip': ToolTip}

    def IsActive(self):
        return not FreeCAD.ActiveDocument is None

FreeCADGui.addCommand('MBdyn_Info', _InfoCmd())

"""//////////////////////////////////////////////////////////////////////////////NODE/JOINT CENTER OF MASS////////////////////////////////////////////////////"""
class _Cm1Cmd:  
    def Activated(self):
        b = FreeCADGui.Selection.getSelection()
        if(len(b)!=1):
            QtGui.QMessageBox.information(None,"Error","Select only one structural node, joint or rigid body firs.")
        else:	   
            if(b[0].Label.startswith('structural:')):
                x = FreeCAD.Units.Quantity(b[0].position_X).Value
                y = FreeCAD.Units.Quantity(b[0].position_Y).Value
                z = FreeCAD.Units.Quantity(b[0].position_Z).Value
                
            if(b[0].Label.startswith('joint:')):
                x = float(b[0].absolute_pin_position[:-2].split(",")[0])*1000.0
                y = float(b[0].absolute_pin_position[:-2].split(",")[1])*1000.0
                z = float(b[0].absolute_pin_position[:-2].split(",")[2])*1000.0
                
            if(b[0].Label.startswith('body:')):
                x = FreeCAD.Units.Quantity(b[0].absolute_center_of_mass_X).Value
                y = FreeCAD.Units.Quantity(b[0].absolute_center_of_mass_Y).Value
                z = FreeCAD.Units.Quantity(b[0].absolute_center_of_mass_Z).Value
                
            length = FreeCAD.ActiveDocument.getObject("Line").End[0]
            
            FreeCAD.ActiveDocument.cmx.X1=x+length
            FreeCAD.ActiveDocument.cmx.Y1=y
            FreeCAD.ActiveDocument.cmx.Z1=z
            FreeCAD.ActiveDocument.cmx.X2=x-length
            FreeCAD.ActiveDocument.cmx.Y2=y
            FreeCAD.ActiveDocument.cmx.Z2=z
            
            FreeCAD.ActiveDocument.cmy.X1=x
            FreeCAD.ActiveDocument.cmy.Y1=y+length
            FreeCAD.ActiveDocument.cmy.Z1=z
            FreeCAD.ActiveDocument.cmy.X2=x
            FreeCAD.ActiveDocument.cmy.Y2=y-length
            FreeCAD.ActiveDocument.cmy.Z2=z
            
            FreeCAD.ActiveDocument.cmz.X1=x
            FreeCAD.ActiveDocument.cmz.Y1=y
            FreeCAD.ActiveDocument.cmz.Z1=z+length
            FreeCAD.ActiveDocument.cmz.X2=x
            FreeCAD.ActiveDocument.cmz.Y2=y
            FreeCAD.ActiveDocument.cmz.Z2=z-length
                              

    def GetResources(self):
        MenuText = QtCore.QT_TRANSLATE_NOOP(
            'MBdyn_highlight_the_position_of_a_node_joint_or_center_of_mass_of_a_rigid_body',
            'Highlight the position of a node, joint, or center of mass of a rigid body')
        ToolTip = QtCore.QT_TRANSLATE_NOOP(
            'MBdyn_highlight_the_position_of_a_node_joint_or_center_of_mass_of_a_rigid_body',
            'Highlight the position of a node, joint, or center of mass of a rigid body')
        return {
            'Pixmap': __dir__ + '/icons/center_of_mass.png',
            'MenuText': MenuText,
            'ToolTip': ToolTip}

    def IsActive(self):
        return not FreeCAD.ActiveDocument is None

FreeCADGui.addCommand('MBdyn_Cm1', _Cm1Cmd())
"""//////////////////////////////////////////////////////////////////////////////SOLID BODY INFO////////////////////////////////////////////////////"""
class _CmCmd:  
    def Activated(self):
        b = FreeCADGui.Selection.getSelection()
        if(len(b)==1):
            reply = QtGui.QInputDialog.getText(None,"Dynamics","Provide the material's density, in kg/m^3:")
            if reply[1]:
                BaseBody = FreeCADGui.Selection.getSelection()[0]
                    #Convert density into FreeCAD unit, in kg/mm^3:
                density = FreeCAD.Units.Quantity(float(reply[0])/(1000.0*1000.0),FreeCAD.Units.Unit('kg/mm^3'))
                dyn.Inspect(BaseBody, density)
        else:
            QtGui.QMessageBox.information(None,"Error","Select only one simple solid body first.")
            

    def GetResources(self):
        MenuText = QtCore.QT_TRANSLATE_NOOP(
            'MBdyn_display_physical_properties_and_highlight_center_of_mass',
            'Display physical properties and highlight center of mass')
        ToolTip = QtCore.QT_TRANSLATE_NOOP(
            'MBdyn_display_physical_properties_and_highlight_center_of_mass',
            'Display physical properties and highlight center of mass')
        return {
            'Pixmap': __dir__ + '/icons/info1.png',
            'MenuText': MenuText,
            'ToolTip': ToolTip}

    def IsActive(self):
        return not FreeCAD.ActiveDocument is None

FreeCADGui.addCommand('MBdyn_Cm', _CmCmd())
"""//////////////////////////////////////////////////////////////////////////////SPREADSHEET////////////////////////////////////////////////////"""
class _SpreadsheetCmd:  
    def Activated(self):
        b = FreeCADGui.Selection.getSelection()
        if(len(b)==0):
            QtGui.QMessageBox.information(None,"Error","Select a node or a joint first.")
        else:
            choice = QtGui.QMessageBox.question(None,'Continue?',"Depending on your computer's resources and the simulation resolution, this may take some time. Hint: you can reduce the simulation resolution by increasing the time_step or reducing the final_time of the MBDyn object, in the MBDyn_simulation container. Continue?", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)

        if choice == QtGui.QMessageBox.Yes:
            Tospreadsheet(b[0])
            
    def GetResources(self):
        MenuText = QtCore.QT_TRANSLATE_NOOP(
            'MBdyn_export_full_simulation_results_to_a_FreeCAD_spreadsheet',
            'Export full simulation results to a FreeCAD spreadsheet')
        ToolTip = QtCore.QT_TRANSLATE_NOOP(
            'MBdyn_export_full_simulation_results_to_a_FreeCAD_spreadsheet',
            'Export full simulation results to a FreeCAD spreadsheet')
        return {
            'Pixmap': __dir__ + '/icons/spread.png',
            'MenuText': MenuText,
            'ToolTip': ToolTip}

    def IsActive(self):
        return not FreeCAD.ActiveDocument is None

FreeCADGui.addCommand('MBdyn_Spreadsheet', _SpreadsheetCmd())
"""//////////////////////////////////////////////////////////////////////////////START ANIMATION////////////////////////////////////////////////////"""
class _Animate1Cmd:  
    def Activated(self):
        #dyn.WriteInputFile()
        #dyn.Run()        
        dyn.StartAnimation()
        
    def GetResources(self):
        MenuText = QtCore.QT_TRANSLATE_NOOP(
            'MBdyn_start_animation',
            'Start animation')
        ToolTip = QtCore.QT_TRANSLATE_NOOP(
            'MBdyn_start_animation',
            'Start animation')
        return {
            'Pixmap': __dir__ + '/icons/play1.png',
            'MenuText': MenuText,
            'ToolTip': ToolTip}

    def IsActive(self):
        return not FreeCAD.ActiveDocument is None

FreeCADGui.addCommand('MBdyn_Animate1', _Animate1Cmd()) 
"""//////////////////////////////////////////////////////////////////////////////STOP ANIMATION////////////////////////////////////////////////////"""
class _AnimateStopCmd:  
    def Activated(self):
        dyn.StopAnimation()        
            
    def GetResources(self):
        MenuText = QtCore.QT_TRANSLATE_NOOP(
            'MBdyn_stop_animation',
            'Stop animation')
        ToolTip = QtCore.QT_TRANSLATE_NOOP(
            'MBdyn_stop_animation',
            'Stop animation')
        return {
            'Pixmap': __dir__ + '/icons/stop.png',
            'MenuText': MenuText,
            'ToolTip': ToolTip}

    def IsActive(self):
        return not FreeCAD.ActiveDocument is None

FreeCADGui.addCommand('AnimateStopCmd', _AnimateStopCmd()) 
"""//////////////////////////////////////////////////////////////////////////////RESTORE ALL BODIES AND VECTORS TO THEIR POSSITIONS////////////////////////////////////////////////////"""
class _RestoreCmd:  
    def Activated(self):
        dyn.RestoreScene()
        
    def GetResources(self):
        MenuText = QtCore.QT_TRANSLATE_NOOP(
            'MBdyn_restore_the_3D_scene',
            'Restore the 3D scene')
        ToolTip = QtCore.QT_TRANSLATE_NOOP(
            'MBdyn_restore_the_3D_scene',
            'Restore the 3D scene')
        return {
            'Pixmap': __dir__ + '/icons/restore.png',
            'MenuText': MenuText,
            'ToolTip': ToolTip}

    def IsActive(self):
        return not FreeCAD.ActiveDocument is None

FreeCADGui.addCommand('MBdyn_Restore', _RestoreCmd()) 
"""//////////////////////////////////////////////////////////////////////////////EXECUTE MBDYN////////////////////////////////////////////////////"""
class _RunCmd:  
    def Activated(self):
        #dyn.WriteInputFile()
        dyn.Run()
       
    def GetResources(self):
        MenuText = QtCore.QT_TRANSLATE_NOOP(
            'MBdyn_execute_mbdyn_simulation',
            'Execute MBDyn simulation')
        ToolTip = QtCore.QT_TRANSLATE_NOOP(
            'MBdyn_execute_mbdyn_simulation',
            'Execute MBDyn simulation')
        return {
            'Pixmap': __dir__ + '/icons/play.png',
            'MenuText': MenuText,
            'ToolTip': ToolTip}

    def IsActive(self):
        return not FreeCAD.ActiveDocument is None

FreeCADGui.addCommand('MBdyn_Run', _RunCmd())  
"""//////////////////////////////////////////////////////////////////////////////SPHERICAL HINGE////////////////////////////////////////////"""
class _AddSphericalHingeCmd: 
    def Activated(self):
        b = FreeCADGui.Selection.getSelection()
        if(len(b)<1):
            QtGui.QMessageBox.information(None,"Error...","Select a structural static node and a structural dynamic node first.")
        if(len(b)==2):
            node1 = FreeCADGui.Selection.getSelection()[0]
            node2 = FreeCADGui.Selection.getSelection()[1]
            dyn.AddSphericalHinge(node1, node2)

    def GetResources(self):
        MenuText = QtCore.QT_TRANSLATE_NOOP(
            'MBdyn_add_spherical_hinge',
            'Add spherical hinge')
        ToolTip = QtCore.QT_TRANSLATE_NOOP(
            'MBdyn_add_spherical_hinge',
            'Add spherical hinge')
        return {
            'Pixmap': __dir__ + '/icons/spherical.png',
            'MenuText': MenuText,
            'ToolTip': ToolTip}

    def IsActive(self):
        return not FreeCAD.ActiveDocument is None

FreeCADGui.addCommand('MBdyn_AddSphericalHinge', _AddSphericalHingeCmd()) 
"""//////////////////////////////////////////////////////////////////////////////WRITE INPUT FILE////////////////////////////////////////////"""
class _AddMBDCmd:
    def Activated(self):
        dyn.WriteInputFile()

    def GetResources(self):
        MenuText = QtCore.QT_TRANSLATE_NOOP(
            'MBdyn_write_mbdyn_input_file',
            'Write MBDyn input file')
        ToolTip = QtCore.QT_TRANSLATE_NOOP(
            'MBdyn_write_mbdyn_input_file',
            'Write MBDyn input file')
        return {
            'Pixmap': __dir__ + '/icons/mbd.png',
            'MenuText': MenuText,
            'ToolTip': ToolTip}

    def IsActive(self):
        return not FreeCAD.ActiveDocument is None

FreeCADGui.addCommand('MBdyn_AddMBD', _AddMBDCmd()) 
"""//////////////////////////////////////////////////////////////////////////////AXIAL ROTATION JOINT////////////////////////////////////////////////////"""
class _AddAxialRotationCmd:   
    def Activated(self):
        b = FreeCADGui.Selection.getSelection()
        if(len(b)<1):
            QtGui.QMessageBox.information(None,"Error...","Select a structural static node and a structural dynamic node first.")
        if(len(b)==2):
            static = FreeCADGui.Selection.getSelection()[0]
            dynamic = FreeCADGui.Selection.getSelection()[1]
            dyn.AddAxialRotationJoint(static, dynamic)           
                                
    def GetResources(self):
        MenuText = QtCore.QT_TRANSLATE_NOOP(
            'MBdyn_add_axial_rotation_joint',
            'Add axial rotation joint')
        ToolTip = QtCore.QT_TRANSLATE_NOOP(
            'MBdyn_add_axial_rotation_joint',
            'Add axial rotation joint')
        return {
            'Pixmap': __dir__ + '/icons/axial.png',
            'MenuText': MenuText,
            'ToolTip': ToolTip}

    def IsActive(self):
        return not FreeCAD.ActiveDocument is None

FreeCADGui.addCommand('MBdyn_AxialRotation', _AddAxialRotationCmd()) 


"""//////////////////////////////////////////////////////////////////////////////NERLY FINISHED/////////////////////////////////////////////"""
"""//////////////////////////////////////////////////////////////////////////////CLAMP JOINT///////////////////////////////////////////"""
class _AddClampCmd:    
    def Activated(self):
        b = FreeCADGui.Selection.getSelection()
        if(len(b)<1):
            QtGui.QMessageBox.information(None,"Error...","Select a structural static node first.")
        if(len(b)==1):
            node = FreeCADGui.Selection.getSelection()[0]
            dyn.AddClampJoint(node)

    def GetResources(self):
        MenuText = QtCore.QT_TRANSLATE_NOOP(
            'MBdyn_add_clamp_joint',
            'Add clamp joint')
        ToolTip = QtCore.QT_TRANSLATE_NOOP(
            'MBdyn_add_clamp_joint',
            'Add clamp joint')
        return {
            'Pixmap': __dir__ + '/icons/clamp.png',
            'MenuText': MenuText,
            'ToolTip': ToolTip}

    def IsActive(self):
        return not FreeCAD.ActiveDocument is None

FreeCADGui.addCommand('MBdyn_AddClamp', _AddClampCmd())  

"""//////////////////////////////////////////////////////////////////////////////STRUCTURAL STATIC NODE///////////////////////////////////////////"""
class _AddStructuralStaticCmd:    
    def Activated(self):
        b = FreeCADGui.Selection.getSelection()
        if(len(b)==0):
            QtGui.QMessageBox.information(None,"","Select a solid object first.")
        else:
            body = FreeCADGui.Selection.getSelection()[0]    
            dyn.AddStructuralStaticNode(body) 
    
    def GetResources(self):
        MenuText = QtCore.QT_TRANSLATE_NOOP(
            'MBdyn_add_structural_static_node',
            'Add structural static node')
        ToolTip = QtCore.QT_TRANSLATE_NOOP(
            'MBdyn_add_structural_static_node',
            'Add structural static node')
        return {
            'Pixmap': __dir__ + '/icons/StructuralStatic.png',
            'MenuText': MenuText,
            'ToolTip': ToolTip}

    def IsActive(self):
        return not FreeCAD.ActiveDocument is None

FreeCADGui.addCommand('MBdyn_AddStructuralStatic', _AddStructuralStaticCmd()) 
"""//////////////////////////////////////////////////////////////////////////////PLOT////////////////////////////////////////////////////"""
class _PlotCmd:  
    def Activated(self):
        b = FreeCADGui.Selection.getSelection()
        if(len(b)==0):
            QtGui.QMessageBox.information(None,"Error","Select one node or one joint first.")
        else:
            if(b[0].Label.startswith('structural:')):
                node = int(b[0].label)
                reply = QtGui.QInputDialog.getText(None,"FreeDyn","Enter plot expression:")
                dyn.PlotNode(node, reply[0])#Plot all the data contained in the .mov file
            
            if(b[0].Label.startswith('joint:')):
                joint = int(b[0].label)
                reply = QtGui.QInputDialog.getText(None,"FreeDyn","Enter plot expression:")
                dyn.PlotJoint(joint, reply[0])#Plot all the data contained in the .mov file

    def GetResources(self):
        MenuText = QtCore.QT_TRANSLATE_NOOP(
            'MBdyn_plot_simulation_results',
            'Plot simulation results')
        ToolTip = QtCore.QT_TRANSLATE_NOOP(
            'MBdyn_plot_simulation_results',
            'Plot simulation results')
        return {
            'Pixmap': __dir__ + '/icons/Matplotlib.png',
            'MenuText': MenuText,
            'ToolTip': ToolTip}

    def IsActive(self):
        return not FreeCAD.ActiveDocument is None

FreeCADGui.addCommand('MBdyn_Plot', _PlotCmd())
"""//////////////////////////////////////////////////////////////////////////////REVOLUTE HINGE JOINT///////////////////////////////////////////////////"""
class _AddRevolutehingeCmd:   
    def Activated(self):
        b = FreeCADGui.Selection.getSelection()
        if(len(b)<3):
            QtGui.QMessageBox.information(None,"Error...","Select two structural dynamic nodes and a reference cylinder first.")
        if(len(b)==3):
            node1 = FreeCADGui.Selection.getSelection()[0]
            node2 = FreeCADGui.Selection.getSelection()[1]
            cylinder = FreeCADGui.Selection.getSelection()[2]
            dyn.AddRevoluteHingeJoint(node1, node2, cylinder)              

    def GetResources(self):
        MenuText = QtCore.QT_TRANSLATE_NOOP(
            'MBdyn_create_revolute_hinge_joint',
            'Create revolute hinge joint')
        ToolTip = QtCore.QT_TRANSLATE_NOOP(
            'MBdyn_create_revolute_hinge_joint',
            'Create revolute hinge joint')
        return {
            'Pixmap': __dir__ + '/icons/hinge1.png',
            'MenuText': MenuText,
            'ToolTip': ToolTip}

    def IsActive(self):
        return not FreeCAD.ActiveDocument is None

FreeCADGui.addCommand('MBdyn_AddRevolutehinge', _AddRevolutehingeCmd()) 
"""//////////////////////////////////////////////////////////////////////////////DRIVE HINGE JOINT///////////////////////////////////////////////////"""
class _AddDrivehingeCmd:   
    def Activated(self):
        b = FreeCADGui.Selection.getSelection()
        if(len(b)!=2):
            QtGui.QMessageBox.information(None,"Error...","Select two structural nodes first.")
        if(len(b)==2):
            node1 = FreeCADGui.Selection.getSelection()[0]
            node2 = FreeCADGui.Selection.getSelection()[1]
            dyn.AddDriveHingeJoint(node1, node2)             

    def GetResources(self):
        MenuText = QtCore.QT_TRANSLATE_NOOP(
            'MBdyn_Create_drive_hinge_joint',
            'Create drive hinge joint')
        ToolTip = QtCore.QT_TRANSLATE_NOOP(
            'MBdyn_Create_drive_hinge_joint',
            'Create drive hinge joint')
        return {
            'Pixmap': __dir__ + '/icons/drivehinge.png',
            'MenuText': MenuText,
            'ToolTip': ToolTip}

    def IsActive(self):
        return not FreeCAD.ActiveDocument is None

FreeCADGui.addCommand('MBdyn_AddDrivehinge', _AddDrivehingeCmd()) 
"""//////////////////////////////////////////////////////////////////////////////DUMMY/STATIC BODY////////////////////////////////////////////////////"""
class _AddDummyBodyCmd:
    def Activated(self):
        b = FreeCADGui.Selection.getSelection()
        if(len(b)==1):    
            dyn.AddDummyOrStaticBody(b[0])
                    
        else:
            QtGui.QMessageBox.information(None,"FreeDyn", "Dummy bodies do not have mass or inertia. They are only required to visualize the motion of dummy nodes. Select a solid object first. A dummy body associated to it's respective dummy node will be created.")
            
    def GetResources(self):
        MenuText = QtCore.QT_TRANSLATE_NOOP(
            'MBdyn_create_dummy_static_body',
            'Create dummy/static body')
        ToolTip = QtCore.QT_TRANSLATE_NOOP(
            'MBdyn_create_dummy_static_body',
            'Create dummy/static body')
        return {
            'Pixmap': __dir__ + '/icons/viga1.png',
            'MenuText': MenuText,
            'ToolTip': ToolTip}

    def IsActive(self):
        return not FreeCAD.ActiveDocument is None

FreeCADGui.addCommand('MBdyn_AddDummyBody', _AddDummyBodyCmd())

"""//////////////////////////////////////////////////////////////////////////////REVOLUTE PIN JOINT////////////////////////////////////////////////////"""
class _AddRevolutepinCmd:   
    def Activated(self):
        b = FreeCADGui.Selection.getSelection()                 
        if(len(b)==2):
            dyn.AddRevolutePin(FreeCADGui.Selection.getSelection()[0],FreeCADGui.Selection.getSelection()[1])                        
        else:
            QtGui.QMessageBox.information(None,"FreeDyn","Select a structural dynamic node and a reference cylinder first.")

    def GetResources(self):
        MenuText = QtCore.QT_TRANSLATE_NOOP(
            'MBdyn_create_revolute_pin_joint',
            'Create revolute pin joint')
        ToolTip = QtCore.QT_TRANSLATE_NOOP(
            'MBdyn_create_revolute_pin_joint',
            'Create revolute pin joint')
        return {
            'Pixmap': __dir__ + '/icons/hinge.png',
            'MenuText': MenuText,
            'ToolTip': ToolTip}

    def IsActive(self):
        return not FreeCAD.ActiveDocument is None

FreeCADGui.addCommand('MBdyn_AddRevolutepin', _AddRevolutepinCmd())  
"""//////////////////////////////////////////////////////////////////////////////RIGID BODY///////////////////////////////////////////""" 
class _AddRigidBodyCmd:
    def Activated(self):
        b = FreeCADGui.Selection.getSelection()
        if(len(b)!=1):
            QtGui.QMessageBox.information(None,"FreeDyn","A structural node provides the degrees of freedom for a rigid body but it does not define a body. To define a body, mass, center of mass, and moments of inertia are required. A rigid body carries this information.\n\n Hint: select a simple (non-parametric) solid object first, enter the material's density, and FreeDyn will calculate the body's volume, mass, and moments of inertia. The rigid body will inherit the shape of the original solid object, and will be placed in the Rigid_bodies container, within Bodies.")
        else:
            dyn.AddRigidBody(b[0]) 

    def GetResources(self):
        MenuText = QtCore.QT_TRANSLATE_NOOP(
            'MBdyn_create_rigid_body',
            'Create rigid body')
        ToolTip = QtCore.QT_TRANSLATE_NOOP(
            'MBdyn_create_rigid_body',
            'Create rigid body')
        return {
            'Pixmap': __dir__ + '/icons/viga.png',
            'MenuText': MenuText,
            'ToolTip': ToolTip}

    def IsActive(self):
        return not FreeCAD.ActiveDocument is None

FreeCADGui.addCommand('MBdyn_AddRigidBody', _AddRigidBodyCmd())  

"""//////////////////////////////////////////////////////////////////////////////STRUCTURAL DUMMY NODE////////////////////////////////////////////////////"""
class _AddDummyNodeCmd:  
    def Activated(self):
        b = FreeCADGui.Selection.getSelection()   
        if(len(b)==2):
            dyn.AddStructuralDumyNode(FreeCADGui.Selection.getSelection()[0],FreeCADGui.Selection.getSelection()[1])           
        else:
            QtGui.QMessageBox.information(None,"FreeDyn","Unlike dynamic nodes, a dummy node cannot assume any degree of freedom, and has to be attached to another node. Hint: select a structural dynamic node and a solid object firts. A dummy node will be attached to the selected dynamic node, and will be positioned at the center of mass of the solid object.")
        
    def GetResources(self):
        MenuText = QtCore.QT_TRANSLATE_NOOP(
            'MBdyn_add_structural_dummy_node',
            'Add structural dummy node')
        ToolTip = QtCore.QT_TRANSLATE_NOOP(
            'MBdyn_add_structural_dummy_node',
            'Add structural dummy node')
        return {
            'Pixmap': __dir__ + '/icons/StructuralDummy.png',
            'MenuText': MenuText,
            'ToolTip': ToolTip}

    def IsActive(self):
        return not FreeCAD.ActiveDocument is None

FreeCADGui.addCommand('MBdyn_AddDummyNode', _AddDummyNodeCmd())

"""//////////////////////////////////////////////////////////////////////////////STRUCTURAL DYNAMIC NODE///////////////////////////////////////////////////////////////"""
class _AddStructuralDynamicNodeCmd:  
    def Activated(self):
        b = FreeCADGui.Selection.getSelection()
        if(len(b)==1):
            dyn.AddStructuralDynamicNode(b[0])
            
        else:
            QtGui.QMessageBox.information(None,"FreeDyn","A structural node is a point in space which has six degrees of freedom, three define its possition, using cartesian coordinates (x,y,z), and three define its orientation, using Euler angles (Yaw, Pitch, Roll). A structural node is dynamic when it has inertia (linear and angular momentum). Hint: select a simple (non-parametric) solid object first. A structural dynamic node will be created at the center of mass of the object, and added to the Dynamic_nodes container, inside Structural_nodes. You can change the node's initial conditions in the node's properties.")
           
    def GetResources(self):
        MenuText = QtCore.QT_TRANSLATE_NOOP(
            'MBdyn_add_structural_dynamic_node',
            'Add structural dynamic node')
        ToolTip = QtCore.QT_TRANSLATE_NOOP(
            'MBdyn_add_structural_dynamic_node',
            'Add structural dynamic node')
        return {
            'Pixmap': __dir__ + '/icons/StructuralDynamic.png',
            'MenuText': MenuText,
            'ToolTip': ToolTip}

    def IsActive(self):
        return not FreeCAD.ActiveDocument is None

FreeCADGui.addCommand('MBdyn_AddStructuralDynamicNodeCmd', _AddStructuralDynamicNodeCmd())
"""//////////////////////////////////////////////////////////////////////////////StructuralForce////////////////////////////////////////////////////"""
class _AddStructuralForceCmd:    
    def Activated(self):
        b = FreeCADGui.Selection.getSelection()
        if((len(b)==1)and(b[0].Label.startswith('structural:'))):
            dyn.AddStructuralForce(b[0])
           
        else:
            QtGui.QMessageBox.information(None,"FreeDyn","Select only one structural dynamic node first.")
        

    def GetResources(self):
        MenuText = QtCore.QT_TRANSLATE_NOOP(
            'MBdyn_add_structural_force',
            'Add structural force')
        ToolTip = QtCore.QT_TRANSLATE_NOOP(
            'MBdyn_add_structural_force',
            'Add structural force')
        return {
            'Pixmap': __dir__ + '/icons/force.png',
            'MenuText': MenuText,
            'ToolTip': ToolTip}

    def IsActive(self):
        return not FreeCAD.ActiveDocument is None

FreeCADGui.addCommand('MBdyn_AddStructuralForce', _AddStructuralForceCmd()) 
"""//////////////////////////////////////////////////////////////////////////////GRAVITY////////////////////////////////////////////////////"""
class _AddGravityCmd:    
    def Activated(self):
        dyn.AddGravity()

    def GetResources(self):
        MenuText = QtCore.QT_TRANSLATE_NOOP(
            'MBdyn_add_gravity',
            'Add gravity')
        ToolTip = QtCore.QT_TRANSLATE_NOOP(
            'MBdyn_add_gravity',
            'Add gravity')
        return {
            'Pixmap': __dir__ + '/icons/apple.svg',
            'MenuText': MenuText,
            'ToolTip': ToolTip}

    def IsActive(self):
        return not FreeCAD.ActiveDocument is None

FreeCADGui.addCommand('MBdyn_AddGravity', _AddGravityCmd()) 
"""//////////////////////////////////////////////////////////////////////////////RANDOM Color////////////////////////////////////////////////////"""
class _RandomColorCmd:    
    def Activated(self):
        b = FreeCADGui.Selection.getSelection()
        if((len(b)==1)and(b[0].Label.startswith('body:'))):
            dyn.RandomColor(b[0])
           
        else:
            QtGui.QMessageBox.information(None,"FreeDyn","Select only one rigid body first.")
           
    def GetResources(self):
        MenuText = QtCore.QT_TRANSLATE_NOOP(
            'MBdyn_give_a_random_color_to_a_rigid_body',
            'Gives a random color to a rigid body')
        ToolTip = QtCore.QT_TRANSLATE_NOOP(
            'MBdyn_give_a_random_color_to_a_rigid_body',
            'Gives a random color to a rigid body')
        return {
            'Pixmap': __dir__ + '/icons/colors.png',
            'MenuText': MenuText,
            'ToolTip': ToolTip}

    def IsActive(self):
        return not FreeCAD.ActiveDocument is None

FreeCADGui.addCommand('MBdyn_RandomColor', _RandomColorCmd()) 
"""//////////////////////////////////////////////////////////////////////////////RECALCULATE////////////////////////////////////////////////////"""
class _RecalculateOrientation:    
    def Activated(self):
        objeto = FreeCADGui.Selection.getSelection()[0]
        if(objeto.Label.startswith('structural: ')):            
            dyn.UpdateDynamicNode(objeto.Label)
            
        if(objeto.Label.startswith('joint: ')):
            dyn.UpdateJoint(objeto.Label)
  
        if(objeto.Label.startswith('body: ')):#Update the rigid body physical properties:
            dyn.UpdateRigidBody(objeto)

    def GetResources(self):
        MenuText = QtCore.QT_TRANSLATE_NOOP(
            'MBdyn_recalculate_the_phisical_properties_of_a_rigid_body',
            'Select a rigid body, a structural node or a joint to recalculate')
        ToolTip = QtCore.QT_TRANSLATE_NOOP(
            'MBdyn_recalculate_the_phisical_properties_of_a_rigid_body',
            'Select a rigid body, a structural node or a joint to recalculate')
        return {
            'Pixmap': __dir__ + '/icons/recalculate_node.png',
            'MenuText': MenuText,
            'ToolTip': ToolTip}

    def IsActive(self):
        return not FreeCAD.ActiveDocument is None

FreeCADGui.addCommand('MBdyn_RecalculateOrientation', _RecalculateOrientation()) 
"""//////////////////////////////////////////////////////////////////////////////CREATE GLOBAL REFERENCE FRAME AND ADD CONTAINERS//////////////////////////////////////////////////"""
class _AddXYZCmd:
    
    def Activated(self):          
        dyn.CreateWorld();

    def GetResources(self):
        MenuText = QtCore.QT_TRANSLATE_NOOP(
            'MBdyn_add_global_reference_frame_and_all_the_necesary_containers',
            'Add global reference frame and all the necesary containers')
        ToolTip = QtCore.QT_TRANSLATE_NOOP(
            'MBdyn_add_global_reference_frame_and_all_the_necesary_containers',
            'Add global reference frame and all the necesary containers')
        return {
            'Pixmap': __dir__ + '/icons/earth.png',
            'MenuText': MenuText,
            'ToolTip': ToolTip}

    def IsActive(self):
        return not FreeCAD.ActiveDocument is None

FreeCADGui.addCommand('MBdyn_AddXYZ', _AddXYZCmd())

"""//////////////////////////////////////////////////////////////////////////////LOAD WORKING EXAMPLES//////////////////////////////////////////////////"""
"""//////////////////////////////////////////////////////////////////////////////Free Fall//////////////////////////////////////////////////"""
class _MBdyn_LoadExampleFreeFallingBody1Cmd:
    
    def Activated(self):          
        FreeCAD.open(__dir__ +u"/Samples/Basic examples/1. Free falling body/Solved simulation/FreeFallingBody.FCStd")
        FreeCAD.setActiveDocument("FreeFallingBody")
        FreeCAD.ActiveDocument=FreeCAD.getDocument("FreeFallingBody")
        FreeCADGui.ActiveDocument=FreeCADGui.getDocument("FreeFallingBody")
        FreeCADGui.SendMsgToActiveView("ViewFit")

    def GetResources(self):
        MenuText = QtCore.QT_TRANSLATE_NOOP(
            'Free falling body',
            'Free falling body')
        ToolTip = QtCore.QT_TRANSLATE_NOOP(
            'Free falling body',
            'Free falling body')
        return {
            'Pixmap': __dir__ + '/icons/load.png',
            'MenuText': MenuText,
            'ToolTip': ToolTip}

    def IsActive(self):
        return not FreeCAD.ActiveDocument is None

FreeCADGui.addCommand('MBdyn_LoadExampleFreeFallingBody1', _MBdyn_LoadExampleFreeFallingBody1Cmd())

class _MBdyn_LoadExampleFreeFallingBody2Cmd:
    
    def Activated(self):          
        FreeCAD.open(__dir__ +u"/Samples/Basic examples/1. Free falling body/CAD only/FreeFallingBodyCAD.FCStd")
        FreeCAD.setActiveDocument("FreeFallingBodyCAD")
        FreeCAD.ActiveDocument=FreeCAD.getDocument("FreeFallingBodyCAD")
        FreeCADGui.ActiveDocument=FreeCADGui.getDocument("FreeFallingBodyCAD")
        FreeCADGui.SendMsgToActiveView("ViewFit")

    def GetResources(self):
        MenuText = QtCore.QT_TRANSLATE_NOOP(
            'Free falling body - CAD only',
            'Free falling body - CAD only')
        ToolTip = QtCore.QT_TRANSLATE_NOOP(
            'Free falling body - CAD only',
            'Free falling body - CAD only')
        return {
            'Pixmap': __dir__ + '/icons/load.png',
            'MenuText': MenuText,
            'ToolTip': ToolTip}

    def IsActive(self):
        return not FreeCAD.ActiveDocument is None

FreeCADGui.addCommand('MBdyn_LoadExampleFreeFallingBody2', _MBdyn_LoadExampleFreeFallingBody2Cmd())

"""//////////////////////////////////////////////////////////////////////////////Tennis racket theorem//////////////////////////////////////////////////"""

class _MBdyn_LoadExampleTennisRacketStableCmd:
    
    def Activated(self):          
        FreeCAD.open(__dir__ +u"/Samples/Basic examples/2. Tennis racket theorem/Solved simulation/Stable/TennisRacketStable.FCStd")
        FreeCAD.setActiveDocument("TennisRacketStable")
        FreeCAD.ActiveDocument=FreeCAD.getDocument("TennisRacketStable")
        FreeCADGui.ActiveDocument=FreeCADGui.getDocument("TennisRacketStable")
        FreeCADGui.SendMsgToActiveView("ViewFit")

    def GetResources(self):
        MenuText = QtCore.QT_TRANSLATE_NOOP(
            'Tennis racket theorem - stable rotation',
            'Tennis racket theorem - stable rotation')
        ToolTip = QtCore.QT_TRANSLATE_NOOP(
            'Tennis racket theorem - solved simulation - stable rotation',
            'Tennis racket theorem - solved simulation - stable rotation')
        return {
            'Pixmap': __dir__ + '/icons/load.png',
            'MenuText': MenuText,
            'ToolTip': ToolTip}

    def IsActive(self):
        return not FreeCAD.ActiveDocument is None

FreeCADGui.addCommand('MBdyn_LoadExampleTennisRacketStable', _MBdyn_LoadExampleTennisRacketStableCmd())

class _MBdyn_LoadExampleTennisRacketUnStableCmd:
    
    def Activated(self):          
        FreeCAD.open(__dir__ +u"/Samples/Basic examples/2. Tennis racket theorem/Solved simulation/Unstable/TennisRacketUnstable.FCStd")
        FreeCAD.setActiveDocument("TennisRacketUnstable")
        FreeCAD.ActiveDocument=FreeCAD.getDocument("TennisRacketUnstable")
        FreeCADGui.ActiveDocument=FreeCADGui.getDocument("TennisRacketUnstable")
        FreeCADGui.SendMsgToActiveView("ViewFit")

    def GetResources(self):
        MenuText = QtCore.QT_TRANSLATE_NOOP(
            'Tennis racket theorem - unstable rotation',
            'Tennis racket theorem - unstable rotation')
        ToolTip = QtCore.QT_TRANSLATE_NOOP(
            'Tennis racket theorem - unstable rotation',
            'Tennis racket theorem - unstable rotation')
        return {
            'Pixmap': __dir__ + '/icons/load.png',
            'MenuText': MenuText,
            'ToolTip': ToolTip}

    def IsActive(self):
        return not FreeCAD.ActiveDocument is None

FreeCADGui.addCommand('MBdyn_LoadExampleTennisRacketUnStable', _MBdyn_LoadExampleTennisRacketUnStableCmd())

class _MBdyn_LoadExampleTennisRacketCADCmd:
    
    def Activated(self):          
        FreeCAD.open(__dir__ +u"/Samples/Basic examples/2. Tennis racket theorem/CAD only/TennisRacketCAD.FCStd")
        FreeCAD.setActiveDocument("TennisRacketCAD")
        FreeCAD.ActiveDocument=FreeCAD.getDocument("TennisRacketCAD")
        FreeCADGui.ActiveDocument=FreeCADGui.getDocument("TennisRacketCAD")
        FreeCADGui.SendMsgToActiveView("ViewFit")

    def GetResources(self):
        MenuText = QtCore.QT_TRANSLATE_NOOP(
            'Tennis racket theorem - CAD only',
            'Tennis racket theorem - CAD only')
        ToolTip = QtCore.QT_TRANSLATE_NOOP(
            'Tennis racket theorem - CAD only',
            'Tennis racket theorem - CAD only')
        return {
            'Pixmap': __dir__ + '/icons/load.png',
            'MenuText': MenuText,
            'ToolTip': ToolTip}

    def IsActive(self):
        return not FreeCAD.ActiveDocument is None

FreeCADGui.addCommand('MBdyn_LoadExampleTennisRacketCAD', _MBdyn_LoadExampleTennisRacketCADCmd())

"""//////////////////////////////////////////////////////////////////////////////Simple rigid pendulum//////////////////////////////////////////////////"""

class _MBdyn_LoadExampleSimplePendulum1Cmd:
    
    def Activated(self):          
        FreeCAD.open(__dir__ +u"/Samples/Basic examples/3. Rigid pendulum/Solved simulation/SimplePendulum.FCStd")
        FreeCAD.setActiveDocument("SimplePendulum")
        FreeCAD.ActiveDocument=FreeCAD.getDocument("SimplePendulum")
        FreeCADGui.ActiveDocument=FreeCADGui.getDocument("SimplePendulum")
        FreeCADGui.SendMsgToActiveView("ViewFit")

    def GetResources(self):
        MenuText = QtCore.QT_TRANSLATE_NOOP(
            'Simple rigid pendulum',
            'Simple rigid pendulum')
        ToolTip = QtCore.QT_TRANSLATE_NOOP(
            'Simple rigid pendulum',
            'Simple rigid pendulum')
        return {
            'Pixmap': __dir__ + '/icons/load.png',
            'MenuText': MenuText,
            'ToolTip': ToolTip}

    def IsActive(self):
        return not FreeCAD.ActiveDocument is None

FreeCADGui.addCommand('MBdyn_LoadExampleSimplePendulum1', _MBdyn_LoadExampleSimplePendulum1Cmd())

class _MBdyn_LoadExampleSimplePendulum2Cmd:
    
    def Activated(self):          
        FreeCAD.open(__dir__ +u"/Samples/Basic examples/3. Rigid pendulum/CAD only/SimplePendulumCAD.FCStd")
        FreeCAD.setActiveDocument("SimplePendulumCAD")
        FreeCAD.ActiveDocument=FreeCAD.getDocument("SimplePendulumCAD")
        FreeCADGui.ActiveDocument=FreeCADGui.getDocument("SimplePendulumCAD")
        FreeCADGui.SendMsgToActiveView("ViewFit")

    def GetResources(self):
        MenuText = QtCore.QT_TRANSLATE_NOOP(
            'Simple rigid pendulum - CAD only',
            'Simple rigid pendulum - CAD only')
        ToolTip = QtCore.QT_TRANSLATE_NOOP(
            'Simple rigid pendulum - CAD only',
            'Simple rigid pendulum - CAD only')
        return {
            'Pixmap': __dir__ + '/icons/load.png',
            'MenuText': MenuText,
            'ToolTip': ToolTip}

    def IsActive(self):
        return not FreeCAD.ActiveDocument is None

FreeCADGui.addCommand('MBdyn_LoadExampleSimplePendulum2', _MBdyn_LoadExampleSimplePendulum2Cmd())

"""//////////////////////////////////////////////////////////////////////////////Double rigid pendulum//////////////////////////////////////////////////"""

class _MBdyn_LoadExampleDoublePendulum1Cmd:
    
    def Activated(self):          
        FreeCAD.open(__dir__ +u"/Samples/Basic examples/4. Double rigid pendulum/Solved simulation/DoublePendulum.FCStd")
        FreeCAD.setActiveDocument("DoublePendulum")
        FreeCAD.ActiveDocument=FreeCAD.getDocument("DoublePendulum")
        FreeCADGui.ActiveDocument=FreeCADGui.getDocument("DoublePendulum")
        FreeCADGui.SendMsgToActiveView("ViewFit")

    def GetResources(self):
        MenuText = QtCore.QT_TRANSLATE_NOOP(
            'Double rigid pendulum',
            'Double rigid pendulum')
        ToolTip = QtCore.QT_TRANSLATE_NOOP(
            'Double rigid pendulum',
            'Double rigid pendulum')
        return {
            'Pixmap': __dir__ + '/icons/load.png',
            'MenuText': MenuText,
            'ToolTip': ToolTip}

    def IsActive(self):
        return not FreeCAD.ActiveDocument is None

FreeCADGui.addCommand('MBdyn_LoadExampleDoublePendulum1', _MBdyn_LoadExampleDoublePendulum1Cmd())

class _MBdyn_LoadExampleDoublePendulum2Cmd:
    
    def Activated(self):          
        FreeCAD.open(__dir__ +u"/Samples/Basic examples/4. Double rigid pendulum/CAD only/DoublePendulumCAD.FCStd")
        FreeCAD.setActiveDocument("DoublePendulumCAD")
        FreeCAD.ActiveDocument=FreeCAD.getDocument("DoublePendulumCAD")
        FreeCADGui.ActiveDocument=FreeCADGui.getDocument("DoublePendulumCAD")
        FreeCADGui.SendMsgToActiveView("ViewFit")

    def GetResources(self):
        MenuText = QtCore.QT_TRANSLATE_NOOP(
            'Double rigid pendulum - CAD only',
            'Double rigid pendulum - CAD only')
        ToolTip = QtCore.QT_TRANSLATE_NOOP(
            'Double rigid pendulum - CAD only',
            'Double rigid pendulum - CAD only')
        return {
            'Pixmap': __dir__ + '/icons/load.png',
            'MenuText': MenuText,
            'ToolTip': ToolTip}

    def IsActive(self):
        return not FreeCAD.ActiveDocument is None

FreeCADGui.addCommand('MBdyn_LoadExampleDoublePendulum2', _MBdyn_LoadExampleDoublePendulum2Cmd())

"""/////////////////////////////////////////////////////////////////////////////Sliding pendulum//////////////////////////////////////////////////"""

class _MBdyn_LoadExampleSlidingPendulum1Cmd:
    
    def Activated(self):          
        FreeCAD.open(__dir__ +u"/Samples/Basic examples/5. Sliding pendulum/Solved simulation/SlidingPendulum.FCStd")
        FreeCAD.setActiveDocument("SlidingPendulum")
        FreeCAD.ActiveDocument=FreeCAD.getDocument("SlidingPendulum")
        FreeCADGui.ActiveDocument=FreeCADGui.getDocument("SlidingPendulum")
        FreeCADGui.SendMsgToActiveView("ViewFit")

    def GetResources(self):
        MenuText = QtCore.QT_TRANSLATE_NOOP(
            'Sliding rigid pendulum',
            'Sliding rigid pendulum')
        ToolTip = QtCore.QT_TRANSLATE_NOOP(
            'Sliding rigid pendulum',
            'Sliding rigid pendulum')
        return {
            'Pixmap': __dir__ + '/icons/load.png',
            'MenuText': MenuText,
            'ToolTip': ToolTip}

    def IsActive(self):
        return not FreeCAD.ActiveDocument is None

FreeCADGui.addCommand('MBdyn_LoadExampleSlidingPendulum1', _MBdyn_LoadExampleSlidingPendulum1Cmd())

class _MBdyn_LoadExampleSlidingPendulum2Cmd:
    
    def Activated(self):          
        FreeCAD.open(__dir__ +u"/Samples/Basic examples/5. Sliding pendulum/CAD only/SlidingPendulumCAD.FCStd")
        FreeCAD.setActiveDocument("SlidingPendulumCAD")
        FreeCAD.ActiveDocument=FreeCAD.getDocument("SlidingPendulumCAD")
        FreeCADGui.ActiveDocument=FreeCADGui.getDocument("SlidingPendulumCAD")
        FreeCADGui.SendMsgToActiveView("ViewFit")

    def GetResources(self):
        MenuText = QtCore.QT_TRANSLATE_NOOP(
            'Sliding rigid pendulum - CAD only',
            'Sliding rigid pendulum - CAD only')
        ToolTip = QtCore.QT_TRANSLATE_NOOP(
            'Sliding rigid pendulum - CAD only',
            'Sliding rigid pendulum - CAD only')
        return {
            'Pixmap': __dir__ + '/icons/load.png',
            'MenuText': MenuText,
            'ToolTip': ToolTip}

    def IsActive(self):
        return not FreeCAD.ActiveDocument is None

FreeCADGui.addCommand('MBdyn_LoadExampleSlidingPendulum2', _MBdyn_LoadExampleSlidingPendulum2Cmd())

"""/////////////////////////////////////////////////////////////////////////////Sliding body//////////////////////////////////////////////////"""

class _MBdyn_LoadExampleSlidingBody1Cmd:
    
    def Activated(self):          
        FreeCAD.open(__dir__ +u"/Samples/Basic examples/6. Sliding body/Solved simulation/SlidingBody.FCStd")
        FreeCAD.setActiveDocument("SlidingBody")
        FreeCAD.ActiveDocument=FreeCAD.getDocument("SlidingBody")
        FreeCADGui.ActiveDocument=FreeCADGui.getDocument("SlidingBody")
        FreeCADGui.SendMsgToActiveView("ViewFit")

    def GetResources(self):
        MenuText = QtCore.QT_TRANSLATE_NOOP(
            'Sliding rigid body',
            'Sliding rigid body')
        ToolTip = QtCore.QT_TRANSLATE_NOOP(
            'Sliding rigid body',
            'Sliding rigid body')
        return {
            'Pixmap': __dir__ + '/icons/load.png',
            'MenuText': MenuText,
            'ToolTip': ToolTip}

    def IsActive(self):
        return not FreeCAD.ActiveDocument is None

FreeCADGui.addCommand('MBdyn_LoadExampleSlidingBody1', _MBdyn_LoadExampleSlidingBody1Cmd())

class _MBdyn_LoadExampleSlidingBody2Cmd:
    
    def Activated(self):          
        FreeCAD.open(__dir__ +u"/Samples/Basic examples/6. Sliding body/CAD only/SlidingBodyCAD.FCStd")
        FreeCAD.setActiveDocument("SlidingBodyCAD")
        FreeCAD.ActiveDocument=FreeCAD.getDocument("SlidingBodyCAD")
        FreeCADGui.ActiveDocument=FreeCADGui.getDocument("SlidingBodyCAD")
        FreeCADGui.SendMsgToActiveView("ViewFit")

    def GetResources(self):
        MenuText = QtCore.QT_TRANSLATE_NOOP(
            'Sliding rigid body - CAD only',
            'Sliding rigid body - CAD only')
        ToolTip = QtCore.QT_TRANSLATE_NOOP(
            'Sliding rigid body - CAD only',
            'Sliding rigid body - CAD only')
        return {
            'Pixmap': __dir__ + '/icons/load.png',
            'MenuText': MenuText,
            'ToolTip': ToolTip}

    def IsActive(self):
        return not FreeCAD.ActiveDocument is None

FreeCADGui.addCommand('MBdyn_LoadExampleSlidingBody2', _MBdyn_LoadExampleSlidingBody2Cmd())

"""/////////////////////////////////////////////////////////////////////////////Motor balance//////////////////////////////////////////////////"""

class _MBdyn_LoadExampleMotorBalance1Cmd:
    
    def Activated(self):          
        FreeCAD.open(__dir__ +u"/Samples/Basic examples/7. Motor balance/Solved simulation/MotorBalance.FCStd")
        FreeCAD.setActiveDocument("MotorBalance")
        FreeCAD.ActiveDocument=FreeCAD.getDocument("MotorBalance")
        FreeCADGui.ActiveDocument=FreeCADGui.getDocument("MotorBalance")
        FreeCADGui.SendMsgToActiveView("ViewFit")

    def GetResources(self):
        MenuText = QtCore.QT_TRANSLATE_NOOP(
            'Motor balance',
            'Motor balance')
        ToolTip = QtCore.QT_TRANSLATE_NOOP(
            'Motor balance',
            'Motor balance')
        return {
            'Pixmap': __dir__ + '/icons/load.png',
            'MenuText': MenuText,
            'ToolTip': ToolTip}

    def IsActive(self):
        return not FreeCAD.ActiveDocument is None

FreeCADGui.addCommand('MBdyn_LoadExampleMotorBalance1', _MBdyn_LoadExampleMotorBalance1Cmd())

class _MBdyn_LoadExampleMotorBalance2Cmd:
    
    def Activated(self):          
        FreeCAD.open(__dir__ +u"/Samples/Basic examples/7. Motor balance/CAD only/MotorBalanceCAD.FCStd")
        FreeCAD.setActiveDocument("MotorBalanceCAD")
        FreeCAD.ActiveDocument=FreeCAD.getDocument("MotorBalanceCAD")
        FreeCADGui.ActiveDocument=FreeCADGui.getDocument("MotorBalanceCAD")
        FreeCADGui.SendMsgToActiveView("ViewFit")

    def GetResources(self):
        MenuText = QtCore.QT_TRANSLATE_NOOP(
            'Motor balance - CAD only',
            'Motor balance - CAD only')
        ToolTip = QtCore.QT_TRANSLATE_NOOP(
            'Motor balance - CAD only',
            'Motor balance - CAD only')
        return {
            'Pixmap': __dir__ + '/icons/load.png',
            'MenuText': MenuText,
            'ToolTip': ToolTip}

    def IsActive(self):
        return not FreeCAD.ActiveDocument is None

FreeCADGui.addCommand('MBdyn_LoadExampleMotorBalance2', _MBdyn_LoadExampleMotorBalance2Cmd())

"""/////////////////////////////////////////////////////////////////////////////Crank-slider//////////////////////////////////////////////////"""

class _MBdyn_LoadExampleCrankSlider1Cmd:
    
    def Activated(self):          
        FreeCAD.open(__dir__ +u"/Samples/Basic examples/8. Crank slider/Solved simulation/CrankSlider.FCStd")
        FreeCAD.setActiveDocument("CrankSlider")
        FreeCAD.ActiveDocument=FreeCAD.getDocument("CrankSlider")
        FreeCADGui.ActiveDocument=FreeCADGui.getDocument("CrankSlider")
        FreeCADGui.SendMsgToActiveView("ViewFit")

    def GetResources(self):
        MenuText = QtCore.QT_TRANSLATE_NOOP(
            'Crank-slider',
            'Crank-slider')
        ToolTip = QtCore.QT_TRANSLATE_NOOP(
            'Crank-slider',
            'Crank-slider')
        return {
            'Pixmap': __dir__ + '/icons/load.png',
            'MenuText': MenuText,
            'ToolTip': ToolTip}

    def IsActive(self):
        return not FreeCAD.ActiveDocument is None

FreeCADGui.addCommand('MBdyn_LoadExampleCrankSlider1', _MBdyn_LoadExampleCrankSlider1Cmd())

class _MBdyn_LoadExampleCrankSlider2Cmd:
    
    def Activated(self):          
        FreeCAD.open(__dir__ +u"/Samples/Basic examples/8. Crank slider/CAD only/CrankSliderCAD.FCStd")
        FreeCAD.setActiveDocument("CrankSliderCAD")
        FreeCAD.ActiveDocument=FreeCAD.getDocument("CrankSliderCAD")
        FreeCADGui.ActiveDocument=FreeCADGui.getDocument("CrankSliderCAD")
        FreeCADGui.SendMsgToActiveView("ViewFit")

    def GetResources(self):
        MenuText = QtCore.QT_TRANSLATE_NOOP(
            'Crank-slider - CAD only',
            'Crank-slider - CAD only')
        ToolTip = QtCore.QT_TRANSLATE_NOOP(
            'Crank-slider - CAD only',
            'Crank-slider - CAD only')
        return {
            'Pixmap': __dir__ + '/icons/load.png',
            'MenuText': MenuText,
            'ToolTip': ToolTip}

    def IsActive(self):
        return not FreeCAD.ActiveDocument is None

FreeCADGui.addCommand('MBdyn_LoadExampleCrankSlider2', _MBdyn_LoadExampleCrankSlider2Cmd())

"""/////////////////////////////////////////////////////////////////////////////Jansen's linkage//////////////////////////////////////////////////"""

class _MBdyn_LoadExampleJansensLinkage1Cmd:
    
    def Activated(self):          
        FreeCAD.open(__dir__ +u"/Samples/Basic examples/9. Hansens linkage/Solved simulation/JansensLinkage.FCStd")
        FreeCAD.setActiveDocument("JansensLinkage")
        FreeCAD.ActiveDocument=FreeCAD.getDocument("JansensLinkage")
        FreeCADGui.ActiveDocument=FreeCADGui.getDocument("JansensLinkage")
        FreeCADGui.SendMsgToActiveView("ViewFit")

    def GetResources(self):
        MenuText = QtCore.QT_TRANSLATE_NOOP(
            'Jansens linkage',
            'Jansens linkage')
        ToolTip = QtCore.QT_TRANSLATE_NOOP(
            'Jansens linkage',
            'Jansens linkage')
        return {
            'Pixmap': __dir__ + '/icons/load.png',
            'MenuText': MenuText,
            'ToolTip': ToolTip}

    def IsActive(self):
        return not FreeCAD.ActiveDocument is None

FreeCADGui.addCommand('MBdyn_LoadExampleJansensLinkage1', _MBdyn_LoadExampleJansensLinkage1Cmd())

class _MBdyn_LoadExampleJansensLinkage2Cmd:   
    def Activated(self):          
        FreeCAD.open(__dir__ +u"/Samples/Basic examples/9. Hansens linkage/CAD only/JansensLinkageCAD.FCStd")
        FreeCAD.setActiveDocument("JansensLinkageCAD")
        FreeCAD.ActiveDocument=FreeCAD.getDocument("JansensLinkageCAD")
        FreeCADGui.ActiveDocument=FreeCADGui.getDocument("JansensLinkageCAD")
        FreeCADGui.SendMsgToActiveView("ViewFit")

    def GetResources(self):
        MenuText = QtCore.QT_TRANSLATE_NOOP(
            'Jansens linkage - CAD only',
            'Jansens linkage - CAD only')
        ToolTip = QtCore.QT_TRANSLATE_NOOP(
            'Jansens linkage - CAD only',
            'Jansens linkage - CAD only')
        return {
            'Pixmap': __dir__ + '/icons/load.png',
            'MenuText': MenuText,
            'ToolTip': ToolTip}

    def IsActive(self):
        return not FreeCAD.ActiveDocument is None

FreeCADGui.addCommand('MBdyn_LoadExampleJansensLinkage2', _MBdyn_LoadExampleJansensLinkage2Cmd())

"""/////////////////////////////////////////////////////////////////////////////Jansen's linkage//////////////////////////////////////////////////"""

class _MBdyn_LoadExampleMassSpringDamper1Cmd:    
    def Activated(self):          
        FreeCAD.open(__dir__ +u"/Samples/Basic examples/10. Mass Spring Damper/Solved simulation/MassSpringDamper.FCStd")
        FreeCAD.setActiveDocument("MassSpringDamper")
        FreeCAD.ActiveDocument=FreeCAD.getDocument("MassSpringDamper")
        FreeCADGui.ActiveDocument=FreeCADGui.getDocument("MassSpringDamper")
        FreeCADGui.SendMsgToActiveView("ViewFit")

    def GetResources(self):
        MenuText = QtCore.QT_TRANSLATE_NOOP(
            'Mass-spring-damper',
            'Mass-spring-damper')
        ToolTip = QtCore.QT_TRANSLATE_NOOP(
            'Mass-spring-damper',
            'Mass-spring-damper')
        return {
            'Pixmap': __dir__ + '/icons/load.png',
            'MenuText': MenuText,
            'ToolTip': ToolTip}

    def IsActive(self):
        return not FreeCAD.ActiveDocument is None

FreeCADGui.addCommand('MBdyn_LoadExampleMassSpringDamper1', _MBdyn_LoadExampleMassSpringDamper1Cmd())

class _MBdyn_LoadExampleMassSpringDamper2Cmd:   
    def Activated(self):          
        FreeCAD.open(__dir__ +u"/Samples/Basic examples/10. Mass Spring Damper/CAD only/MassSpringDamperCAD.FCStd")
        FreeCAD.setActiveDocument("MassSpringDamperCAD")
        FreeCAD.ActiveDocument=FreeCAD.getDocument("MassSpringDamperCAD")
        FreeCADGui.ActiveDocument=FreeCADGui.getDocument("MassSpringDamperCAD")
        FreeCADGui.SendMsgToActiveView("ViewFit")

    def GetResources(self):
        MenuText = QtCore.QT_TRANSLATE_NOOP(
            'Mass-spring-damper - CAD only',
            'Mass-spring-damper - CAD only')
        ToolTip = QtCore.QT_TRANSLATE_NOOP(
            'Mass-spring-damper - CAD only',
            'Mass-spring-damper - CAD only')
        return {
            'Pixmap': __dir__ + '/icons/load.png',
            'MenuText': MenuText,
            'ToolTip': ToolTip}

    def IsActive(self):
        return not FreeCAD.ActiveDocument is None

FreeCADGui.addCommand('MBdyn_LoadExampleMassSpringDamper2', _MBdyn_LoadExampleMassSpringDamper2Cmd())

"""///////////////////////////////////////////////////////////////////////////// Vibrations //////////////////////////////////////////////////"""
class _MBdyn_LoadExampleVibrationDamping1Cmd:
    def Activated(self):          
        FreeCAD.open(__dir__ +u"/Samples/Basic examples/11. 1D vibration-damping analysis/Solved simulation/VibrationDamping.FCStd")
        FreeCAD.setActiveDocument("VibrationDamping")
        FreeCAD.ActiveDocument=FreeCAD.getDocument("VibrationDamping")
        FreeCADGui.ActiveDocument=FreeCADGui.getDocument("VibrationDamping")
        FreeCADGui.SendMsgToActiveView("ViewFit")

    def GetResources(self):
        MenuText = QtCore.QT_TRANSLATE_NOOP(
            '1D vibration-damping',
            '1D vibration-damping')
        ToolTip = QtCore.QT_TRANSLATE_NOOP(
            '1D vibration-damping',
            '1D vibration-damping')
        return {
            'Pixmap': __dir__ + '/icons/load.png',
            'MenuText': MenuText,
            'ToolTip': ToolTip}

    def IsActive(self):
        return not FreeCAD.ActiveDocument is None

FreeCADGui.addCommand('MBdyn_LoadExampleVibrationDamping1', _MBdyn_LoadExampleVibrationDamping1Cmd())

class _MBdyn_LoadExampleVibrationDamping2Cmd:
    def Activated(self):          
        FreeCAD.open(__dir__ +u"/Samples/Basic examples/11. 1D vibration-damping analysis/CAD only/VibrationDampingCAD.FCStd")
        FreeCAD.setActiveDocument("VibrationDampingCAD")
        FreeCAD.ActiveDocument=FreeCAD.getDocument("VibrationDampingCAD")
        FreeCADGui.ActiveDocument=FreeCADGui.getDocument("VibrationDampingCAD")
        FreeCADGui.SendMsgToActiveView("ViewFit")

    def GetResources(self):
        MenuText = QtCore.QT_TRANSLATE_NOOP(
            '1D vibration-damping - CAD only',
            '1D vibration-damping - CAD only')
        ToolTip = QtCore.QT_TRANSLATE_NOOP(
            '1D vibration-damping - CAD only',
            '1D vibration-damping - CAD only')
        return {
            'Pixmap': __dir__ + '/icons/load.png',
            'MenuText': MenuText,
            'ToolTip': ToolTip}

    def IsActive(self):
        return not FreeCAD.ActiveDocument is None

FreeCADGui.addCommand('MBdyn_LoadExampleVibrationDamping2', _MBdyn_LoadExampleVibrationDamping2Cmd())

"""///////////////////////////////////////////////////////////////////////////// Gyroscopic precession //////////////////////////////////////////////////"""
class _MBdyn_LoadExampleGyroscopicPrecession1Cmd:
    def Activated(self):          
        FreeCAD.open(__dir__ +u"/Samples/Basic examples/12. Gyroscopic precession/Solved simulation/GyroscopicPrecession.FCStd")
        FreeCAD.setActiveDocument("GyroscopicPrecession")
        FreeCAD.ActiveDocument=FreeCAD.getDocument("GyroscopicPrecession")
        FreeCADGui.ActiveDocument=FreeCADGui.getDocument("GyroscopicPrecession")
        FreeCADGui.SendMsgToActiveView("ViewFit")

    def GetResources(self):
        MenuText = QtCore.QT_TRANSLATE_NOOP(
            'Gyroscopic precession',
            'Gyroscopic precession')
        ToolTip = QtCore.QT_TRANSLATE_NOOP(
            'Gyroscopic precession',
            'Gyroscopic precession')
        return {
            'Pixmap': __dir__ + '/icons/load.png',
            'MenuText': MenuText,
            'ToolTip': ToolTip}

    def IsActive(self):
        return not FreeCAD.ActiveDocument is None

FreeCADGui.addCommand('MBdyn_LoadExampleGyroscopicPrecession1', _MBdyn_LoadExampleGyroscopicPrecession1Cmd())

class _MBdyn_LoadExampleGyroscopicPrecession2Cmd:
    def Activated(self):          
        FreeCAD.open(__dir__ +u"/Samples/Basic examples/12. Gyroscopic precession/CAD only/GyroscopicPrecession.FCStd")
        FreeCAD.setActiveDocument("GyroscopicPrecession")
        FreeCAD.ActiveDocument=FreeCAD.getDocument("GyroscopicPrecession")
        FreeCADGui.ActiveDocument=FreeCADGui.getDocument("GyroscopicPrecession")
        FreeCADGui.SendMsgToActiveView("ViewFit")

    def GetResources(self):
        MenuText = QtCore.QT_TRANSLATE_NOOP(
            'Gyroscopic precession - CAD only',
            'Gyroscopic precession - CAD only')
        ToolTip = QtCore.QT_TRANSLATE_NOOP(
            'Gyroscopic precession - CAD only',
            'Gyroscopic precession - CAD only')
        return {
            'Pixmap': __dir__ + '/icons/load.png',
            'MenuText': MenuText,
            'ToolTip': ToolTip}

    def IsActive(self):
        return not FreeCAD.ActiveDocument is None

FreeCADGui.addCommand('MBdyn_LoadExampleGyroscopicPrecession2', _MBdyn_LoadExampleGyroscopicPrecession2Cmd())

"""///////////////////////////////////////////////////////////////////////////// Servos //////////////////////////////////////////////////"""
class _MBdyn_LoadExampleServomotor1Cmd:
    def Activated(self):          
        FreeCAD.open(__dir__ +u"/Samples/Basic examples/13. Servomotor/Solved simulation/Servomotor.FCStd")
        FreeCAD.setActiveDocument("Servomotor")
        FreeCAD.ActiveDocument=FreeCAD.getDocument("Servomotor")
        FreeCADGui.ActiveDocument=FreeCADGui.getDocument("Servomotor")
        FreeCADGui.SendMsgToActiveView("ViewFit")

    def GetResources(self):
        MenuText = QtCore.QT_TRANSLATE_NOOP(
            'Servomotor',
            'Servomotor')
        ToolTip = QtCore.QT_TRANSLATE_NOOP(
            'Servomotor',
            'Servomotor')
        return {
            'Pixmap': __dir__ + '/icons/load.png',
            'MenuText': MenuText,
            'ToolTip': ToolTip}

    def IsActive(self):
        return not FreeCAD.ActiveDocument is None

FreeCADGui.addCommand('MBdyn_LoadExampleServomotor1', _MBdyn_LoadExampleServomotor1Cmd())

class _MBdyn_LoadExampleServomotor2Cmd:
    def Activated(self):          
        FreeCAD.open(__dir__ +u"/Samples/Basic examples/13. Servomotor/CAD only/ServomotorCAD.FCStd")
        FreeCAD.setActiveDocument("ServomotorCAD")
        FreeCAD.ActiveDocument=FreeCAD.getDocument("ServomotorCAD")
        FreeCADGui.ActiveDocument=FreeCADGui.getDocument("ServomotorCAD")
        FreeCADGui.SendMsgToActiveView("ViewFit")

    def GetResources(self):
        MenuText = QtCore.QT_TRANSLATE_NOOP(
            'Servomotor - CAD only',
            'Servomotor - CAD only')
        ToolTip = QtCore.QT_TRANSLATE_NOOP(
            'Servomotor - CAD only',
            'Servomotor - CAD only')
        return {
            'Pixmap': __dir__ + '/icons/load.png',
            'MenuText': MenuText,
            'ToolTip': ToolTip}

    def IsActive(self):
        return not FreeCAD.ActiveDocument is None

FreeCADGui.addCommand('MBdyn_LoadExampleServomotor2', _MBdyn_LoadExampleServomotor2Cmd())

"""///////////////////////////////////////////////////////////////////////////// Robot gripper //////////////////////////////////////////////////"""
class _MBdyn_LoadExampleRobotGripper1Cmd:
    def Activated(self):          
        FreeCAD.open(__dir__ +u"/Samples/Basic examples/14. Robot gripper/Solved simulation/RobotGripper.FCStd")
        FreeCAD.setActiveDocument("RobotGripper")
        FreeCAD.ActiveDocument=FreeCAD.getDocument("RobotGripper")
        FreeCADGui.ActiveDocument=FreeCADGui.getDocument("RobotGripper")
        FreeCADGui.SendMsgToActiveView("ViewFit")

    def GetResources(self):
        MenuText = QtCore.QT_TRANSLATE_NOOP(
            'Robot gripper',
            'Robot gripper')
        ToolTip = QtCore.QT_TRANSLATE_NOOP(
            'Robot gripper',
            'Robot gripper')
        return {
            'Pixmap': __dir__ + '/icons/load.png',
            'MenuText': MenuText,
            'ToolTip': ToolTip}

    def IsActive(self):
        return not FreeCAD.ActiveDocument is None

FreeCADGui.addCommand('MBdyn_LoadExampleRobotGripper1', _MBdyn_LoadExampleRobotGripper1Cmd())

class _MBdyn_LoadExampleRobotGripper2Cmd:
    def Activated(self):          
        FreeCAD.open(__dir__ +u"/Samples/Basic examples/14. Robot gripper/CAD only/RobotGripperCAD.FCStd")
        FreeCAD.setActiveDocument("RobotGripperCAD")
        FreeCAD.ActiveDocument=FreeCAD.getDocument("RobotGripperCAD")
        FreeCADGui.ActiveDocument=FreeCADGui.getDocument("RobotGripperCAD")
        FreeCADGui.SendMsgToActiveView("ViewFit")

    def GetResources(self):
        MenuText = QtCore.QT_TRANSLATE_NOOP(
            'Robot gripper - CAD only',
            'Robot gripper - CAD only')
        ToolTip = QtCore.QT_TRANSLATE_NOOP(
            'Robot gripper - CAD only',
            'Robot gripper - CAD only')
        return {
            'Pixmap': __dir__ + '/icons/load.png',
            'MenuText': MenuText,
            'ToolTip': ToolTip}

    def IsActive(self):
        return not FreeCAD.ActiveDocument is None

FreeCADGui.addCommand('MBdyn_LoadExampleRobotGripper2', _MBdyn_LoadExampleRobotGripper2Cmd())
