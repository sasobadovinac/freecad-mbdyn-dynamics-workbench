# -*- coding: utf-8 -*-
import FreeCAD
import numpy as np
#import os
#__dir__ = os.path.dirname(__file__)

import tempfile

__dir__ = tempfile.gettempdir()

class Tospreadsheet:  
    def __init__(self, obj):
        data = np.genfromtxt(__dir__ + '/MBDynCase.mov', delimiter=' ')
        InitialTime = float(FreeCAD.ActiveDocument.getObject('MBDyn').initial_time[:-2])
        FinalTime = float(FreeCAD.ActiveDocument.getObject('MBDyn').final_time[:-2]) 
        if(obj.Label.startswith('structural:')):  
            label = "MBDyn_node_"+str(obj.label)
            data = np.genfromtxt(__dir__ + '/MBDynCase.mov', delimiter=' ')
            x,y,z = [],[],[]
            Eux,Euy,Euz = [],[],[]
            Vx,Vy,Vz = [],[],[]    
            Wx,Wy,Wz = [],[],[]
            for row in data:
                if(row[0]==int(obj.label)):
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
            
            FreeCAD.ActiveDocument.addObject('Spreadsheet::Sheet',label)
    
            sheet = FreeCAD.ActiveDocument.getObject(label)
    
            sheet.set('A1', 'time [s]')
            sheet.set('B1', 'x possition [m]')
            sheet.set('C1', 'y possition [m]')
            sheet.set('D1', 'z possition [m]')
            sheet.set('E1', 'Yaw [deg]')
            sheet.set('F1', 'Pitch [deg]')
            sheet.set('G1', 'Roll [deg]')
            sheet.set('H1', 'x speed [m/s]')
            sheet.set('I1', 'y speed [m/s]')
            sheet.set('J1', 'z speed [m/s]')
            sheet.set('K1', 'x angular speed [rad/s]')
            sheet.set('L1', 'y angular speed [rad/s]')
            sheet.set('M1', 'z angular speed [rad/s]')
                
            for j in range(1, len(x)):
                sheet.set('A'+str(j+1), str(time[j]))
                sheet.set('B'+str(j+1), str(x[j]))
                sheet.set('C'+str(j+1), str(y[j]))
                sheet.set('D'+str(j+1), str(z[j]))
                sheet.set('E'+str(j+1), str(Eux[j]))
                sheet.set('F'+str(j+1), str(Euy[j]))
                sheet.set('G'+str(j+1), str(Euz[j]))
                sheet.set('H'+str(j+1), str(Vx[j]))
                sheet.set('I'+str(j+1), str(Vy[j]))
                sheet.set('J'+str(j+1), str(Vz[j]))
                sheet.set('K'+str(j+1), str(Wx[j]))
                sheet.set('L'+str(j+1), str(Wy[j]))
                sheet.set('M'+str(j+1), str(Wz[j]))
            
        if(obj.Label.startswith('joint:')):  
            label = "MBDyn_joint_"+str(obj.label)
            data = np.genfromtxt(__dir__ + '/MBDynCase.jnt', delimiter=' ',  usecols=(0,1,2,3,4,5,6,7,8,9,10,11,12))
            fx,fy,fz = [],[],[]
            tx,ty,tz = [],[],[]
            ffx,ffy,ffz = [],[],[]    
            ttx,tty,ttz = [],[],[]
            for row in data:
                if(row[0]==int(obj.label)):
                    fx.append(row[1])
                    fy.append(row[2])
                    fz.append(row[3])
                    tx.append(row[4])
                    ty.append(row[5])
                    tz.append(row[6])
                    ffx.append(row[7])
                    ffy.append(row[8])
                    ffz.append(row[9])
                    ttx.append(row[10])
                    tty.append(row[11])
                    ttz.append(row[12])

            time = np.linspace(InitialTime,FinalTime,len(fx))        
    
            FreeCAD.ActiveDocument.addObject('Spreadsheet::Sheet',label)
    
            sheet = FreeCAD.ActiveDocument.getObject(label)
    
            sheet.set('A1', 'time [s]')
            sheet.set('B1', 'x local reaction force [N]')
            sheet.set('C1', 'y local reaction force [N]')
            sheet.set('D1', 'z local reaction force [N]')
            sheet.set('E1', 'x local reaction torque [N*m]')
            sheet.set('F1', 'y local reaction torque [N*m]')
            sheet.set('G1', 'z local reaction torque [N*m]')
            sheet.set('H1', 'x global reaction force [N]')
            sheet.set('I1', 'y global reaction force [N]')
            sheet.set('J1', 'z global reaction force [N]')
            sheet.set('K1', 'x global reaction torque [N*m]')
            sheet.set('L1', 'y global reaction torque [N*m]')
            sheet.set('M1', 'z global reaction torque [N*m]')
                
            for j in range(1, len(fx)):
                sheet.set('A'+str(j+1), str(time[j]))
                sheet.set('B'+str(j+1), str(fx[j]))
                sheet.set('C'+str(j+1), str(fy[j]))
                sheet.set('D'+str(j+1), str(fz[j]))
                sheet.set('E'+str(j+1), str(tx[j]))
                sheet.set('F'+str(j+1), str(ty[j]))
                sheet.set('G'+str(j+1), str(tz[j]))
                sheet.set('H'+str(j+1), str(ffx[j]))
                sheet.set('I'+str(j+1), str(ffy[j]))
                sheet.set('J'+str(j+1), str(ffz[j]))
                sheet.set('K'+str(j+1), str(ttx[j]))
                sheet.set('L'+str(j+1), str(tty[j]))
                sheet.set('M'+str(j+1), str(ttz[j]))    
                
        FreeCAD.ActiveDocument.recompute()        
