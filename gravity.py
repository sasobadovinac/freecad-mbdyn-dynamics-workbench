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
https://www.sky-engin.jp/en/MBDynTutorial/chap05/chap05.html
Defines gravity for the simulation. The syntax is:

gravity: direction, type, g;

direction: defines the direction of the gravitational pull. Eg: '0,0,-1' indicates g pulls towards the negative Z axis
type: is the gravitational pull cosntant? Eg: 'const'
g: the gravitational acceleration. Eg: '9.81 m/s^2' for Earth's gravity 
'''

import FreeCAD

class Gravity:
    def __init__(self, obj):
        
        obj.addExtension("App::GroupExtensionPython", self)  
        obj.addProperty("App::PropertyString","direction","Gravity","direction").direction = '0,-1,0'
        obj.addProperty("App::PropertyString","g","Gravity","g").g = '9.81 m/s^2'
        obj.addProperty("App::PropertyString","type","Gravity","type").type = 'const' 
        
        obj.Proxy = self
        
    def execute(self, fp):
        '''Do something when doing a recomputation, this method is mandatory'''
        FreeCAD.Console.PrintMessage("Recompute...\n")