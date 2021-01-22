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

'''

import FreeCAD

class ControlData:
    def __init__(self, obj):

        obj.addExtension("App::GroupExtensionPython", self)
        
        obj.addProperty("App::PropertyEnumeration","skip initial joint assembly","ControlData","skip initial joint assembly")
        obj.skip_initial_joint_assembly = ['false','true']        
        #obj.addProperty("App::PropertyString","skip initial joint assembly","ControlData","skip initial joint assembly").skip_initial_joint_assembly = 'false'
        obj.addProperty("App::PropertyString","output_frequency","ControlData","output_frequency").output_frequency = 'none'
        obj.addProperty("App::PropertyString","initial position stiffness","ControlData","initial position stiffness").initial_position_stiffness = '1.0'    
        obj.addProperty("App::PropertyString","initial velocity stiffness","ControlData","initial velocity stiffness").initial_velocity_stiffness = '1.0'

        obj.Proxy = self
        
    def execute(self, fp):
        '''Do something when doing a recomputation, this method is mandatory'''
        FreeCAD.Console.PrintMessage("Recompute...\n")
        
        
   