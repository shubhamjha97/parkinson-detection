# -*- coding: utf-8 -*-
"""
Created on Sat Feb 17 17:57:04 2018

@author: Saurabh
"""

import numpy as np
import pandas as pd
import os
import seaborn as sns
from math import sqrt

control_data_path=os.path.join('hw_dataset', 'control')
parkinson_data_path=os.path.join('hw_dataset', 'parkinson')
    
control_file_list=[os.path.join(control_data_path, x) for x in os.listdir(control_data_path)]
parkinson_file_list=[os.path.join(parkinson_data_path, x) for x in os.listdir(parkinson_data_path)]

header_row=["X", "Y", "Z", "Pressure" , "GripAngle" , "Timestamp" , "Test_ID"]

def count_strokes(f):
    global header_row
    dat_pat=pd.read_csv(f, sep=';', header=None, names=header_row)
    dat_pat=dat_pat[dat_pat["Test_ID"]==0]    # Use only static test
    initial_timestamp=dat_pat['Timestamp'][0]
    dat_pat['Timestamp']=dat_pat['Timestamp']- initial_timestamp
    sns.tsplot(dat_pat['Pressure'],dat_pat['Timestamp'])
    
#count_strokes( parkinson_file_list[0])

def find_velocity(f):
    '''
    change in direction and its position
    
    '''
    data_pat=pd.read_csv(f, sep=';', header=None, names=header_row)
    data_pat=data_pat[data_pat["Test_ID"]==1]    # Use only static test
    initial_timestamp=data_pat['Timestamp'][0]
    data_pat['Timestamp']=data_pat['Timestamp']- initial_timestamp
    Vel = []
    horz_Vel = []
    horz_vel_mag = []
    vert_vel_mag = []
    vert_Vel = []
    magnitude = []
    timestamp_diff =  []
    
    print ('No of Cordinates:',len(data_pat))
    t = 0
    for i in range(len(data_pat)-2):
        if t+10 <= len(data_pat)-1:
            Vel.append(((data_pat['X'][t+10] - data_pat['X'][t])/(data_pat['Timestamp'][t+10]-data_pat['Timestamp'][t]) , (data_pat['Y'][t+10]-data_pat['Y'][t])/(data_pat['Timestamp'][t+10]-data_pat['Timestamp'][t])))
            horz_Vel.append((data_pat['X'][t+10] - data_pat['X'][t])/(data_pat['Timestamp'][t+10]-data_pat['Timestamp'][t]))
            
            vert_Vel.append((data_pat['Y'][t+10] - data_pat['Y'][t])/(data_pat['Timestamp'][t+10]-data_pat['Timestamp'][t]))
            magnitude.append(sqrt(((data_pat['X'][t+10]-data_pat['X'][t])/(data_pat['Timestamp'][t+10]-data_pat['Timestamp'][t]))**2 + (((data_pat['Y'][t+10]-data_pat['Y'][t])/(data_pat['Timestamp'][t+10]-data_pat['Timestamp'][t]))**2)))
            timestamp_diff.append(data_pat['Timestamp'][t+10]-data_pat['Timestamp'][t])
            horz_vel_mag.append(abs(horz_Vel[len(horz_Vel)-1]))
            vert_vel_mag.append(abs(vert_Vel[len(vert_Vel)-1]))
            t = t+10
        else:
            break
    magnitude_vel = np.mean(magnitude)  
    magnitude_horz_vel = np.mean(horz_vel_mag)
    magnitude_vert_vel = np.mean(vert_vel_mag)
    print (magnitude_vel , ' ' ,magnitude_horz_vel, ' ',magnitude_vert_vel )
    return Vel,magnitude,timestamp_diff,horz_Vel,vert_Vel,magnitude_vel,magnitude_horz_vel,magnitude_vert_vel
    
def find_acceleration(f):
    '''
    change in direction and its velocity
   
    '''
    Vel,magnitude,timestamp_diff,horz_Vel,vert_Vel,magnitude_vel,magnitude_horz_vel,magnitude_vert_vel = find_velocity(f)
    #data_pat=pd.read_csv(f, sep=';', header=None, names=header_row)
    #data_pat=data_pat[data_pat["Test_ID"]==0]    # Use only static test
    #initial_timestamp=data_pat['Timestamp'][0]
    #data_pat['Timestamp']=data_pat['Timestamp']- initial_timestamp
    accl = []
    horz_Accl =  []
    vert_Accl = []
    magnitude = []
    horz_acc_mag = []
    vert_acc_mag = []
    print ('No of Cordinates:',len(Vel))
    for i in range(len(Vel)-2):
        accl.append(((Vel[i+1][0]-Vel[i][0])/timestamp_diff[i] , (Vel[i+1][1]-Vel[i][1])/timestamp_diff[i]))
        horz_Accl.append((horz_Vel[i+1]-horz_Vel[i])/timestamp_diff[i])
        vert_Accl.append((vert_Vel[i+1]-vert_Vel[i])/timestamp_diff[i])
        horz_acc_mag.append(abs(horz_Accl[len(horz_Accl)-1]))
        vert_acc_mag.append(abs(vert_Accl[len(vert_Accl)-1]))
        magnitude.append(sqrt(((Vel[i+1][0]-Vel[i][0])/timestamp_diff[i])**2 + ((Vel[i+1][1]-Vel[i][1])/timestamp_diff[i])**2))
    
    magnitude_acc = np.mean(magnitude)  
    magnitude_horz_acc = np.mean(horz_acc_mag)
    magnitude_vert_acc = np.mean(vert_acc_mag)
    print (magnitude_acc , ' ' ,magnitude_horz_acc, ' ',magnitude_vert_acc )
    return accl,magnitude,horz_Accl,vert_Accl,timestamp_diff,magnitude_acc,magnitude_horz_acc,magnitude_vert_acc
    
def find_jerk(f):
    
    accl,magnitude,horz_Accl,vert_Accl,timestamp_diff,magnitude_acc,magnitude_horz_acc,magnitude_vert_acc = find_acceleration(f)
    jerk = []
    hrz_jerk = []
    vert_jerk = []
    magnitude = []
    horz_jerk_mag = []
    vert_jerk_mag = []
    print ('No of cordinates', len(accl))
    
    for i in range(len(accl)-2):
        jerk.append(((accl[i+1][0]-accl[i][0])/timestamp_diff[i] , (accl[i+1][1]-accl[i][1])/timestamp_diff[i]))
        hrz_jerk.append((horz_Accl[i+1]-horz_Accl[i])/timestamp_diff[i])
        vert_jerk.append((vert_Accl[i+1]-vert_Accl[i])/timestamp_diff[i])
        horz_jerk_mag.append(abs(hrz_jerk[len(hrz_jerk)-1]))
        vert_jerk_mag.append(abs(vert_jerk[len(vert_jerk)-1]))
        magnitude.append(sqrt(((accl[i+1][0]-accl[i][0])/timestamp_diff[i])**2 + ((accl[i+1][1]-accl[i][1])/timestamp_diff[i])**2))
        
    magnitude_jerk = np.mean(magnitude)  
    magnitude_horz_jerk = np.mean(horz_jerk_mag)
    magnitude_vert_jerk = np.mean(vert_jerk_mag)
    print (magnitude_jerk , ' ' ,magnitude_horz_jerk, ' ',magnitude_vert_jerk )
    return jerk,magnitude,hrz_jerk,vert_jerk,timestamp_diff,magnitude_jerk,magnitude_horz_jerk,magnitude_vert_jerk


def NCV_per_halfcircle(f):
    data_pat=pd.read_csv(f, sep=';', header=None, names=header_row)
    data_pat=data_pat[data_pat["Test_ID"]==0]    # Use only static test
    initial_timestamp=data_pat['Timestamp'][0]
    data_pat['Timestamp']=data_pat['Timestamp']- initial_timestamp
    Vel = []
    ncv = []
    temp_ncv = 0
    basex = data_pat['X'][0]
    for i in range(len(data_pat)-2):
        if data_pat['X'][i] == basex:
            ncv.append(temp_ncv)
            #print ('tempNCV::',temp_ncv)
            temp_ncv = 0
            #print (i)
            continue
            
        Vel.append(((data_pat['X'][i+1] - data_pat['X'][i])/(data_pat['Timestamp'][i+1]-data_pat['Timestamp'][i]) , (data_pat['Y'][i+1]-data_pat['Y'][i])/(data_pat['Timestamp'][i+1]-data_pat['Timestamp'][i])))
        if Vel[len(Vel)-1] != (0,0):
            temp_ncv+=1
    ncv.append(temp_ncv)
    #ncv = list(filter((2).__ne__, ncv))
    ncv_Val = np.sum(ncv)/np.count_nonzero(ncv)
    print (ncv_Val)
    return ncv,ncv_Val

def NCA_per_halfcircle(f):
    data_pat=pd.read_csv(f, sep=';', header=None, names=header_row)
    data_pat=data_pat[data_pat["Test_ID"]==0]    # Use only static test
    initial_timestamp=data_pat['Timestamp'][0]
    data_pat['Timestamp']=data_pat['Timestamp']- initial_timestamp
    Vel,magnitude,timestamp_diff,horz_Vel,vert_Vel,magnitude_vel,magnitude_horz_vel,magnitude_vert_vel = find_velocity(f)
    #data_pat=pd.read_csv(f, sep=';', header=None, names=header_row)
    #data_pat=data_pat[data_pat["Test_ID"]==0]    # Use only static test
    #initial_timestamp=data_pat['Timestamp'][0]
    #data_pat['Timestamp']=data_pat['Timestamp']- initial_timestamp
    accl = []
    nca = []
    temp_nca = 0
    basex = data_pat['X'][0]
    for i in range(len(Vel)-2):
        if data_pat['X'][i] == basex:
            nca.append(temp_nca)
            #print ('tempNCa::',temp_nca)
            temp_nca = 0
            #print (i)
            continue
            
        accl.append(((Vel[i+1][0]-Vel[i][0])/timestamp_diff[i] , (Vel[i+1][1]-Vel[i][1])/timestamp_diff[i]))
        if accl[len(accl)-1] != (0,0):
            temp_nca+=1
    nca.append(temp_nca)
    nca = list(filter((2).__ne__, nca))
    nca_Val = np.sum(nca)/np.count_nonzero(nca)
    print (nca_Val)
    return nca,nca_Val

print ('Velocity')    
find_velocity(parkinson_file_list[0])
print ('Acceleration')
find_acceleration(parkinson_file_list[0])
print ('Jerk')
find_jerk(parkinson_file_list[0])
print ('NCV')
NCV_per_halfcircle(parkinson_file_list[0])   
print ('NCA')
NCA_per_halfcircle(parkinson_file_list[0])
    
    
    #sns.tsplot(dat_pat['Pressure'],dat_pat['Timestamp'])
    
    
    