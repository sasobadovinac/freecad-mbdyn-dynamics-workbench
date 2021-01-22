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

class StructuralForce:
    def __init__(self, obj, label, node):
     
        obj.addExtension("App::GroupExtensionPython", self)  

        #Create scripted object:
        obj.addProperty("App::PropertyString","label","Structural force","label",1).label = label
        obj.addProperty("App::PropertyString","force","Structural force","force",1).force = 'structural force'
        obj.addProperty("App::PropertyString","node","Structural force","node",1).node = node.label
        obj.addProperty("App::PropertyString","type","Structural force","type",1).type = 'absolute'
        obj.addProperty("App::PropertyString","position","Structural force","position",1).position = 'null'

        #Force parameters        

        obj.addProperty("App::PropertyEnumeration","force type","Force parameters","force type")
        obj.force_type=['single']

        obj.addProperty("App::PropertyString","direction","Force parameters","direction").direction = '-1, 0, 0'
        obj.addProperty("App::PropertyString","force value","Force parameters","force value").force_value = 'const, 1.0'

        obj.Proxy = self                   