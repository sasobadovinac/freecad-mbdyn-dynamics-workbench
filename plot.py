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
There are two classes in this file. 
The first class implements functions used to plot node's simulation results. 
The second class implements functions to plot joint's simulation results.
'''
import FreeCAD
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
#import os
import tempfile

__dir__ = tempfile.gettempdir()
#__dir__ = os.path.dirname(__file__)
#///////////////////////////////////////////////THIS CLASS PLOTS NODE'S INFORMATION. COULD BE A DYNAMIC OR A DUMMY NODE, BUT NOT A STATIC NODE, BECAUSE STATIC NODES DO NOT OWN DEGREES OF FREEDOM///////////////////////////////////////////////////
class Plotnode:  
    def __init__(self, nodenumber, expression):
        #Retrieve the simulation paarmeters required by the plots
        InitialTime = float(FreeCAD.ActiveDocument.getObject("MBDyn").initial_time[:-2])
        FinalTime = float(FreeCAD.ActiveDocument.getObject("MBDyn").final_time[:-2])
        #Retrieve the data from the .mov file 
        data = np.genfromtxt(__dir__ + '/MBDynCase.mov', delimiter=' ')
        #Precission variable is used to round the numbers, to save ram memory when plotting large simulations
        precission = int(FreeCAD.ActiveDocument.getObjectsByLabel('MBDyn')[0].precision)
        #Vectors to store position
        x = []
        y = []
        z = []
        #Vectors to store orientation (Euler angles)
        Eux = []
        Euy = []
        Euz = []
        #Vectors to store velocity
        Vx = []
        Vy = []
        Vz = []
        #Vectors to store angular velocity
        Wx = []
        Wy = []
        Wz = []
        #Retrieve the data from the .mov file
        for row in data:
            if(row[0]==nodenumber):
                x.append(round(row[1],precission))
                y.append(round(row[2],precission))
                z.append(round(row[3],precission))
                Eux.append(round(row[6],precission))
                Euy.append(round(row[5],precission))
                Euz.append(round(row[4],precission))
                Vx.append(round(row[7],precission))
                Vy.append(round(row[8],precission))
                Vz.append(round(row[9],precission))
                Wx.append(round(row[10],precission))
                Wy.append(round(row[11],precission))
                Wz.append(round(row[12],precission))
        #Create a time vector to plot
        time = np.linspace(InitialTime,FinalTime,len(x))  
        
 #///////////////////////////////////////////////POSITION (P)///////////////////////////////////////////////////
            
#Position components (x,y,z) as function of time (t):

        if (expression == 'Px(t)'):
            fig = plt.figure()
            plt.plot(time,x,label='Px(t)',color='red')
            plt.ylabel('Px[m]')
            plt.xlabel('t[s]')
            plt.legend()            
            plt.grid()
            plt.suptitle('X global position component as function of time. Node: '+ str(nodenumber))
            plt.show()

        if (expression == 'Py(t)'):
            fig = plt.figure()
            plt.plot(time,y,label='Py(t)',color='green')
            plt.ylabel('Py[m]')
            plt.xlabel('t[s]')
            plt.legend()
            plt.grid()
            plt.suptitle('Y global position component as function of time. Node: '+ str(nodenumber))
            plt.show() 

        if (expression == 'Pz(t)'):
            fig = plt.figure()
            plt.plot(time,z,label='Pz(t)',color='blue')
            plt.ylabel('Pz[m]')
            plt.xlabel('t[s]')
            plt.legend()
            plt.grid()
            plt.suptitle('Z global position component as function of time. Node: '+ str(nodenumber))
            plt.show() 

#Planar position:

        if (expression == 'Py(Px)'):
            fig = plt.figure()
            plt.plot(x,y,label='Py(Px)',color='black')
            plt.ylabel('Py[m]')
            plt.xlabel('Px[m]')
            plt.legend()
            plt.grid()
            plt.suptitle('Y global position component as function of X global position component. Node: '+ str(nodenumber))
            plt.show() 
            
        if (expression == 'Px(Py)'):
            fig = plt.figure()
            plt.plot(y,x,label='Px(Py)',color='black')
            plt.ylabel('Px[m]')
            plt.xlabel('Py[m]')            
            plt.legend()
            plt.grid()
            plt.suptitle('X global position component as function of Y global position component. Node: '+ str(nodenumber))
            plt.show() 
            
        if (expression == 'Pz(Px)'):
            fig = plt.figure()
            plt.plot(x,z,label='Pz(Px)',color='black')
            plt.ylabel('Pz[m]')
            plt.xlabel('Px[m]')
            plt.legend()
            plt.grid()
            plt.suptitle('Z global position component as function of X global position component. Node: '+ str(nodenumber))
            plt.show() 

        if (expression == 'Px(Pz)'):
            fig = plt.figure()
            plt.plot(z,x,label='Pz(Px)',color='black')
            plt.ylabel('Px[m]')
            plt.xlabel('Pz[m]')
            plt.legend()
            plt.grid()
            plt.suptitle('X global position component as function of Z global position component. Node: '+ str(nodenumber))
            plt.show() 

        if (expression == 'Py(Pz)'):
            fig = plt.figure()
            plt.plot(z,y,label='Py(Pz)',color='black')
            plt.ylabel('Py[m]')
            plt.xlabel('Pz[m]')
            plt.legend()
            plt.grid()
            plt.suptitle('Y global position component as function of Z global position component. Node: '+ str(nodenumber))
            plt.show() 

        if (expression == 'Pz(Py)'):
            fig = plt.figure()
            plt.plot(y,z,label='Pz(Py)',color='black')
            plt.ylabel('Pz[m]')
            plt.xlabel('Py[m]')
            plt.legend()
            plt.grid()
            plt.suptitle('Z global position component as function of Y global position component. Node: '+ str(nodenumber))
            plt.show() 
            
#All the position componets as function of time:
        
        if (expression == 'P(t)'):
            fig = plt.figure()
            plt.plot(time,x,label='Px',color='red')
            plt.plot(time,y,label='Py',color='green')
            plt.plot(time,z,label='Pz',color='blue')
            plt.ylabel('P[m]')
            plt.xlabel('t[s]')
            plt.legend()
            plt.grid()
            plt.suptitle('Global position as function of time. Node: '+ str(nodenumber))
            plt.show() 

#All the position cmponets in a 3D plot:
            
        if (expression == 'P3D'):
            fig = plt.figure()
            ax = fig.gca(projection='3d')
            ax.plot(x, y, z, label='Px,Py,Pz')
            ax.legend()            
            ax.set_xlabel('x[m]')
            ax.set_ylabel('y[m]')
            ax.set_zlabel('z[m]')
            plt.legend()
            plt.grid()
            plt.suptitle('Global 3D trajectory. Node: '+ str(nodenumber))
            plt.show() 
            
#///////////////////////////////////////////////VELOCITY(V)///////////////////////////////////////////////////

#Velocity as function of time:

        if (expression == 'Vx(t)'):
            fig = plt.figure()
            plt.plot(time,Vx,label='Vx(t)',color='red')
            plt.ylabel('Vx[m/s]')
            plt.xlabel('t[s]')
            plt.legend()
            plt.grid()
            plt.suptitle('X global velocity component as function of time. Node: '+ str(nodenumber))
            plt.show() 

        if (expression == 'Vy(t)'):
            fig = plt.figure()
            plt.plot(time,Vy,label='Vy(t)',color='green')
            plt.ylabel('Vy[m/s]')
            plt.xlabel('t[s]')
            plt.legend()
            plt.grid()
            plt.suptitle('Y global velocity component as function of time. Node: '+ str(nodenumber))
            plt.show() 

        if (expression == 'Vz(t)'):
            fig = plt.figure()
            plt.plot(time,Vz,label='Vz(t)',color='blue')
            plt.ylabel('Vz[m/s]')
            plt.xlabel('t[s]')
            plt.legend()
            plt.grid()
            plt.suptitle('Z global velocity component as function of time. Node: '+ str(nodenumber))
            plt.show() 

#Planar velocity:

        if (expression == 'Vy(Vx)'):
            fig = plt.figure()
            plt.plot(Vx,Vy,label='Vy(Vx)',color='black')
            plt.ylabel('Vy[m]')
            plt.xlabel('Vx[m]')
            plt.legend()
            plt.grid()
            plt.suptitle('Y global velocity component as function of X global velocity component. Node: '+ str(nodenumber))
            plt.show() 

        if (expression == 'Vx(Vy)'):
            fig = plt.figure()
            plt.plot(Vy,Vx,label='Vx(Vy)',color='black')
            plt.ylabel('Vx[m]')
            plt.xlabel('Vy[m]')
            plt.legend()
            plt.grid()
            plt.suptitle('X global velocity component as function of Y global velocity component. Node: '+ str(nodenumber))
            plt.show() 
            
        if (expression == 'Vz(Vx)'):
            fig = plt.figure()
            plt.plot(Vx,Vz,label='Vz(Vx)',color='black')
            plt.ylabel('Vz[m]')
            plt.xlabel('Vx[m]')
            plt.legend()
            plt.grid()
            plt.suptitle('Z global velocity component as function of X global velocity component. Node: '+ str(nodenumber))
            plt.show() 

        if (expression == 'Vx(Vz)'):
            fig = plt.figure()
            plt.plot(Vz,Vx,label='Vx(Vz)',color='black')
            plt.ylabel('Vx[m]')
            plt.xlabel('Vz[m]')
            plt.legend()
            plt.grid()
            plt.suptitle('X global velocity component as function of Z global velocity component. Node: '+ str(nodenumber))
            plt.show() 

        if (expression == 'Vy(Vz)'):
            fig = plt.figure()
            plt.plot(Vz,Vy,label='Vy(Vz)',color='black')
            plt.ylabel('Vy[m]')
            plt.xlabel('Vz[m]')            
            plt.legend()
            plt.grid()
            plt.suptitle('Y global velocity component as function of Z global velocity component. Node: '+ str(nodenumber))
            plt.show() 
            
        if (expression == 'Vz(Vy)'):
            fig = plt.figure()
            plt.plot(Vy,Vz,label='Vz(Vy)',color='black')
            plt.ylabel('Vz[m]')
            plt.xlabel('Vy[m]')            
            plt.legend()
            plt.grid()
            plt.suptitle('Z global velocity component as function of Y global velocity component. Node: '+ str(nodenumber))
            plt.show() 

#All the velocities:
        
        if (expression == 'V(t)'):
            fig = plt.figure()
            plt.plot(time,Vx,label='Vx',color='red')
            plt.plot(time,Vy,label='Vy',color='green')
            plt.plot(time,Vz,label='Vz',color='blue')
            plt.ylabel('V[m/s]')
            plt.xlabel('t[s]')
            plt.legend()
            plt.grid()
            plt.suptitle('Global velocity as function of time. Node: '+ str(nodenumber))
            plt.show() 

#All the velocities in 3D:
            
        if (expression == 'V3D'):
            fig = plt.figure()
            ax = fig.gca(projection='3d')
            ax.plot(Vx, Vy, Vz, label='Vx,Vy,Vz')
            ax.legend()            
            ax.set_xlabel('Vx[m]')
            ax.set_ylabel('Vy[m]')
            ax.set_zlabel('Vz[m]')
            plt.legend()
            plt.grid()
            plt.suptitle('Global 3D velocity. Node: '+ str(nodenumber))
            plt.show()               
            
#///////////////////////////////////////////////ANGULAR VELOCITY (W)///////////////////////////////////////////////////
        
#Angular velocity as function of time:
        
        if (expression == 'Wx(t)'):
            fig = plt.figure()
            plt.plot(time,Wx,label='Wx(t)',color='red')
            plt.ylabel('Wx[rad/s]')
            plt.xlabel('t[s]')
            plt.legend()
            plt.grid()
            plt.suptitle('X global angular velocity component as function of time. Node: '+ str(nodenumber))
            plt.show() 

        if (expression == 'Wy(t)'):
            fig = plt.figure()
            plt.plot(time,Wy,label='Wy(t)',color='green')
            plt.ylabel('Wy[rad/s]')
            plt.xlabel('t[s]')
            plt.legend()
            plt.grid()
            plt.suptitle('Y global angular velocity component as function of time. Node: '+ str(nodenumber))
            plt.show() 

        if (expression == 'Wz(t)'):
            fig = plt.figure()
            plt.plot(time,Wz,label='Wz(t)',color='blue')
            plt.ylabel('Wz[rad/s]')
            plt.xlabel('t[s]')
            plt.legend()
            plt.grid()
            plt.suptitle('Z global angular velocity component as function of time. Node: '+ str(nodenumber))
            plt.show() 
 
#Planar angular velocity:

        if (expression == 'Wy(Wx)'):
            fig = plt.figure()
            plt.plot(Wx,Wy,label='Wy(Wx)',color='black')
            plt.ylabel('Wy[m]')
            plt.xlabel('Wx[m]')
            plt.legend()
            plt.grid()
            plt.suptitle('Y global angular velocity component as function of X global angular velocity component. Node: '+ str(nodenumber))
            plt.show() 

        if (expression == 'Wx(Wy)'):
            fig = plt.figure()
            plt.plot(Vy,Vx,label='Wx(Wy)',color='black')
            plt.ylabel('Wx[m]')
            plt.xlabel('Wy[m]')
            plt.legend()
            plt.grid()
            plt.suptitle('X global angular velocity component as function of Y global angular velocity component. Node: '+ str(nodenumber))
            plt.show() 
            
        if (expression == 'Wz(Wx)'):
            fig = plt.figure()
            plt.plot(Wx,Wz,label='Wz(Wx)',color='black')
            plt.ylabel('Wz[m]')
            plt.xlabel('wx[m]')
            plt.legend()
            plt.grid()
            plt.suptitle('Z global angular velocity component as function of X global angular velocity component. Node: '+ str(nodenumber))
            plt.show() 

        if (expression == 'Wx(Wz)'):
            fig = plt.figure()
            plt.plot(Wz,Wx,label='Wx(Wz)',color='black')
            plt.ylabel('Wx[m]')
            plt.xlabel('Wz[m]')
            plt.legend()
            plt.grid()
            plt.suptitle('X global angular velocity component as function of Z global angular velocity component. Node: '+ str(nodenumber))
            plt.show() 

        if (expression == 'Wy(Wz)'):
            fig = plt.figure()
            plt.plot(Wz,Wy,label='Wy(Wz)',color='black')
            plt.ylabel('Wy[m]')
            plt.xlabel('Wz[m]')            
            plt.legend()
            plt.grid()
            plt.suptitle('Y global angular velocity component as function of Z global angular velocity component. Node: '+ str(nodenumber))
            plt.show() 
            
        if (expression == 'Wz(Wy)'):
            fig = plt.figure()
            plt.plot(Wy,Wz,label='Wy(Wz)',color='black')
            plt.ylabel('Wz[m]')
            plt.xlabel('Wy[m]')            
            plt.legend()
            plt.grid()
            plt.suptitle('Z global angular velocity component as function of Y global angular velocity component. Node: '+ str(nodenumber))
            plt.show() 
         
#All the angular velocities in a single plot: 
            
        if (expression == 'W(t)'):
            fig = plt.figure()
            plt.plot(time,Wx,label='Wx',color='red')
            plt.plot(time,Wy,label='Wy',color='green')
            plt.plot(time,Wz,label='Wz',color='blue')
            plt.ylabel('W[rad/s]')
            plt.xlabel('t[s]')
            plt.legend()
            plt.grid()
            plt.suptitle('Global angular velocity as function of time. Node: '+ str(nodenumber))
            plt.show() 

#All the angular velocities in 3D:
            
        if (expression == 'W3D'):
            fig = plt.figure()
            ax = fig.gca(projection='3d')
            ax.plot(Wx, Wy, Wz, label='Wx,Wy,Wz')
            ax.legend()            
            ax.set_xlabel('Wx[m]')
            ax.set_ylabel('Wy[m]')
            ax.set_zlabel('Wz[m]')
            plt.legend()
            plt.grid()
            plt.suptitle('Global 3D angular velocity. Node: '+ str(nodenumber))
            plt.show()
            
#///////////////////////////////////////////////ORIENTATION (O)///////////////////////////////////////////////////
            
#Oientations as function of time:

        if (expression == 'yaw(t)'):
            fig = plt.figure()
            plt.plot(time,Euz,label='yaw(t)')
            plt.ylabel('yaw[deg]')
            plt.xlabel('t[s]')
            plt.legend()
            plt.grid()
            plt.suptitle('Global yaw as function of time. Node: '+ str(nodenumber))
            plt.show() 

        if (expression == 'pitch(t)'):
            fig = plt.figure()
            plt.plot(time,Euy,label='pitch(t)')
            plt.ylabel('pitch[deg]')
            plt.xlabel('t[s]')
            plt.legend()
            plt.grid()
            plt.suptitle('Global pitch as function of time. Node: '+ str(nodenumber))
            plt.show() 
            
        if (expression == 'roll(t)'):
            fig = plt.figure()
            plt.plot(time,Eux,label='roll(t)')
            plt.ylabel('roll[deg]')
            plt.xlabel('t[s]')
            plt.legend()
            plt.grid()
            plt.suptitle('Global roll as function of time. Node: '+ str(nodenumber))
            plt.show() 
            
#Planar orientation:

        if (expression == 'yaw(pitch)'):
            fig = plt.figure()
            plt.plot(Euy,Euz,label='yaw(pitch)',color='black')
            plt.ylabel('yaw[deg]')
            plt.xlabel('pitch[deg]')
            plt.legend()
            plt.grid()
            plt.suptitle('Global yaw as function of absolute pitch. Node: '+ str(nodenumber))
            plt.show() 

        if (expression == 'pitch(yaw)'):
            fig = plt.figure()
            plt.plot(Euz,Euy,label='pitch(yaw)',color='black')
            plt.ylabel('pitch[deg]')
            plt.xlabel('way[deg]')
            plt.legend()
            plt.grid()
            plt.suptitle('Global pitch as function of absolute yaw. Node: '+ str(nodenumber))
            plt.show() 

        if (expression == 'roll(pitch)'):
            fig = plt.figure()
            plt.plot(Euy,Eux,label='roll(pitch)',color='black')
            plt.ylabel('roll[deg]')
            plt.xlabel('pitch[deg]')
            plt.legend()
            plt.grid()
            plt.suptitle('Global roll as function of absolute pitch. Node: '+ str(nodenumber))
            plt.show() 

        if (expression == 'pitch(roll)'):
            fig = plt.figure()
            plt.plot(Eux,Euy,label='pitch(roll)',color='black')
            plt.ylabel('pitch[deg]')
            plt.xlabel('roll[deg]')
            plt.legend()
            plt.grid()
            plt.suptitle('Global pitch as function of absolute roll. Node: '+ str(nodenumber))
            plt.show() 

        if (expression == 'yaw(roll)'):
            fig = plt.figure()
            plt.plot(Eux,Euz,label='yaw(roll)',color='black')
            plt.ylabel('yaw[deg]')
            plt.xlabel('roll[deg]')
            plt.legend()
            plt.grid()
            plt.suptitle('Global yaw as function of absolute roll. Node: '+ str(nodenumber))
            plt.show() 

        if (expression == 'roll(yaw)'):
            fig = plt.figure()
            plt.plot(Euz,Eux,label='roll(yaw)',color='black')
            plt.ylabel('roll[deg]')
            plt.xlabel('yaw[deg]')
            plt.legend()
            plt.grid()
            plt.suptitle('Global roll as function of absolute pitch. Node: '+ str(nodenumber))
            plt.show()
            
#All the orientations:
        
        if (expression == 'O(t)'):
            fig = plt.figure()
            plt.plot(time,Euz,label='yaw',color='blue')
            plt.plot(time,Euy,label='pitch',color='green')
            plt.plot(time,Eux,label='roll',color='red')
            plt.ylabel('angle[deg]')
            plt.xlabel('t[s]')
            plt.legend()
            plt.grid()
            plt.suptitle('Global orientation as function of time. Node: '+ str(nodenumber))            
            plt.show() 

#All the orientations in 3D:
            
        if (expression == 'O3D'):
            fig = plt.figure()
            ax = fig.gca(projection='3d')
            ax.plot(Eux, Euy, Euz, label='roll,pitch,way')
            ax.legend()            
            ax.set_xlabel('roll[deg]')
            ax.set_ylabel('pitch[deg]')
            ax.set_zlabel('yaw[deg]')
            plt.legend()
            plt.grid()
            plt.suptitle('Absolute 3D orientation. Node: '+ str(nodenumber))
            plt.show()        
 
#///////////////////////////////////////////////PLOTS EVERYTHING///////////////////////////////////////////////////
            
        if (expression == 'all'):
            fig = plt.figure()
            ax1 = fig.add_subplot(341)
            ax2 = fig.add_subplot(342)
            ax3 = fig.add_subplot(343)
            ax4 = fig.add_subplot(344)
            ax5 = fig.add_subplot(345)
            ax6 = fig.add_subplot(346)
            ax7 = fig.add_subplot(347)
            ax8 = fig.add_subplot(348)
            ax9 = fig.add_subplot(349)
            ax10 = fig.add_subplot(3,4,10)
            ax11 = fig.add_subplot(3,4,11)
            ax12 = fig.add_subplot(3,4,12)            
            ax1.plot(time,x)
            ax5.plot(time,y)
            ax9.plot(time,z)
            ax1.set_ylabel('x[m]')
            ax1.set_xlabel('t[s]')
            ax5.set_ylabel('y[m]')
            ax5.set_xlabel('t[s]')
            ax9.set_ylabel('z[m]')
            ax9.set_xlabel('t[s]')        
            ax2.plot(time,Eux)
            ax6.plot(time,Euy)
            ax10.plot(time,Euz)
            ax2.set_ylabel('yaw[deg]')
            ax2.set_xlabel('t[s]')
            ax6.set_ylabel('pithc[deg]')
            ax6.set_xlabel('t[s]')
            ax10.set_ylabel('roll[deg]')
            ax10.set_xlabel('t[s]')
            ax3.plot(time,Vx)
            ax7.plot(time,Vy)
            ax11.plot(time,Vz)
            ax3.set_ylabel('Vx[m/s]')
            ax3.set_xlabel('t[s]')
            ax7.set_ylabel('Vy[m/s]')
            ax7.set_xlabel('t[s]')
            ax11.set_ylabel('Vz[m/s]')
            ax11.set_xlabel('t[s]')
            ax4.plot(time,Wx)
            ax8.plot(time,Wy)
            ax12.plot(time,Wz)
            ax4.set_ylabel('Wx[rad/s]')
            ax4.set_xlabel('t[s]')
            ax8.set_ylabel('Wy[rad/s]')
            ax8.set_xlabel('t[s]')
            ax12.set_ylabel('Wz[rad/s]')
            ax12.set_xlabel('t[s]')
            plt.legend()
            plt.suptitle('Simulation results. Node: '+ str(nodenumber))
            plt.show() 
                    
#///////////////////////////////////////////////THIS CLASS PLOTS JOINT'S INFORMATION///////////////////////////////////////////////////       
        
class Plotjoint:  
    def __init__(self, jointnumber, expression):
        InitialTime = float(FreeCAD.ActiveDocument.getObject("MBDyn").initial_time[:-2])
        FinalTime = float(FreeCAD.ActiveDocument.getObject("MBDyn").final_time[:-2])
        data = np.genfromtxt(__dir__ + '/MBDynCase.jnt', delimiter=' ',  usecols=(0,1,2,3,4,5,6,7,8,9,10,11,12))#Joints data
        precission = int(FreeCAD.ActiveDocument.getObjectsByLabel('MBDyn')[0].precision)
        #Components of the reaction force in a local frame:        
        fx = []
        fy = []
        fz = []
        #Total reaction force in a local frame:        
        ft = []
        #Components of the reaction torque in a local frame:
        tx = []
        ty = []
        tz = []
        #Total reaction torque in a local frame:        
        tt = []
        #Components of the reaction force in the global frame:
        f1x = []
        f1y = []
        f1z = []
        #Total reaction force in a global frame:
        f1t = []        
        #Components of the reaction torque in the global frame:
        t1x = []
        t1y = []
        t1z = []
        #Total reaction torque in a global frame:
        tt1 = []
        
        for row in data:
            if(row[0]==jointnumber):
                #Restrieve local forces
                fx.append(round(row[1],precission))
                fy.append(round(row[2],precission))
                fz.append(round(row[3],precission))
                ft.append(pow(pow(round(row[1],precission),2)+pow(round(row[2],precission),2)+pow(round(row[3],precission),2),0.5))
                #Retrieve local torques
                tx.append(round(row[4],precission))
                ty.append(round(row[5],precission))
                tz.append(round(row[6],precission))
                tt.append(pow(pow(round(row[4],precission),2)+pow(round(row[5],precission),2)+pow(round(row[6],precission),2),0.5))
                #Retrieve global forces
                f1x.append(round(row[7],precission))
                f1y.append(round(row[8],precission))
                f1z.append(round(row[9],precission))
                f1t.append(pow(pow(round(row[7],precission),2)+pow(round(row[8],precission),2)+pow(round(row[9],precission),2),0.5))
                
                t1x.append(round(row[10],precission))
                t1y.append(round(row[11],precission))
                t1z.append(round(row[12],precission))
                tt1.append(pow(pow(round(row[10],precission),2)+pow(round(row[11],precission),2)+pow(round(row[12],precission),2),0.5))

        time = np.linspace(InitialTime,FinalTime,len(fx))

#/////////////////////////////////////////////////////FRORCE RELATIVE TO LOCAL REFERENCE FRAME (F)///////////////////////////////////////////

#Force components as function of time:

        if (expression == 'Fx(t)'):
            fig = plt.figure()
            plt.plot(time,fx,label='Fx(t)',color='red')
            plt.ylabel('Fx[N]')
            plt.xlabel('t[s]')
            plt.legend()
            plt.grid()
            plt.suptitle('X component of local reaction force as function of time. Joint: '+ str(jointnumber))
            plt.show() 

        if (expression == 'Fy(t)'):
            fig = plt.figure()
            plt.plot(time,fy,label='Fy(t)',color='green')
            plt.ylabel('Fy[N]')
            plt.xlabel('t[s]')
            plt.legend()
            plt.grid()
            plt.suptitle('Y component of local reaction force as function of time. Joint: '+ str(jointnumber))
            plt.show() 

        if (expression == 'Fz(t)'):
            fig = plt.figure()
            plt.plot(time,fz,label='Fz(t)',color='blue')
            plt.ylabel('Fz[N]')
            plt.xlabel('t[s]')
            plt.legend()
            plt.grid()
            plt.suptitle('Z component of local reaction force as function of time. Joint: '+ str(jointnumber))
            plt.show() 

#Planar forces:

        if (expression == 'Fy(Fx)'):
            fig = plt.figure()
            plt.plot(fx,fy,label='Fy(Fx)',color='black')
            plt.ylabel('Fy[N]')
            plt.xlabel('Fx[N]')
            plt.legend()
            plt.grid()
            plt.suptitle('Y component of local reaction force as function of X component of local reaction force. Joint: '+ str(jointnumber))
            plt.show() 

        if (expression == 'Fx(Fy)'):    
            fig = plt.figure()
            plt.plot(fy,fx,label='Fx(Fy)',color='black')
            plt.ylabel('Fx[N]')
            plt.xlabel('Fy[N]')
            plt.legend()
            plt.grid()
            plt.suptitle('X component of local reaction force as function of Y component of local reaction force. Joint: '+ str(jointnumber))
            plt.show() 
            
        if (expression == 'Fz(Fx)'):
            fig = plt.figure()
            plt.plot(fx,fz,label='Fz(Fx)',color='black')
            plt.ylabel('Fz[N]')
            plt.xlabel('Fx[N]')
            plt.legend()
            plt.grid()
            plt.suptitle('Z component of local reaction force as function of X component of local reaction force. Joint: '+ str(jointnumber))            
            plt.show() 

        if (expression == 'Fx(Fz)'):  
            fig = plt.figure()
            plt.plot(fz,fx,label='Fx(Fz)',color='black')
            plt.ylabel('Fx[N]')
            plt.xlabel('Fz[N]')
            plt.legend()
            plt.grid()
            plt.suptitle('X component of local reaction force as function of Z component of local reaction force. Joint: '+ str(jointnumber))
            plt.show() 

        if (expression == 'Fy(Fz)'):
            fig = plt.figure()
            plt.plot(fz,fy,label='Fy(Fz)',color='black')
            plt.ylabel('Fy[N]')
            plt.xlabel('Fz[N]')
            plt.legend()
            plt.grid()
            plt.suptitle('Y component of local reaction force as function of Z component of local reaction force. Joint: '+ str(jointnumber))
            plt.show() 

        if (expression == 'Fz(Fy)'):
            fig = plt.figure()
            plt.plot(fy,fz,label='Fz(Fy)',color='black')
            plt.ylabel('Fz[N]')
            plt.xlabel('Fy[N]')
            plt.legend()
            plt.grid()
            plt.suptitle('Z component of local reaction force as function of Y component of local reaction force. Joint: '+ str(jointnumber))
            plt.show() 

#All forces:
        
        if (expression == 'F(t)'):    
            fig = plt.figure()
            plt.plot(time,fx,label='fx',color='red')
            plt.plot(time,fy,label='fy',color='green')
            plt.plot(time,fz,label='fz',color='blue')
            plt.plot(time,ft,label='total',color='black')
            plt.ylabel('F[N]')
            plt.xlabel('t[s]')
            plt.legend()
            plt.grid()
            plt.suptitle('Local reaction force as function of time. Joint: '+ str(jointnumber))
            plt.show() 
            
        if (expression == 'F3D'):
            fig = plt.figure()
            ax = fig.gca(projection='3d')
            ax.plot(fx, fy, fz, label='Fx,Fy,Fz')           
            ax.set_xlabel('Fx[N]')
            ax.set_ylabel('Fy[N]')
            ax.set_zlabel('Fz[N]')
            plt.legend()
            plt.grid()
            plt.suptitle('3D local reaction force. Joint: '+ str(jointnumber))
            plt.show() 

#/////////////////////////////////////////////////////FORCE RELATIVE TO GLOBAL REFERENCE FRAME (FF)///////////////////////////////////////////

#Components of the force as function of time:

        if (expression == 'FFx(t)'):
            fig = plt.figure()
            plt.plot(time,f1x,label='FFx(t)',color='red')
            plt.ylabel('FFx[N]')
            plt.xlabel('t[s]')
            plt.legend()
            plt.grid()
            plt.suptitle('X component of global reaction force as function of time. Joint: '+ str(jointnumber))
            plt.show() 

        if (expression == 'FFy(t)'):
            fig = plt.figure()
            plt.plot(time,f1y,label='FFy(t)',color='green')
            plt.ylabel('FFy[N]')
            plt.xlabel('t[s]')
            plt.legend()
            plt.grid()
            plt.suptitle('Y component of global reaction force as function of time. Joint: '+ str(jointnumber))
            plt.show() 

        if (expression == 'FFz(t)'):
            fig = plt.figure()
            plt.plot(time,f1z,label='FFz(t)',color='blue')
            plt.ylabel('FFz[N]')
            plt.xlabel('t[s]')
            plt.legend()
            plt.grid()
            plt.suptitle('Z component of global reaction force as function of time. Joint: '+ str(jointnumber))
            plt.show() 

#Planar forces:

        if (expression == 'FFy(FFx)'):
            fig = plt.figure()
            plt.plot(f1x,f1y,label='FFy(FFx)',color='black')
            plt.ylabel('FFy[N]')
            plt.xlabel('FFx[N]')
            plt.legend()
            plt.grid()
            plt.suptitle('Y component of global reaction force as function of X component of global reaction force. Joint: '+ str(jointnumber))
            plt.show() 
            
        if (expression == 'FFx(FFy)'):
            fig = plt.figure()
            plt.plot(f1y,f1x,label='FFx(FFy)',color='black')
            plt.ylabel('FFx[N]')
            plt.xlabel('FFy[N]')
            plt.legend()
            plt.grid()
            plt.suptitle('X component of global reaction force as function of Y component of global reaction force. Joint: '+ str(jointnumber))
            plt.show()             
            
        if (expression == 'FFz(FFx)'):
            fig = plt.figure()
            plt.plot(f1x,f1z,label='FFz(FFx)',color='black')
            plt.ylabel('FFz[N]')
            plt.xlabel('FFx[N]')
            plt.legend()
            plt.grid()
            plt.suptitle('Z component of global reaction force as function of X component of global reaction force. Joint: '+ str(jointnumber))
            plt.show() 

        if (expression == 'FFx(FFz)'):
            fig = plt.figure()
            plt.plot(f1z,f1x,label='FFx(FFz)',color='black')
            plt.ylabel('FFx[N]')
            plt.xlabel('FFz[N]')
            plt.legend()
            plt.grid()
            plt.suptitle('X component of global reaction force as function of Z component of global reaction force. Joint: '+ str(jointnumber))
            plt.show() 

        if (expression == 'FFy(FFz)'):
            fig = plt.figure()
            plt.plot(f1z,f1y,label='FFy(FFz)',color='black')
            plt.ylabel('FFy[N]')
            plt.xlabel('FFz[N]')
            plt.legend()
            plt.grid()
            plt.suptitle('Y component of global reaction force as function of Z component of global reaction force. Joint: '+ str(jointnumber))
            plt.show() 

        if (expression == 'FFz(FFy)'):
            fig = plt.figure()
            plt.plot(f1y,f1z,label='FFy(FFz)',color='black')
            plt.ylabel('FFz[N]')
            plt.xlabel('FFy[N]')
            plt.legend()
            plt.grid()
            plt.suptitle('Z component of global reaction force as function of Y component of global reaction force. Joint: '+ str(jointnumber))
            plt.show() 

#All global forces as function of time:
        
        if (expression == 'FF(t)'):
            fig = plt.figure()
            plt.plot(time,f1x,label='FFx',color='red')
            plt.plot(time,f1y,label='FFy',color='green')
            plt.plot(time,f1z,label='FFz',color='blue')
            plt.plot(time,f1t,label='total',color='black')
            plt.ylabel('F[N]')
            plt.xlabel('t[s]')
            plt.legend()
            plt.grid()
            plt.suptitle('Global reaction force as function of time. Joint: '+ str(jointnumber))
            plt.show()             

        if (expression == 'FF3D'):
            fig = plt.figure()
            ax = fig.gca(projection='3d')
            ax.plot(f1x, f1y, f1z, label='FFx,FFy,FFz')           
            ax.set_xlabel('FFx[N]')
            ax.set_ylabel('FFy[N]')
            ax.set_zlabel('FFz[N]')
            plt.legend()
            plt.grid()
            plt.suptitle('3D global reaction force. Joint: '+ str(jointnumber))
            plt.show() 

#////////////////////////////////////////////////////////////////////////////TORQUE/////////////////////////////////////////////////////////////////

#TORQUE (T) AS FUNCTION OF TIME:

        if (expression == 'Tx(t)'):
            fig = plt.figure()
            plt.plot(time,tx,label='Tx(t)')
            plt.ylabel('Tx[N*m]')
            plt.xlabel('t[s]')
            plt.legend()
            plt.grid()
            plt.suptitle('X component of global torque as function of time. Joint: '+ str(jointnumber))
            plt.show() 

        if (expression == 'Ty(t)'):
            fig = plt.figure()
            plt.plot(time,ty,label='Ty(t)')
            plt.ylabel('Ty[N*m]')
            plt.xlabel('t[s]')
            plt.legend()
            plt.grid()
            plt.suptitle('Y component of global torque as function of time. Joint: '+ str(jointnumber))
            plt.show() 
            
        if (expression == 'Tz(t)'):
            fig = plt.figure()
            plt.plot(time,tz,label='Tz(t)')
            plt.ylabel('Tz[N*m]')
            plt.xlabel('t[s]')
            plt.legend()
            plt.grid()
            plt.suptitle('Y component of global torque as function of time. Joint: '+ str(jointnumber))
            plt.show() 
            

#ALL TORQUES AS FUNCTION OF TIME
        
        if (expression == 'T(t)'):
            fig = plt.figure()
            plt.plot(time,tx,label='Tx',color='red')
            plt.plot(time,ty,label='Ty',color='green')
            plt.plot(time,tz,label='Tz',color='blue')
            plt.plot(time,tt,label='total',color='black')
            plt.ylabel('T[N*m]')
            plt.xlabel('t[s]')
            plt.legend()
            plt.grid()
            plt.suptitle('Global torque as function of time. Joint: '+ str(jointnumber))
            plt.show() 
            
        if (expression == 'T3D'):
            fig = plt.figure()
            ax = fig.gca(projection='3d')
            ax.plot(tx, ty, tz, label='Tx,Ty,Tz')
            ax.set_xlabel('Tx[N*m]')
            ax.set_ylabel('Ty[N*m]')
            ax.set_zlabel('Tz[N*m]')
            plt.legend()
            plt.grid()
            plt.suptitle('Global 3D torque. Joint: '+ str(jointnumber))
            plt.show() 
                
#All the variables

        if (expression == 'all'):                
            fig = plt.figure()
            ax1 = fig.add_subplot(341)
            ax2 = fig.add_subplot(342)
            ax3 = fig.add_subplot(343)
            ax4 = fig.add_subplot(344)
            ax5 = fig.add_subplot(345)
            ax6 = fig.add_subplot(346)
            ax7 = fig.add_subplot(347)
            ax8 = fig.add_subplot(348)
            ax9 = fig.add_subplot(349)
            ax10 = fig.add_subplot(3,4,10)
            ax11 = fig.add_subplot(3,4,11)
            ax12 = fig.add_subplot(3,4,12)            
            ax1.plot(time,fx)
            ax5.plot(time,fy)
            ax9.plot(time,fz)
            ax1.set_ylabel('Fx[N]')
            ax1.set_xlabel('t[s]')
            ax5.set_ylabel('Fy[N]')
            ax5.set_xlabel('t[s]')
            ax9.set_ylabel('Fz[N]')
            ax9.set_xlabel('t[s]')        
            ax2.plot(time,tx)
            ax6.plot(time,ty)
            ax10.plot(time,tz)
            ax2.set_ylabel('local reaction torque x [N*m]')
            ax2.set_xlabel('t[s]')
            ax6.set_ylabel('local reaction torque y [N*m]')
            ax6.set_xlabel('t[s]')
            ax10.set_ylabel('local reaction torque z [N*m]')
            ax10.set_xlabel('t[s]')
            ax3.plot(time,f1x)
            ax7.plot(time,f1y)
            ax11.plot(time,f1z)
            ax3.set_ylabel('global reaction force x [N]')
            ax3.set_xlabel('t[s]')
            ax7.set_ylabel('global reaction force y [N]')
            ax7.set_xlabel('t[s]')
            ax11.set_ylabel('global reaction force z [N]')
            ax11.set_xlabel('t[s]')
            ax4.plot(time,t1x)
            ax8.plot(time,t1y)
            ax12.plot(time,t1z)
            ax4.set_ylabel('global reaction torque x [N*m]')
            ax4.set_xlabel('t[s]')
            ax8.set_ylabel('global reaction torque y [N*m]')
            ax8.set_xlabel('t[s]')
            ax12.set_ylabel('global reaction torque z [N*m]')
            ax12.set_xlabel('t[s]')
            plt.legend()
            plt.suptitle('Simulation results. Joint: '+ str(jointnumber))
            plt.show() 
            
            
       
