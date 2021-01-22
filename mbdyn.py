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
This class implements the parameters to define a MBDyn simulation. 

From the webpage https://www.sky-engin.jp/en/MBDynTutorial/chap04/chap04.html

"In this block we set various conditions related to numerical computation for the problem selected in the data block. 
Because only the initial value problem is supported at present, the syntax of the block is as follows.  

begin: initial value;
   initial time: 0.;
   final time: 1.;
   time step: 1.e-3;
   max iterations: 10;
   tolerance: 1.e-6;
end: initial value;

In this example, it is set that the numerical integration is to be carried out from time 0 to 1 with a time step 1e-3. 
Conditions such as "time step," "max iterations," and "tolerance" are usually determined considering the trade off 
between computational cost and accuracy. There are many other conditions that can be set. 
Refer to the official input manual for more information."
'''

import FreeCAD

class MBDyn:
    def __init__(self, obj):
        
        obj.addExtension("App::GroupExtensionPython", self)  
        obj.addProperty("App::PropertyString","initial time","MBDyn","initial time").initial_time = '0.0 s'
        obj.addProperty("App::PropertyString","final time","MBDyn","final time").final_time = '2.0 s'
        obj.addProperty("App::PropertyString","time step","MBDyn","time step").time_step = '1.0e-2 s'
        obj.addProperty("App::PropertyString","max iterations","MBDyn","max iterations").max_iterations = '10'
        obj.addProperty("App::PropertyString","tolerance","MBDyn","tolerance").tolerance = '1.0e-6'
        obj.addProperty("App::PropertyString","precision","MBDyn","precision").precision = '5'
        obj.addProperty("App::PropertyString","derivatives tolerance","MBDyn","derivatives tolerance").derivatives_tolerance = '1.e-4'
        obj.addProperty("App::PropertyString","derivatives max iterations","MBDyn","derivatives max iterations").derivatives_max_iterations = '100'

        obj.Proxy = self
        
    def execute(self, fp):
        '''Do something when doing a recomputation, this method is mandatory'''
        FreeCAD.Console.PrintMessage("Recompute...\n") 