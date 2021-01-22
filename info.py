# -*- coding: utf-8 -*-
import FreeCAD
import numpy as np
#import os
#__dir__ = os.path.dirname(__file__)

import tempfile

__dir__ = tempfile.gettempdir()

class Infonode:  
    def __init__(self, bodynumber):
        label = "minimum_kinematic_info_node_"+str(bodynumber)	
        InitialTime = float(FreeCAD.ActiveDocument.getObject("MBDyn").initial_time[:-2])
        FinalTime = float(FreeCAD.ActiveDocument.getObject("MBDyn").final_time[:-2])
        data = np.genfromtxt(__dir__ + '/MBDynCase.mov', delimiter=' ')
        x,y,z = [],[],[]#Possition
        Eux,Euy,Euz = [],[],[]#Orientation
        Vx,Vy,Vz = [],[],[]#Speed      
        Wx,Wy,Wz = [],[],[]#Angular speed

        for row in data:
            if(row[0]==bodynumber):
                x.append(row[1])
                y.append(row[2])
                z.append(row[3])
                Eux.append(row[4])
                Euy.append(row[5])
                Euz.append(row[6])
                Vx.append(row[7])
                Vy.append(row[8])
                Vz.append(row[9])
                Wx.append(row[10])
                Wy.append(row[11])
                Wz.append(row[12])

        time = np.linspace(InitialTime,FinalTime,len(x))

        maxx = str(max(x))
        minx = str(min(x))       
        maxy = str(max(y))
        miny = str(min(y))      
        maxz = str(max(z))
        minz = str(min(z))     

        maxEux = str(max(Eux))
        minEux = str(min(Eux))
        maxEuy = str(max(Euy))
        minEuy = str(min(Euy))
        maxEuz = str(max(Euz))
        minEuz = str(min(Euz))

        maxVx = str(max(Vx))
        minVx = str(min(Vx))
        maxVy = str(max(Vy))
        minVy = str(min(Vy)) 
        maxVz = str(max(Vz))
        minVz = str(min(Vz)) 

        maxWx = str(max(Wx))
        minWx = str(min(Wx))
        maxWy = str(max(Wy))
        minWy = str(min(Wy))    
        maxWz = str(max(Wz))
        minWz = str(min(Wz))    

        FreeCAD.ActiveDocument.addObject('Spreadsheet::Sheet',label)

        FreeCAD.ActiveDocument.getObject(label).set('A1', 'POSITION INFORMATION:')
        FreeCAD.ActiveDocument.getObject(label).set('B1', 'max x possition [m]:')
        FreeCAD.ActiveDocument.getObject(label).set('B2', 'min x possition [m]:')
        FreeCAD.ActiveDocument.getObject(label).set('B3', 'max y possition [m]:')
        FreeCAD.ActiveDocument.getObject(label).set('B4', 'min y possition [m]:')
        FreeCAD.ActiveDocument.getObject(label).set('B5', 'max z possition [m]:')
        FreeCAD.ActiveDocument.getObject(label).set('B6', 'min z possition [m]:')

        FreeCAD.ActiveDocument.getObject(label).set('C1', maxx)
        FreeCAD.ActiveDocument.getObject(label).set('C2', minx)
        FreeCAD.ActiveDocument.getObject(label).set('C3', maxy)
        FreeCAD.ActiveDocument.getObject(label).set('C4', miny)
        FreeCAD.ActiveDocument.getObject(label).set('C5', maxz)
        FreeCAD.ActiveDocument.getObject(label).set('C6', minz)
        
        FreeCAD.ActiveDocument.getObject(label).mergeCells('A1:A6')
        FreeCAD.ActiveDocument.getObject(label).setBackground('A1:C6', (1.000000,1.000000,0.000000))
        
        FreeCAD.ActiveDocument.getObject(label).set('A8', 'ORIENTATION INFORMATION:')
        FreeCAD.ActiveDocument.getObject(label).set('B8', 'Max yaw [deg]:')
        FreeCAD.ActiveDocument.getObject(label).set('B9', 'Min yaw [deg]:')
        FreeCAD.ActiveDocument.getObject(label).set('B10', 'Max pitch [deg]:')
        FreeCAD.ActiveDocument.getObject(label).set('B11', 'Min pitch [deg]:')
        FreeCAD.ActiveDocument.getObject(label).set('B12', 'Max roll [deg]:')
        FreeCAD.ActiveDocument.getObject(label).set('B13', 'Min roll [deg]:')
        
        FreeCAD.ActiveDocument.getObject(label).set('C8', maxEux)
        FreeCAD.ActiveDocument.getObject(label).set('C9', minEux)
        FreeCAD.ActiveDocument.getObject(label).set('C10', maxEuy)
        FreeCAD.ActiveDocument.getObject(label).set('C11', minEuy)
        FreeCAD.ActiveDocument.getObject(label).set('C12', maxEuz)
        FreeCAD.ActiveDocument.getObject(label).set('C13', minEuz)	
        FreeCAD.ActiveDocument.getObject(label).mergeCells('A8:A13')
        FreeCAD.ActiveDocument.getObject(label).setBackground('A8:C13', (1.000000,1.000000,0.000000))

        FreeCAD.ActiveDocument.getObject(label).set('E1', 'SPEED INFORMATION:')
        FreeCAD.ActiveDocument.getObject(label).set('F1', 'max x speed [m/s]:')
        FreeCAD.ActiveDocument.getObject(label).set('F2', 'min x speed [m/s]:')
        FreeCAD.ActiveDocument.getObject(label).set('F3', 'max y speed [m/s]:')
        FreeCAD.ActiveDocument.getObject(label).set('F4', 'min y speed [m/s]:')
        FreeCAD.ActiveDocument.getObject(label).set('F5', 'max z speed [m/s]:')
        FreeCAD.ActiveDocument.getObject(label).set('F6', 'min z speed [m/s]:')

        FreeCAD.ActiveDocument.getObject(label).set('G1', maxVx)
        FreeCAD.ActiveDocument.getObject(label).set('G2', minVx)
        FreeCAD.ActiveDocument.getObject(label).set('G3', maxVy)
        FreeCAD.ActiveDocument.getObject(label).set('G4', minVy)
        FreeCAD.ActiveDocument.getObject(label).set('G5', maxVz)
        FreeCAD.ActiveDocument.getObject(label).set('G6', minVz)
        
        FreeCAD.ActiveDocument.getObject(label).mergeCells('E1:E6')
        FreeCAD.ActiveDocument.getObject(label).setBackground('E1:G6', (1.000000,1.000000,0.000000))
        
        FreeCAD.ActiveDocument.getObject(label).set('E8', 'ANGULAR VELOCITY INFORMATION:')
        FreeCAD.ActiveDocument.getObject(label).set('F8', 'max x angular velocity [rad/s]:')
        FreeCAD.ActiveDocument.getObject(label).set('F9', 'min x angular velocity [rad/s]:')
        FreeCAD.ActiveDocument.getObject(label).set('F10', 'max y angular velocity [rad/s]')
        FreeCAD.ActiveDocument.getObject(label).set('F11', 'min y angular velocity [rad/s]')
        FreeCAD.ActiveDocument.getObject(label).set('F12', 'max z angular velocity [rad/s]')
        FreeCAD.ActiveDocument.getObject(label).set('F13', 'min z angular velocity [rad/s]')
        
        FreeCAD.ActiveDocument.getObject(label).set('G8', maxWx)
        FreeCAD.ActiveDocument.getObject(label).set('G9', minWx)
        FreeCAD.ActiveDocument.getObject(label).set('G10', maxWy)
        FreeCAD.ActiveDocument.getObject(label).set('G11', minWy)
        FreeCAD.ActiveDocument.getObject(label).set('G12', maxWz)
        FreeCAD.ActiveDocument.getObject(label).set('G13', minWz)	
        FreeCAD.ActiveDocument.getObject(label).mergeCells('E8:E13')
        FreeCAD.ActiveDocument.getObject(label).setBackground('E8:G13', (1.000000,1.000000,0.000000))

        FreeCAD.ActiveDocument.getObject(label).setColumnWidth('A', 210)
        FreeCAD.ActiveDocument.getObject(label).setColumnWidth('B', 135)
        FreeCAD.ActiveDocument.getObject(label).setColumnWidth('C', 144)
        FreeCAD.ActiveDocument.getObject(label).setColumnWidth('E', 210)
        FreeCAD.ActiveDocument.getObject(label).setColumnWidth('F', 200)
        FreeCAD.ActiveDocument.getObject(label).setColumnWidth('G', 144)
        
        FreeCAD.ActiveDocument.recompute() 

class Infojoint:  
    def __init__(self, bodynumber):
        label = "minimum_reaction_info_joint_"+str(bodynumber)	
        InitialTime = float(FreeCAD.ActiveDocument.getObject("MBDyn").initial_time[:-2])
        FinalTime = float(FreeCAD.ActiveDocument.getObject("MBDyn").final_time[:-2])
        data = np.genfromtxt(__dir__ + '/MBDynCase.jnt', delimiter=' ',  usecols=(0,1,2,3,4,5,6,7,8,9,10,11,12))#Joints data       
        fx,fy,fz = [],[],[]#Components of the reaction force in a local frame: 
        tfx,tfy,tfz = '0','0','0'#Times when the maximum forces occur
        tx,ty,tz = [],[],[]#Components of the reaction couple (torque) in a local frame:
        f1x,f1y,f1z = [],[],[]#Components of the reaction force in the global frame:
        t1x,t1y,t1z = [],[],[]#Components of the reaction couple (torque) in the global frame:

        for row in data:
            if(row[0]==bodynumber):
                fx.append(row[2])
                fy.append(row[1])
                fz.append(row[3])
                tx.append(row[4])
                ty.append(row[5])
                tz.append(row[6])
                f1x.append(row[7])
                f1y.append(row[8])
                f1z.append(row[9])
                t1x.append(row[10])
                t1y.append(row[11])
                t1z.append(row[12])
                
        time = np.linspace(InitialTime,FinalTime,len(fx))
        
        maxfx = str(max(fx))
        minfx = str(min(fx))       
        maxfy = str(max(fy))
        minfy = str(min(fy))      
        maxfz = str(max(fz))
        minfz = str(min(fz))     

        maxtx = str(max(tx))
        mintx = str(min(tx))
        maxty = str(max(ty))
        minty = str(min(ty))
        maxtz = str(max(tz))
        mintz = str(min(tz))

        maxf1x = str(max(f1x))
        minf1x = str(min(f1x))       
        maxf1y = str(max(f1y))
        minf1y = str(min(f1y))      
        maxf1z = str(max(f1z))
        minf1z = str(min(f1z))     

        maxt1x = str(max(t1x))
        mint1x = str(min(t1x))
        maxt1y = str(max(t1y))
        mint1y = str(min(t1y))
        maxt1z = str(max(t1z))
        mint1z = str(min(t1z))
        
        tfx = str(time[fx.index(float(maxfx))])
        tfy = str(time[fy.index(float(maxfy))])
        tfz = str(time[fz.index(float(maxfz))])

        FreeCAD.ActiveDocument.addObject('Spreadsheet::Sheet',label)

        FreeCAD.ActiveDocument.getObject(label).set('A2', 'LOCAL FRAME REACTION FORCE INFORMATION:')
        FreeCAD.ActiveDocument.getObject(label).set('B2', 'max x reaction force [N]:')
        FreeCAD.ActiveDocument.getObject(label).set('B3', 'min x reaction force [N]:')
        FreeCAD.ActiveDocument.getObject(label).set('B4', 'max y reaction force [N]:')
        FreeCAD.ActiveDocument.getObject(label).set('B5', 'min y reaction force [N]:')
        FreeCAD.ActiveDocument.getObject(label).set('B6', 'max z reaction force [N]:')
        FreeCAD.ActiveDocument.getObject(label).set('B7', 'min z reaction force [N]:')

        FreeCAD.ActiveDocument.getObject(label).set('C2', maxfx)
        FreeCAD.ActiveDocument.getObject(label).set('C3', minfx)
        FreeCAD.ActiveDocument.getObject(label).set('C4', maxfy)
        FreeCAD.ActiveDocument.getObject(label).set('C5', minfy)
        FreeCAD.ActiveDocument.getObject(label).set('C6', maxfz)
        FreeCAD.ActiveDocument.getObject(label).set('C7', minfz)
	
        FreeCAD.ActiveDocument.getObject(label).mergeCells('A2:A7')
        FreeCAD.ActiveDocument.getObject(label).setBackground('A2:C7', (1.000000,1.000000,0.000000))

        FreeCAD.ActiveDocument.getObject(label).set('A9', 'LOCAL FRAME REACTION TORQUE INFORMATION:')
        FreeCAD.ActiveDocument.getObject(label).set('B9', 'max x local reaction torque [N*m]')
        FreeCAD.ActiveDocument.getObject(label).set('B10', 'min x local reaction torque [N*m]')
        FreeCAD.ActiveDocument.getObject(label).set('B11', 'max y local reaction torque [N*m]')
        FreeCAD.ActiveDocument.getObject(label).set('B12', 'min y local reaction torque [N*m]')
        FreeCAD.ActiveDocument.getObject(label).set('B13', 'max z local reaction torque [N*m]')
        FreeCAD.ActiveDocument.getObject(label).set('B14', 'min z local reaction torque [N*m]')

        FreeCAD.ActiveDocument.getObject(label).set('C9', maxtx)
        FreeCAD.ActiveDocument.getObject(label).set('C10', mintx)
        FreeCAD.ActiveDocument.getObject(label).set('C11', maxty)
        FreeCAD.ActiveDocument.getObject(label).set('C12', minty)
        FreeCAD.ActiveDocument.getObject(label).set('C13', maxtz)
        FreeCAD.ActiveDocument.getObject(label).set('C14', mintz)	
        FreeCAD.ActiveDocument.getObject(label).mergeCells('A9:A14')
        FreeCAD.ActiveDocument.getObject(label).setBackground('A9:C14', (1.000000,1.000000,0.000000))

        FreeCAD.ActiveDocument.getObject(label).set('E2', 'GLOBAL FRAME REACTION FORCE INFORMATION:')
        FreeCAD.ActiveDocument.getObject(label).set('F2', 'max x reaction force [N]:')
        FreeCAD.ActiveDocument.getObject(label).set('F3', 'min x reaction force [N]:')
        FreeCAD.ActiveDocument.getObject(label).set('F4', 'max y reaction force [N]:')
        FreeCAD.ActiveDocument.getObject(label).set('F5', 'min y reaction force [N]:')
        FreeCAD.ActiveDocument.getObject(label).set('F6', 'max z reaction force [N]:')
        FreeCAD.ActiveDocument.getObject(label).set('F7', 'min z reaction force [N]:')

        FreeCAD.ActiveDocument.getObject(label).set('G2', maxf1x)
        FreeCAD.ActiveDocument.getObject(label).set('G3', minf1x)
        FreeCAD.ActiveDocument.getObject(label).set('G4', maxf1y)
        FreeCAD.ActiveDocument.getObject(label).set('G5', minf1y)
        FreeCAD.ActiveDocument.getObject(label).set('G6', maxf1z)
        FreeCAD.ActiveDocument.getObject(label).set('G7', minf1z)
	
        FreeCAD.ActiveDocument.getObject(label).mergeCells('E2:E7')
        FreeCAD.ActiveDocument.getObject(label).setBackground('E2:G7', (1.000000,1.000000,0.000000))

        FreeCAD.ActiveDocument.getObject(label).set('E9', 'GLOBAL FRAME REACTION TORQUE INFORMATION:')
        FreeCAD.ActiveDocument.getObject(label).set('F9', 'max x global reaction torque [N*m]')
        FreeCAD.ActiveDocument.getObject(label).set('F10', 'min x global reaction torque [N*m]')
        FreeCAD.ActiveDocument.getObject(label).set('F11', 'max y global reaction torque [N*m]')
        FreeCAD.ActiveDocument.getObject(label).set('F12', 'min y global reaction torque [N*m]')
        FreeCAD.ActiveDocument.getObject(label).set('F13', 'max z global reaction torque [N*m]')
        FreeCAD.ActiveDocument.getObject(label).set('F14', 'min z global reaction torque [N*m]')

        FreeCAD.ActiveDocument.getObject(label).set('G9', maxt1x)
        FreeCAD.ActiveDocument.getObject(label).set('G10', mint1x)
        FreeCAD.ActiveDocument.getObject(label).set('G11', maxt1y)
        FreeCAD.ActiveDocument.getObject(label).set('G12', mint1y)
        FreeCAD.ActiveDocument.getObject(label).set('G13', maxt1z)
        FreeCAD.ActiveDocument.getObject(label).set('G14', mint1z)	
        FreeCAD.ActiveDocument.getObject(label).mergeCells('E9:E14')
        FreeCAD.ActiveDocument.getObject(label).setBackground('E9:G14', (1.000000,1.000000,0.000000))
        
        FreeCAD.ActiveDocument.getObject(label).set('D1', 'Time [s]')
        FreeCAD.ActiveDocument.getObject(label).set('D2', tfx)
        FreeCAD.ActiveDocument.getObject(label).set('D4', tfy)
        FreeCAD.ActiveDocument.getObject(label).set('D6', tfz)

        FreeCAD.ActiveDocument.getObject(label).setColumnWidth('A', 210)
        FreeCAD.ActiveDocument.getObject(label).setColumnWidth('B', 255)
        FreeCAD.ActiveDocument.getObject(label).setColumnWidth('C', 144)
        FreeCAD.ActiveDocument.getObject(label).setColumnWidth('E', 210)
        FreeCAD.ActiveDocument.getObject(label).setColumnWidth('F', 240)
        FreeCAD.ActiveDocument.getObject(label).setColumnWidth('G', 144)

        FreeCAD.ActiveDocument.recompute()         
